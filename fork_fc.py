# /// script
# dependencies = [
#  "requests-unixsocket"
# ]
# ///

import requests_unixsocket
import json

# The Firecracker API listens on a Unix socket.
# The "http+unix" URL encodes the path; here /tmp/firecracker.sock becomes %2Ftmp%2Ffirecracker.sock.
FC_SOCKET = "http+unix://%2Ftmp%2Ffirecracker.socket"

def pause_vm():
    url = f"{FC_SOCKET}/vm"
    data = {"state": "Paused"}
    resp = requests_unixsocket.patch(url, json=data)
    if resp.status_code == 204:
        print("VM paused successfully.")
    else:
        print(f"Failed to pause VM: {resp.status_code} {resp.text}")

def create_snapshot(snapshot_path, mem_file_path):
    url = f"{FC_SOCKET}/snapshot/create"
    data = {
        "snapshot_type": "Full",
        "snapshot_path": snapshot_path,
        "mem_file_path": mem_file_path,
    }
    resp = requests_unixsocket.put(url, json=data)
    if resp.status_code == 204:
        print("Snapshot created successfully.")
    else:
        print(f"Snapshot creation failed: {resp.status_code} {resp.text}")

def resume_vm():
    url = f"{FC_SOCKET}/vm"
    data = {"state": "Resumed"}
    resp = requests_unixsocket.patch(url, json=data)
    if resp.status_code == 204:
        print("VM resumed successfully.")
    else:
        print(f"Failed to resume VM: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    # Step 1: Pause the VM (e.g. when your Python script hits a breakpoint)
    pause_vm()

    # Step 2: Create a snapshot of the VM's state
    # This will write two files: a snapshot (e.g. snapshot.bin) and a memory file (e.g. snapshot.mem)
    create_snapshot(snapshot_path="snapshot.bin", mem_file_path="snapshot.mem")

    # At this point you could load this snapshot into a new Firecracker instance to branch execution

    # (Optional) Resume the current VM if desired
    resume_vm()
