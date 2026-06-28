import json
import os


# Path to backup records file
RECORDS_PATH = "backups/backup_records.json"


# Load all backup records from JSON file
def load_records():
    if not os.path.exists(RECORDS_PATH):
        return []
    with open(RECORDS_PATH, "r") as f:
        return json.load(f)


# Display all past backups in a table format
def view_backup_history():
    records = load_records()

    if not records:
        print("\n[INFO] No backups found yet.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<10} {'Date & Time':<22} {'Size(KB)':<10} {'Status':<10} {'Source'}")
    print("=" * 65)

    for record in records:
        print(
            f"{record['backup_id']:<10} "
            f"{record['timestamp']:<22} "
            f"{record['size_kb']:<10} "
            f"{record['status']:<10} "
            f"{record['source']}"
        )

    print("=" * 65)
    print(f"Total Backups: {len(records)}\n")


# Display quick backup statistics
def get_backup_summary():
    records = load_records()

    total = len(records)
    success = sum(1 for r in records if r["status"] == "SUCCESS")
    failed = total - success
    total_size = sum(r["size_kb"] for r in records)

    print("\n" + "=" * 40)
    print("       BACKUP SUMMARY REPORT")
    print("=" * 40)
    print(f"  Total Backups   : {total}")
    print(f"  Successful      : {success}")
    print(f"  Failed          : {failed}")
    print(f"  Total Size Used : {total_size} KB")
    print("=" * 40 + "\n")


# Display only the most recent backup
def get_latest_backup():
    records = load_records()

    if not records:
        print("\n[INFO] No backups available.")
        return

    latest = records[-1]
    print("\n--- Latest Backup ---")
    print(f"  ID        : {latest['backup_id']}")
    print(f"  Timestamp : {latest['timestamp']}")
    print(f"  Source    : {latest['source']}")
    print(f"  Size      : {latest['size_kb']} KB")
    print(f"  Status    : {latest['status']}\n")