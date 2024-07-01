#!/bin/ksh

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Install Homebrew if not already installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Update Homebrew
brew update

# Install necessary tools via Homebrew
brew install gpg nmap wireshark dnscrypt-proxy privoxy gnupg exiftool little-snitch radio-silence lulu tor knockknock ransomwhere blockblock

# AppleScript to make system tweaks
osascript <<EOF
-- Disable Siri Suggestions
tell application "System Preferences"
    reveal anchor "Siri" of pane id "com.apple.preference.siri"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click checkbox "Enable Ask Siri" of window "Siri"
    end tell
end tell

-- Disable Location Services
tell application "System Preferences"
    reveal anchor "Privacy_LocationServices" of pane id "com.apple.preference.security"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click checkbox "Enable Location Services" of window "Security & Privacy"
    end tell
end tell

-- Disable Sharing Analytics
tell application "System Preferences"
    reveal anchor "Privacy_Analytics" of pane id "com.apple.preference.security"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click checkbox "Share Mac Analytics" of window "Security & Privacy"
    end tell
end tell

-- Enable FileVault
tell application "System Preferences"
    reveal anchor "FileVault" of pane id "com.apple.preference.security"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click button "Turn On FileVault…" of window "Security & Privacy"
    end tell
end tell

-- Enable Firewall
tell application "System Preferences"
    reveal anchor "Firewall" of pane id "com.apple.preference.security"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click button "Turn On Firewall" of window "Security & Privacy"
    end tell
end tell

-- Disable Spotlight Suggestions
tell application "System Preferences"
    reveal anchor "Privacy_Spotlight" of pane id "com.apple.preference.spotlight"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click checkbox "Allow Spotlight Suggestions in Look up" of window "Spotlight"
    end tell
end tell

-- Configure Privacy Settings for Safari
tell application "System Preferences"
    reveal anchor "Privacy" of pane id "com.apple.preference.safari"
    delay 1
    tell application "System Events" to tell process "System Preferences"
        click checkbox "Prevent cross-site tracking" of window "Privacy"
        click checkbox "Block all cookies" of window "Privacy"
    end tell
end tell
EOF

# Set DNS settings
networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1

# Configure dnscrypt-proxy
sudo cp $(brew --prefix)/etc/dnscrypt-proxy/dnscrypt-proxy.toml $(brew --prefix)/etc/dnscrypt-proxy/dnscrypt-proxy.toml.backup
sudo sed -i '' 's/^# server_names = \["scaleway-fr", "google"\]$/server_names = \["cloudflare"\]/' $(brew --prefix)/etc/dnscrypt-proxy/dnscrypt-proxy.toml
sudo brew services start dnscrypt-proxy

# Configure Privoxy
sudo cp $(brew --prefix)/etc/privoxy/config $(brew --prefix)/etc/privoxy/config.backup
echo 'forward-socks5 / 127.0.0.1:9050 .' | sudo tee -a $(brew --prefix)/etc/privoxy/config
sudo brew services start privoxy

# Install Firefox and privacy-focused extensions
brew install --cask firefox
open -a Firefox
osascript <<EOF
tell application "Firefox"
    open location "https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/"
    delay 5
    open location "https://addons.mozilla.org/en-US/firefox/addon/privacy-badger17/"
    delay 5
    open location "https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/"
end tell
EOF

# Set up SSH keys
echo "Setting up SSH keys..."
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Configure SSH
echo "Configuring SSH..."
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
sed -i '' 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemsetup -setremotelogin on
launchctl unload /System/Library/LaunchDaemons/ssh.plist
launchctl load -w /System/Library/LaunchDaemons/ssh.plist

# Install and configure Tor
brew install tor
tor &

# Use Dnscrypt-proxy
brew install dnscrypt-proxy
sudo cp -f /usr/local/etc/dnscrypt-proxy.toml /usr/local/etc/dnscrypt-proxy.toml.orig
sudo cp -f /usr/local/opt/dnscrypt-proxy/*.example /usr/local/etc/dnscrypt-proxy.toml
brew services start dnscrypt-proxy

# Install antivirus
brew install --cask malwarebytes

# Install password manager (Bitwarden)
brew install --cask bitwarden

# Enable System Integrity Protection (SIP)
csrutil enable

# Clean up metadata from files
brew install exiftool
alias strip_metadata='exiftool -all= '

echo "Setup completed. Please review and adjust the settings as needed."

# Reboot to apply some of the changes
echo "Rebooting the system to apply changes..."
reboot
