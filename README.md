@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+.             +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%     -@@-   .%@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  . +@@@@@@  @@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.  -@@@@@@@@  @@@@@@@@.  +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ .@@@@@@@@@   +@@@@@@@@.  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@. +@@@@@@@@*    @@@@@@@@@: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  #@@@@@@@%      %@@@@@@@. :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   :@@@@@-  -@@-   @@@@@   =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@         .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                      .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@   -      +   @@@@  +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@   *  :   @  .@@@@  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@%%  +=  @#@@@@@.      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       +@@@@@@@@@@@@@@@@@   .   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@. #@%   .@@@@@@@@@@@@:    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ..@@@@@@@%.  .%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@    .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@ .   +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   . @@@@@@@@@% .  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        =@@@@@@@@@@@@@@-        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@+   .-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@%   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+@@@@@@@@@@@@@@@@@@@@  :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                                          
                                                          


# Albator - macOS 15 Hardening Tool  
A series of scripts to harden macOS 15 (Sequoia) for security and privacy, inspired by NIST guidelines. Suitable for power users and novices alike. This project evolved from the macOS Security Compliance Project, a Python-based tool, with the current focus on Bash scripts while preserving legacy features.  

## Usage  
Run the main script with options to harden specific areas or fetch security advisories:  

```bash
./albator.sh [options]
```

### Options  
- `-f, --firewall`: Enable and configure the firewall  
- `-p, --privacy`: Adjust privacy settings (e.g., disable telemetry, configure Safari)  
- `-e, --encryption`: Enable FileVault encryption  
- `-s, --app-security`: Enable Gatekeeper and verify Hardened Runtime  
- `-c, --cve`: Fetch recent CVE advisories relevant to macOS  
- `-a, --apple`: Fetch Apple security updates for macOS Sequoia 15  
- `-h, --help`: Display help message  

### Example  
To fetch CVE advisories, Apple security updates, and enable the firewall:  

```bash
./albator.sh --cve --apple --firewall
```

## Requirements  
- macOS 15 (Sequoia)  
- Administrator privileges (sudo access)  
- `curl` and `jq` for fetching CVE advisories (`brew install jq`)  
- `pup` for parsing Apple security updates (`brew install pup`, optional but recommended)  
- See `requirements.txt` for a detailed list of dependencies and installation instructions.  
- **Legacy Python Requirements:** Python 3.9+ and `pyyaml` (if using the original Python implementation).  

## Features  
- Modular scripts for targeted hardening (firewall, privacy, encryption, app security)  
- NIST-inspired security standards  
- Disables unnecessary services (remote login, remote management, mDNS multicast)  
- CVE advisory fetching to keep users informed about potential vulnerabilities  
- Cross-referencing with Apple’s security updates for a comprehensive view of macOS vulnerabilities  

### Legacy Features (Previous Python Implementation)  
The project originated as a Python-based tool with the following capabilities:  
- **Rule Collection:** Aggregated security rules from `rules/` and `custom/rules/` directories.  
- **Baseline Generation:** Created YAML security baselines (e.g., STIG) based on keyword tags.  
- **Control Verification:** Checked compliance against NIST 800-53 controls.  
- **Tailoring:** Customized baselines with user-specific configurations and Organizational Defined Values (ODVs).  
- **Fix Application:** Applied security fixes directly to the system, with prompts for confirmation (some require `sudo`).  

### Interfaces  
- **Command-Line:** Flags like `-l`, `-k`, `-c`, `-t`, `-i`, `--gui`.  
- **Interactive Mode:** Run with `-i` for a command-line prompt.  
- **GUI Mode:** Launch with `--gui` for a window with radio buttons.  

### Supported Version  
- **macOS 15.4 (Sequoia)**, with rules adapted from **NIST Revision 1.1 (December 16, 2024)**.  

## Security Rules (Applicable to Both Versions)  
- **Disable Guest Account** (`os_guest_account_disable`)  
- **Enable System Integrity Protection** (`os_sip_enable`)  
- **Enable Gatekeeper** (`os_gatekeeper_enable`)  
- **Disable Bluetooth** (`os_bluetooth_disable`)  
- **Disable Root Account** (`os_root_disable`)  
- **Require Password for Screensaver** (`os_screensaver_password`)  
- **Enable Firewall** (`os_firewall_enable`)  
- **Enable Software Updates** (`os_software_update_auto`)  
- **Disable SSH** (`os_ssh_disable`)  
- **Disable Remote Management** (`os_remote_management_disable`)  
- **Secure Keyboard Settings** (`os_keyboard_secure`)  
- **Disable Wi-Fi** (`os_wifi_disable`)  
- **Enable FileVault** (`os_filevault_enable`)  
- **Enable Lockdown Mode** (`os_lockdown_enable`)  

## Notes and Limitations  
- Some changes (e.g., FileVault) may require a system restart.  
- Always back up your system before applying hardening scripts.  
- CVE and Apple updates fetching require an internet connection.  
- Disabling mDNS multicast may require temporarily disabling **System Integrity Protection (SIP)** on some systems. To do this, reboot into **Recovery Mode**, run `csrutil disable`, apply the changes, then re-enable SIP with `csrutil enable`.  
- The Apple security updates script provides links to detailed pages where CVEs and vulnerability details are listed. Future enhancements could include scraping these details directly.  

## Installation (Legacy Python Setup)  

### Set Up Directory  
```bash
mkdir -p ~/macoshardening/MACOS_HARDENING
cd ~/macoshardening/MACOS_HARDENING
```

### Create Subdirectories  
```bash
mkdir -p rules custom/rules includes build/baselines
```

### Install Python Dependencies  
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml
```

### Verify Files  
Ensure `main.py`, `arg_parser.py`, `rule_handler.py`, `utils.py`, `VERSION.yaml`, `includes/800-53_baselines.yaml`, `includes/mscp-data.yaml`, and `rules/*.yaml` exist.  

## Usage (Legacy Python Commands)  

### Command-Line Mode  
**List Tags:**  
```bash
python main.py -l
```

**Generate Baseline:**  
```bash
python main.py -k stig
```

**Check Controls:**  
```bash
python main.py -c
```

**Tailor Baseline:**  
```bash
python main.py -k stig -t
```

### Interactive Mode  
**Start:**  
```bash
sudo python main.py -i
```

**Commands:** `list`, `generate <tag>`, `check`, `tailor <tag>`, `apply <tag>`, `exit`.  

### GUI Mode  
**Start:**  
```bash
sudo python main.py --gui
```

**Interface:** Radio buttons for actions, click "Proceed" to execute.  

## Project Structure (Legacy)  
```
macoshardening/
├── MACOS_HARDENING/
│   ├── main.py            # Core script
│   ├── arg_parser.py      # Argument parsing
│   ├── rule_handler.py    # Rule handling
│   ├── utils.py           # Utilities
│   ├── includes/          # Configuration
│   ├── VERSION.yaml       # Version info
│   ├── build/             # Baselines
│   └── venv/              # Virtual env
├── rules/                 # Rule YAMLs
├── custom/                # Custom rules
└── README.md              # This file
```

## Contributing  
Feel free to submit issues or pull requests to improve Albator, including enhancements to the Bash scripts or revival of Python features!  

## License  
Open-source under the MIT License.  

## Acknowledgments  
- Built on **NIST macOS Security Guidelines (Revision 1.1, 2024)**.  
- Inspired by the **macOS Security and Privacy Guide** and Derrick https://github.com/supdevinci/derrick/tree/main.  
- Developed by **Maxime at Cyberdyne Systems**.  
