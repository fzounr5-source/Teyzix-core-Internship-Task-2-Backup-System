import os
import json
from datetime import datetime


# File paths
RECORDS_PATH = "backups/backup_records.json"
RECOVERY_LOG_PATH = "logs/recovery_log.txt"
REPORT_OUTPUT_PATH = "logs/backup_report.txt"


# Load all backup records from JSON file
def load_records():
    if not os.path.exists(RECORDS_PATH):
        return []
    with open(RECORDS_PATH, "r") as f:
        return json.load(f)


# Generate full backup report and save to file
def generate_backup_report():
    records = load_records()

    total = len(records)
    success = sum(1 for r in records if r["status"] == "SUCCESS")
    failed = total - success
    total_size = sum(r["size_kb"] for r in records)

    report = []
    report.append("=" * 55)
    report.append("       AUTOMATED BACKUP SYSTEM - FULL REPORT")
    report.append(f"       Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 55)
    report.append("")
    report.append("  BACKUP STATISTICS")
    report.append(f"  Total Backups   : {total}")
    report.append(f"  Successful      : {success}")
    report.append(f"  Failed          : {failed}")
    report.append(f"  Total Size Used : {total_size} KB")
    report.append("")
    report.append("=" * 55)
    report.append("  BACKUP HISTORY")
    report.append("=" * 55)

    if not records:
        report.append("  No backups found.")
    else:
        for r in records:
            report.append(f"\n  Backup ID  : {r['backup_id']}")
            report.append(f"  Date       : {r['timestamp']}")
            report.append(f"  Source     : {r['source']}")
            report.append(f"  Saved At   : {r['destination']}")
            report.append(f"  Size       : {r['size_kb']} KB")
            report.append(f"  Status     : {r['status']}")
            report.append("  " + "-" * 50)

    report.append("")
    report.append("=" * 55)
    report.append("  RECOVERY ACTIVITY LOG")
    report.append("=" * 55)

    if os.path.exists(RECOVERY_LOG_PATH):
        with open(RECOVERY_LOG_PATH, "r") as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                report.append(f"  {line.strip()}")
        else:
            report.append("  No recovery activity yet.")
    else:
        report.append("  No recovery log found.")

    report.append("")
    report.append("=" * 55)
    report.append("         END OF REPORT")
    report.append("=" * 55)

    # Print report to terminal
    print("\n")
    for line in report:
        print(line)

    # Save report to file
    with open(REPORT_OUTPUT_PATH, "w") as f:
        f.write("\n".join(report))

    print(f"\n[INFO] Report saved to: {REPORT_OUTPUT_PATH}\n")


# Display storage used by each backup
def show_storage_usage():
    records = load_records()

    if not records:
        print("\n[INFO] No backup records found.\n")
        return

    print("\n" + "=" * 45)
    print("       STORAGE USAGE PER BACKUP")
    print("=" * 45)

    for r in records:
        print(f"  {r['backup_id']} | {r['timestamp']} | {r['size_kb']} KB")

    total = sum(r["size_kb"] for r in records)
    print("=" * 45)
    print(f"  Total Storage Used: {total} KB")
    print("=" * 45 + "\n")