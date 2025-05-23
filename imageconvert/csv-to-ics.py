#!/usr/bin/env python3
import csv
import datetime
import os
import sys

def generate_ics(csv_file, ics_file):
    # The lines we’ll write to the final .ics:
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Chillaid//Bulk ICS Generator//EN",
    ]

    # Read the CSV with error handling
    try:
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_number, row in enumerate(reader, start=1):
                try:
                    event_name = row["Event"]
                    date_str = row["Date"]      # e.g. "2025-03-03"
                    start_str = row["StartTime"]  # e.g. "10:00"
                    end_str = row["EndTime"]      # e.g. "16:00"

                    # Parse date/time to build ICS-friendly strings (UTC not required here,
                    # but we do need the "YYYYMMDDTHHMMSS" format).
                    dt_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

                    # Combine date + start time
                    start_parts = start_str.split(":")
                    dt_start = dt_date.replace(hour=int(start_parts[0]), minute=int(start_parts[1]))
                    dtstart_str = dt_start.strftime("%Y%m%dT%H%M%S")

                    # Combine date + end time
                    end_parts = end_str.split(":")
                    dt_end = dt_date.replace(hour=int(end_parts[0]), minute=int(end_parts[1]))
                    dtend_str = dt_end.strftime("%Y%m%dT%H%M%S")

                    # For UID + DTSTAMP, we can use the current time or the shift start time
                    uid = dt_start.strftime("%Y%m%dT%H%M%S") + "-" + event_name.replace(" ", "_")
                    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

                    # Build each event’s text
                    vevent = [
                        "BEGIN:VEVENT",
                        f"UID:{uid}",
                        f"DTSTAMP:{dtstamp}",
                        f"DTSTART:{dtstart_str}",
                        f"DTEND:{dtend_str}",
                        f"SUMMARY:{event_name}",
                        "END:VEVENT",
                    ]
                    ics_lines.extend(vevent)
                except KeyError as e:
                    print(f"Skipping row {row_number} due to missing column: {e}")
                except ValueError as e:
                    print(f"Skipping row {row_number} due to invalid data: {e}")
    except FileNotFoundError:
        print(f"ERROR: CSV file not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: An error occurred while reading the CSV file: {e}")
        sys.exit(1)

    ics_lines.append("END:VCALENDAR")

    # Write everything to the .ics file with error handling
    try:
        with open(ics_file, mode="w", encoding="utf-8") as f:
            for line in ics_lines:
                f.write(line + "\n")
    except Exception as e:
        print(f"ERROR: An error occurred while writing the ICS file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: csv-to-ics.py <icon_file.icns>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    ics_file = "pati_praca.ics"

    # Generate ICS from CSV
    generate_ics(csv_file, ics_file)

    # Print a confirmation
    if os.path.exists(ics_file):
        print(f"Successfully created {ics_file}")
    else:
        print(f"ERROR: Could not create {ics_file}.")

if __name__ == "__main__":
    main()