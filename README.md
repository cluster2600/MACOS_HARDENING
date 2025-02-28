     # macOS Security Compliance Project
     This project is a Python-based tool designed to enhance the security and privacy of macOS systems, specifically targeting macOS 15.4 (Sequoia) as of February 28, 2025. It automates the generation, customization, and application of security baselines aligned with standards such as NIST SP 800-53 and DISA STIG, drawing inspiration from the [NIST macOS Security Guidelines](https://github.com/usnistgov/macos_security) and the [macOS Security and Privacy Guide](#macos-security-and-privacy-guide).

     The tool supports multiple interfaces—command-line, interactive mode, and a graphical user interface (GUI)—making it accessible to both power users and novices aiming to harden their macOS systems.

     ## Features
     - **Rule Collection**: Aggregates security rules from `rules/` and `custom/rules/` directories.
     - **Baseline Generation**: Creates YAML security baselines (e.g., STIG) based on keyword tags.
     - **Control Verification**: Checks compliance against NIST 800-53 controls.
     - **Tailoring**: Customizes baselines with user-specific configurations and Organizational Defined Values (ODVs).
     - **Fix Application**: Applies security fixes directly to the system, with prompts for confirmation (some require `sudo`).
     - **Interfaces**:
       - **Command-Line**: Use flags like `-l`, `-k`, `-c`, `-t`, `-i`, `--gui`.
       - **Interactive Mode**: Run with `-i` for a command-line prompt experience.
       - **GUI Mode**: Launch with `--gui` for a window with radio buttons to select actions.

     ## Supported macOS Version
     - macOS 15.4 (Sequoia), with rules adapted from NIST Revision 1.1 guidance for macOS 15.0 (December 16, 2024) and customized for 15.4.

     ## Prerequisites
     - **Python 3.9+**: Pre-installed on macOS 15.4 or available via Homebrew (`brew install python`).
     - **Dependencies**: Install with:
       ```bash
       pip install pyyaml
       ```
     - **Tkinter**: Included with Python for GUI mode; ensure Xcode is installed for full compatibility (`xcode-select --install`).
     - **Sudo Access**: Required for applying system-level security fixes.

     ## Installation
     1. **Set Up Directory**:
        - Clone this repo or create the structure manually:
          ```bash
          mkdir -p /Users/maxime/macoshardening/MACOS_HARDENING
          cd /Users/maxime/macoshardening/MACOS_HARDENING
          ```
        - Ensure `rules/`, `custom/rules/`, `includes/`, and `build/baselines/` exist:
          ```bash
          mkdir -p ../rules ../custom/rules includes build/baselines
          ```
     2. **Install Python Dependencies**:
        - Create and activate a virtual environment (optional):
          ```bash
          python3 -m venv venv
          source venv/bin/activate
          ```
        - Install PyYAML:
          ```bash
          pip install pyyaml
          ```
     3. **Verify Files**:
        - Ensure `main.py`, `arg_parser.py`, `rule_handler.py`, `utils.py`, `VERSION.yaml`, `includes/800-53_baselines.yaml`, `includes/mscp-data.yaml`, and rule files in `../rules/` are present.

     ## Usage
     ### Command-Line Mode
     - **List Tags**:
       ```bash
       python main.py -l
       ```
     - **Generate Baseline**:
       ```bash
       python main.py -k stig
       ```
     - **Check Controls**:
       ```bash
       python main.py -c
       ```
     - **Tailor Baseline**:
       ```bash
       python main.py -k stig -t
       ```

     ### Interactive Mode
     - Start:
       ```bash
       sudo python main.py -i
       ```
     - Commands:
       - `list`: Display all tags (e.g., `stig`, `security`).
       - `generate <tag>`: Create a baseline (e.g., `generate stig`).
       - `check`: Verify NIST 800-53 control coverage.
       - `tailor <tag>`: Customize a baseline (e.g., `tailor stig`).
       - `apply <tag>`: Apply fixes for rules with the tag (e.g., `apply stig`).
       - `exit`: Quit interactive mode.

     ### GUI Mode
     - Start:
       ```bash
       sudo python main.py --gui
       ```
     - Interface:
       - Radio buttons for: List Tags, Generate Baseline, Check Controls, Tailor Baseline, Apply Fixes.
       - Click "Proceed" to execute the selected action, follow prompts as needed.

     **Note**: Use `sudo` for commands applying fixes (e.g., `apply`) that modify system settings.

     ## Project Structure
     ```
     macoshardening/
     ├── MACOS_HARDENING/
     │   ├── main.py            # Core script with CLI, interactive, and GUI modes
     │   ├── arg_parser.py      # Command-line argument parsing
     │   ├── rule_handler.py    # Rule collection, control checking, baseline generation
     │   ├── utils.py           # Utility functions and MacSecurityRule class
     │   ├── includes/          # Configuration files
     │   │   ├── 800-53_baselines.yaml  # NIST 800-53 control baselines
     │   │   └── mscp-data.yaml         # Metadata for authors and titles
     │   ├── VERSION.yaml       # macOS version info
     │   ├── build/             # Generated outputs
     │   │   └── baselines/     # Baseline YAML files (e.g., stig.yaml)
     │   └── venv/              # Virtual environment (optional)
     ├── rules/                 # Security rule YAML files
     │   ├── os_auto_login_disable.yaml
     │   ├── os_bluetooth_disable.yaml
     │   ├── os_filevault_enable.yaml
     │   ├── os_firewall_enable.yaml
     │   ├── os_gatekeeper_enable.yaml
     │   ├── os_guest_account_disable.yaml
     │   ├── os_keyboard_secure.yaml
     │   ├── os_lockdown_enable.yaml
     │   ├── os_remote_management_disable.yaml
     │   ├── os_require_password_wake.yaml
     │   ├── os_root_disable.yaml
     │   ├── os_screensaver_password.yaml
     │   ├── os_sip_enable.yaml
     │   ├── os_software_update_auto.yaml
     │   ├── os_ssh_disable.yaml
     │   └── os_wifi_disable.yaml
     ├── custom/
     │   └── rules/             # Optional custom rule overrides
     └── README.md              # This documentation
     ```

     ## Security Rules
     The tool applies the following security measures via rules in `../rules/`:
     - **Disable Guest Account**: Prevents unauthorized access (`os_guest_account_disable`).
     - **Enable System Integrity Protection**: Protects system files (`os_sip_enable`, manual).
     - **Enable Gatekeeper**: Restricts untrusted apps (`os_gatekeeper_enable`).
     - **Disable Bluetooth**: Reduces wireless risks (`os_bluetooth_disable`).
     - **Disable Root Account**: Limits root access (`os_root_disable`).
     - **Disable Automatic Login**: Secures startup (`os_auto_login_disable`).
     - **Require Password to Wake**: Protects idle systems (`os_require_password_wake`).
     - **Require Password for Screensaver**: Secures screen lock (`os_screensaver_password`).
     - **Enable Firewall**: Blocks incoming connections (`os_firewall_enable`).
     - **Enable Software Updates**: Ensures patch updates (`os_software_update_auto`).
     - **Disable SSH**: Prevents remote login (`os_ssh_disable`).
     - **Disable Remote Management**: Limits remote access (`os_remote_management_disable`).
     - **Secure Keyboard Settings**: Mitigates keylogging (`os_keyboard_secure`).
     - **Disable Wi-Fi**: Reduces wireless exposure (`os_wifi_disable`).
     - **Enable FileVault**: Encrypts disk (manual, `os_filevault_enable`).
     - **Enable Lockdown Mode**: Protects against advanced threats (manual, `os_lockdown_enable`).

     To add new rules:
     1. Create a `.yaml` file in `../rules/` with `title`, `id`, `check`, `fix`, etc.
     2. Test with `apply <tag>` in interactive mode.

     ## Known Limitations
     - **Manual Fixes**: Rules like FileVault and Lockdown Mode require manual steps due to GUI dependencies.
     - **Sudo Requirement**: Many fixes need root privileges; run with `sudo` for full functionality.
     - **macOS 15.4 Specificity**: Rules are based on Sequoia 15.0 guidance; verify compatibility with 15.4 updates.

     ## Contributing
     - Add new rules to `../rules/` or improve scripts.
     - Submit feedback or enhancements via issues or pull requests if hosted on a repository.

     ## License
     Open-source under the MIT License (to be added as `LICENSE`).

     ## Acknowledgments
     - Built on NIST macOS Security Guidelines (Revision 1.1, 2024).
     - Inspired by the [macOS Security and Privacy Guide](#macos-security-and-privacy-guide).
     - Developed by Maxime at Cyberdyne Systems.
     EOF
     ```

2. **Verify Content**:
   - Check the file:
     ```bash
     cat README.md
     ```
   - Ensure it looks correct and reflects your project’s capabilities.

3. **Customize (Optional)**:
   - If you’ve hosted this on GitHub, replace `<repository-url>` with the actual URL.
   - Adjust the project name or add personal details if desired.

---

### Explanation of Updates
- **Features**: Expanded to include fix application and GUI mode with radio buttons.
- **Security Rules**: Lists all implemented rules from the document, ensuring completeness.
- **Usage**: Provides detailed examples for all three modes, with `sudo` noted where necessary.
- **Structure**: Matches your current directory layout, including all rule files.
- **Limitations**: Highlights manual steps and sudo requirements for clarity.


---

## Miscellaneous

- Enable Find My Mac.
- Use a YubiKey for 2FA.
- Install updates promptly.
- Review settings regularly.

---

## Related Software

- [KnockKnock](https://objective-see.com/products/knockknock.html)
- [RansomWhere?](https://objective-see.com/products/ransomwhere.html)
- [BlockBlock](https://objective-see.com/products/blockblock.html)

---

## Additional Resources

- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
- [SecureMac Guide](https://www.securemac.com/mac-security-guide)
- [Objective-See](https://objective-see.com/)
- [MacRumors Forums](https://forums.macrumors.com/)

---

## Author

Created by Cluster2600, inspired by [NIST macOS Security](https://github.com/usnistgov/macos_security).