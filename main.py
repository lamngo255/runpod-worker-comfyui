import runpod

counter = 0

def handler(event):
    global counter
    counter += 1
    return {"counter": counter}

runpod.serverless.start({"handler": handler})