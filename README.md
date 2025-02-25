# macOS Security and Privacy Guide

This guide provides comprehensive techniques for enhancing the security and privacy of [Apple silicon](https://support.apple.com/116943) Mac computers running macOS 15 (Sequoia), a [currently supported version](https://support.apple.com/HT201222). **Intel-based Macs are vulnerable to unpatchable hardware exploits like [checkm8](https://github.com/axi0mX/ipwndfu?tab=readme-ov-file#checkm8)**, making Apple silicon the minimum recommendation for security-conscious users. Newer silicon chips generally offer improved security features.

Targeted at power users seeking enterprise-grade security and novices interested in bolstering their privacy, this guide complements the [macOS Security Compliance Project](#macos-security-compliance-project) tools included in this repository.

For organizational deployments, refer to the [official NIST guidelines for macOS](https://github.com/usnistgov/macos_security). Security is an ongoing process—your system's protection depends on your ability to implement and maintain these practices effectively.

**Disclaimer**: This guide is provided "as is" without warranties. You assume full responsibility for any consequences of applying these recommendations.

Contribute improvements via pull requests or [open an issue](https://github.com/drduh/macOS-Security-and-Privacy-Guide/issues).

## Table of Contents

- [Basics](#basics)
- [Threat Modeling](#threat-modeling)
- [macOS Security Compliance Project](#macos-security-compliance-project)
- [Hardware](#hardware)
- [Installing macOS](#installing-macos)
- [First Boot](#first-boot)
- [Admin and User Accounts](#admin-and-user-accounts)
- [Firmware](#firmware)
- [FileVault](#filevault)
- [Lockdown Mode](#lockdown-mode)
- [Firewall](#firewall)
- [Services](#services)
- [Siri and Spotlight](#siri-and-spotlight)
- [Homebrew](#homebrew)
- [DNS](#dns)
- [Certificate Authorities](#certificate-authorities)
- [Privoxy](#privoxy)
- [Browser](#browser)
- [Tor](#tor)
- [VPN](#vpn)
- [PGP/GPG](#pgpgpg)
- [Messengers](#messengers)
- [Malware Protection](#malware-protection)
- [System Integrity Protection](#system-integrity-protection)
- [Metadata Management](#metadata-management)
- [Passwords](#passwords)
- [Backup](#backup)
- [Wi-Fi](#wi-fi)
- [SSH](#ssh)
- [Physical Security](#physical-security)
- [System Monitoring](#system-monitoring)
- [Binary Authorization](#binary-authorization)
- [Miscellaneous](#miscellaneous)
- [Related Software](#related-software)
- [Additional Resources](#additional-resources)
- [Author](#author)

---

## Basics

Foundational security practices include:

- **Threat Modeling**: Define what you're protecting and from whom (see [Threat Modeling](#threat-modeling)).
- **Updates**: Keep macOS and all software current via [System Settings](https://support.apple.com/guide/mac-help/keep-your-mac-up-to-date-mchlpx1065) or `softwareupdate`. Subscribe to [Apple security-announce](https://lists.apple.com/mailman/listinfo/security-announce).
- **Encryption**: Use [FileVault](#filevault) and the [built-in password manager](https://support.apple.com/105115).
- **Backups**: Maintain [encrypted backups](https://support.apple.com/104984) and verify them regularly ([restore guide](https://support.apple.com/102551)).
- **Caution**: Install software only from trusted, official sources.

---

## Threat Modeling

Effective security starts with a [threat model](https://www.owasp.org/index.php/Application_Threat_Modeling):

1. **Identify Assets**: List what you value (e.g., devices, passwords, browsing history) and categorize by sensitivity.
2. **Identify Adversaries**: Define potential threats (e.g., thieves, state actors) and their motivations.
3. **Identify Capabilities**: Assess adversary skills (e.g., basic theft vs. advanced surveillance).
4. **Identify Mitigations**: Implement countermeasures tailored to your risks.

Example:

| Adversary          | Motivation                  | Capabilities                          | Mitigation                              |
|--------------------|-----------------------------|---------------------------------------|-----------------------------------------|
| Roommate           | Curiosity                   | Physical access                       | Biometrics, privacy screen              |
| Thief              | Financial gain              | Steal unlocked device                 | Lock screen, keep device secure         |
| State Actor        | Surveillance                | Firmware exploits, network monitoring | Trusted hardware, encrypted channels    |

---

## macOS Security Compliance Project

This repository includes Python tools to generate and customize security baselines for macOS, aligned with NIST guidelines. These scripts automate rule collection, baseline generation, and compliance checking.

### Features
- **Rule Collection**: Aggregates security rules from predefined and custom directories.
- **Baseline Generation**: Creates YAML baselines based on keyword tags (e.g., STIG, CIS Level 1).
- **Customization**: Allows tailoring baselines with organization-defined values (ODVs) via interactive prompts.
- **Control Verification**: Checks coverage against NIST 800-53 controls.

### Usage
1. **Clone Repository**: `git clone <repo-url>`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run Commands**:
   - List available tags: `python main.py -l`
   - Check control coverage: `python main.py -c`
   - Generate a baseline: `python main.py -k stig`
   - Generate a tailored baseline: `python main.py -k cis_lvl1 -t`

### Examples
- **List Tags**: `python main.py -l`
  - Output: Lists all available tags like `stig`, `cis_lvl1`, `all_rules`.
- **Generate STIG Baseline**: `python main.py -k stig`
  - Creates `stig.yaml` in the `build/baselines` directory.
- **Tailor a Baseline**: `python main.py -k recommended -t`
  - Prompts for a custom name, author details, and rule inclusion/ODV customization.

See the script source code for additional details.

---

## Hardware

Assume hardware and firmware may be compromised. Apple silicon Macs offer:
- **Secure Enclave**: Hardware-based encryption for sensitive data.
- **T2 Chip** (select models): Secure boot and storage encryption.

For high-risk scenarios, use a dedicated, offline machine for sensitive tasks.

---

## Installing macOS

Start fresh for a clean slate:
1. **Download Installer**: Get macOS 15 from the [Mac App Store](https://apps.apple.com/us/story/id1527743152354257857?src=changeRegion®ion=us).
2. **Create Bootable USB**: Use `createinstallmedia`.
3. **Erase Drive**: Boot to Recovery (Command-R), format as APFS via Disk Utility.
4. **Install**: Run the installer from USB.

### System Activation
Skip Apple ID creation with "Set Up Later" unless needed.

### Apple ID
Use unique IDs per device to limit exposure.

### App Store
Verify software signatures when downloading outside the App Store.

### Virtualization
Use Parallels or VMware Fusion to sandbox untrusted apps.

---

## First Boot

Configure carefully:
- Disable Location Services, Analytics, and unnecessary features.
- Connect to a trusted network.
- Set up Screen Time for usage monitoring.

---

## Admin and User Accounts

- **Standard User**: Create a non-admin account for daily use.
- **Disable Auto-Login**: System Settings > Users & Groups > Login Options.
- **Fast Switching**: Enable for convenience.

### Caveats
- Avoid enabling the root account; use `sudo` instead.
- Limit admin accounts.

---

## Firmware

Update via System Settings > Software Update. Consider EFI password protection.

---

## FileVault

Enable in System Settings > Security & Privacy > FileVault. Store the recovery key securely off-device.

---

## Lockdown Mode

For high-risk users, enable Lockdown Mode in System Settings > Security & Privacy to restrict features against sophisticated attacks.

---

## Firewall

### Application Layer
Enable in System Settings > Security & Privacy > Firewall. Customize allowed apps.

### Third-Party
Options: [Little Snitch](https://www.obdev.at/products/littlesnitch), [LuLu](https://objective-see.com/products/lulu.html).

### Packet Filtering
Use `pfctl` and edit `/etc/pf.conf` for kernel-level control.

---

## Services

Disable unused services in System Settings > Sharing and remove unnecessary Login Items.

---

## Siri and Spotlight

Disable Siri Suggestions and limit Spotlight indexing in System Settings for privacy.

---

## Homebrew

Install via [brew.sh](https://brew.sh/) and use for tools like `gpg` or `nmap`.

---

## DNS

### Profiles
Set secure DNS (e.g., Cloudflare: 1.1.1.1) in Network Settings.

### Hosts File
Block domains via `/etc/hosts`.

### DNSCrypt
Install with `brew install dnscrypt-proxy` and configure.

### Dnsmasq
Install with `brew install dnsmasq` and edit `/usr/local/etc/dnsmasq.conf`.

---

## Certificate Authorities

Remove untrusted CAs in Keychain Access > System Roots.

---

## Privoxy

Install (`brew install privoxy`) and configure `/usr/local/etc/privoxy/config` for privacy filtering.

---

## Browser

### Firefox
Enable Enhanced Tracking Protection, DNS over HTTPS, and add uBlock Origin.

### Chrome
Use Safe Browsing, disable telemetry, and add privacy extensions.

### Safari
Enable tracking prevention and consider AdGuard.

### Privacy Tools
Use ClearURLs, Decentraleyes, and Cookie AutoDelete.

---

## Tor

Install [Tor Browser](https://www.torproject.org/) for anonymous browsing.

---

## VPN

Choose a no-logs provider with strong encryption and configure per instructions.

---

## PGP/GPG

Install (`brew install gnupg`), generate keys, and use for email encryption.

---

## Messengers

### XMPP
Use Pidgin with OTR encryption.

### Signal
Install from [signal.org](https://signal.org/) for E2E messaging.

### iMessage
Enable encryption in Messages settings.

---

## Malware Protection

- **Sources**: Download only from trusted sites.
- **Sandbox**: Ensure app sandboxing.
- **Hardened Runtime**: Verify enabled.
- **Antivirus**: Consider Malwarebytes or Sophos.
- **Gatekeeper**: Set to "App Store and identified developers" in Security & Privacy.

---

## System Integrity Protection

Check and enable with `csrutil` in Terminal.

---

## Metadata Management

Install ExifTool (`brew install exiftool`) to strip file metadata.

---

## Passwords

Use a manager like 1Password or Bitwarden to generate strong passwords.

---

## Backup

Enable Time Machine with encryption to a secure location.

---

## Wi-Fi

Use WPA3, change default credentials, and disable WPS.

---

## SSH

Generate keys with `ssh-keygen` and disable password auth in `sshd_config`.

---

## Physical Security

Use a lock, enable screen lock, and add a privacy screen.

---

## System Monitoring

### OpenBSM
Enable with `audit` and review logs.

### DTrace
Use `dtrace` for real-time tracing.

### Execution
Monitor with Activity Monitor or Objective-See tools.

### Network
Use Little Snitch or Wireshark (`brew install wireshark`).

---

## Binary Authorization

Configure with `spctl` to control executable permissions.

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