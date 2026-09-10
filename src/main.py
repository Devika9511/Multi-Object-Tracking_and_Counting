import cv2
import os
import csv
import json
import sys
from datetime import datetime
from collections import Counter
from ultralytics import YOLO


# ============================================================
# SMARTFLOW - MULTI-OBJECT TRACKING & COUNTING
# ============================================================
# Detect, track, and count moving objects across a video
# without double-counting.
#
# Supported object classes include:
#   Person
#   Bicycle
#   Car
#   Motorcycle
#   Bus
#   Truck
#   Other YOLO-supported classes
#
# YOLO detects the objects.
# ByteTrack assigns and maintains object IDs.
# A virtual line is used to count objects crossing the line.
# Each tracked ID is counted only once.
# ============================================================


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

# Input video can be selected from the command line:
#   python src\main.py input\traffic.mp4
#   python src\main.py input\example1.mp4
# If no argument is supplied, traffic.mp4 remains the default.
VIDEO_PATH = sys.argv[1] if len(sys.argv) > 1 else "input/traffic.mp4"

MODEL_PATH = "yolo11n.pt"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

VIDEO_STEM = os.path.splitext(os.path.basename(VIDEO_PATH))[0]

# Each input video gets its own output file, so multiple videos can be
# processed without overwriting the previous result.
OUTPUT_VIDEO = os.path.join(
    OUTPUT_DIR,
    f"smartflow_{VIDEO_STEM}_tracked.mp4"
)

# Keep a common latest-results CSV for compatibility with the dashboard.
CSV_FILE = os.path.join(
    REPORT_DIR,
    "traffic_data.csv"
)

# Also save a separate CSV for this specific video.
VIDEO_CSV_FILE = os.path.join(
    REPORT_DIR,
    f"{VIDEO_STEM}_traffic_data.csv"
)


# ============================================================
# DETECTION SETTINGS
# ============================================================

CONFIDENCE = 0.30

# Position of the virtual counting line.
# 0.60 means 60% of the video width.
LINE_POSITION = 0.60

# Log data every 2 seconds.
LOG_SECONDS = 2


# ============================================================
# OBJECT CLASSES
# ============================================================
# These are displayed separately in the dashboard/report.
#
# Other YOLO-supported classes are still detected and tracked.
# They are stored under "other_objects" and "object_types".
# ============================================================

MAIN_CLASSES = {
    "person": "Persons",
    "bicycle": "Bicycles",
    "car": "Cars",
    "motorcycle": "Motorcycles",
    "bus": "Buses",
    "truck": "Trucks",
}


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ============================================================
# START SMARTFLOW
# ============================================================

print("\n==============================================")
print("       SMARTFLOW MULTI-OBJECT ENGINE")
print("==============================================")
print(f"Input video : {VIDEO_PATH}")


# ============================================================
# LOAD YOLO MODEL
# ============================================================

print("\nLoading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully!")
print("Multi-object detection enabled.")


# ============================================================
# OPEN INPUT VIDEO
# ============================================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print("\nERROR: Could not open video.")
    print("Check video path:")
    print(VIDEO_PATH)

    raise SystemExit(1)


# ============================================================
# VIDEO INFORMATION
# ============================================================

width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

fps = cap.get(
    cv2.CAP_PROP_FPS
)

if fps <= 0:
    fps = 25


total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)


print("\nVideo opened successfully!")

print(f"Resolution : {width} x {height}")
print(f"FPS        : {fps:.2f}")
print(f"Frames     : {total_frames}")


# ============================================================
# COUNTING LINE
# ============================================================

COUNT_LINE_X = int(
    width * LINE_POSITION
)

print(
    f"Counting line position: X = {COUNT_LINE_X}"
)


# ============================================================
# CREATE OUTPUT VIDEO
# ============================================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)

writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (width, height)
)


if not writer.isOpened():

    print("\nERROR: Could not create output video.")

    cap.release()

    raise SystemExit(1)


print(
    f"Output video: {OUTPUT_VIDEO}"
)


# ============================================================
# CREATE CLEAN CSV REPORT
# ============================================================
# We use "w" instead of "a" so repeated executions don't
# create duplicate blocks of historical data.
# ============================================================

csv_file = open(
    CSV_FILE,
    "w",
    newline="",
    encoding="utf-8"
)

video_csv_file = open(
    VIDEO_CSV_FILE,
    "w",
    newline="",
    encoding="utf-8"
)

csv_writer = csv.writer(csv_file)
video_csv_writer = csv.writer(video_csv_file)


# ============================================================
# CSV HEADER
# ============================================================

csv_header = [
    "timestamp",
    "frame",
    "objects",
    "vehicles",
    "persons",
    "bicycles",
    "cars",
    "motorcycles",
    "buses",
    "trucks",
    "other_objects",
    "object_types",
    "density",
    "right_direction",
    "left_direction",
    "flow_rate"
]

csv_writer.writerow(csv_header)
video_csv_writer.writerow(csv_header)


# ============================================================
# TRACKING VARIABLES
# ============================================================

# Stores the previous X position of every tracked object.
previous_positions = {}


# IDs that have already crossed the counting line.
#
# This is the main mechanism that prevents the same object
# from being counted multiple times.
counted_ids = set()


# Direction-specific IDs.
right_ids = set()
left_ids = set()


# Total crossing counts.
total_count = 0

right_crossings = 0
left_crossings = 0


# Cumulative count by object class.
counted_class_totals = Counter()


# Frame counter.
frame_number = 0


# Current flow rate.
flow_rate = 0.0


# ============================================================
# HELPER FUNCTION - DENSITY
# ============================================================

def get_density(object_count):

    """
    Estimate traffic/object density from the number
    of objects visible in the current frame.
    """

    if object_count < 5:

        return "LOW"

    elif object_count < 10:

        return "MODERATE"

    else:

        return "HIGH"


# ============================================================
# HELPER FUNCTION - CLASS NAME
# ============================================================

def get_class_name(class_id):

    """
    Convert YOLO class ID into a readable class name.
    """

    try:

        return str(
            model.names[int(class_id)]
        )

    except Exception:

        return "Unknown"


# ============================================================
# MAIN VIDEO PROCESSING LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # READ FRAME
    # --------------------------------------------------------

    success, frame = cap.read()


    if not success:

        break


    frame_number += 1


    # ========================================================
    # YOLO + BYTETRACK
    # ========================================================
    #
    # No vehicle-only class filter is used.
    #
    # Therefore YOLO can detect all supported classes.
    # ByteTrack maintains IDs across frames.
    # ========================================================

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=CONFIDENCE,
        verbose=False
    )


    result = results[0]


    # ========================================================
    # DRAW COUNTING LINE
    # ========================================================

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
        (
            max(
                COUNT_LINE_X - 150,
                10
            ),
            50
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )


    # ========================================================
    # CURRENT FRAME OBJECT COUNTS
    # ========================================================

    current_class_counts = Counter()


    # ========================================================
    # PROCESS TRACKED OBJECTS
    # ========================================================

    if (
        result.boxes is not None
        and result.boxes.id is not None
    ):

        # Bounding boxes.
        boxes = (
            result.boxes.xyxy
            .cpu()
            .numpy()
        )


        # ByteTrack IDs.
        track_ids = (
            result.boxes.id
            .cpu()
            .numpy()
            .astype(int)
        )


        # YOLO class IDs.
        classes = (
            result.boxes.cls
            .cpu()
            .numpy()
            .astype(int)
        )


        # Detection confidence.
        confidences = (
            result.boxes.conf
            .cpu()
            .numpy()
        )


        # ----------------------------------------------------
        # PROCESS EACH OBJECT
        # ----------------------------------------------------

        for (
            box,
            track_id,
            class_id,
            confidence
        ) in zip(
            boxes,
            track_ids,
            classes,
            confidences
        ):

            # ------------------------------------------------
            # BOUNDING BOX
            # ------------------------------------------------

            x1, y1, x2, y2 = map(
                int,
                box
            )


            # ------------------------------------------------
            # OBJECT CLASS
            # ------------------------------------------------

            class_name = get_class_name(
                class_id
            )


            # ------------------------------------------------
            # CURRENT FRAME CLASS COUNT
            # ------------------------------------------------

            current_class_counts[
                class_name
            ] += 1


            # ------------------------------------------------
            # OBJECT CENTER
            # ------------------------------------------------

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )


            # =================================================
            # DRAW BOUNDING BOX
            # =================================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # =================================================
            # OBJECT LABEL
            # =================================================

            label = (
                f"ID:{track_id} "
                f"{class_name} "
                f"{confidence:.2f}"
            )


            cv2.putText(
                frame,
                label,
                (
                    x1,
                    max(
                        y1 - 10,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


            # =================================================
            # DRAW CENTER POINT
            # =================================================

            cv2.circle(
                frame,
                (
                    center_x,
                    center_y
                ),
                5,
                (0, 0, 255),
                -1
            )


            # =================================================
            # LINE CROSSING DETECTION
            # =================================================

            if track_id in previous_positions:

                previous_x = (
                    previous_positions[
                        track_id
                    ]
                )


                # =================================================
                # LEFT -> RIGHT
                # =================================================

                if (
                    previous_x < COUNT_LINE_X
                    and center_x >= COUNT_LINE_X
                    and track_id not in counted_ids
                ):

                    # Mark this ID as counted.
                    counted_ids.add(
                        track_id
                    )


                    right_ids.add(
                        track_id
                    )


                    # Update total counts.
                    total_count += 1

                    right_crossings += 1


                    # Update object class count.
                    counted_class_totals[
                        class_name
                    ] += 1


                    print(
                        f"RIGHT | "
                        f"ID {track_id} | "
                        f"{class_name}"
                    )


                # =================================================
                # RIGHT -> LEFT
                # =================================================

                elif (
                    previous_x > COUNT_LINE_X
                    and center_x <= COUNT_LINE_X
                    and track_id not in counted_ids
                ):

                    # Mark this ID as counted.
                    counted_ids.add(
                        track_id
                    )


                    left_ids.add(
                        track_id
                    )


                    # Update total counts.
                    total_count += 1

                    left_crossings += 1


                    # Update object class count.
                    counted_class_totals[
                        class_name
                    ] += 1


                    print(
                        f"LEFT | "
                        f"ID {track_id} | "
                        f"{class_name}"
                    )


            # ------------------------------------------------
            # SAVE CURRENT POSITION
            # ------------------------------------------------

            previous_positions[
                track_id
            ] = center_x


    # ========================================================
    # CURRENT OBJECT COUNT
    # ========================================================

    current_object_count = sum(
        current_class_counts.values()
    )


    # ========================================================
    # COMPATIBILITY VEHICLE VALUE
    # ========================================================
    #
    # This column is retained so the existing dashboard/data
    # structure does not immediately break.
    #
    # It now represents total visible objects.
    # The new dashboard will use "objects" instead.
    # ========================================================

    vehicles_compatibility_count = (
        current_object_count
    )


    # ========================================================
    # OBJECT DENSITY
    # ========================================================

    density = get_density(
        current_object_count
    )


    # ========================================================
    # FLOW RATE
    # ========================================================
    #
    # Flow is based on objects that have crossed the line.
    # ========================================================

    elapsed_seconds = (
        frame_number / fps
    )


    if elapsed_seconds > 0:

        flow_rate = (
            total_count
            / elapsed_seconds
        ) * 60

    else:

        flow_rate = 0.0


    # ========================================================
    # DASHBOARD INFORMATION ON VIDEO
    # ========================================================

    cv2.rectangle(
        frame,
        (20, 20),
        (620, 285),
        (0, 0, 0),
        -1
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    cv2.putText(
        frame,
        "SMARTFLOW",
        (40, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        3
    )


    # --------------------------------------------------------
    # OBJECTS IN FRAME
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"Objects in Frame : {current_object_count}",
        (40, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # TOTAL COUNTED
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"Total Counted    : {total_count}",
        (40, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # LEFT CROSSINGS
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"LEFT Crossings   : {left_crossings}",
        (40, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # RIGHT CROSSINGS
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"RIGHT Crossings  : {right_crossings}",
        (40, 195),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # DENSITY
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"Density          : {density}",
        (40, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.70,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # FLOW RATE
    # --------------------------------------------------------

    cv2.putText(
        frame,
        f"Flow             : {flow_rate:.2f} objects/min",
        (40, 265),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    # ========================================================
    # LOG DATA EVERY FEW SECONDS
    # ========================================================

    log_interval = max(
        1,
        int(
            fps * LOG_SECONDS
        )
    )


    if frame_number % log_interval == 0:

        timestamp = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # ----------------------------------------------------
        # MAIN OBJECT CLASSES
        # ----------------------------------------------------

        persons = current_class_counts.get(
            "person",
            0
        )


        bicycles = current_class_counts.get(
            "bicycle",
            0
        )


        cars = current_class_counts.get(
            "car",
            0
        )


        motorcycles = current_class_counts.get(
            "motorcycle",
            0
        )


        buses = current_class_counts.get(
            "bus",
            0
        )


        trucks = current_class_counts.get(
            "truck",
            0
        )


        # ----------------------------------------------------
        # OTHER OBJECTS
        # ----------------------------------------------------

        other_objects = (
            current_object_count
            - persons
            - bicycles
            - cars
            - motorcycles
            - buses
            - trucks
        )


        # ----------------------------------------------------
        # ALL OBJECT TYPES
        # ----------------------------------------------------
        # Example:
        # {"car":8,"person":2,"truck":1}
        # ----------------------------------------------------

        object_types = json.dumps(
            dict(
                sorted(
                    current_class_counts.items()
                )
            ),
            separators=(
                ",",
                ":"
            )
        )


        # ----------------------------------------------------
        # WRITE CSV ROW
        # ----------------------------------------------------

        csv_row = [

            timestamp,

            frame_number,

            current_object_count,

            vehicles_compatibility_count,

            persons,

            bicycles,

            cars,

            motorcycles,

            buses,

            trucks,

            other_objects,

            object_types,

            density,

            right_crossings,

            left_crossings,

            f"{flow_rate:.2f}"

        ]

        csv_writer.writerow(csv_row)
        video_csv_writer.writerow(csv_row)

        csv_file.flush()
        video_csv_file.flush()


        # ----------------------------------------------------
        # TERMINAL LOG
        # ----------------------------------------------------

        print(
            f"Data logged | "
            f"Frame={frame_number} | "
            f"Objects={current_object_count} | "
            f"Density={density}"
        )


    # ========================================================
    # SAVE ANNOTATED FRAME
    # ========================================================

    writer.write(
        frame
    )


    # ========================================================
    # LIVE DISPLAY
    # ========================================================

    display_frame = cv2.resize(
        frame,
        (1000, 600)
    )


    cv2.imshow(
        "SMARTFLOW - Multi-Object Tracking & Counting",
        display_frame
    )


    # ========================================================
    # PRESS Q TO STOP
    # ========================================================

    if (
        cv2.waitKey(1) & 0xFF
        == ord("q")
    ):

        break


# ============================================================
# RELEASE RESOURCES
# ============================================================

cap.release()

writer.release()

csv_file.close()
video_csv_file.close()

cv2.destroyAllWindows()


# ============================================================
# FINAL REPORT
# ============================================================

print("\n==============================================")
print("       SMARTFLOW FINAL REPORT")
print("==============================================")


print(
    f"Total Objects Counted : {total_count}"
)


print(
    f"Right Crossings       : {right_crossings}"
)


print(
    f"Left Crossings        : {left_crossings}"
)


# ============================================================
# COUNTED OBJECT TYPES
# ============================================================

print("\nCounted Object Types:")


if counted_class_totals:

    for (
        class_name,
        count
    ) in sorted(
        counted_class_totals.items(),
        key=lambda item: (
            -item[1],
            item[0]
        )
    ):

        print(
            f"  {class_name:<15}: {count}"
        )

else:

    print(
        "  No objects crossed the counting line."
    )


# ============================================================
# FLOW
# ============================================================

print(
    f"\nAverage Flow         : "
    f"{flow_rate:.2f} objects/min"
)


# ============================================================
# OUTPUT INFORMATION
# ============================================================

print(
    "\n----------------------------------------------"
)


print(
    "Output video:"
)


print(
    OUTPUT_VIDEO
)


print(
    "\nCSV report:"
)


print(
    CSV_FILE
)

print(
    "\nVideo-specific CSV report:"
)

print(
    VIDEO_CSV_FILE
)


print(
    "----------------------------------------------"
)


print(
    "SMARTFLOW multi-object processing completed!"
)


print(
    "==============================================\n"
)