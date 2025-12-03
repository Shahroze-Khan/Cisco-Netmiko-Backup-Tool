from netmiko import ConnectHandler
from datetime import datetime
import getpass
import os

# ----------------------------------------------------------------------
#                     WELCOME MESSAGE / DESCRIPTION
# ----------------------------------------------------------------------
print("=== Multi-Device Cisco Backup Tool (Enhanced) ===\n")
print("- SSH first -> Auto-fallback to Telnet")
print("- Increased timeouts for large configs")
print("- Clean filenames (.txt)")
print("-------------------------------------------------------------------\n")

# ----------------------------------------------------------------------
#             GET INPUTS
# ----------------------------------------------------------------------
ip_input = input("Enter switch IPs separated by commas or spaces:\n> ")
ips = [ip.strip() for ip in ip_input.replace(",", " ").split()]

username = input("\nEnter your username: ")
password = getpass.getpass("Enter your password: ")
secret = getpass.getpass("Enter enable password (press Enter if same): ")
if not secret:
    secret = password

# ----------------------------------------------------------------------
#             SETUP DIRECTORIES
# ----------------------------------------------------------------------
now = datetime.now()
day_dir = os.path.join("Backups", now.strftime("%Y"), now.strftime("%B"), now.strftime("%d-%b"))
timestamp = now.strftime("%Y%m%d_%H%M%S")

os.makedirs(day_dir, exist_ok=True)
print(f"\nBackups will be saved in: {day_dir}\n")

# ----------------------------------------------------------------------
#             MAIN LOOP
# ----------------------------------------------------------------------
for ip in ips:
    print(f"Connecting to {ip}...")

    # Define base device params
    # global_delay_factor=2 helps with slow/older switches
    device_base = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret,
        "global_delay_factor": 2, 
    }

    conn = None

    # --- ATTEMPT CONNECTION (SSH -> TELNET) ---
    try:
        print(f"  -> Trying SSH...")
        conn = ConnectHandler(**device_base)
        print("  ✔ Connected using SSH")
    except Exception:
        print("  ❌ SSH failed, trying Telnet...")
        try:
            # Modify device type for Telnet
            device_base["device_type"] = "cisco_ios_telnet"
            conn = ConnectHandler(**device_base)
            print("  ✔ Connected using Telnet")
        except Exception as telnet_error:
            print(f"  ❌ Telnet also failed for {ip}")
            print(f"  Error details: {telnet_error}\n")
            continue 

    # --- EXECUTE BACKUP ---
    try:
        conn.enable()
        
        # Disable paging
        conn.send_command("terminal length 0")

        # Get Clean Hostname (Netmiko property)
        hostname = conn.base_prompt 

        # Get Config (With increased timeout for big stacks)
        # read_timeout=90 means wait up to 90 seconds for output
        running_config = conn.send_command("show running-config", read_timeout=90)

        # Optional: Clean the "Building configuration..." line
        if "Building configuration..." in running_config:
            running_config = running_config.split("\n", 1)[-1]

        # Construct Filename (Readable with underscores)
        filename = f"{hostname}_running_config_{timestamp}.txt"
        filepath = os.path.join(day_dir, filename)

        with open(filepath, "w") as f:
            f.write(running_config)

        print(f"  ✔ Backup saved: {filename}\n")
        conn.disconnect()

    except Exception as e:
        print(f"  ❌ Error during backup of {ip}: {e}\n")

print("=== Backup Process Finished ===")