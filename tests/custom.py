#!/usr/bin/env python3
from util import post_request
import random


if __name__ == '__main__':
    payload = {
        "input": {
            "workflow": "custom",
            "payload": {
                "3": {
                    "inputs": {
                        "seed": 475272654367769,
                        "steps": 22,
                        "cfg": 8,
                        "sampler_name": "dpmpp_3m_sde",
                        "scheduler": "karras",
                        "denoise": 0.6,
                        "model": [
                            "4",
                            0
                        ],
                        "positive": [
                            "6",
                            0
                        ],
                        "negative": [
                            "7",
                            0
                        ],
                        "latent_image": [
                            "11",
                            0
                        ]
                    },
                    "class_type": "KSampler",
                    "_meta": {
                        "title": "KSampler"
                    }
                },
                "4": {
                    "inputs": {
                        "ckpt_name": "sd_xl_base_1.0.safetensors"
                    },
                    "class_type": "CheckpointLoaderSimple",
                    "_meta": {
                        "title": "Load Checkpoint"
                    }
                },
                "6": {
                    "inputs": {
                    "text": "White Woman in a orange bikini standing in middle of a crowded place, skyscrapers in the background, cinematic, monotone colors, bright, utopia",
                    "clip": [
                        "4",
                        1
                    ]
                    },
                    "class_type": "CLIPTextEncode",
                    "_meta": {
                        "title": "CLIP Text Encode (Prompt)"
                    }
                },
                "7": {
                    "inputs": {
                    "text": "text, watermark",
                    "clip": [
                        "4",
                        1
                    ]
                    },
                    "class_type": "CLIPTextEncode",
                    "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                    }
                },
                "8": {
                    "inputs": {
                    "samples": [
                        "3",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                    },
                    "class_type": "VAEDecode",
                    "_meta": {
                        "title": "VAE Decode"
                    }
                },
                "9": {
                    "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                    },
                    "class_type": "SaveImage",
                    "_meta": {
                        "title": "Save Image"
                    }
                },
                "11": {
                    "inputs": {
                    "pixels": [
                        "12",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                    },
                    "class_type": "VAEEncode",
                    "_meta": {
                        "title": "VAE Encode"
                    }
                },
                "12": {
                    "inputs": {
                        "url": "https://dream-home-ai.s3.ap-southeast-2.amazonaws.com/yzsyrbgsO7JpnCOycMI6s-704w-embedded.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIA5EP2GGUK4LCKDDXQ%2F20241105%2Fap-southeast-2%2Fs3%2Faws4_request&X-Amz-Date=20241105T143703Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0yIkcwRQIhAIavX92NvfzIYxmCdmj4wpxYz0b%2FufaN5reI7uMOQdLOAiBJGunVy8Nhu6vp46mIpKP980oDrftYFRy72Fil9KuesSrsAggYEAEaDDkwMzAwNDY5Nzg3NyIMZdjZpwms2E%2FjtWNTKskC5L1OrmZToD6BcHM%2BBnzgzq0pZ7fv5UoyyxkVqe%2FfUb82QMpfbLkZuURKx8UfUAHHfHpVYiHmX4tjlpxwVi17fNvdGB3MxX0NtTtc%2BynvEWwEKth9u%2FpnOwRG7c%2Bt8WzDY5FQ8r74GDD3muKbPN4azmx8q8D4AF%2B1NyVmxznEX1i623ziXzIcnP%2B59nwFlub926T7YaD4bHaxxgn1ApNZHFGxgCaMdpdKOFN5Hk1oIRqg3TKDegHjn7cyRq6RvZoNQsQXBmBGAMFSjr7c9DNm5WHlBICpXtXbZirHQuwv%2BTMGwFL5H2zr%2BXeCzWVA24gIfSnoOkBwgPl5HGkKrBg%2FPMHpj3wdsyZBbjgGkgsxJNMfLRQ%2BRTVyWh66oDeQmXTeqgXWq9hZz1ph79reaY%2FydDVO7Jui3rkVnND7w%2FWunYUrL4fYP5wN5vow68%2BouQY6swL4FvuoRmRAc0NcRhxqQQ1Maj1uIKxLfcWsHTDq1f8mBBM9a2DjvMnR7aQEYNZCiFMCY04avPkkvK3WU0kvWcRcpPkZtc2NRCJX7FeealAg36hn4up4Y0HxE9vk1%2FMQaw0qi12wNZzbU%2FKUSetQ62tI5SMl%2F5D9Eq%2F0NqyC8AdbfheRbST%2Fez06cCEiHq%2BP1dNt1NWqNZM5HxusKbEYInY%2FUd%2BPw%2B9kRJx12pPUqjbqVXW4Su1DsdrAdBrMspJ44YMUUYoU0Qy%2FP2tjQujlyKIsmyDoeibYDeniN9ki57pZekyo0cM8gSs%2FDst%2BoN7l5ZAPW5QIVmwRD85y8fz56sZVrZuQF37NP8cKi78x1l1LWRzmpDJgyl7tdl3uw1RnyisvBd2qgBJUr4SvsIWazUcj1Jxi&X-Amz-Signature=47780d5f8dfd9b2d690e4a89865e3bd971aae4f069353751d03fab7c5e5b0bbf&X-Amz-SignedHeaders=host&response-content-disposition=inline",
                        "cache": "true"
                    },
                    "class_type": "LoadImageByUrl //Browser",
                    "_meta": {
                        "title": "Load Image By URL"
                    }
                },
                "13": {
                    "inputs": {
                        "images": [
                            "12",
                            0
                        ]
                    },
                    "class_type": "PreviewImage",
                    "_meta": {
                        "title": "Preview Image"
                    }
                }
            }
        }
    }

    payload["input"]["payload"]["3"]["inputs"]["seed"] = random.randrange(1, 1000000)

    post_request(payload)
