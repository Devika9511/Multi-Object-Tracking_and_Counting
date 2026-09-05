import cv2
from ultralytics import YOLO

# ============================================
# SMARTFLOW - VEHICLE COUNTING
# Horizontal Traffic Counting
# ============================================

print("========================================")
print("     SMARTFLOW VEHICLE COUNTING")
print("========================================")

# Load YOLO model
model = YOLO("yolo11n.pt")

# Video
video_path = "input/traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Could not open video")
    exit()

print("✅ Video opened successfully!")

# ============================================
# VIDEO INFORMATION
# ============================================

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Video size: {width} x {height}")
print(f"FPS: {fps}")

# ============================================
# COUNTING LINE
# ============================================

# Vertical line
# Vehicles crossing this X coordinate will be counted

COUNT_LINE_X = int(width * 0.60)

print(f"Counting line X = {COUNT_LINE_X}")

# ============================================
# VEHICLE CLASSES
# ============================================

# COCO classes:
# 2 = car
# 3 = motorcycle
# 5 = bus
# 7 = truck

VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}

# ============================================
# COUNTERS
# ============================================

total_count = 0

car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

# IDs that have already been counted
counted_ids = set()

# Store previous X position for every tracked object
previous_positions = {}

# ============================================
# PROCESS VIDEO
# ============================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ========================================
    # YOLO TRACKING
    # ========================================

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=list(VEHICLE_CLASSES.keys()),
        conf=0.30,
        verbose=False
    )

    result = results[0]

    # ========================================
    # DRAW COUNTING LINE
    # ========================================

    cv2.line(
        frame,
        (COUNT_LINE_X, 0),
        (COUNT_LINE_X, height),
        (0, 0, 255),
        4
    )

    cv2.putText(
        frame,
        "COUNTING LINE",
        (COUNT_LINE_X - 130, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # ========================================
    # TRACKED OBJECTS
    # ========================================

    if result.boxes.id is not None:

        track_ids = result.boxes.id.int().cpu().tolist()

        boxes = result.boxes.xyxy.cpu().tolist()

        class_ids = result.boxes.cls.int().cpu().tolist()

        confidences = result.boxes.conf.cpu().tolist()

        for track_id, box, class_id, confidence in zip(
            track_ids,
            boxes,
            class_ids,
            confidences
        ):

            # --------------------------------
            # Bounding box
            # --------------------------------

            x1, y1, x2, y2 = map(int, box)

            # Center point
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # --------------------------------
            # Vehicle name
            # --------------------------------

            vehicle_name = VEHICLE_CLASSES.get(
                class_id,
                "Vehicle"
            )

            # --------------------------------
            # Previous X position
            # --------------------------------

            previous_x = previous_positions.get(
                track_id
            )

            # ====================================
            # COUNTING LOGIC
            # ====================================

            if previous_x is not None:

                # Vehicle moving LEFT -> RIGHT
                crossed_left_to_right = (
                    previous_x < COUNT_LINE_X
                    and center_x >= COUNT_LINE_X
                )

                # Vehicle moving RIGHT -> LEFT
                crossed_right_to_left = (
                    previous_x > COUNT_LINE_X
                    and center_x <= COUNT_LINE_X
                )

                crossed_line = (
                    crossed_left_to_right
                    or crossed_right_to_left
                )

                # Count only once
                if crossed_line and track_id not in counted_ids:

                    counted_ids.add(track_id)

                    total_count += 1

                    if class_id == 2:
                        car_count += 1

                    elif class_id == 3:
                        motorcycle_count += 1

                    elif class_id == 5:
                        bus_count += 1

                    elif class_id == 7:
                        truck_count += 1

                    print(
                        f"🚗 Counted: "
                        f"ID={track_id} "
                        f"Type={vehicle_name} "
                        f"Total={total_count}"
                    )

            # Save current position
            previous_positions[track_id] = center_x

            # ====================================
            # DRAW TRACKING POINT
            # ====================================

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 255, 0),
                -1
            )

            # ====================================
            # DRAW ID + CLASS
            # ====================================

            label = (
                f"ID:{track_id} "
                f"{vehicle_name} "
                f"{confidence:.2f}"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            # ====================================
            # DRAW BOX
            # ====================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )

    # ============================================
    # DISPLAY STATISTICS
    # ============================================

    cv2.putText(
        frame,
        f"Total Vehicles: {total_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        f"Cars: {car_count}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Motorcycles: {motorcycle_count}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Buses: {bus_count}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Trucks: {truck_count}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ============================================
    # RESIZE FOR DISPLAY
    # ============================================

    display_frame = cv2.resize(
        frame,
        (1000, 600)
    )

    cv2.imshow(
        "SmartFlow - Vehicle Counting",
        display_frame
    )

    # ============================================
    # PRESS Q TO STOP
    # ============================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================
# CLEANUP
# ============================================

cap.release()
cv2.destroyAllWindows()

# ============================================
# FINAL RESULTS
# ============================================

print()
print("========================================")
print("       SMARTFLOW COUNTING RESULTS")
print("========================================")
print(f"Total Vehicles : {total_count}")
print(f"Cars           : {car_count}")
print(f"Motorcycles    : {motorcycle_count}")
print(f"Buses          : {bus_count}")
print(f"Trucks         : {truck_count}")
print("========================================")
print("✅ Processing completed!")