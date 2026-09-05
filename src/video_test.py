import cv2

# Path to our input video
video_path = "input/traffic.mp4"

# Open the video
cap = cv2.VideoCapture(video_path)

# Check whether video opened successfully
if not cap.isOpened():
    print("❌ Could not open the video.")
    exit()

print("✅ Video opened successfully!")

# Read and display frames
while True:

    ret, frame = cap.read()

    # Stop when video ends
    if not ret:
        break

    # Display current frame
    # Resize video to fit the screen
    display_width = 1000
    display_height = 600

    resized_frame = cv2.resize(frame, (display_width, display_height))

    cv2.imshow("SmartFlow - Video Test", resized_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release video
cap.release()

# Close OpenCV windows
cv2.destroyAllWindows()

print("✅ Video processing completed!")