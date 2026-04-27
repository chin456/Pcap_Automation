#!/bin/bash
set -e

# Configurable variables
CONFIG_TARGET=${CONFIG_TARGET:-"udm"} # udm, udr, etc.
CAPTURE_FILTER=${CAPTURE_FILTER:-""}  # e.g., host 10.128.12.0/24
INTERFACE=${INTERFACE:-"any"}
IDLE_TIMEOUT=${IDLE_TIMEOUT:-0} # 0 means manual stop

# 1. Update config
python3 config-updater.py --target "$CONFIG_TARGET"

# 2. Start packet capture
./pcap-capture.sh --interface "$INTERFACE" --filter "$CAPTURE_FILTER" --idle-timeout "$IDLE_TIMEOUT"
