import os
import subprocess
import webbrowser
import time

def update_vpn_address(vpn_name, address):
    """Update the VPN address in the rasphone.pbk file."""
    phonebook_path = r"C:\Users\Yoni\AppData\Roaming\Microsoft\Network\Connections\Pbk\rasphone.pbk"
    
    # Check if the phonebook file exists
    if not os.path.exists(phonebook_path):
        print(f"Phonebook file not found at {phonebook_path}")
        exit(1)
    
    try:
        with open(phonebook_path, 'r') as file:
            lines = file.readlines()

        # Update the PhoneNumber field in the specified VPN section
        with open(phonebook_path, 'w') as file:
            in_section = False
            for line in lines:
                if line.strip().startswith(f"[{vpn_name}]"):
                    in_section = True
                elif in_section and line.strip().startswith("[") and not line.strip().startswith(f"[{vpn_name}]"):
                    in_section = False
                
                # Update PhoneNumber only in the target VPN section
                if in_section and line.strip().startswith("PhoneNumber="):
                    print(f"Updating PhoneNumber to {address}")
                    line = f"PhoneNumber={address}\n"
                
                file.write(line)

        print(f"VPN address updated successfully to {address} for '{vpn_name}'.")
    except Exception as e:
        print(f"Failed to update VPN address. Error: {e}")
        exit(1)

def connect_to_winbox(address):
    """Attempt to connect to Winbox with the provided address."""
    try:
        winbox_path = r"C:\Users\Yoni\Desktop\winbox64.exe"  # Path to Winbox
        subprocess.Popen([winbox_path, address, "admin", "ip6576pi"])
        print(f"Trying to connect to Winbox with address: {address}...")
        time.sleep(5)  # Wait a few seconds to allow Winbox to initiate
        return True  # Assume success if no error occurs
    except Exception as e:
        print(f"Failed to connect to Winbox with address {address}. Error: {e}")
        return False

def connect_to_vpn(vpn_name, username, password, domain):
    """Initiate a VPN connection using rasdial with credentials."""
    try:
        print(f"Connecting to VPN '{vpn_name}' with domain '{domain}'...")
        subprocess.run(["rasdial", vpn_name, username, password, "/domain:" + domain], check=True)
        print("VPN connection successfully initiated.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to VPN '{vpn_name}'. Error: {e}")
        exit(1)

def open_browser():
    """Open an incognito browser to access the managed device."""
    url = "http://10.0.0.250"
    print(f"Opening incognito browser to access {url}...")
    
    # Use Chrome with incognito mode
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update if needed
        subprocess.Popen([chrome_path, "--incognito", url])
        print(f"Browser opened for {url} in incognito mode.")
    except FileNotFoundError:
        print("Chrome not found. Opening default browser instead.")
        webbrowser.open(url)

def main():
    """Main function to automate the connection process."""
    vpn_name = "VPN"  # Replace with your VPN entry name in Rasphone
    username = "iPcomVPN"
    password = "ip576dr"  # Updated password as per clarification
    
    while True:
        # Ask for the Mikrotik Winbox address
        mikrotik_address = input("Enter the Mikrotik Winbox address (e.g., WAN1, WAN2, LTE): ").strip()
        vpn_address = mikrotik_address  # Use the same address for VPN
        
        # Step 1: Try to connect to Winbox
        if connect_to_winbox(mikrotik_address):
            print(f"Successfully connected to Winbox with address: {mikrotik_address}")
            
            # Step 2: Update VPN address in the phonebook
            update_vpn_address(vpn_name, vpn_address)
            
            # Step 3: Connect to VPN
            connect_to_vpn(vpn_name, username, password, vpn_address)
            
            # Step 4: Open incognito browser to 10.0.0.250
            open_browser()
            
            print("All tasks completed!")
            break
        else:
            print(f"Failed to connect to Winbox with address: {mikrotik_address}. Please try again.")

if __name__ == "__main__":
    main()