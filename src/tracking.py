import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open traffic video
video_path = "input/traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Could not open the video.")
    exit()

print("✅ Video opened successfully!")
print("🚀 Starting object tracking...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # YOLO detection + ByteTrack tracking
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml"
    )

    # Draw bounding boxes and tracking IDs
    annotated_frame = results[0].plot()

    # Resize for display
    display_width = 1000
    display_height = 600

    resized_frame = cv2.resize(
        annotated_frame,
        (display_width, display_height)
    )

    cv2.imshow(
        "SmartFlow - Object Tracking",
        resized_frame
    )

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ Tracking completed!")