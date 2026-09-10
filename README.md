md


🚦 SMARTFLOW – Smart Traffic Detection, Tracking and Counting System
<p align="center"> <b>Multi-Object Detection • Tracking • Counting • Traffic Analytics</b> </p>

SMARTFLOW is a computer vision-based traffic monitoring system that detects, tracks, classifies, and counts moving objects from traffic video footage.

The system combines YOLO11 for object detection, ByteTrack for multi-object tracking, OpenCV for video processing, and Streamlit for an interactive dashboard.

📌 Project Overview
SMARTFLOW processes traffic videos frame by frame and assigns a unique tracking ID to each detected object.

A virtual counting line is placed across the video. When an object's center crosses the line, the system records:

Object ID

Object type

Crossing direction

Timestamp

Frame number

Each tracked ID is counted only once, helping prevent double-counting.

🎯 Objectives
Detect moving objects from traffic videos.

Track objects across consecutive frames.

Assign a unique ID to each tracked object.

Count objects crossing a virtual line.

Determine LEFT and RIGHT crossing directions.

Estimate traffic density and flow rate.

Store traffic statistics in CSV reports.

Compare automated counts with manual counts.

Provide an interactive Streamlit dashboard.

✨ Features
Feature	Description
🔍 Object Detection	Detects objects using YOLO11
🎯 Multi-Object Tracking	Tracks objects using ByteTrack
🆔 Unique IDs	Maintains an ID for each tracked object
🚧 Line Crossing	Counts objects crossing a virtual line
↔️ Direction Detection	Identifies LEFT and RIGHT crossings
🚗 Object Classification	Classifies detected object types
📊 Density Estimation	Estimates traffic density
📈 Flow Estimation	Calculates objects/minute
📝 CSV Logging	Saves frame-level traffic information
🖥️ Dashboard	Interactive Streamlit interface
✅ Manual Validation	Compares manual and system counts
🎬 Demo Output	Includes a processed tracking demonstration
🛠️ Technologies Used
Technology	Purpose
Python 3.11	Application development
YOLO11 / Ultralytics	Object detection
ByteTrack	Multi-object tracking
OpenCV	Video processing
Pandas	Data processing and CSV reports
Streamlit	Interactive dashboard
Matplotlib	Analytics and visualization
🔄 System Workflow
                ┌─────────────────┐
                │   Input Video   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     YOLO11      │
                │ Object Detection│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    ByteTrack    │
                │ Object Tracking │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Unique Track   │
                │       IDs       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Counting Line   │
                │    Crossing     │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │    LEFT     │       │    RIGHT    │
       │   Crossing  │       │   Crossing  │
       └──────┬──────┘       └──────┬──────┘
              └──────────┬──────────┘
                         ▼
                ┌─────────────────┐
                │ Traffic Counts  │
                │ Density & Flow  │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │ CSV Reports │       │ Tracked     │
       │             │       │ Video       │
       └─────────────┘       └──────┬──────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Streamlit       │
                           │ Dashboard       │
                           └─────────────────┘
🚧 Counting Method
SMARTFLOW uses a vertical virtual counting line positioned at approximately 60% of the video width.

             LEFT SIDE              RIGHT SIDE

                    │
                    │  Counting Line
                    │
       ◄────────────│────────────►
                    │
                    │
Direction Rules
LEFT crossing: object moves from the right side of the line to the left side.

RIGHT crossing: object moves from the left side of the line to the right side.

An object is counted only once using its unique tracking ID.

Objects that do not cross the line are not included in the crossing count.

This prevents the same tracked object from being intentionally counted multiple times.

🧠 Object Detection & Tracking
YOLO11
YOLO11 detects objects in each video frame and provides:

Bounding boxes

Object classes

Confidence scores

ByteTrack
ByteTrack associates detections across consecutive frames and maintains tracking IDs.

The tracking ID allows SMARTFLOW to follow the same object over time and apply the count-once rule when it crosses the counting line.

🚗 Supported Object Types
The current pipeline supports multiple YOLO/COCO object classes, including:

👤 Person

🚲 Bicycle

🚗 Car

🏍️ Motorcycle

🚌 Bus

🚚 Truck

Other supported YOLO classes

Note: The standard COCO-trained YOLO model does not contain a dedicated auto-rickshaw class. Therefore, an auto-rickshaw may be classified as another available class such as car or truck. This is a known limitation of the general-purpose model.

📁 Project Structure
SMARTFLOW/
│
├── input/
│   ├── traffic.mp4
│   └── example1.mp4
│
├── models/
│
├── output/
│   └── smartflow_demo.mp4
│
├── reports/
│   ├── traffic_data.csv
│   ├── example1_traffic_data.csv
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
├── SMARTFLOW_Two_Video_Technical_Report.pdf
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Devika9511/Multi-Object-Tracking_and_Counting.git
cd Multi-Object-Tracking_and_Counting
2. Create a Virtual Environment
python -m venv venv
Activate the environment:

.\venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
The repository includes the yolo11n.pt model file.

🎥 Input Video
Place your MP4 video inside:

input/
Example:

input/
├── traffic.mp4
└── example1.mp4
Large input videos are kept outside the GitHub repository to keep the repository lightweight. After cloning, place the required video inside the input/ folder.

▶️ Run the Tracking Pipeline
Analyze traffic.mp4
python src\main.py input\traffic.mp4
Analyze example1.mp4
python src\main.py input\example1.mp4
Default Video
If no video path is provided:

python src\main.py
The default input is:

input/traffic.mp4
🖥️ Run the Streamlit Dashboard
Start the dashboard:

streamlit run app.py
The dashboard allows you to:

Select an input video.

Run the analysis.

View the tracked video.

View objects currently in the frame.

View total counted objects.

View LEFT crossings.

View RIGHT crossings.

View traffic density.

View flow rate.

View object-type statistics.

View analytics.

View count validation.

📊 Dashboard Metrics
The dashboard displays:

┌──────────────────────────────┐
│ Objects in Frame             │
├──────────────────────────────┤
│ Total Objects Counted        │
├──────────────────────────────┤
│ LEFT Crossings               │
├──────────────────────────────┤
│ RIGHT Crossings              │
├──────────────────────────────┤
│ Traffic Density              │
├──────────────────────────────┤
│ Flow Rate                    │
└──────────────────────────────┘
🎬 Output
The project generates a processed video containing:

Object bounding boxes

Object labels

Tracking IDs

Counting line

Direction information

Count information

Demo Output
A short demonstration output is included:

output/
└── smartflow_demo.mp4
Generated Outputs
For a video such as traffic.mp4, the system generates:

output/
├── smartflow_traffic_tracked.mp4
└── smartflow_traffic_tracked_h264.mp4
For example1.mp4:

output/
├── smartflow_example1_tracked.mp4
└── smartflow_example1_tracked_h264.mp4
The H.264 version is suitable for browser/dashboard playback.

📝 Reports
Traffic Data
reports/traffic_data.csv
Contains frame-level information including:

Timestamp

Frame number

Objects

Object types

Density

Direction

Flow rate

Example Video Report
reports/example1_traffic_data.csv
Contains the traffic analysis data generated for example1.mp4.

Count Validation
reports/count_report.csv
Contains manual-versus-system count comparison.

Technical Report
SMARTFLOW_Two_Video_Technical_Report.pdf
Contains:

Project objective

Methodology

Detector and tracker selection

Counting method

Test results

Manual validation

Known limitations

Conclusion

🧪 Experimental Results
The system was tested on two videos.

Video	Resolution	FPS	Frames	System Total	LEFT	RIGHT
traffic.mp4	1920×1080	25	525	9	4	5
example1.mp4	3840×2160	30	323	6	6	0
traffic.mp4
Detected object types:

Object Type	Count
Car	6
Truck	2
Person	1
Total	9
System result:

Total Objects Counted : 9
LEFT Crossings        : 4
RIGHT Crossings       : 5
Average Flow          : 25.71 objects/min
example1.mp4
Detected object types:

Object Type	Count
Car	2
Person	2
Bus	1
Motorcycle	1
Total	6
System result:

Total Objects Counted : 6
LEFT Crossings        : 6
RIGHT Crossings       : 0
Average Flow          : 33.44 objects/min
✅ Manual Count Validation
For example1.mp4, manual counting was performed using the same virtual counting line and crossing rules used by the system.

Metric	Manual	System	Difference
LEFT	6	6	0
RIGHT	0	0	0
Total	6	6	0
Accuracy	100%	100%	0% difference
Validation file:

reports/count_report.csv
The traffic.mp4 values above represent the automated pipeline test. A manual accuracy value for traffic.mp4 should only be added after separate manual validation.

⚠️ Known Limitations
Detection accuracy depends on video quality, lighting, camera angle, and object size.

Heavy occlusion can cause missed detections.

Small or distant objects may not be detected reliably.

Severe occlusion can result in temporary tracking loss or ID changes.

The counting-line position may need adjustment for different camera views.

The general COCO model does not provide a dedicated auto-rickshaw class.

High-resolution videos require more processing time.

Manual validation depends on applying the same counting-line rule consistently.

🚀 Future Improvements
Train a custom traffic-specific YOLO model.

Add a dedicated auto-rickshaw class.

Improve tracking under heavy occlusion.

Add configurable counting lines.

Add region-of-interest selection.

Add real-time CCTV/camera support.

Add more detailed traffic analytics.

Compare multiple tracking algorithms.

Deploy the dashboard as a web application.

📦 Assignment Deliverables
Deliverable	Status
Object detection pipeline	✅ Completed
Multi-object tracking	✅ Completed
Unique object IDs	✅ Completed
Line-crossing counting	✅ Completed
Direction detection	✅ Completed
Video testing	✅ Completed
CSV traffic reports	✅ Completed
Manual count validation	✅ Completed for example1.mp4
Count report	✅ Completed
Streamlit dashboard	✅ Completed
Tracked demo output	✅ Included
Technical report	✅ Included
GitHub README	✅ Completed
📌 Quick Start
# Clone
git clone https://github.com/Devika9511/Multi-Object-Tracking_and_Counting.git

# Enter project
cd Multi-Object-Tracking_and_Counting

# Create environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Place a video inside input/

# Run analysis
python src\main.py input\traffic.mp4

# Launch dashboard
streamlit run app.py
🔗 GitHub Repository
Repository:
https://github.com/Devika9511/Multi-Object-Tracking_and_Counting

👩‍💻 Project
SMARTFLOW – Smart Traffic Detection, Tracking and Counting System

Built using:

YOLO11 + ByteTrack + OpenCV + Streamlit

