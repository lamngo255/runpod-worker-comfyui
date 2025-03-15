echo "Installing Ubuntu updates"
apt update
apt -y upgrade

echo "Creating and activating venv"
cd /workspace/ComfyUI
python -m venv /workspace/venv
source /workspace/venv/bin/activate

echo "Installing Torch"
pip install --no-cache-dir torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo "Installing xformers"
pip3 install --no-cache-dir xformers==0.0.22

echo "Installing RunPod Serverless dependencies"
pip3 install huggingface_hub runpod

echo "Downloading models"

# Checkpoints
cd /workspace/ComfyUI/models/checkpoints
wget -O depth_anything_vitl14.pth https://huggingface.co/spaces/LiheYoung/Depth-Anything/resolve/main/checkpoints/depth_anything_vitl14.pth
wget -O RealitiesEdgeXLSDXL_TURBOXLV2.safetensors https://huggingface.co/SEVUNX/sdxl_model/resolve/main/download_5/RealitiesEdgeXLSDXL_TURBOXLV2.safetensors
wget https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

# IP Adapter
cd /workspace/ComfyUI/models/ipadapter
wget https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter_sdxl_vit-h.safetensors

# CLIP Vision
cd /workspace/ComfyUI/models/clip_vision
wget https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors

# ControlNet
cd /workspace/ComfyUI/models/controlnet
wget -O diffusion_pytorch_model.safetensors https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/resolve/4f29d5315034aaab86c11dc8c91b88bf188674ca/diffusion_pytorch_model.safetensors

echo "Creating log directory"
mkdir -p /workspace/logs
