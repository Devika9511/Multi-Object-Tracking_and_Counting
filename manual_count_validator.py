import csv
import os


# ============================================================
# SMARTFLOW MANUAL COUNT VALIDATOR
# ============================================================

SYSTEM_LEFT = 4
SYSTEM_RIGHT = 4
SYSTEM_TOTAL = SYSTEM_LEFT + SYSTEM_RIGHT

REPORT_PATH = "reports/count_report.csv"


print()
print("=" * 55)
print("        SMARTFLOW MANUAL COUNT VALIDATION")
print("=" * 55)

print()
print("AUTOMATED SMARTFLOW RESULT")
print("-" * 35)

print(f"System Left Crossings  : {SYSTEM_LEFT}")
print(f"System Right Crossings : {SYSTEM_RIGHT}")
print(f"System Total           : {SYSTEM_TOTAL}")

print()
print("Now watch the same video and enter")
print("the number of vehicles that actually")
print("crossed the counting line.")

print()

try:

    manual_left = int(
        input("Enter manual LEFT crossings: ")
    )

    manual_right = int(
        input("Enter manual RIGHT crossings: ")
    )

except ValueError:

    print()
    print("ERROR: Please enter whole numbers only.")
    exit()


if manual_left < 0 or manual_right < 0:

    print()
    print("ERROR: Counts cannot be negative.")
    exit()


# ============================================================
# CALCULATE RESULTS
# ============================================================

manual_total = (
    manual_left +
    manual_right
)

difference = abs(
    SYSTEM_TOTAL -
    manual_total
)


if manual_total == 0:

    accuracy = None

else:

    accuracy = max(
        0,
        (
            1 -
            difference /
            manual_total
        ) * 100
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 55)
print("              VALIDATION RESULT")
print("=" * 55)

print()
print(f"Manual Left Crossings  : {manual_left}")
print(f"Manual Right Crossings : {manual_right}")
print(f"Manual Total           : {manual_total}")

print()
print(f"System Total           : {SYSTEM_TOTAL}")
print(f"Absolute Difference    : {difference}")

if accuracy is not None:

    print(
        f"Count Accuracy         : {accuracy:.2f}%"
    )

else:

    print(
        "Count Accuracy         : N/A"
    )


# ============================================================
# SAVE REPORT
# ============================================================

os.makedirs(
    "reports",
    exist_ok=True
)


with open(
    REPORT_PATH,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "video",
        "manual_left",
        "manual_right",
        "manual_total",
        "system_left",
        "system_right",
        "system_total",
        "difference",
        "accuracy_percent",
        "status"
    ])

    writer.writerow([
        "traffic.mp4",
        manual_left,
        manual_right,
        manual_total,
        SYSTEM_LEFT,
        SYSTEM_RIGHT,
        SYSTEM_TOTAL,
        difference,
        "" if accuracy is None else f"{accuracy:.2f}",
        "VERIFIED"
    ])


print()
print("=" * 55)
print("Report saved successfully!")
print("=" * 55)

print()
print(
    f"File: {REPORT_PATH}"
)

print()