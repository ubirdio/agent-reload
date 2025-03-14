TAP_DEV="tap0"
TAP_IP="172.16.0.1"
MASK_SHORT="/30"

# Setup network interface
sudo ip link del "$TAP_DEV" 2> /dev/null || true
sudo ip tuntap add dev "$TAP_DEV" mode tap
sudo ip addr add "${TAP_IP}${MASK_SHORT}" dev "$TAP_DEV"
sudo ip link set dev "$TAP_DEV" up

# Enable ip forwarding
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -P FORWARD ACCEPT

# This tries to determine the name of the host network interface to forward
# VM's outbound network traffic through. If outbound traffic doesn't work,
# double check this returns the correct interface!
HOST_IFACE=$(ip -j route list default |jq -r '.[0].dev')

# Set up microVM internet access
sudo iptables -t nat -D POSTROUTING -o "$HOST_IFACE" -j MASQUERADE || true
sudo iptables -t nat -A POSTROUTING -o "$HOST_IFACE" -j MASQUERADE

API_SOCKET="/tmp/firecracker.socket"
LOGFILE="./firecracker.log"

# Create log file
touch $LOGFILE

# Set log file
sudo curl -X PUT --unix-socket "${API_SOCKET}" \
    --data "{
        \"log_path\": \"${LOGFILE}\",
        \"level\": \"Debug\",
        \"show_level\": true,
        \"show_log_origin\": true
    }" \
    "http://localhost/logger"

KERNEL="./$(ls vmlinux* | tail -1)"
KERNEL_BOOT_ARGS="console=ttyS0 reboot=k panic=1 pci=off"

ARCH=$(uname -m)

if [ ${ARCH} = "aarch64" ]; then
    KERNEL_BOOT_ARGS="keep_bootcon ${KERNEL_BOOT_ARGS}"
fi


# # Set machine configuration (adjust memory and vCPUs as needed)
# sudo curl -X PUT --unix-socket "${API_SOCKET}" \
#     --data "{
#         \"vcpu_count\": 2,
#         \"mem_size_mib\": 2048
#     }" \
#     "http://localhost/machine-config"

ROOTFS="./ubuntu-24.04.ext4"

# # Set rootfs
# sudo curl -X PUT --unix-socket "${API_SOCKET}" \
#     --data "{
#         \"drive_id\": \"rootfs\",
#         \"path_on_host\": \"${ROOTFS}\",
#         \"is_root_device\": true,
#         \"is_read_only\": false
#     }" \
#     "http://localhost/drives/rootfs"

# The IP address of a guest is derived from its MAC address with
# `fcnet-setup.sh`, this has been pre-configured in the guest rootfs. It is
# important that `TAP_IP` and `FC_MAC` match this.
FC_MAC="06:00:AC:10:00:02"

# # Set network interface
# sudo curl -X PUT --unix-socket "${API_SOCKET}" \
#     --data "{
#         \"iface_id\": \"net1\",
#         \"guest_mac\": \"$FC_MAC\",
#         \"host_dev_name\": \"$TAP_DEV\"
#     }" \
#     "http://localhost/network-interfaces/net1"

# API requests are handled asynchronously, it is important the configuration is
# set, before `InstanceStart`.
sleep 0.015s

# Load from snapshot
sudo curl --unix-socket "${API_SOCKET}" \
    -X PUT "http://localhost/snapshot/load" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    --data "{
        \"snapshot_path\": \"./snapshot.bin\",
        \"mem_backend\": {
            \"backend_path\": \"./snapshot.mem\",
            \"backend_type\": \"File\"
        },
        \"enable_diff_snapshots\": false,
        \"resume_vm\": true
    }"
