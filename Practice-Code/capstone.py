"""
Capstone: Campus Energy-Use Dashboard (Simple Version)

Tasks covered:
1) Data ingestion & validation
2) Aggregation logic (daily, weekly, building summary)
3) OOP modelling (Building, MeterReading, simple manager)
4) Visualization with Matplotlib (3 charts in one figure)
5) Saving cleaned data, summary CSV, and text summary
"""

import os
import glob
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


# =========================
#   TASK 3: SIMPLE CLASSES
# =========================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []  # list of MeterReading objects

    def add_reading(self, reading):
        self.readings.append(reading)

    def total_consumption(self):
        return sum(r.kwh for r in self.readings)

    def peak_reading(self):
        if not self.readings:
            return None
        return max(self.readings, key=lambda r: r.kwh)

    def report(self):
        peak = self.peak_reading()
        return {
            "building": self.name,
            "total_kwh": self.total_consumption(),
            "peak_kwh": peak.kwh if peak else 0,
            "peak_time": peak.timestamp if peak else None,
            "readings_count": len(self.readings),
        }


class BuildingManager:
    def __init__(self):
        self.buildings = {}  # name -> Building

    def get_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            bname = row["building"]
            ts = row["timestamp"]
            kwh = row["kwh"]
            b = self.get_building(bname)
            b.add_reading(MeterReading(ts, kwh))

    def all_reports(self):
        return [b.report() for b in self.buildings.values()]


# ================================
#   TASK 1: DATA INGESTION
# ================================

def load_all_csv(data_folder="data"):
    """
    Reads all CSV files from the data/ folder and returns one combined DataFrame.
    Adds 'building' column from filename if missing.
    Also returns a list of error messages.
    """
    all_files = glob.glob(os.path.join(data_folder, "*.csv"))
    dfs = []
    errors = []

    if not all_files:
        print("No CSV files found in 'data/' folder.")
        return pd.DataFrame(), ["No CSV files found."]

    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines="skip")  # skip corrupt lines

            # Check required columns
            if "kwh" not in df.columns or "timestamp" not in df.columns:
                errors.append(f"{os.path.basename(file)} missing 'kwh' or 'timestamp' column. Skipped.")
                continue

            # Convert timestamp
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp"])

            # Add building column if not present
            if "building" not in df.columns:
                # infer from filename: e.g. "library_jan.csv" -> "library_jan"
                building_name = os.path.splitext(os.path.basename(file))[0]
                df["building"] = building_name

            # Add month column if not present
            if "month" not in df.columns:
                df["month"] = df["timestamp"].dt.to_period("M").astype(str)

            dfs.append(df)

        except Exception as e:
            errors.append(f"Error reading {os.path.basename(file)}: {e}")

    if not dfs:
        return pd.DataFrame(), errors

    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.sort_values("timestamp")

    return combined, errors


# ===========================================
#   TASK 2: AGGREGATIONS (DAILY / WEEKLY)
# ===========================================

def calculate_daily_totals(df):
    """
    Returns DataFrame with columns: timestamp (date), building, daily_kwh
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    # group by building then resample per day
    daily = df.groupby("building").resample("D")["kwh"].sum().reset_index()
    daily.rename(columns={"kwh": "daily_kwh"}, inplace=True)
    return daily


def calculate_weekly_totals(df):
    """
    Returns DataFrame with columns: timestamp (week), building, weekly_kwh
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    weekly = df.groupby("building").resample("W")["kwh"].sum().reset_index()
    weekly.rename(columns={"kwh": "weekly_kwh"}, inplace=True)
    return weekly


def building_summary(df):
    """
    Summary per building: total, mean, min, max, count.
    """
    grouped = df.groupby("building")["kwh"]
    summary_df = grouped.agg(
        total_kwh="sum",
        mean_kwh="mean",
        min_kwh="min",
        max_kwh="max",
        readings_count="count",
    ).reset_index()
    return summary_df


def campus_summary_numbers(df):
    """
    Returns:
    - total campus kwh
    - highest consuming building
    - peak load timestamp (when kwh is max)
    """
    total_campus = df["kwh"].sum()

    building_totals = df.groupby("building")["kwh"].sum()
    highest_building = building_totals.idxmax()

    peak_row = df.loc[df["kwh"].idxmax()]
    peak_time = peak_row["timestamp"]

    return total_campus, highest_building, peak_time


# ===========================================
#   TASK 4: VISUALIZATION (DASHBOARD)
# ===========================================

def create_dashboard(daily_df, weekly_df, output_path="output/dashboard.png"):
    """
    Creates a figure with 3 subplots:
    1) Line chart - daily consumption over time (per building)
    2) Bar chart - average weekly consumption per building
    3) Scatter - peak daily consumption per building
    """
    # Make sure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Line Chart - Daily consumption
    ax1 = axes[0]
    for building, group in daily_df.groupby("building"):
        ax1.plot(group["timestamp"], group["daily_kwh"], label=building)
    ax1.set_title("Daily Consumption Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Daily kWh")
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend(fontsize=8)

    # 2. Bar Chart - Average weekly usage per building
    ax2 = axes[1]
    weekly_mean = weekly_df.groupby("building")["weekly_kwh"].mean().reset_index()
    ax2.bar(weekly_mean["building"], weekly_mean["weekly_kwh"])
    ax2.set_title("Average Weekly Usage by Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Avg Weekly kWh")
    ax2.tick_params(axis="x", rotation=45)

    # 3. Scatter Plot - Peak daily usage per building
    ax3 = axes[2]
    peak_daily = daily_df.groupby("building")["daily_kwh"].max().reset_index()
    ax3.scatter(peak_daily["building"], peak_daily["daily_kwh"])
    ax3.set_title("Peak Daily Consumption by Building")
    ax3.set_xlabel("Building")
    ax3.set_ylabel("Peak Daily kWh")
    ax3.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


# ===========================================
#   TASK 5: SAVE CSVs + TEXT SUMMARY
# ===========================================

def save_outputs(df_clean, summary_df, total_campus, highest_building, peak_time,
                 daily_df, weekly_df, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)

    # 1. Cleaned full data
    cleaned_path = os.path.join(output_folder, "cleaned_energy_data.csv")
    df_clean.to_csv(cleaned_path, index=False)

    # 2. Building summary
    summary_path = os.path.join(output_folder, "building_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    # 3. Short text summary
    # Simple trend comments:
    daily_totals_by_date = daily_df.groupby("timestamp")["daily_kwh"].sum().reset_index()
    weekly_totals_by_week = weekly_df.groupby("timestamp")["weekly_kwh"].sum().reset_index()

    if len(daily_totals_by_date) >= 2:
        if daily_totals_by_date.iloc[-1]["daily_kwh"] > daily_totals_by_date.iloc[0]["daily_kwh"]:
            daily_comment = "Daily consumption is generally increasing."
        else:
            daily_comment = "Daily consumption is generally stable or decreasing."
    else:
        daily_comment = "Not enough data to analyse daily trend."

    if len(weekly_totals_by_week) >= 2:
        if weekly_totals_by_week.iloc[-1]["weekly_kwh"] > weekly_totals_by_week.iloc[0]["weekly_kwh"]:
            weekly_comment = "Weekly consumption is generally increasing."
        else:
            weekly_comment = "Weekly consumption is generally stable or decreasing."
    else:
        weekly_comment = "Not enough data to analyse weekly trend."

    summary_txt_path = os.path.join(output_folder, "summary.txt")
    with open(summary_txt_path, "w", encoding="utf-8") as f:
        f.write("Campus Energy Consumption Summary\n")
        f.write("--------------------------------\n\n")
        f.write(f"Total campus consumption: {total_campus:.2f} kWh\n")
        f.write(f"Highest consuming building: {highest_building}\n")
        f.write(f"Peak load time (max single reading): {peak_time}\n\n")
        f.write("Daily Trend: " + daily_comment + "\n")
        f.write("Weekly Trend: " + weekly_comment + "\n")

    print("Saved:")
    print(" -", cleaned_path)
    print(" -", summary_path)
    print(" -", summary_txt_path)


# ===========================================
#   MAIN FUNCTION (RUN EVERYTHING)
# ===========================================

def main():
    print("=== Campus Energy Dashboard (Simple Version) ===")

    # Task 1: Load data
    df, errors = load_all_csv("data")
    if errors:
        print("Errors during loading:")
        for e in errors:
            print("  -", e)

    if df.empty:
        print("No valid data loaded. Exiting.")
        return

    # Clean basic: drop rows with missing important values
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp", "kwh", "building"])

    # Task 2: Aggregations
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_totals(df)
    summary_df = building_summary(df)
    total_campus, highest_building, peak_time = campus_summary_numbers(df)

    # Task 3: OOP demo (not required for output, but for understanding)
    manager = BuildingManager()
    manager.load_from_dataframe(df)
    reports = manager.all_reports()
    print("\nSample building reports (OOP):")
    for r in reports[:3]:
        print(" ", r)

    # Task 4: Visualization
    create_dashboard(daily, weekly, output_path="output/dashboard.png")
    print("\nDashboard saved to output/dashboard.png")

    # Task 5: Save CSVs + text summary
    save_outputs(df, summary_df, total_campus, highest_building, peak_time, daily, weekly)

    print("\nAll tasks completed successfully.")


if __name__ == "__main__":
    main()
