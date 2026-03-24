
from ultralytics import YOLO
import cv2
# Load pretrained YOLOv8 model (trained on COCO)
model = YOLO('yolov8m.pt')

# Load your image
img = cv2.imread('Images/j14.jpg')

# Perform detection
results = model(img)

# Count cars
car_count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'car':
            car_count += 1

print("Number of cars detected:", car_count)

# Count cars
motorcycle_count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'motorcycle':
            motorcycle_count += 1

print("Number of motorcycles detected:", motorcycle_count)

truck_count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'truck':
            truck_count += 1

print("Number of trucks detected:", truck_count)

bicycle_count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'bicycle':
            bicycle_count += 1

print("Number of bicycles detected:", bicycle_count)

person_count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'person':
            person_count += 1

print("Number of persons detected:", person_count)



# Show the image with bounding boxes
results[0].show()

