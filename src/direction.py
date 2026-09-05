import cv2
from ultralytics import YOLO

# ============================================================
# SMARTFLOW - DIRECTION & ENTRY/EXIT COUNTING
# ============================================================

print("========================================")
print("   SMARTFLOW DIRECTION ANALYSIS")
print("========================================")

# Load YOLO
model = YOLO("yolo11n.pt")

# Video
video_path = "input/traffic.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Could not open video")
    exit()

print("✅ Video opened successfully!")

# ============================================================
# VIDEO INFORMATION
# ============================================================

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Video size: {width} x {height}")
print(f"FPS: {fps:.2f}")

# ============================================================
# COUNTING LINE
# ============================================================

COUNT_LINE_X = int(width * 0.60)

# ============================================================
# VEHICLE CLASSES
# ============================================================

VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}

# ============================================================
# COUNTERS
# ============================================================

entry_count = 0
exit_count = 0

total_count = 0

car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

# IDs already counted
counted_ids = set()

# Previous X positions
previous_positions = {}

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ========================================================
    # YOLO + BYTETRACK
    # ========================================================

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=list(VEHICLE_CLASSES.keys()),
        conf=0.30,
        verbose=False
    )

    result = results[0]

    # ========================================================
    # COUNTING LINE
    # ========================================================

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
        0.7,
        (0, 0, 255),
        2
    )

    # ========================================================
    # PROCESS TRACKED VEHICLES
    # ========================================================

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

            if class_id not in VEHICLE_CLASSES:
                continue

            vehicle_name = VEHICLE_CLASSES[class_id]

            x1, y1, x2, y2 = map(int, box)

            # Center
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # =================================================
            # PREVIOUS POSITION
            # =================================================

            previous_x = previous_positions.get(track_id)

            # =================================================
            # DIRECTION DETECTION
            # =================================================

            if previous_x is not None:

                # LEFT → RIGHT
                moving_right = (
                    previous_x < COUNT_LINE_X
                    and center_x >= COUNT_LINE_X
                )

                # RIGHT → LEFT
                moving_left = (
                    previous_x > COUNT_LINE_X
                    and center_x <= COUNT_LINE_X
                )

                # =================================================
                # COUNT CROSSING
                # =================================================

                if track_id not in counted_ids:

                    if moving_right:

                        counted_ids.add(track_id)

                        entry_count += 1
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
                            f"➡ ENTRY | "
                            f"ID={track_id} | "
                            f"Type={vehicle_name} | "
                            f"Total={total_count}"
                        )

                    elif moving_left:

                        counted_ids.add(track_id)

                        exit_count += 1
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
                            f"⬅ EXIT | "
                            f"ID={track_id} | "
                            f"Type={vehicle_name} | "
                            f"Total={total_count}"
                        )

            # Save current X position
            previous_positions[track_id] = center_x

            # =================================================
            # DRAW CENTER
            # =================================================

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 255, 0),
                -1
            )

            # =================================================
            # DRAW TRACKING LABEL
            # =================================================

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

            # =================================================
            # DRAW BOX
            # =================================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )

    # ========================================================
    # DISPLAY STATISTICS
    # ========================================================

    cv2.putText(
        frame,
        f"Total Vehicles: {total_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        f"Entry: {entry_count}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Exit: {exit_count}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Cars: {car_count}",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Motorcycles: {motorcycle_count}",
        (20, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Buses: {bus_count}",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Trucks: {truck_count}",
        (20, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # ========================================================
    # RESIZE
    # ========================================================

    display_frame = cv2.resize(
        frame,
        (1000, 600)
    )

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        "SmartFlow - Direction Analysis",
        display_frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()

# ============================================================
# FINAL RESULTS
# ============================================================

print()
print("========================================")
print("     SMARTFLOW FINAL RESULTS")
print("========================================")

print(f"Total Vehicles : {total_count}")
print(f"Entry          : {entry_count}")
print(f"Exit           : {exit_count}")

print("----------------------------------------")

print(f"Cars           : {car_count}")
print(f"Motorcycles    : {motorcycle_count}")
print(f"Buses          : {bus_count}")
print(f"Trucks         : {truck_count}")

print("========================================")
print("✅ Direction analysis completed!")