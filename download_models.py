import urllib.request
import os

def download_file(url, filename):
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded {filename} successfully!")

# Create directories if they don't exist
directories = [
    "object_detection_model",
    "object_detection_model/weights",
    "object_detection_model/config",
    "object_detection_model/objectLabels"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Download YOLOv3-tiny weights
weights_url = "https://pjreddie.com/media/files/yolov3-tiny.weights"
weights_path = "object_detection_model/weights/yolov3-tiny.weights"
download_file(weights_url, weights_path)

# Download YOLOv3-tiny config
config_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg"
config_path = "object_detection_model/config/yolov3-tiny.cfg"
download_file(config_url, config_path)

# Download COCO class names
coco_names_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
coco_names_path = "object_detection_model/objectLabels/coco.names"
download_file(coco_names_url, coco_names_path)

print("\nAll files downloaded successfully!")
print("\nYou can now run your server with: python server.py") 