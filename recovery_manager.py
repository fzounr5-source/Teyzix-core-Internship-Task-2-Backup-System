import os
import json
import zipfile
from datetime import datetime


# File paths
RECORDS_PATH = "backups/backup_records.json"
RECOVERY_LOG_PATH = "logs/recovery_log.txt"


# Load all backup records from JSON file
def load_records():
    if not os.path.exists(RECORDS_PATH):
        return []
    with open(RECORDS_PATH, "r") as f:
        return json.load(f)


# Write recovery activity to log file
def log_recovery(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RECOVERY_LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# Show all available backups user can restore from
def list_available_backups():
    records = load_records()

    if not records:
        print("\n[INFO] No backups available to restore.")
        return []

    print("\n" + "=" * 65)
    print(f"{'No.':<5} {'ID':<10} {'Date & Time':<22} {'Size(KB)':<10} {'Source'}")
    print("=" * 65)

    for index, record in enumerate(records, start=1):
        print(
            f"{index:<5} "
            f"{record['backup_id']:<10} "
            f"{record['timestamp']:<22} "
            f"{record['size_kb']:<10} "
            f"{record['source']}"
        )

    print("=" * 65 + "\n")
    return records


# Check if backup zip file is valid before restoring
def verify_backup(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            result = zipf.testzip()
            if result is None:
                return True
            else:
                print(f"[WARNING] Corrupted file found: {result}")
                return False
    except Exception as e:
        print(f"[ERROR] Backup verification failed: {e}")
        return False


# Restore a selected backup to destination folder
def restore_backup(restore_destination):
    records = list_available_backups()

    if not records:
        return

    # Ask user which backup to restore
    try:
        choice = int(input("Enter backup number to restore: ")) - 1
        if choice < 0 or choice >= len(records):
            print("[ERROR] Invalid choice.")
            return
    except ValueError:
        print("[ERROR] Please enter a valid number.")
        return

    selected = records[choice]
    zip_path = selected["destination"]

    # Check if zip file exists
    if not os.path.exists(zip_path):
        print(f"[ERROR] Backup file not found: {zip_path}")
        log_recovery(f"FAILED - Backup file missing: {zip_path}")
        return

    # Verify backup before restoring
    print("\n[INFO] Verifying backup integrity...")
    if not verify_backup(zip_path):
        print("[ERROR] Backup is corrupted. Restore cancelled.")
        log_recovery(f"FAILED - Corrupted backup: {zip_path}")
        return

    # Create destination folder if not exists
    os.makedirs(restore_destination, exist_ok=True)

    # Extract zip to destination
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(restore_destination)

        print(f"\n[SUCCESS] Files restored to: {restore_destination}")
        print(f"          Backup ID : {selected['backup_id']}")
        print(f"          Source was: {selected['source']}\n")

        log_recovery(
            f"SUCCESS - Backup ID: {selected['backup_id']} "
            f"restored to {restore_destination}"
        )

    except Exception as e:
        print(f"[ERROR] Restore failed: {e}")
        log_recovery(f"FAILED - Error during restore: {e}")