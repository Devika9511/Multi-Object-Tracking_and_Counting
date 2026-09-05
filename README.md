# SMARTFLOW – Smart Traffic Detection, Tracking and Counting System

SMARTFLOW is a computer vision-based traffic monitoring system that detects, tracks, and counts vehicles from video footage.

The system uses YOLO for vehicle detection, ByteTrack for object tracking, OpenCV for video processing, and Streamlit for the interactive dashboard.

## Features

- Vehicle detection using YOLO
- Multi-object tracking using ByteTrack
- Unique vehicle counting using line-crossing logic
- Direction-based crossing counts
- Vehicle classification
- Traffic density estimation
- Traffic flow estimation
- CSV-based traffic data logging
- Interactive Streamlit dashboard
- Manual count validation
- Count accuracy reporting

## Technologies Used

- Python 3.11
- YOLO / Ultralytics
- ByteTrack
- OpenCV
- Pandas
- Streamlit
- Matplotlib

## Project Structure

```text
SMARTFLOW/
│
├── input/
│   └── traffic.mp4
│
├── models/
│
├── output/
│   ├── smartflow_tracked.mp4
│   └── smartflow_tracked_h264.mp4
│
├── reports/
│   ├── traffic_data.csv
│   ├── ml_dataset.csv
│   └── count_report.csv
│
├── src/
│   ├── main.py
│   ├── tracking.py
│   ├── counter.py
│   ├── direction.py
│   ├── density.py
│   ├── data_logger.py
│   ├── yolo_detect.py
│   ├── video_test.py
│   ├── analyze_data.py
│   └── prepare_dataset.py
│
├── app.py
├── manual_count_validator.py
├── yolo11n.pt
├── requirements.txt
└── README.md