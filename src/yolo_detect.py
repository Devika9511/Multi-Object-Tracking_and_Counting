import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open our traffic video
video_path = "input/traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Could not open the video.")
    exit()

print("✅ Video opened successfully!")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Draw detected objects on the frame
    annotated_frame = results[0].plot()

    # Resize for display
    display_width = 1000
    display_height = 600

    resized_frame = cv2.resize(
        annotated_frame,
        (display_width, display_height)
    )

    cv2.imshow("SmartFlow - YOLO Detection", resized_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ YOLO detection completed!")