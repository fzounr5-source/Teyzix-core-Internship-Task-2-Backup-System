import os
import zipfile
import json
import uuid
from datetime import datetime


# Load settings from config.json
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


# Save backup record to JSON file
def save_metadata(metadata):
    path = "backups/backup_records.json"
    records = []

    if os.path.exists(path):
        with open(path, "r") as f:
            records = json.load(f)

    records.append(metadata)

    with open(path, "w") as f:
        json.dump(records, f, indent=4)


# Create a zip backup of a file or folder
def create_backup(source_path):
    config = load_config()
    destination = config["backup_destination"]

    # Check if source path exists
    if not os.path.exists(source_path):
        print(f"[ERROR] Source path not found: {source_path}")
        return False

    # Generate unique backup ID and timestamp
    backup_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    source_name = os.path.basename(source_path)
    zip_name = f"backup_{source_name}_{timestamp}.zip"

    # Create backups folder if it does not exist
    os.makedirs(destination, exist_ok=True)
    zip_path = os.path.join(destination, zip_name)

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(source_path):
                # Backup single file
                zipf.write(source_path, os.path.basename(source_path))
            elif os.path.isdir(source_path):
                # Backup entire folder
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)

        # Calculate backup size in KB
        size_kb = round(os.path.getsize(zip_path) / 1024, 2)

        # Save backup details to records
        metadata = {
            "backup_id": backup_id,
            "timestamp": timestamp,
            "source": source_path,
            "destination": zip_path,
            "size_kb": size_kb,
            "status": "SUCCESS"
        }
        save_metadata(metadata)

        print(f"[SUCCESS] Backup complete! ID: {backup_id}")
        print(f"          File: {zip_name}")
        print(f"          Size: {size_kb} KB")
        return True

    except Exception as e:
        print(f"[FAILED] Backup failed: {e}")
        return False


# Delete old backups if limit is exceeded
def cleanup_old_backups():
    config = load_config()
    max_versions = config["max_versions"]
    path = "backups/backup_records.json"

    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        records = json.load(f)

    # Remove oldest backups if over limit
    if len(records) > max_versions:
        to_delete = records[:len(records) - max_versions]
        for record in to_delete:
            if os.path.exists(record["destination"]):
                os.remove(record["destination"])
                print(f"[CLEANUP] Old backup removed: {record['destination']}")
        records = records[len(records) - max_versions:]

        with open(path, "w") as f:
            json.dump(records, f, indent=4)