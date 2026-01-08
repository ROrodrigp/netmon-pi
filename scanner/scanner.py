#!/usr/bin/env python3
"""
Network scanner using arp-scan.
Detects devices on the local network and saves results to JSON.
"""
import json
import re
import socket
import subprocess
import sys
from datetime import datetime

from config import (
    DATA_DIR,
    NETWORK_INTERFACE,
    SCAN_RESULTS_FILE,
    TIMESTAMP_FORMAT,
)


def get_hostname() -> str:
    """Get the hostname of this machine."""
    return socket.gethostname()


def run_arp_scan(interface: str | None = None) -> tuple[str, str]:
    """
    Execute arp-scan and return the output.

    Args:
        interface: Network interface to scan (None for auto-detect)

    Returns:
        Tuple of (stdout, interface_used)

    Raises:
        RuntimeError: If arp-scan fails
    """
    cmd = ["sudo", "arp-scan", "--localnet"]

    if interface:
        cmd.extend(["--interface", interface])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"arp-scan failed: {e.stderr}") from e
    except FileNotFoundError:
        raise RuntimeError("arp-scan not found. Install with: sudo apt install arp-scan")

    # Extract interface from output
    interface_match = re.search(r"Interface: (\w+)", result.stdout)
    interface_used = interface_match.group(1) if interface_match else "unknown"

    return result.stdout, interface_used


def parse_arp_output(output: str) -> list[dict]:
    """
    Parse arp-scan output and extract device information.

    Args:
        output: Raw output from arp-scan

    Returns:
        List of unique device dictionaries with ip, mac, and vendor
    """
    seen = {}  # Key: (ip, mac) -> device dict

    # arp-scan output format: IP\tMAC\tVendor
    # Example: 192.168.1.1\taa:bb:cc:dd:ee:ff\tNETGEAR
    pattern = re.compile(
        r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+"  # IP address
        r"([0-9a-fA-F:]{17})\s+"                      # MAC address
        r"(.+)$",                                      # Vendor
        re.MULTILINE
    )

    for match in pattern.finditer(output):
        ip = match.group(1)
        mac = match.group(2).lower()
        vendor_raw = match.group(3).strip()

        # Skip duplicate entries (arp-scan marks them as "DUP: N")
        if "(DUP:" in vendor_raw:
            continue

        # Clean vendor string: remove tabs and extra parenthetical MAC addresses
        vendor = re.sub(r"\t", " ", vendor_raw)  # Replace tabs with spaces
        vendor = re.sub(r"\([0-9a-fA-F:]{17}\)", "", vendor)  # Remove MAC in parens
        vendor = re.sub(r"\s+", " ", vendor).strip()  # Normalize whitespace

        key = (ip, mac)
        if key not in seen:
            seen[key] = {
                "ip": ip,
                "mac": mac,
                "vendor": vendor,
            }

    # Convert to list and sort by IP address
    devices = list(seen.values())
    devices.sort(key=lambda d: tuple(map(int, d["ip"].split("."))))

    return devices


def save_results(devices: list[dict], interface: str) -> dict:
    """
    Save scan results to JSON file.

    Args:
        devices: List of detected devices
        interface: Network interface used for scanning

    Returns:
        The complete results dictionary
    """
    results = {
        "scan_timestamp": datetime.now().strftime(TIMESTAMP_FORMAT),
        "host": get_hostname(),
        "interface": interface,
        "devices_count": len(devices),
        "devices": devices,
    }

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(SCAN_RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    return results


def main() -> int:
    """Main entry point."""
    print(f"Starting network scan at {datetime.now().strftime(TIMESTAMP_FORMAT)}")

    try:
        # Run scan
        print("Running arp-scan...")
        output, interface = run_arp_scan(NETWORK_INTERFACE)

        # Parse results
        devices = parse_arp_output(output)
        print(f"Found {len(devices)} devices on interface {interface}")

        # Save results
        results = save_results(devices, interface)
        print(f"Results saved to {SCAN_RESULTS_FILE}")

        # Print summary
        print("\nDevices found:")
        for device in devices:
            print(f"  {device['ip']:15} {device['mac']}  {device['vendor']}")

        return 0

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except PermissionError:
        print("Error: Permission denied. Run with sudo.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
