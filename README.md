# macOS Security Setup Script

This script automates the process of enhancing the security and privacy of your macOS system. It follows guidelines from the macOS Security and Privacy Guide and incorporates new features available in macOS 15 (Sequoia).

## Features

- Installs essential security tools using Homebrew.
- Configures system settings for improved security and privacy.
- Sets up DNS settings with `dnscrypt-proxy`.
- Configures the built-in macOS firewall.
- Enables FileVault for disk encryption.
- Disables unnecessary services and features to reduce the attack surface.
- Sets up and configures Tor for anonymous browsing.
- Installs and configures antivirus software.
- Sets up a password manager.
- Cleans up metadata from files using `exiftool`.
- Enables System Integrity Protection (SIP).

## Requirements

- macOS 15 (Sequoia)
- Administrative privileges

## Installation

1. **Download and Save the Script**

   Save the script to a file on your macOS system. For example, you can create a file named `macos_security_setup.sh`.

   ```sh
   nano macos_security_setup.sh
   
### Make the Script Executable

Change the permissions of the script to make it executable:

```sh
chmod +x macos_security_setup.sh

### Run the Script with Root Privileges

Since the script performs tasks that require administrative privileges, you need to run it with sudo:

```sh
sudo ./macos_security_setup.sh

### Usage
Step-by-Step Instructions
Backup Your Data

Before running any script that makes significant changes to your system, make sure to back up your important data.

Run the Script

Open Terminal and navigate to the directory where you saved the script. Execute the script using the following command:

```sh
sudo ./macos_security_setup.sh

## Review and Adjust Settings

After running the script, review the changes made to ensure everything is configured to your liking. Some settings might require manual intervention or additional configuration.

Script Explanation
Homebrew Installation: Installs Homebrew if it's not already installed and updates it.
Security Tools Installation: Installs various security tools such as gpg, nmap, wireshark, dnscrypt-proxy, privoxy, gnupg, exiftool, little-snitch, radio-silence, lulu, tor, knockknock, ransomwhere, and blockblock.
System Configuration: Uses AppleScript to disable Siri Suggestions, Location Services, and Sharing Analytics. Enables FileVault and Firewall.
DNS Configuration: Sets up DNS settings with Cloudflare DNS and configures dnscrypt-proxy.
Privacy Tools Configuration: Configures privoxy for web privacy.
Firefox Setup: Installs Firefox and privacy-focused extensions.
SSH Key Setup: Generates SSH keys and configures SSH for improved security.
Tor Setup: Installs and configures Tor for anonymous browsing.
Antivirus Installation: Installs Malwarebytes antivirus.
Password Manager Installation: Installs Bitwarden password manager.
System Integrity Protection: Ensures SIP is enabled.
Metadata Cleanup: Installs and configures exiftool to strip metadata from files.
License
This script is provided as-is without any warranties of any kind. Use it at your own risk. Only you are responsible if you break anything or get into any trouble by following this guide.

Contributing
To suggest an improvement, send a pull request or open an issue on the GitHub repository.

This script is inspired by the macOS Security and Privacy Guide.
