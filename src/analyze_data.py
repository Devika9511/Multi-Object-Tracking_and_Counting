import pandas as pd
import os

# ============================================================
# SMARTFLOW - DATASET ANALYSIS
# ============================================================

CSV_FILE = "reports/traffic_data.csv"

print("=" * 60)
print("          SMARTFLOW DATASET ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# Check file
# ------------------------------------------------------------

if not os.path.exists(CSV_FILE):

    print("❌ traffic_data.csv not found")

    exit()

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------

df = pd.read_csv(CSV_FILE)

print()
print("✅ Dataset loaded successfully")

# ------------------------------------------------------------
# Basic information
# ------------------------------------------------------------

print()
print("-" * 60)
print("DATASET INFORMATION")
print("-" * 60)

print(f"Total rows       : {len(df)}")
print(f"Total columns    : {len(df.columns)}")

print()
print("Columns:")

for column in df.columns:
    print(f"  • {column}")

# ------------------------------------------------------------
# Missing values
# ------------------------------------------------------------

print()
print("-" * 60)
print("MISSING VALUES")
print("-" * 60)

missing = df.isnull().sum()

for column, value in missing.items():

    print(
        f"{column:20} : {value}"
    )

# ------------------------------------------------------------
# Duplicate rows
# ------------------------------------------------------------

print()
print("-" * 60)
print("DUPLICATE ANALYSIS")
print("-" * 60)

duplicate_count = df.duplicated(
    subset=[
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
    ]
).sum()

print(
    f"Duplicate observations : {duplicate_count}"
)

# ------------------------------------------------------------
# Density distribution
# ------------------------------------------------------------

print()
print("-" * 60)
print("TRAFFIC DENSITY")
print("-" * 60)

density_counts = df["density"].value_counts()

for density, count in density_counts.items():

    print(
        f"{density:15} : {count}"
    )

# ------------------------------------------------------------
# Vehicle statistics
# ------------------------------------------------------------

print()
print("-" * 60)
print("VEHICLE STATISTICS")
print("-" * 60)

print(
    f"Average vehicles : "
    f"{df['vehicles'].mean():.2f}"
)

print(
    f"Maximum vehicles : "
    f"{df['vehicles'].max()}"
)

print(
    f"Minimum vehicles : "
    f"{df['vehicles'].min()}"
)

print(
    f"Average cars     : "
    f"{df['cars'].mean():.2f}"
)

print(
    f"Average trucks   : "
    f"{df['trucks'].mean():.2f}"
)

# ------------------------------------------------------------
# Flow statistics
# ------------------------------------------------------------

print()
print("-" * 60)
print("FLOW STATISTICS")
print("-" * 60)

print(
    f"Average flow     : "
    f"{df['flow_rate'].mean():.2f}"
)

print(
    f"Maximum flow     : "
    f"{df['flow_rate'].max():.2f}"
)

print(
    f"Minimum flow     : "
    f"{df['flow_rate'].min():.2f}"
)

# ------------------------------------------------------------
# Direction statistics
# ------------------------------------------------------------

print()
print("-" * 60)
print("DIRECTION STATISTICS")
print("-" * 60)

print(
    f"Average right    : "
    f"{df['right_direction'].mean():.2f}"
)

print(
    f"Average left     : "
    f"{df['left_direction'].mean():.2f}"
)

# ------------------------------------------------------------
# Show first rows
# ------------------------------------------------------------

print()
print("-" * 60)
print("FIRST 10 RECORDS")
print("-" * 60)

print(
    df.head(10).to_string(index=False)
)

# ------------------------------------------------------------
# Show last rows
# ------------------------------------------------------------

print()
print("-" * 60)
print("LAST 10 RECORDS")
print("-" * 60)

print(
    df.tail(10).to_string(index=False)
)

# ------------------------------------------------------------
# Completion
# ------------------------------------------------------------

print()
print("=" * 60)
print("✅ DATASET ANALYSIS COMPLETED")
print("=" * 60)