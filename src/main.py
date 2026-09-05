import cv2
import os
import csv
from datetime import datetime
from ultralytics import YOLO


# ============================================================
# SMARTFLOW - MULTI-OBJECT TRACKING & COUNTING
# ============================================================

VIDEO_PATH = "input/traffic.mp4"
MODEL_PATH = "yolo11n.pt"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

OUTPUT_VIDEO = os.path.join(
    OUTPUT_DIR,
    "smartflow_tracked.mp4"
)

CSV_FILE = os.path.join(
    REPORT_DIR,
    "traffic_data.csv"
)

CONFIDENCE = 0.30

# Counting line position as percentage of video width
LINE_POSITION = 0.60

# Log data every 2 seconds
LOG_SECONDS = 2


# COCO vehicle classes
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


# ============================================================
# CREATE DIRECTORIES
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ============================================================
# LOAD MODEL
# ============================================================

print("\n==============================================")
print("        SMARTFLOW TRAFFIC ENGINE")
print("==============================================")

print("\nLoading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded!")


# ============================================================
# OPEN VIDEO
# ============================================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("\n❌ Could not open video.")
    print("Check:", VIDEO_PATH)
    exit()


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("\nVideo opened successfully!")
print(f"Resolution : {width} x {height}")
print(f"FPS        : {fps:.2f}")
print(f"Frames     : {total_frames}")


# ============================================================
# COUNTING LINE
# ============================================================

COUNT_LINE_X = int(width * LINE_POSITION)

print(f"Counting line: X = {COUNT_LINE_X}")


# ============================================================
# VIDEO WRITER
# ============================================================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (width, height)
)

if not writer.isOpened():
    print("\n❌ Could not create output video.")
    exit()

print(f"Output video: {OUTPUT_VIDEO}")


# ============================================================
# CSV SETUP
# ============================================================

csv_exists = os.path.exists(CSV_FILE)

csv_file = open(
    CSV_FILE,
    "a",
    newline="",
    encoding="utf-8"
)

csv_writer = csv.writer(csv_file)

if not csv_exists:
    csv_writer.writerow([
        "timestamp",
        "frame",
        "vehicles",
        "cars",
        "motorcycles",
        "buses",
        "trucks",
        "density",
        "right_direction",
        "left_direction",
        "flow_rate"
    ])


# ============================================================
# TRACKING VARIABLES
# ============================================================

previous_positions = {}

counted_ids = set()

right_ids = set()
left_ids = set()

total_count = 0

car_count = 0
motorcycle_count = 0
bus_count = 0
truck_count = 0

frame_number = 0

right_crossings = 0
left_crossings = 0

# Used for flow calculation
video_start_time = None


# ============================================================
# MAIN PROCESSING LOOP
# ============================================================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    # --------------------------------------------------------
    # TRACK OBJECTS
    # --------------------------------------------------------

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=CONFIDENCE,
        verbose=False
    )

    result = results[0]

    # --------------------------------------------------------
    # DRAW COUNTING LINE
    # --------------------------------------------------------

    cv2.line(
        frame,
        (COUNT_LINE_X, 0),
        (COUNT_LINE_X, height),
        (255, 255, 0),
        4
    )

    cv2.putText(
        frame,
        "COUNTING LINE",
        (COUNT_LINE_X - 150, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )


    # Current-frame vehicle counts
    current_cars = 0
    current_motorcycles = 0
    current_buses = 0
    current_trucks = 0


    # --------------------------------------------------------
    # PROCESS TRACKED OBJECTS
    # --------------------------------------------------------

    if result.boxes is not None and result.boxes.id is not None:

        boxes = result.boxes.xyxy.cpu().numpy()
        track_ids = result.boxes.id.cpu().numpy().astype(int)
        classes = result.boxes.cls.cpu().numpy().astype(int)
        confidences = result.boxes.conf.cpu().numpy()


        for box, track_id, class_id, confidence in zip(
            boxes,
            track_ids,
            classes,
            confidences
        ):

            # Ignore non-vehicle classes
            if class_id not in VEHICLE_CLASSES:
                continue


            x1, y1, x2, y2 = map(int, box)

            class_name = VEHICLE_CLASSES[class_id]

            # ------------------------------------------------
            # CURRENT FRAME VEHICLE COUNTS
            # ------------------------------------------------

            if class_name == "Car":
                current_cars += 1

            elif class_name == "Motorcycle":
                current_motorcycles += 1

            elif class_name == "Bus":
                current_buses += 1

            elif class_name == "Truck":
                current_trucks += 1


            # ------------------------------------------------
            # CENTER POINT
            # ------------------------------------------------

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)


            # ------------------------------------------------
            # DRAW BOUNDING BOX
            # ------------------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # ------------------------------------------------
            # TRACKING LABEL
            # ------------------------------------------------

            label = (
                f"ID:{track_id} "
                f"{class_name} "
                f"{confidence:.2f}"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


            # ------------------------------------------------
            # DRAW CENTER POINT
            # ------------------------------------------------

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )


            # ------------------------------------------------
            # COUNT LINE CROSSING
            # ------------------------------------------------

            if track_id in previous_positions:

                previous_x = previous_positions[track_id]

                # --------------------------------------------
                # LEFT -> RIGHT
                # --------------------------------------------

                if (
                    previous_x < COUNT_LINE_X
                    and center_x >= COUNT_LINE_X
                    and track_id not in counted_ids
                ):

                    counted_ids.add(track_id)
                    right_ids.add(track_id)

                    total_count += 1
                    right_crossings += 1

                    if class_name == "Car":
                        car_count += 1

                    elif class_name == "Motorcycle":
                        motorcycle_count += 1

                    elif class_name == "Bus":
                        bus_count += 1

                    elif class_name == "Truck":
                        truck_count += 1

                    print(
                        f"➡ RIGHT | ID {track_id} | {class_name}"
                    )


                # --------------------------------------------
                # RIGHT -> LEFT
                # --------------------------------------------

                elif (
                    previous_x > COUNT_LINE_X
                    and center_x <= COUNT_LINE_X
                    and track_id not in counted_ids
                ):

                    counted_ids.add(track_id)
                    left_ids.add(track_id)

                    total_count += 1
                    left_crossings += 1

                    if class_name == "Car":
                        car_count += 1

                    elif class_name == "Motorcycle":
                        motorcycle_count += 1

                    elif class_name == "Bus":
                        bus_count += 1

                    elif class_name == "Truck":
                        truck_count += 1

                    print(
                        f"⬅ LEFT | ID {track_id} | {class_name}"
                    )


            # Save current position
            previous_positions[track_id] = center_x


    # ========================================================
    # DENSITY
    # ========================================================

    current_vehicle_count = (
        current_cars
        + current_motorcycles
        + current_buses
        + current_trucks
    )


    if current_vehicle_count < 5:
        density = "LOW"

    elif current_vehicle_count < 10:
        density = "MODERATE"

    else:
        density = "HIGH"


    # ========================================================
    # FLOW RATE
    # ========================================================

    elapsed_seconds = frame_number / fps

    if elapsed_seconds > 0:
        flow_rate = (
            total_count / elapsed_seconds
        ) * 60
    else:
        flow_rate = 0


    # ========================================================
    # DISPLAY INFORMATION ON VIDEO
    # ========================================================

    # Header
    cv2.rectangle(
        frame,
        (20, 20),
        (520, 235),
        (0, 0, 0),
        -1
    )


    cv2.putText(
        frame,
        "SMARTFLOW",
        (40, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        3
    )


    cv2.putText(
        frame,
        f"Total Count : {total_count}",
        (40, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"LEFT : {left_crossings}",
        (40, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"RIGHT : {right_crossings}",
        (40, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Density : {density}",
        (40, 195),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Flow : {flow_rate:.2f} vehicles/min",
        (40, 225),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    # ========================================================
    # LOG DATA EVERY FEW SECONDS
    # ========================================================

    log_interval = max(1, int(fps * LOG_SECONDS))

    if frame_number % log_interval == 0:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        csv_writer.writerow([
            timestamp,
            frame_number,
            current_vehicle_count,
            current_cars,
            current_motorcycles,
            current_buses,
            current_trucks,
            density,
            right_crossings,
            left_crossings,
            f"{flow_rate:.2f}"
        ])

        csv_file.flush()

        print(
            f"📊 Data logged | "
            f"Frame={frame_number} | "
            f"Vehicles={current_vehicle_count} | "
            f"Density={density}"
        )


    # ========================================================
    # SHOW VIDEO
    # ========================================================

    display_frame = cv2.resize(
        frame,
        (1000, 600)
    )

    cv2.imshow(
        "SMARTFLOW - Tracking & Counting",
        display_frame
    )


    # Save annotated frame
    writer.write(frame)


    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# RELEASE RESOURCES
# ============================================================

cap.release()
writer.release()
csv_file.close()

cv2.destroyAllWindows()


# ============================================================
# FINAL REPORT
# ============================================================

print("\n==============================================")
print("        SMARTFLOW FINAL REPORT")
print("==============================================")

print(f"Total Vehicles : {total_count}")
print(f"Right Direction: {right_crossings}")
print(f"Left Direction : {left_crossings}")

print(f"Cars           : {car_count}")
print(f"Motorcycles    : {motorcycle_count}")
print(f"Buses          : {bus_count}")
print(f"Trucks         : {truck_count}")

print(f"Average Flow   : {flow_rate:.2f} vehicles/min")

print("\n----------------------------------------------")
print("Output video:")
print(OUTPUT_VIDEO)

print("\nCSV report:")
print(CSV_FILE)

print("----------------------------------------------")
print("SMARTFLOW processing completed!")
print("==============================================\n")