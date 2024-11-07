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
                    "seed": 8361161853600,
                    "steps": 8,
                    "cfg": 2,
                    "sampler_name": "dpmpp_sde",
                    "scheduler": "karras",
                    "denoise": 1,
                    "model": [
                        "33",
                        0
                    ],
                    "positive": [
                        "39",
                        0
                    ],
                    "negative": [
                        "39",
                        1
                    ],
                    "latent_image": [
                        "19",
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
                    "ckpt_name": "RealitiesEdgeXLSDXL_TURBOXLV2.safetensors"
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "6": {
                "inputs": {
                    "text": "high resolution, master piece, realistic",
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
                    "text": "oil painting, 3d, anime, bad image, bad room, low resolution",
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
            "19": {
                "inputs": {
                    "pixels": [
                        "77",
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
            "29": {
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
            "30": {
                "inputs": {
                    "weight": 0.6,
                    "weight_type": "style transfer",
                    "combine_embeds": "concat",
                    "start_at": 0.1,
                    "end_at": 1,
                    "embeds_scaling": "V only",
                    "model": [
                        "4",
                        0
                    ],
                    "ipadapter": [
                        "34",
                        0
                    ],
                    "image": [
                        "32",
                        0
                    ],
                    "clip_vision": [
                        "31",
                        0
                    ]
                },
                "class_type": "IPAdapterAdvanced",
                "_meta": {
                    "title": "IPAdapter Advanced"
                }
            },
            "31": {
                "inputs": {
                    "clip_name": "model.safetensors"
                },
                "class_type": "CLIPVisionLoader",
                "_meta": {
                    "title": "Load CLIP Vision"
                }
            },
            "32": {
                "inputs": {
                    "interpolation": "LANCZOS",
                    "crop_position": "center",
                    "sharpening": 0.15,
                    "image": [
                        "37",
                        0
                    ]
                },
                "class_type": "PrepImageForClipVision",
                "_meta": {
                    "title": "Prep Image For ClipVision"
                }
            },
            "33": {
                "inputs": {
                    "model": [
                        "30",
                        0
                    ]
                },
                "class_type": "DifferentialDiffusion",
                "_meta": {
                    "title": "Differential Diffusion"
                }
            },
            "34": {
                "inputs": {
                    "ipadapter_file": "ip-adapter_sdxl_vit-h.safetensors"
                },
                "class_type": "IPAdapterModelLoader",
                "_meta": {
                    "title": "IPAdapter Model Loader"
                }
            },
            "37": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "interpolation": "lanczos",
                    "method": "keep proportion",
                    "condition": "always",
                    "multiple_of": 0,
                    "image": [
                        "76",
                        0
                    ]
                },
                "class_type": "ImageResize+",
                "_meta": {
                    "title": "🔧 Image Resize"
                }
            },
            "39": {
                "inputs": {
                    "strength": 0.7000000000000001,
                    "start_percent": 0,
                    "end_percent": 1,
                    "positive": [
                        "6",
                        0
                    ],
                    "negative": [
                        "7",
                        0
                    ],
                    "control_net": [
                        "41",
                        0
                    ],
                    "image": [
                        "43",
                        0
                    ]
                },
                "class_type": "ControlNetApplyAdvanced",
                "_meta": {
                    "title": "Apply ControlNet"
                }
            },
            "41": {
                "inputs": {
                    "control_net_name": "diffusion_pytorch_model.safetensors"
                },
                "class_type": "ControlNetLoader",
                "_meta": {
                    "title": "Load ControlNet Model"
                }
            },
            "43": {
                "inputs": {
                    "ckpt_name": "depth_anything_vitl14.pth",
                    "resolution": 512,
                    "image": [
                        "77",
                        0
                    ]
                },
                "class_type": "DepthAnythingPreprocessor",
                "_meta": {
                    "title": "Depth Anything"
                }
            },
            "76": {
                "inputs": {
                    "url": "https://firebasestorage.googleapis.com/v0/b/interior-design-907b0.appspot.com/o/blue_room.png?alt=media&token=bce9c6a7-9c9e-492c-b35b-f9f2d8ef82b0",
                    "cache": "true"
                },
                "class_type": "LoadImageByUrl //Browser",
                "_meta": {
                    "title": "Load Image By URL"
                }
            },
            "77": {
                "inputs": {
                    "url": "https://firebasestorage.googleapis.com/v0/b/interior-design-907b0.appspot.com/o/IMG_0295.JPG?alt=media&token=483edf67-2c6e-41f5-a1b3-d4c0285f9a1a",
                    "cache": "true"
                },
                "class_type": "LoadImageByUrl //Browser",
                "_meta": {
                    "title": "Load Image By URL"
                }
            }
        }
    }
}

    payload["input"]["payload"]["3"]["inputs"]["seed"] = random.randrange(1, 1000000)

    post_request(payload)
