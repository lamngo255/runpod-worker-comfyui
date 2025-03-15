#!/usr/bin/env bash

echo "Worker Initiated"

echo "Symlinking files from Network Volume"
rm -rf /workspace && \
  ln -s /runpod-volume /workspace

echo "Starting ComfyUI API"
source /workspace/venv/bin/activate
TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
export LD_PRELOAD="${TCMALLOC}"
export PYTHONUNBUFFERED=true
export HF_HOME="/workspace"
cd /workspace/ComfyUI
echo "Run ComfyUI server"
python main.py --port 3000 > /workspace/logs/comfyui.log 2>&1 &
deactivate

echo "Starting RunPod Handler"
python3 -u /rp_handler.py

# in local

# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

# We need to do 3 things
# 1) Start local test server:
# python rp_handler.py --rp_serve_api

# 2) Start ComfyUI:
# cd ~/Documents/AI/ComfyUI && python3 main.py

# 3) Start the test
# python txt2img.py
