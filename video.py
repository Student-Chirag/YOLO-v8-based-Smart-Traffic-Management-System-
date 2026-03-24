
from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8 model
model = YOLO('yolov8s.pt')  # You can also try 'yolov8n.pt' for faster inference

# Load the video
video_path = "Video/traffic car2.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video details
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Output video writer (optional: save result video)
out = cv2.VideoWriter('output_vehicles.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

total_vehicle_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on the frame
    results = model(frame, verbose=False)

    # Current frame vehicle count
    frame_vehicle_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            
            # Detect common vehicle types
            if label in ['car', 'bus', 'truck', 'motorbike']:
                frame_vehicle_count += 1
                # Draw bounding boxes
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Update total count (optional: use tracking for more accuracy)
    total_vehicle_count += frame_vehicle_count

    # Show frame count
    cv2.putText(frame, f"Vehicles in frame: {frame_vehicle_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.imshow("Vehicle Detection", frame)

    # Write the output frame
    out.write(frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("Total vehicle detections across frames:", total_vehicle_count)
print("Output video saved as: output_vehicles.mp4")



