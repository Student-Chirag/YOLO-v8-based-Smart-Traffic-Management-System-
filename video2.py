from ultralytics import YOLO
import cv2
import os

# ========== USER SETTINGS ==========
video_path = "traffic car.mp4"   # Input video
snapshot_interval = 5            # Capture image every 5 seconds
output_folder = "captured_frames"  # Folder to save captured images
model_path = "yolov8s.pt"        # YOLO model
# ===================================

# Load YOLOv8 model
model = YOLO(model_path)

# Create folder to store captured frames
os.makedirs(output_folder, exist_ok=True)

# Open video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_interval = int(snapshot_interval * fps)  # frame gap between captures
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video FPS: {fps}, Total Frames: {frame_count}")
print(f"Capturing an image every {snapshot_interval} seconds...")

current_frame = 0
image_index = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Capture frame at specified interval
    if current_frame % frame_interval == 0:
        image_path = os.path.join(output_folder, f"frame_{image_index}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Captured: {image_path}")

        # Run YOLOv8 on captured image
        results = model(frame, verbose=False)

        # Count vehicles
        vehicle_count = 0
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                if label in ['car', 'bus', 'truck', 'motorbike']:
                    vehicle_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display vehicle count
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow("Vehicle Detection", frame)
        print(f"Vehicles detected in frame_{image_index}: {vehicle_count}")

        image_index += 1

        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    current_frame += 1

cap.release()
cv2.destroyAllWindows()
print("\n✅ Vehicle detection complete!")

