#!/bin/bash
set -e

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --interface)
      INTERFACE="$2"; shift 2;;
    --filter)
      FILTER="$2"; shift 2;;
    --idle-timeout)
      IDLE_TIMEOUT="$2"; shift 2;;
    *) shift;;
  esac
done

PCAP_DIR="/mnt/data/pcap"
mkdir -p "$PCAP_DIR"
PCAP_FILE="$PCAP_DIR/capture-$(date +%F-%H%M%S).pcap"

CMD="tcpdump -i $INTERFACE $FILTER -w $PCAP_FILE"

echo "Starting packet capture: $CMD"
$CMD &
TCPDUMP_PID=$!

echo "Packet capture started. Press Enter to stop..."
read -r
kill $TCPDUMP_PID
wait $TCPDUMP_PID 2>/dev/null

echo "Capture saved to $PCAP_FILE"
