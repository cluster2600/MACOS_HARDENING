#!/bin/bash

# Help function to display usage
function show_help() {
    echo "Usage: ./albator.sh [options]"
    echo "Options:"
    echo "  -f, --firewall      Enable and configure the firewall"
    echo "  -p, --privacy       Adjust privacy settings"
    echo "  -e, --encryption    Enable FileVault encryption"
    echo "  -s, --app-security   Enable Gatekeeper and verify Hardened Runtime"
    echo "  -c, --cve          Fetch recent CVE advisories"
    echo "  -a, --apple         Fetch Apple security updates"
    echo "  -h, --help          Display this help message"
}

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -f|--firewall) ./firewall.sh ;;
        -p|--privacy) ./privacy.sh ;;
        -e|--encryption) ./encryption.sh ;;
        -s|--app-security) ./app_security.sh ;;
        -c|--cve) ./cve_fetch.sh ;;
        -a|--apple) ./apple_updates.sh ;;
        -g|--generate) python3 generate_guidance.py ;;
    -p|--privacy) ./privacy.sh ;;
    -a|--apple) ./apple_updates.sh ;;
    -c|--cve) ./cve_fetch.sh ;;
    -e|--encryption) ./encryption.sh ;;
    -s|--app-security) ./app_security.sh ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
    shift
done

echo "No options provided. Use -h or --help for usage information."
