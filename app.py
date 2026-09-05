import os
import pandas as pd
import streamlit as st


# ============================================================
# SMARTFLOW - STREAMLIT DASHBOARD
# ============================================================

st.set_page_config(
    page_title="SMARTFLOW",
    page_icon="🚦",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

TRAFFIC_CSV = "reports/traffic_data.csv"
COUNT_REPORT = "reports/count_report.csv"

VIDEO_OPTIONS = [
    "output/smartflow_tracked_h264.mp4",
    "output/smartflow_tracked.mp4",
    "input/traffic.mp4"
]


# ============================================================
# FIND VIDEO
# ============================================================

VIDEO_PATH = None

for path in VIDEO_OPTIONS:

    if os.path.exists(path):
        VIDEO_PATH = path
        break


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.30);
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .status-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.30);
        min-height: 120px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚦 SMARTFLOW</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Multi-Object Tracking & Counting From Video</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# LOAD TRAFFIC DATA
# ============================================================

if not os.path.exists(TRAFFIC_CSV):

    st.error(
        "Traffic data was not found. "
        "Please run `python src/main.py` first."
    )

    st.stop()


try:

    df = pd.read_csv(
        TRAFFIC_CSV
    )

except Exception as exc:

    st.error(
        f"Unable to read traffic data: {exc}"
    )

    st.stop()


if df.empty:

    st.warning(
        "No traffic data is available."
    )

    st.stop()


# ============================================================
# CLEAN NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "frame",
    "vehicles",
    "cars",
    "motorcycles",
    "buses",
    "trucks",
    "right_direction",
    "left_direction",
    "flow_rate"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


if "frame" in df.columns:

    df = df.dropna(
        subset=["frame"]
    )


df = df.reset_index(
    drop=True
)


# ============================================================
# LATEST DATA
# ============================================================

latest = df.iloc[-1]


vehicles_in_frame = int(
    latest.get(
        "vehicles",
        0
    )
)


current_cars = int(
    latest.get(
        "cars",
        0
    )
)


current_motorcycles = int(
    latest.get(
        "motorcycles",
        0
    )
)


current_buses = int(
    latest.get(
        "buses",
        0
    )
)


current_trucks = int(
    latest.get(
        "trucks",
        0
    )
)


left_count = int(
    latest.get(
        "left_direction",
        0
    )
)


right_count = int(
    latest.get(
        "right_direction",
        0
    )
)


total_counted = (
    left_count +
    right_count
)


density = str(
    latest.get(
        "density",
        "UNKNOWN"
    )
)


flow_rate = float(
    latest.get(
        "flow_rate",
        0
    )
)


# ============================================================
# TRAFFIC OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Traffic Overview</div>',
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Vehicles in Frame",
        vehicles_in_frame
    )


with c2:

    st.metric(
        "Total Vehicles Counted",
        total_counted
    )


with c3:

    st.metric(
        "Left Crossings",
        left_count
    )


with c4:

    st.metric(
        "Right Crossings",
        right_count
    )


# ============================================================
# CURRENT VEHICLE COMPOSITION
# ============================================================

st.markdown(
    '<div class="section-title">🚘 Current Vehicle Composition</div>',
    unsafe_allow_html=True
)


st.caption(
    "Vehicle-type values represent vehicles detected "
    "in the latest logged frame, not cumulative crossings."
)


v1, v2, v3, v4 = st.columns(4)


with v1:

    st.metric(
        "Cars",
        current_cars
    )


with v2:

    st.metric(
        "Motorcycles",
        current_motorcycles
    )


with v3:

    st.metric(
        "Buses",
        current_buses
    )


with v4:

    st.metric(
        "Trucks",
        current_trucks
    )


# ============================================================
# CURRENT TRAFFIC STATUS
# ============================================================

st.markdown(
    '<div class="section-title">🚦 Current Traffic Status</div>',
    unsafe_allow_html=True
)


s1, s2 = st.columns(2)


with s1:

    st.markdown(
        '<div class="status-box">',
        unsafe_allow_html=True
    )

    st.caption(
        "Traffic Density"
    )

    st.subheader(
        density
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with s2:

    st.markdown(
        '<div class="status-box">',
        unsafe_allow_html=True
    )

    st.caption(
        "Flow Estimate"
    )

    st.subheader(
        f"{flow_rate:.2f} vehicles/min"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TRACKED VIDEO
# ============================================================

st.markdown(
    '<div class="section-title">🎥 Tracked Video</div>',
    unsafe_allow_html=True
)


if VIDEO_PATH:

    try:

        with open(
            VIDEO_PATH,
            "rb"
        ) as video_file:

            video_bytes = video_file.read()


        st.video(
            video_bytes,
            format="video/mp4"
        )


        st.caption(
            "Annotated video generated using YOLO11 detection, "
            "ByteTrack tracking and line-crossing counting."
        )


    except Exception as exc:

        st.error(
            f"Unable to load tracked video: {exc}"
        )

else:

    st.warning(
        "No tracked video found."
    )


# ============================================================
# TRAFFIC ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Traffic Analytics</div>',
    unsafe_allow_html=True
)


chart1, chart2 = st.columns(2)


with chart1:

    st.subheader(
        "Vehicles Detected Over Frames"
    )

    if (
        "frame" in df.columns
        and "vehicles" in df.columns
    ):

        vehicle_chart = (
            df[
                [
                    "frame",
                    "vehicles"
                ]
            ]
            .set_index(
                "frame"
            )
        )

        st.line_chart(
            vehicle_chart
        )


with chart2:

    st.subheader(
        "Flow Rate Over Frames"
    )

    if (
        "frame" in df.columns
        and "flow_rate" in df.columns
    ):

        flow_chart = (
            df[
                [
                    "frame",
                    "flow_rate"
                ]
            ]
            .set_index(
                "frame"
            )
        )

        st.line_chart(
            flow_chart
        )


# ============================================================
# VEHICLE TYPE DISTRIBUTION
# ============================================================

st.subheader(
    "Vehicle Type Distribution - Latest Logged Frame"
)


vehicle_distribution = pd.DataFrame(
    {
        "Vehicle Type": [
            "Cars",
            "Motorcycles",
            "Buses",
            "Trucks"
        ],

        "Count": [
            current_cars,
            current_motorcycles,
            current_buses,
            current_trucks
        ]
    }
)


st.bar_chart(
    vehicle_distribution.set_index(
        "Vehicle Type"
    )
)


# ============================================================
# DIRECTION ANALYSIS
# ============================================================

st.subheader(
    "Cumulative Direction Crossings"
)


direction_distribution = pd.DataFrame(
    {
        "Direction": [
            "Left",
            "Right"
        ],

        "Count": [
            left_count,
            right_count
        ]
    }
)


st.bar_chart(
    direction_distribution.set_index(
        "Direction"
    )
)


# ============================================================
# VERIFIED MANUAL COUNT
# ============================================================

st.markdown(
    '<div class="section-title">✅ Count Validation</div>',
    unsafe_allow_html=True
)


if os.path.exists(COUNT_REPORT):

    try:

        validation = pd.read_csv(
            COUNT_REPORT
        )


        if not validation.empty:

            result = validation.iloc[-1]


            manual_left = int(
                result["manual_left"]
            )

            manual_right = int(
                result["manual_right"]
            )

            manual_total = int(
                result["manual_total"]
            )

            system_total = int(
                result["system_total"]
            )

            difference = int(
                result["difference"]
            )

            accuracy = float(
                result["accuracy_percent"]
            )


            st.success(
                "Manual count verification completed."
            )


            m1, m2, m3, m4 = st.columns(4)


            with m1:

                st.metric(
                    "Manual Total",
                    manual_total
                )


            with m2:

                st.metric(
                    "System Total",
                    system_total
                )


            with m3:

                st.metric(
                    "Difference",
                    difference
                )


            with m4:

                st.metric(
                    "Count Accuracy",
                    f"{accuracy:.2f}%"
                )


            st.write(
                f"Manual Left: **{manual_left}**  |  "
                f"Manual Right: **{manual_right}**"
            )


    except Exception as exc:

        st.warning(
            f"Could not read count report: {exc}"
        )

else:

    st.info(
        "Manual count validation report has not "
        "been created yet."
    )


# ============================================================
# COUNTING METHOD
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Counting Method</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-box">

    <b>1. YOLO11 Detection</b><br>
    Detects vehicles in each video frame.

    <br><br>

    <b>2. ByteTrack Tracking</b><br>
    Associates detections across frames and maintains
    persistent tracking IDs.

    <br><br>

    <b>3. Position Tracking</b><br>
    SMARTFLOW stores the previous position of every
    tracked vehicle.

    <br><br>

    <b>4. Line Crossing</b><br>
    A vehicle is counted when its tracked center crosses
    the configured vertical counting line.

    <br><br>

    <b>5. Double-Count Prevention</b><br>
    Once a tracking ID is counted, it is stored in a
    counted-ID set so the same vehicle is not counted again.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TRAFFIC DATA
# ============================================================

with st.expander(
    "📋 View Traffic Data"
):

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# ============================================================
# PIPELINE
# ============================================================

st.divider()


st.markdown(
    '<div class="section-title">🧠 SMARTFLOW Pipeline</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    **🎥 Video Input**

    ↓

    **🔎 YOLO11 Object Detection**

    ↓

    **🎯 ByteTrack Multi-Object Tracking**

    ↓

    **🆔 Persistent Object IDs**

    ↓

    **📏 Line-Crossing Detection**

    ↓

    **🔢 Unique Vehicle Count**

    ↓

    **📊 CSV Data Logging**

    ↓

    **🖥️ Streamlit Dashboard**
    """
)


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown(
    '<div class="section-title">🛠️ Technology Stack</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    - **Python** — application development
    - **YOLO11 / Ultralytics** — vehicle detection
    - **ByteTrack** — multi-object tracking
    - **OpenCV** — video processing
    - **Pandas** — traffic data handling
    - **Streamlit** — dashboard and demonstration
    """
)


# ============================================================
# PROJECT OBJECTIVE
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Project Objective</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    SMARTFLOW detects and tracks vehicles in traffic video,
    assigns persistent IDs and counts each tracked vehicle
    once when it crosses a predefined counting line.

    The dashboard provides a visual demonstration of the
    tracked output, traffic composition, directional
    crossings, density, flow information and manual
    validation accuracy.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SMARTFLOW | Multi-Object Tracking & Counting From Video"
)