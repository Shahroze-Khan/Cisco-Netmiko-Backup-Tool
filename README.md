📘 Cisco Netmiko Backup Automation Tool

🚀 Overview

This tool automates the process of retrieving running configurations from multiple Cisco IOS network devices (Switches/Routers) and saves them in an organized, date-stamped directory structure. It is engineered for resilience, automatically attempting a Telnet fallback if the primary SSH connection fails.

⭐ Key Features

Dual Protocol Resilience: Prioritizes SSH for security, but automatically falls back to Telnet to ensure compatibility with legacy or non-fully-configured devices.

Timeouts for Large Configs: Includes increased read_timeout and global_delay_factor to handle large switch stacks or slow devices without failing the connection.

Structured Archiving: Automatically creates a hierarchical directory structure based on the current date: Backups / YEAR / MONTH / DAY /.

Clean Output: Files are saved as .txt and automatically use the device's actual hostname for clean, consistent file naming.

🛠️ Requirements & Installation

Prerequisites

Python 3.x

The Netmiko library

Installation

Install the Netmiko Library:

pip install netmiko


Save the Script:
Save the provided Python code as backup_tool.py within your chosen project directory.

🏃‍♂️ How to Use

Execute the Script:

python backup_tool.py


Provide Input:

Enter all device IP addresses, separated by commas or spaces.

Enter your username, login password, and enable password when prompted.

Review Output: The script will confirm connections, indicate success, or log any failure to connect, ensuring non-blocking execution across the device list.

📂 Example Directory Structure

Backups/
└── 2025/
    └── December/
        └── 03-Dec/
            ├── CORE_SW_running_config_20251203_103000.txt
            └── ACCESS_01_running_config_20251203_103005.txt
