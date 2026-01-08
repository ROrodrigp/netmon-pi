"""
Configuration for the network scanner.
"""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCAN_RESULTS_FILE = DATA_DIR / "scan_results.json"

# Scanner settings
NETWORK_INTERFACE = None  # None = auto-detect, or specify like "wlan0", "eth0"

# Timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Git settings
AUTO_PUSH = True  # Push to GitHub after each scan
