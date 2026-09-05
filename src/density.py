import cv2
from ultralytics import YOLO

# ============================================================
# SMARTFLOW - TRAFFIC DENSITY ANALYSIS
# ============================================================

print("========================================")
print("      SMARTFLOW TRAFFIC DENSITY")
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

# ============================================================
# VEHICLE CLASSES
# ============================================================

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

# ============================================================
# DENSITY THRESHOLDS
# ============================================================

LOW_THRESHOLD = 5
HIGH_THRESHOLD = 10

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ========================================================
    # YOLO DETECTION
    # ========================================================

    results = model(
        frame,
        classes=list(VEHICLE_CLASSES.keys()),
        conf=0.30,
        verbose=False
    )

    result = results[0]

    # Number of vehicles in current frame
    vehicle_count = 0

    # Individual counts
    car_count = 0
    motorcycle_count = 0
    bus_count = 0
    truck_count = 0

    # ========================================================
    # PROCESS DETECTIONS
    # ========================================================

    if result.boxes is not None:

        class_ids = result.boxes.cls.int().cpu().tolist()

        for class_id in class_ids:

            vehicle_count += 1

            if class_id == 2:
                car_count += 1

            elif class_id == 3:
                motorcycle_count += 1

            elif class_id == 5:
                bus_count += 1

            elif class_id == 7:
                truck_count += 1

    # ========================================================
    # DETERMINE TRAFFIC DENSITY
    # ========================================================

    if vehicle_count < LOW_THRESHOLD:

        density = "LOW"

    elif vehicle_count < HIGH_THRESHOLD:

        density = "MODERATE"

    else:

        density = "HIGH"

    # ========================================================
    # DRAW DETECTIONS
    # ========================================================

    annotated_frame = result.plot()

    # ========================================================
    # DISPLAY DENSITY
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"Vehicles in Frame: {vehicle_count}",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Traffic Density: {density}",
        (25, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        3
    )

    # ========================================================
    # VEHICLE BREAKDOWN
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"Cars: {car_count}",
        (25, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Motorcycles: {motorcycle_count}",
        (25, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Buses: {bus_count}",
        (25, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Trucks: {truck_count}",
        (25, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # ========================================================
    # RESIZE
    # ========================================================

    display_frame = cv2.resize(
        annotated_frame,
        (1000, 600)
    )

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        "SmartFlow - Traffic Density",
        display_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()

print()
print("========================================")
print("✅ Traffic density analysis completed")
print("========================================")