set -e

API_SOCKET="/tmp/firecracker.socket"

# Pause
sudo curl --unix-socket "${API_SOCKET}" \
    -X PATCH "http://localhost/vm" \
    --data "{
        \"state\": \"Paused\"
    }"

# Snapshot
sudo curl --unix-socket "${API_SOCKET}" \
    -X PUT "http://localhost/snapshot/create" \
    --data '{
        "snapshot_type": "Full",
        "snapshot_path": "snapshot.bin",
        "mem_file_path": "snapshot.mem"
    }'

# Resume
sudo curl --unix-socket "${API_SOCKET}" \
    -X PATCH "http://localhost/vm" \
    --data "{
        \"state\": \"Resumed\"
    }"
