import os
import schedule
import time
import threading
from backup_manager import create_backup, cleanup_old_backups
from monitor import view_backup_history, get_backup_summary, get_latest_backup
from recovery_manager import restore_backup
from reports import generate_backup_report, show_storage_usage


# Run backup automatically in background
def run_scheduled_backup(source_path):
    print(f"\n[SCHEDULER] Auto backup started for: {source_path}")
    create_backup(source_path)
    cleanup_old_backups()


# Start background scheduler thread
def start_scheduler(source_path, interval_minutes):
    schedule.every(interval_minutes).minutes.do(
        run_scheduled_backup, source_path=source_path
    )

    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Run in background so main menu stays active
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print(f"\n[INFO] Auto backup scheduled every {interval_minutes} minutes.")


# Display main menu
def show_menu():
    print("\n" + "=" * 45)
    print("    AUTOMATED BACKUP & RECOVERY SYSTEM")
    print("=" * 45)
    print("  1. Create Manual Backup")
    print("  2. View Backup History")
    print("  3. View Latest Backup")
    print("  4. Restore a Backup")
    print("  5. Backup Summary")
    print("  6. Storage Usage Report")
    print("  7. Generate Full Report")
    print("  8. Start Auto Scheduled Backup")
    print("  9. Exit")
    print("=" * 45)


# Main program loop
def main():
    print("\n  Welcome to Backup & Recovery System")
    print("  Teyzix Core Internship -- Task 2\n")

    while True:
        show_menu()
        choice = input("  Enter your choice (1-9): ").strip()

        if choice == "1":
            source = input("\n  Enter full path of file/folder to backup: ").strip()
            create_backup(source)
            cleanup_old_backups()

        elif choice == "2":
            view_backup_history()

        elif choice == "3":
            get_latest_backup()

        elif choice == "4":
            destination = input("\n  Enter folder path where files will be restored: ").strip()
            restore_backup(destination)

        elif choice == "5":
            get_backup_summary()

        elif choice == "6":
            show_storage_usage()

        elif choice == "7":
            generate_backup_report()

        elif choice == "8":
            source = input("\n  Enter path to auto-backup: ").strip()
            try:
                minutes = int(input("  Auto backup every how many minutes?: "))
                start_scheduler(source, minutes)
            except ValueError:
                print("[ERROR] Please enter a valid number.")

        elif choice == "9":
            print("\n  Goodbye! Backup system closed.\n")
            break

        else:
            print("\n  [ERROR] Invalid choice. Please enter 1-9.")


if __name__ == "__main__":
    main()