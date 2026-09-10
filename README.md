SMARTFLOW is a computer vision-based traffic monitoring system that detects, tracks, and counts multiple moving objects from video footage.

The system uses YOLO11 for object detection, ByteTrack for multi-object tracking, OpenCV for video processing, and Streamlit for the interactive dashboard.

Project type: Multi-Object Tracking & Counting From Video
Language: Python 3.11

Features

Multi-object detection using YOLO11

Multi-object tracking using ByteTrack

Unique object IDs across video frames

Line-crossing based counting

Direction-based crossing counts (LEFT / RIGHT)

Object classification

Traffic density estimation

Traffic flow estimation

CSV-based traffic data logging

Interactive Streamlit dashboard

Support for multiple input videos

H.264 tracked-video generation for browser/dashboard playback

Manual count validation

Count accuracy reporting

Technologies Used

Python 3.11

YOLO11 / Ultralytics

ByteTrack

OpenCV

Pandas

Streamlit

Matplotlib

How the System Works

A video is loaded from the input/ folder.

YOLO11 detects objects in each frame.

ByteTrack assigns and maintains a unique ID for each tracked object.

The center point of each object is monitored relative to a virtual vertical counting line.

When an object crosses the line, its ID is counted once.

The crossing direction is recorded as LEFT or RIGHT.

Object counts, density, direction, and flow information are logged to CSV.

The processed video is saved with tracking annotations.

Streamlit displays the results through an interactive dashboard.

Counting Logic

The system uses a vertical counting line positioned at approximately 60% of the video width.

LEFT crossing: object center moves from the right side of the line to the left side.

RIGHT crossing: object center moves from the left side of the line to the right side.

An object is counted only once using its unique tracking ID.

Objects that do not cross the line are not included in the crossing count.

This prevents the same tracked object from being double-counted.

Project Structure

SMARTFLOW/
│
├── input/
│   ├── traffic.mp4
│   └── example1.mp4
│
├── models/
│
├── output/
│   ├── smartflow_traffic_tracked.mp4
│   ├── smartflow_traffic_tracked_h264.mp4
│   ├── smartflow_example1_tracked.mp4
│   └── smartflow_example1_tracked_h264.mp4
│
├── reports/
│   ├── traffic_data.csv
│   ├── example1_traffic_data.csv
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
│   ├── video_test.py
│   ├── analyze_data.py
│   └── prepare_dataset.py
│
├── app.py
├── manual_count_validator.py
├── yolo11n.pt
├── requirements.txt
└── README.md

Installation

1. Clone the repository

git clone https://github.com/Devika9511/Multi-Object-Tracking_and_Counting.git
cd Multi-Object-Tracking_and_Counting

2. Create a virtual environment

Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

If the YOLO model is not already present, place yolo11n.pt in the project root.

Input Video

Place one or more .mp4 files in:

input/

Example:

input/
├── traffic.mp4
└── example1.mp4

The dashboard automatically detects available MP4 files and allows the user to select the video to analyze.

For GitHub, large video files can be kept out of the repository and supplied locally in the input/ folder.

Run the Tracking Pipeline

From the project root:

python src\main.py input\traffic.mp4

For another video:

python src\main.py input\example1.mp4

If no input path is provided, the program uses:

input/traffic.mp4

The processed video is saved under:

output/

and the per-video traffic report is saved under:

reports/

For example:

output/smartflow_example1_tracked.mp4
reports/example1_traffic_data.csv

Run the Streamlit Dashboard

Start the dashboard with:

streamlit run app.py

The dashboard provides:

Input video selection

Run Analysis button

Tracked video preview

Objects in frame

Total objects counted

LEFT crossings

RIGHT crossings

Traffic density

Flow rate

Object-type statistics

Analytics charts

Count validation

Sample Test Results

The pipeline was tested on two videos.

Video

Resolution

FPS

Frames

System Total

LEFT

RIGHT

traffic.mp4

1920×1080

25

525

9

4

5

example1.mp4

3840×2160

30

323

6

6

0

traffic.mp4

Detected object types in the tested run included:

Car: 6

Truck: 2

Person: 1

System result:

Total Objects Counted : 9
Right Crossings       : 5
Left Crossings        : 4
Average Flow          : 25.71 objects/min

example1.mp4

Detected object types in the tested run included:

Car: 2

Person: 2

Bus: 1

Motorcycle: 1

System result:

Total Objects Counted : 6
Right Crossings       : 0
Left Crossings        : 6
Average Flow          : 33.44 objects/min

Manual Count Validation

For example1.mp4, manual counting was performed using the same virtual counting line and the same rule used by the system.

Metric

Manual

System

Difference

LEFT

6

6

0

RIGHT

0

0

0

Total

6

6

0

Accuracy

100%

100%

—

The validation report is stored in:

reports/count_report.csv

The traffic.mp4 system result is included above as a pipeline test result. A separate manual accuracy claim for that video should only be added after completing its manual validation.

Output Reports

traffic_data.csv

Contains frame-level traffic information such as:

Timestamp

Frame number

Objects

Vehicles

Persons

Object categories

Density

Direction

Flow rate

count_report.csv

Contains manual-versus-system validation results.

Example:

video,manual_left,manual_right,manual_total,system_left,system_right,system_total,difference,accuracy_percent,status
example1.mp4,6,0,6,6,0,6,0,100.00,VERIFIED

Object Classes

The current pipeline supports multiple YOLO object classes rather than restricting detection to vehicles.

Common classes include:

Person

Bicycle

Car

Motorcycle

Bus

Truck

Other YOLO-supported objects

The standard COCO model does not provide a dedicated auto-rickshaw class. An auto-rickshaw may therefore be classified as another available class such as car or truck. This is a known limitation of using a general-purpose COCO-trained detector.

Known Limitations

Detection accuracy depends on the quality, resolution, lighting, and camera angle of the input video.

Heavy occlusion can cause missed detections or ID changes.

Very small or distant objects may not be detected reliably.

ByteTrack can lose an object temporarily when it is heavily occluded.

The counting line position may need adjustment for different camera views.

A general YOLO11 COCO model does not have a dedicated auto-rickshaw class.

Very high-resolution videos can require more processing time.

Manual validation must use the same counting-line definition as the automated system.

Why YOLO11 + ByteTrack?

YOLO11

YOLO11 provides real-time object detection and identifies objects in individual video frames.

ByteTrack

ByteTrack associates detections across consecutive frames and maintains track IDs. This allows SMARTFLOW to determine whether an object has crossed the counting line and prevents repeated counting of the same tracked ID.

Assignment Deliverables

The project includes the main components required for the multi-object tracking and counting task:

Working detection and tracking pipeline

Video testing on multiple videos

Line-crossing object counting

Direction-based counting

CSV count/data reports

Manual count validation

Streamlit dashboard

Technical report

GitHub-ready project structure

README documentation

Repository

GitHub repository:

https://github.com/Devika9511/Multi-Object-Tracking_and_Counting

Quick Start

# Activate environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run analysis
python src\main.py input\traffic.mp4

# Run dashboard
streamlit run app.py

Conclusion

SMARTFLOW demonstrates a complete computer-vision pipeline for detecting, tracking, and counting multiple objects in traffic video. By combining YOLO11 detection with ByteTrack tracking and line-crossing logic, the system maintains object identities and counts crossing events without intentionally double-counting the same track.

The Streamlit dashboard provides a simple interface for running analysis, viewing the tracked video, and inspecting traffic statistics and validation results.