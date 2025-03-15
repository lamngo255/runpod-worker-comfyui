import time
import requests
import json
import base64
import runpod
import os
from runpod.serverless.utils import rp_upload
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from requests.adapters import HTTPAdapter, Retry
from schemas.input import INPUT_SCHEMA
import base64


IS_DOCKER = True
BASE_URI = 'http://127.0.0.1:3000' if IS_DOCKER else 'http://127.0.0.1:8188'
VOLUME_MOUNT_PATH = '/runpod-volume'
TIMEOUT = 600

session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
logger = RunPodLogger()


# ---------------------------------------------------------------------------- #
#                               ComfyUI Functions                              #
# ---------------------------------------------------------------------------- #

def wait_for_service(url):
    retries = 0

    while True:
        try:
            requests.get(url)
            return
        except requests.exceptions.RequestException:
            retries += 1

            # Only log every 15 retries so the logs don't get spammed
            if retries % 15 == 0:
                logger.info('Service not ready yet. Retrying...')
        except Exception as err:
            logger.error(f'Error: {err}')

        time.sleep(0.2)


def send_get_request(endpoint):
    return session.get(
        url=f'{BASE_URI}/{endpoint}',
        timeout=TIMEOUT
    )


def send_post_request(endpoint, payload):
    return session.post(
        url=f'{BASE_URI}/{endpoint}',
        json=payload,
        timeout=TIMEOUT
    )

def get_txt2img_payload(workflow, payload):
    workflow["3"]["inputs"]["seed"] = payload["seed"]
    workflow["3"]["inputs"]["steps"] = payload["steps"]
    workflow["3"]["inputs"]["cfg"] = payload["cfg_scale"]
    workflow["3"]["inputs"]["sampler_name"] = payload["sampler_name"]
    workflow["4"]["inputs"]["ckpt_name"] = payload["ckpt_name"]
    workflow["5"]["inputs"]["batch_size"] = payload["batch_size"]
    workflow["5"]["inputs"]["width"] = payload["width"]
    workflow["5"]["inputs"]["height"] = payload["height"]
    workflow["6"]["inputs"]["text"] = payload["prompt"]
    workflow["7"]["inputs"]["text"] = payload["negative_prompt"]
    return workflow


def get_workflow_payload(workflow_name, payload):
    workflow_path = '/workflows' if IS_DOCKER else './workflows'
    with open(f'{workflow_path}/{workflow_name}.json', 'r') as json_file:
        workflow = json.load(json_file)

    if workflow_name == 'txt2img':
        workflow = get_txt2img_payload(workflow, payload)

    return workflow


def get_filenames(output):
    for key, value in output.items():
        if 'images' in value and isinstance(value['images'], list):
            return value['images']
        
def base64_encode(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"{encoded_string}"
        
def process_output_images(image_path, event_id):
    print(f"runpod-worker-comfy - {image_path}")

    # The image is in the output folder
    if os.path.exists(image_path):
        if os.environ.get("BUCKET_ENDPOINT_URL", False):
            # URL to image in AWS S3
            image = rp_upload.upload_image(event_id, image_path)
            print(
                "runpod-worker-comfy - the image was generated and uploaded to AWS S3"
            )
        else:
            # base64 image
            image = base64_encode(image_path)
            print(
                "runpod-worker-comfy - the image was generated and converted to base64"
            )

        return {
            "image": image,
        }
    else:
        print("runpod-worker-comfy - the image does not exist in the output folder")
        return {
            "status": "error",
            "message": f"the image does not exist in the specified output folder: {image_path}",
        }


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    try:
        validated_input = validate(event['input'], INPUT_SCHEMA)

        if 'errors' in validated_input:
            return {
                'error': validated_input['errors']
            }

        payload = validated_input['validated_input']
        workflow_name = payload['workflow']
        payload = payload['payload']

        if workflow_name == 'default':
            workflow_name = 'txt2img'

        logger.info(f'Workflow: {workflow_name}')

        if workflow_name != 'custom':
            try:
                payload = get_workflow_payload(workflow_name, payload)
            except Exception as e:
                logger.error(f'Unable to load workflow payload for: {workflow_name}')
                raise

        logger.debug('Queuing prompt')

        queue_response = send_post_request(
            'prompt',
            {
                'prompt': payload
            }
        )

        resp_json = queue_response.json()
        print(f'resp_json: {resp_json}')

        if queue_response.status_code == 200:
            prompt_id = resp_json['prompt_id']
            logger.info(f'Prompt queued successfully: {prompt_id}')

            while True:
                logger.debug(f'Getting status of prompt: {prompt_id}')
                r = send_get_request(f'history/{prompt_id}')
                resp_json = r.json()

                if r.status_code == 200 and len(resp_json):
                    break

                time.sleep(0.5)

            logger.info(f'resp_json: {resp_json[prompt_id]}')

            if len(resp_json[prompt_id]['outputs']):
                logger.info(f'Images generated successfully for prompt: {prompt_id}')
                image_filenames = get_filenames(resp_json[prompt_id]['outputs'])
                images = []
                uploaded_images = {}

                for image_filename in image_filenames:
                    filename = image_filename['filename']
                    image_path = f'{VOLUME_MOUNT_PATH}/ComfyUI/output/{filename}' if IS_DOCKER else f'/Users/lamngo/Documents/AI/ComfyUI/output/{filename}'

                    with open(image_path, 'rb') as image_file:
                        images.append(base64.b64encode(image_file.read()).decode('utf-8'))
                    uploaded_images = process_output_images(image_path, event["id"])

                return {
                    # 'images': images,
                    'result': uploaded_images
                }
            else:
                raise RuntimeError('No output found, please ensure that the model is correct and that it exists')
        else:
            logger.error(f'HTTP Status code: {queue_response.status_code}')
            logger.error(json.dumps(resp_json, indent=4, default=str))
            return resp_json
    except Exception as e:
        raise


if __name__ == '__main__':
    wait_for_service(url=f'{BASE_URI}/system_stats')
    logger.info('ComfyUI API is ready')
    logger.info('Starting RunPod Serverless...')
    runpod.serverless.start(
        {
            'handler': handler
        }
    )
