#!/bin/bash

# Disable telemetry (diagnostic reports)
echo "Disabling diagnostic reports..."
sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmit -bool false
sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmitVersion -int 0

# Disable Siri analytics
echo "Disabling Siri analytics..."
defaults write com.apple.assistant.analytics "AnalyticsEnabled" -bool false

# Configure Safari privacy settings
echo "Configuring Safari privacy settings..."
defaults write com.apple.Safari UniversalSearchEnabled -bool false
defaults write com.apple.Safari SuppressSearchSuggestions -bool true

# Disable remote login (SSH)
echo "Disabling remote login (SSH)..."
sudo systemsetup -setremotelogin off

# Disable remote management
echo "Disabling remote management..."
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -deactivate -stop

# Disable mDNS multicast advertisements (Bonjour)
echo "Disabling mDNS multicast advertisements..."
sudo defaults write /System/Library/LaunchDaemons/com.apple.mDNSResponder.plist ProgramArguments -array-add "-NoMulticastAdvertisements"

# Verify mDNS setting
echo "Verifying mDNS setting..."
if sudo cat /System/Library/LaunchDaemons/com.apple.mDNSResponder.plist | grep -q "NoMulticastAdvertisements"; then
    echo "mDNS multicast advertisements disabled successfully!"
else
    echo "Error: Failed to disable mDNS multicast advertisements."
    exit 1
fi

# Verify a setting (example: Safari search suggestions)
echo "Verifying Safari privacy settings..."
if defaults read com.apple.Safari SuppressSearchSuggestions | grep -q "1"; then
    echo "Safari privacy settings applied successfully!"
else
    echo "Error: Failed to apply Safari privacy settings."
    exit 1
fi