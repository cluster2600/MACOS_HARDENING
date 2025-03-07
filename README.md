      .e$$$$e.
    e$$$$$$$$$$e
   $$$$$$$$$$$$$$
  d$$$$$$$$$$$$$$b
  $$$$$$$$$$$$$$$$
 4$$$$$$$$$$$$$$$$F
 4$$$$$$$$$$$$$$$$F
  $$$" "$$$$" "$$$
  $$F   4$$F   4$$
  '$F   4$$F   4$"
   $$   $$$$   $P
   4$$$$$"^$$$$$%
    $$$$F  4$$$$
     "$$$ee$$$"
     . *$$$$F4
      $     .$
      "$$$$$$"
       ^$$$$
  4$$c       ""       .$$r
  ^$$$b              e$$$"
  d$$$$$e          z$$$$$b
 4$$$$$$$$c    .$$$$$$r
  ""    ^*$be$$$*"    ^"
           "$$$$"
         .d$$P$$$b
        d$$P   ^$$$b
    .ed$$$"      "$$$be.
  $$$$P          *$$$$
 4$$$$$P            $$$$"
  "*$"            ^$$P
     ""              ^"

# Albator - macOS 15 Hardening Tool  
A series of scripts to harden macOS 15 (Sequoia) for security and privacy, inspired by NIST guidelines. Suitable for power users and novices alike.  

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

## Features  
- Modular scripts for targeted hardening (firewall, privacy, encryption, app security)  
- NIST-inspired security standards  
- Disables unnecessary services (remote login, remote management, mDNS multicast)  
- CVE advisory fetching to keep users informed about potential vulnerabilities  
- Cross-referencing with Apple’s security updates for a comprehensive view of macOS vulnerabilities  

## Notes and Limitations  
- Some changes (e.g., FileVault) may require a system restart.  
- Always back up your system before applying hardening scripts.  
- CVE and Apple updates fetching require an internet connection.  
- Disabling mDNS multicast may require temporarily disabling System Integrity Protection (SIP) on some systems. To do this, reboot into Recovery Mode, run `csrutil disable`, apply the changes, then re-enable SIP with `csrutil enable`.  
- The Apple security updates script provides links to detailed pages where CVEs and vulnerability details are listed. Future enhancements could include scraping these details directly.  

## Contributing  
Feel free to submit issues or pull requests to improve Albator!  