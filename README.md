# Automated Data Backup & Recovery Management System

**Teyzix Core Internship — Task 2 (June Batch 2026)**

---

## About This Project

A Python-based system that automates data backup operations, manages backup versions, monitors backup health, and provides recovery functionality for stored files and directories.

---

## Features

- Create manual backups of any file or folder
- Auto scheduled backups at custom intervals
- View full backup history
- Restore files from any previous backup
- Backup integrity verification before restore
- Backup summary and storage usage reports
- Generate full backup reports saved to file
- Automatic cleanup of old backups (version limit)
- Recovery activity logs

---

## Project Structure

Backup_System/
├── main.py               # Main menu and program entry point
├── backup_manager.py     # Backup creation and cleanup logic
├── monitor.py            # Backup history and status monitoring
├── recovery_manager.py   # File restoration and verification
├── reports.py            # Report generation and storage stats
├── config.json           # System configuration settings
├── logs/                 # Auto-generated log files
└── backups/              # Auto-generated backup zip files

---

## Installation

1. Clone the repository:
git clone https://github.com/fzounr5-source/Teyzix-core--Internship-Task-2-Backup-System.git

2. Create virtual environment:
python -m venv .venv

3. Activate virtual environment:
source .venv/Scripts/activate

4. Install dependencies:
pip install schedule

---

## How To Run

python main.py

---

## Menu Options

| Option | Feature |
|--------|---------|
| 1 | Create Manual Backup |
| 2 | View Backup History |
| 3 | View Latest Backup |
| 4 | Restore a Backup |
| 5 | Backup Summary |
| 6 | Storage Usage Report |
| 7 | Generate Full Report |
| 8 | Start Auto Scheduled Backup |
| 9 | Exit |

---

## Technologies Used

- Python 3.x
- zipfile
- schedule
- json
- os
- threading
- uuid
- datetime

---

## Developer

Fahad Ali
Teyzix Core Internship — June Batch 2026
