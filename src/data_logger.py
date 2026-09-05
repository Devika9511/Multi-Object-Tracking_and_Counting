import csv
import os
from datetime import datetime

# ============================================================
# SMARTFLOW - TRAFFIC DATA LOGGER
# ============================================================

REPORT_FOLDER = "reports"
CSV_FILE = os.path.join(REPORT_FOLDER, "traffic_data.csv")


def initialize_logger():

    # Create reports folder if it doesn't exist
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    # Create CSV with headers if it doesn't exist
    if not os.path.exists(CSV_FILE):

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
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

        print("✅ New traffic_data.csv created")

    else:

        print("✅ Existing traffic_data.csv found")


def log_traffic_data(
    frame,
    vehicles,
    cars,
    motorcycles,
    buses,
    trucks,
    density,
    right_direction,
    left_direction,
    flow_rate
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            frame,
            vehicles,
            cars,
            motorcycles,
            buses,
            trucks,
            density,
            right_direction,
            left_direction,
            round(flow_rate, 2)
        ])


# ============================================================
# TEST LOGGER
# ============================================================

if __name__ == "__main__":

    initialize_logger()

    # Test record
    log_traffic_data(
        frame=1,
        vehicles=5,
        cars=4,
        motorcycles=0,
        buses=0,
        trucks=1,
        density="MODERATE",
        right_direction=3,
        left_direction=2,
        flow_rate=20.5
    )

    print("✅ Test traffic record saved!")
    print(f"📁 File: {CSV_FILE}")