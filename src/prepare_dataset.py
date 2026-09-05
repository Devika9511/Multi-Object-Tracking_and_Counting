import pandas as pd
import os

# ============================================================
# SMARTFLOW - ML DATASET PREPARATION
# ============================================================

INPUT_FILE = "reports/traffic_data.csv"
OUTPUT_FILE = "reports/ml_dataset.csv"

print("=" * 60)
print("       SMARTFLOW ML DATASET PREPARATION")
print("=" * 60)

# ============================================================
# 1. CHECK INPUT FILE
# ============================================================

if not os.path.exists(INPUT_FILE):

    print("❌ traffic_data.csv not found")

    exit()

# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print()
print(f"✅ Original rows: {len(df)}")

# ============================================================
# 3. REMOVE DUPLICATE OBSERVATIONS
# ============================================================

duplicate_columns = [
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

before = len(df)

df = df.drop_duplicates(
    subset=duplicate_columns
).copy()

after = len(df)

print(
    f"✅ Removed duplicates: {before - after}"
)

print(
    f"✅ Rows after cleaning: {after}"
)

# ============================================================
# 4. SORT DATA
# ============================================================

df = df.sort_values(
    by=["timestamp", "frame"]
).reset_index(drop=True)

# ============================================================
# 5. CREATE NEXT DENSITY
# ============================================================

df["next_density"] = (
    df["density"].shift(-1)
)

# The last row has no future observation
df = df.dropna(
    subset=["next_density"]
).copy()

# ============================================================
# 6. CONVERT DENSITY TO NUMERIC VALUES
# ============================================================

density_mapping = {
    "LOW": 0,
    "MODERATE": 1,
    "HIGH": 2
}

df["current_density_value"] = (
    df["density"].map(density_mapping)
)

df["next_density_value"] = (
    df["next_density"].map(density_mapping)
)

# ============================================================
# 7. SELECT ML FEATURES
# ============================================================

features = [
    "vehicles",
    "cars",
    "motorcycles",
    "buses",
    "trucks",
    "right_direction",
    "left_direction",
    "flow_rate",
    "current_density_value"
]

target = "next_density_value"

ml_df = df[
    features + [
        "next_density",
        target
    ]
].copy()

# ============================================================
# 8. CHECK MISSING VALUES
# ============================================================

missing_values = ml_df.isnull().sum().sum()

print()
print(
    f"Missing values: {missing_values}"
)

if missing_values > 0:

    print(
        "⚠️ Missing values detected"
    )

else:

    print(
        "✅ No missing values"
    )

# ============================================================
# 9. SAVE ML DATASET
# ============================================================

ml_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# 10. DISPLAY DATASET
# ============================================================

print()
print("-" * 60)
print("ML DATASET")
print("-" * 60)

print(
    ml_df.to_string(index=False)
)

# ============================================================
# 11. DATASET SUMMARY
# ============================================================

print()
print("-" * 60)
print("DATASET SUMMARY")
print("-" * 60)

print(
    f"Training rows available : {len(ml_df)}"
)

print(
    f"Features available      : {len(features)}"
)

print()
print("Features:")

for feature in features:

    print(
        f"  • {feature}"
    )

print()
print(
    f"Target: {target}"
)

# ============================================================
# 12. TARGET DISTRIBUTION
# ============================================================

print()
print("-" * 60)
print("NEXT DENSITY DISTRIBUTION")
print("-" * 60)

print(
    ml_df["next_density"].value_counts()
)

# ============================================================
# 13. FINAL MESSAGE
# ============================================================

print()
print("=" * 60)
print("✅ ML DATASET PREPARATION COMPLETED")
print("=" * 60)

print()
print(
    f"📁 Saved to: {OUTPUT_FILE}"
)

print("=" * 60)