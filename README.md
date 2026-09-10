# SMARTFLOW – Smart Traffic Detection, Tracking and Counting System

SMARTFLOW is a **computer vision-based traffic monitoring system** that detects, tracks, classifies, and counts moving objects from traffic video footage.

The system uses **YOLO11** for object detection, **ByteTrack** for multi-object tracking, **OpenCV** for video processing, and **Streamlit** for the interactive dashboard.

---

## 📌 Project Overview

SMARTFLOW processes traffic video frame by frame and assigns a **unique tracking ID** to each detected object.

A virtual counting line is placed in the video. When the center of a tracked object crosses this line, the system records the object and its direction. Each tracking ID is counted only once to avoid double-counting.

### What the system provides

- Object detection
- Multi-object tracking
- Unique object IDs
- Line-crossing counting
- LEFT / RIGHT direction detection
- Object classification
- Traffic density estimation
- Traffic flow estimation
- CSV data logging
- Manual count validation
- Interactive Streamlit dashboard
- Processed tracking video output

---

## 🎯 Objectives

- Detect moving objects from traffic videos.
- Track objects across consecutive frames.
- Assign a unique ID to each tracked object.
- Count objects when they cross a virtual line.
- Identify the direction of movement.
- Avoid counting the same tracked object more than once.
- Generate traffic statistics and CSV reports.
- Compare automated counts with manual counts.
- Provide a simple dashboard for visualization.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Object Detection | YOLO11 detects objects in each frame |
| 🎯 Multi-Object Tracking | ByteTrack maintains object identities |
| 🆔 Unique Tracking IDs | Each tracked object receives an ID |
| 🚧 Line Crossing | Objects are counted when crossing the virtual line |
| ↔️ Direction Detection | LEFT and RIGHT crossings are recorded |
| 🚗 Object Classification | Objects are classified by type |
| 📊 Density Estimation | Estimates the current traffic density |
| 📈 Flow Estimation | Calculates objects per minute |
| 📝 CSV Logging | Stores frame-level traffic information |
| 🖥️ Streamlit Dashboard | Provides an interactive visual interface |
| ✅ Manual Validation | Compares manual and automated counts |
| 🎬 Demo Output | Provides a processed tracking video |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| YOLO11 / Ultralytics | Object detection |
| ByteTrack | Multi-object tracking |
| OpenCV | Video processing and annotation |
| Pandas | Data processing and CSV reports |
| Streamlit | Interactive dashboard |
| Matplotlib | Data visualization |

---

## 🔄 System Workflow

```text
Input Video
    ↓
YOLO11 Object Detection
    ↓
ByteTrack Object Tracking
    ↓
Unique Tracking IDs
    ↓
Virtual Counting Line
    ↓
LEFT / RIGHT Crossing Detection
    ↓
Count Each ID Once
    ↓
Traffic Statistics
    ↓
CSV Reports + Tracked Video
    ↓
Streamlit Dashboard
```

---

## 🚧 Counting Method

SMARTFLOW uses a **vertical virtual counting line positioned at approximately 60% of the video width**.

```text
        LEFT SIDE       COUNTING LINE       RIGHT SIDE

             ←                │                →
                              │
                              │
             ←                │                →
```

### Counting Rules

- **LEFT crossing:** object moves from the right side of the line to the left side.
- **RIGHT crossing:** object moves from the left side of the line to the right side.
- Each tracked ID is counted only once.
- Objects that do not cross the line are not included in the crossing count.

This approach helps prevent double-counting.

---

## 🧠 Detection and Tracking

### YOLO11

YOLO11 is used to detect objects in every video frame.

It provides:

- Bounding boxes
- Object classes
- Confidence scores

### ByteTrack

ByteTrack associates detections across consecutive frames and maintains a tracking ID for each object.

The tracking ID allows SMARTFLOW to follow an object over time and determine whether it has crossed the counting line.

---

## 🚗 Supported Object Types

The current multi-object pipeline supports YOLO/COCO classes including:

- Person
- Bicycle
- Car
- Motorcycle
- Bus
- Truck
- Other supported YOLO classes

> **Limitation:** The standard COCO-trained YOLO model does not have a dedicated `auto-rickshaw` class. Therefore, an auto-rickshaw may be classified as another available class such as `car` or `truck`.

---

## 📁 Project Structure

```text
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
├── SMARTFLOW_Two_Video_Technical_Report.pdf
├── .gitignore
└── README.md
```

> **Note:** Large input videos are kept outside the GitHub repository. The `input/` folder is shown above to explain where videos should be placed when running the project locally.

---

## ⚙️ Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/Devika9511/Multi-Object-Tracking_and_Counting.git
cd Multi-Object-Tracking_and_Counting
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.env\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

The repository contains the `yolo11n.pt` model file.

---

## 🎥 Input Video

Place an MP4 video inside:

```text
input/
```

For example:

```text
input/
├── traffic.mp4
└── example1.mp4
```

The Streamlit dashboard automatically detects available MP4 files in the `input/` folder.

---

## ▶️ Run the Tracking Pipeline

### Analyze traffic.mp4

```powershell
python src\main.py input	raffic.mp4
```

### Analyze example1.mp4

```powershell
python src\main.py input\example1.mp4
```

### Use the default video

```powershell
python src\main.py
```

The default video is:

```text
input/traffic.mp4
```

---

## 🖥️ Run the Streamlit Dashboard

Start the dashboard:

```powershell
streamlit run app.py
```

The dashboard allows you to:

1. Select an input video.
2. Run the analysis.
3. View the tracked video.
4. View objects currently in the frame.
5. View total objects counted.
6. View LEFT crossings.
7. View RIGHT crossings.
8. View traffic density.
9. View flow rate.
10. View object-type statistics.
11. View analytics.
12. View count validation.

---

## 🎬 Output

SMARTFLOW generates a processed video containing:

- Object bounding boxes
- Object labels
- Tracking IDs
- Counting line
- Direction information
- Count information

### Demo Output

A short processed demonstration video is included in the repository:

```text
output/
└── smartflow_demo.mp4
```

The demo output is provided so that the project can be inspected without uploading the large original traffic videos.

### Generated Output for traffic.mp4

```text
output/
├── smartflow_traffic_tracked.mp4
└── smartflow_traffic_tracked_h264.mp4
```

### Generated Output for example1.mp4

```text
output/
├── smartflow_example1_tracked.mp4
└── smartflow_example1_tracked_h264.mp4
```

The H.264 version is used for browser and Streamlit playback.

---

## 📊 Reports

### 1. Traffic Data

```text
reports/traffic_data.csv
```

Contains frame-level traffic information such as:

- Timestamp
- Frame number
- Objects
- Object types
- Density
- Direction
- Flow rate

### 2. Example Video Data

```text
reports/example1_traffic_data.csv
```

Contains the analysis data generated for `example1.mp4`.

### 3. Count Validation

```text
reports/count_report.csv
```

Contains manual-versus-system count comparison and accuracy.

### 4. Technical Report

```text
SMARTFLOW_Two_Video_Technical_Report.pdf
```

Contains the project methodology, detector/tracker selection, test results, validation, limitations, and conclusion.

---

## 🧪 Experimental Results

The system was tested on two videos.

| Video | Resolution | FPS | Frames | Total Counted | LEFT | RIGHT |
|---|---:|---:|---:|---:|---:|---:|
| `traffic.mp4` | 1920×1080 | 25 | 525 | **9** | 4 | 5 |
| `example1.mp4` | 3840×2160 | 30 | 323 | **6** | 6 | 0 |

### traffic.mp4

| Object Type | Count |
|---|---:|
| Car | 6 |
| Truck | 2 |
| Person | 1 |
| **Total** | **9** |

```text
Total Objects Counted : 9
LEFT Crossings        : 4
RIGHT Crossings       : 5
Average Flow          : 25.71 objects/min
```

### example1.mp4

| Object Type | Count |
|---|---:|
| Car | 2 |
| Person | 2 |
| Bus | 1 |
| Motorcycle | 1 |
| **Total** | **6** |

```text
Total Objects Counted : 6
LEFT Crossings        : 6
RIGHT Crossings       : 0
Average Flow          : 33.44 objects/min
```

---

## ✅ Manual Count Validation

Manual validation was completed for `example1.mp4` using the same counting line and crossing rules as the automated system.

| Metric | Manual | System | Difference |
|---|---:|---:|---:|
| LEFT | 6 | 6 | 0 |
| RIGHT | 0 | 0 | 0 |
| **Total** | **6** | **6** | **0** |
| **Accuracy** | **100%** | **100%** | **0% difference** |

Validation file:

```text
reports/count_report.csv
```

> The `traffic.mp4` result shown above is the automated pipeline test result. A manual accuracy value for `traffic.mp4` is not reported until separate manual validation is completed.

---

## 🖥️ Dashboard

The Streamlit dashboard provides a simple interface for monitoring and analyzing the selected video.

### Dashboard Metrics

| Metric | Description |
|---|---|
| Objects in Frame | Objects currently visible |
| Total Objects Counted | Unique objects that crossed the line |
| LEFT Crossings | Objects moving right-to-left |
| RIGHT Crossings | Objects moving left-to-right |
| Density | Current traffic density |
| Flow Rate | Estimated objects per minute |

---

## ⚠️ Known Limitations

- Detection accuracy depends on video quality, lighting, camera angle, and object size.
- Heavy occlusion can cause missed detections.
- Small or distant objects may not be detected reliably.
- Severe occlusion can cause temporary tracking loss or ID changes.
- The counting-line position may need adjustment for different camera views.
- The general COCO model does not provide a dedicated auto-rickshaw class.
- High-resolution videos require more processing time.
- Manual validation depends on applying the same counting rule consistently.

---

## 🚀 Future Improvements

- Train a custom traffic-specific YOLO model.
- Add a dedicated auto-rickshaw class.
- Improve tracking under heavy occlusion.
- Add configurable counting lines.
- Add region-of-interest selection.
- Add real-time CCTV/camera support.
- Add more detailed traffic analytics.
- Compare multiple tracking algorithms.
- Deploy the Streamlit dashboard as a web application.

---

## 📦 Assignment Deliverables

| Deliverable | Status |
|---|---|
| Object detection pipeline | ✅ Completed |
| Multi-object tracking | ✅ Completed |
| Unique object IDs | ✅ Completed |
| Line-crossing counting | ✅ Completed |
| Direction detection | ✅ Completed |
| Testing on multiple videos | ✅ Completed |
| CSV traffic reports | ✅ Completed |
| Manual count validation | ✅ Completed for `example1.mp4` |
| Count report | ✅ Completed |
| Streamlit dashboard | ✅ Completed |
| Tracked demo output | ✅ Included |
| Technical report | ✅ Included |
| README documentation | ✅ Completed |

---

## 🚀 Quick Start

```powershell
# Clone repository
git clone https://github.com/Devika9511/Multi-Object-Tracking_and_Counting.git

# Enter project
cd Multi-Object-Tracking_and_Counting

# Create virtual environment
python -m venv venv

# Activate environment
.env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Place an MP4 video in input/

# Run analysis
python src\main.py input	raffic.mp4

# Launch dashboard
streamlit run app.py
```

---

## 🔗 GitHub Repository

**Repository:**  
https://github.com/Devika9511/Multi-Object-Tracking_and_Counting

---

## 👩‍💻 Project

**SMARTFLOW – Smart Traffic Detection, Tracking and Counting System**

**Built with:**  
`YOLO11` • `ByteTrack` • `OpenCV` • `Python` • `Streamlit`
