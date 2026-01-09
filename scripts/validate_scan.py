#!/usr/bin/env python3
"""
Validate scan results JSON structure and print summary.

This script is called by GitHub Actions after each push to data/.
Exit codes:
  0 = Valid JSON
  1 = Invalid JSON or missing fields
"""
import json
import sys
from pathlib import Path


def load_json(filepath: Path) -> dict:
    """Load and parse JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def validate_structure(data: dict) -> list[str]:
    """
    Validate the scan results structure.

    Returns list of errors (empty if valid).
    """
    errors = []

    # Check required top-level fields
    required_fields = ['scan_timestamp', 'host', 'interface', 'devices_count', 'devices']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Check devices is a list
    if 'devices' in data:
        if not isinstance(data['devices'], list):
            errors.append("'devices' must be a list")
        else:
            # Check each device has required fields
            for i, device in enumerate(data['devices']):
                for field in ['ip', 'mac', 'vendor']:
                    if field not in device:
                        errors.append(f"Device {i} missing field: '{field}'")

    return errors


def print_summary(data: dict) -> None:
    """Print a formatted summary of the scan results."""
    print("=" * 60)
    print("SCAN RESULTS VALIDATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Timestamp:    {data['scan_timestamp']}")
    print(f"Host:         {data['host']}")
    print(f"Interface:    {data['interface']}")
    print(f"Device count: {data['devices_count']}")
    print("-" * 60)
    print("Devices:")
    for device in data['devices']:
        print(f"  {device['ip']:15} {device['mac']}  {device['vendor']}")
    print("=" * 60)


def main() -> int:
    """Main entry point."""
    # Path relative to repo root (where GitHub Actions runs)
    json_path = Path('data/scan_results.json')

    # Load JSON
    try:
        data = load_json(json_path)
    except FileNotFoundError:
        print(f"ERROR: {json_path} not found")
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON - {e}")
        return 1

    # Validate structure
    errors = validate_structure(data)

    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    # Print summary
    print_summary(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
