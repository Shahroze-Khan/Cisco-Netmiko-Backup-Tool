🛡️ Multi-Device Cisco Backup Tool 

📖 Overview

This Python automation tool streamlines the daily backup process for Cisco IOS network devices (Switches and Routers).

Unlike standard scripts that fail when encountering legacy equipment, this tool features a resilient connection engine. It prioritizes secure SSH connections but automatically attempts a Telnet fallback if SSH is refused or times out.

⚡ Key Features

Hybrid Protocol Support: * 🚀 Primary: SSH (Port 22) via cisco_ios.

🔄 Fallback: Telnet (Port 23) via cisco_ios_telnet.

Intelligent Organization: Automatically generates a directory tree based on the current date (Backups/YYYY/Month/Day/).

Resilience & Stability:

read_timeout=90: Prevents crashes on large stack switches with massive config files.

global_delay_factor=2: Adds a multiplier to wait times, ensuring slow legacy devices don't disconnect during login.

Clean Output: Sanitizes filenames using the device hostname and saves configurations as standard .txt files.

🛠️ Prerequisites

Python 3.6+

Netmiko Library

pip install netmiko


🚀 Usage

Clone or Download the script backup_tool.py.

Run the script in your terminal:

python backup_tool.py


Provide Inputs when prompted:

IP Addresses: Enter a list of IPs separated by spaces or commas (e.g., 192.168.1.1, 10.0.0.1).

Credentials: Enter your Username, Password, and Enable Secret. (Passwords are hidden for security).

📂 Output Structure

The script creates a structured archive to keep your backups organized over time:

Backups/
└── 2025/
    └── December/
        └── 03-Dec/
            ├── Core_Switch_running_config_20251203_0900.txt
            ├── Access_SW_01_running_config_20251203_0901.txt
            └── Legacy_Router_running_config_20251203_0902.txt


⚙️ Logic Flow

The script follows this decision matrix for every IP provided:

Initialize: specific device parameters (IP, user, pass).

Attempt SSH: Try ConnectHandler with device_type='cisco_ios'.

Catch Error: If SSH fails, log error and swap device_type to cisco_ios_telnet.

Attempt Telnet: Retry connection.

Execute: Disable paging (term len 0), fetch config, save to file.

📝 License

This project is open-source. Feel free to fork and modify!
