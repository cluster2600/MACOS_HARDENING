#!/bin/bash

# Check for required tools
if ! command -v curl &> /dev/null; then
    echo "Error: curl is required but not installed."
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Install it with 'brew install jq' on macOS."
    exit 1
fi

# GitHub Security Advisories API endpoint
API_URL="https://api.github.com/advisories"

# Optional: Use a GitHub token for authenticated requests (uncomment and set your token)
# GITHUB_TOKEN="your_token_here"
# AUTH_HEADER="Authorization: Bearer $GITHUB_TOKEN"
# CURL_AUTH="-H \"$AUTH_HEADER\""

# Fetch advisories (limit to recent ones with 'since' parameter if needed)
echo "Fetching recent CVE advisories from GitHub Security Advisories API..."
response=$(curl -s -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" $CURL_AUTH "$API_URL")

# Check if the API request was successful
if echo "$response" | grep -q "message"; then
    echo "Error: Failed to fetch advisories. API response: $(echo "$response" | jq -r '.message')"
    exit 1
fi

# Filter advisories for macOS-related vulnerabilities
echo "Filtering for macOS-related advisories..."
macos_advisories=$(echo "$response" | jq -r '
    .[] | select(
        (.description | test("macOS|Apple|Safari"; "i")) or
        (.vulnerabilities[].package.ecosystem | test("Swift"; "i"))
    ) | 
    "CVE ID: \(.cve_id)\nSummary: \(.summary)\nSeverity: \(.severity)\nDescription: \(.description)\nAffected Ecosystem: \(.vulnerabilities[].package.ecosystem)\nAffected Package: \(.vulnerabilities[].package.name)\nVulnerable Versions: \(.vulnerabilities[].vulnerable_version_range)\nFirst Patched Version: \(.vulnerabilities[].first_patched_version // "Not specified")\nPublished: \(.published_at)\n---"
')

# Display results
if [ -z "$macos_advisories" ]; then
    echo "No recent macOS-related advisories found."
else
    echo -e "Found macOS-related advisories:\n"
    echo "$macos_advisories"
fi