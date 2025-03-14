ARCH="$(uname -m)"

latest=$(wget "http://spec.ccfc.min.s3.amazonaws.com/?prefix=firecracker-ci/v1.11/$ARCH/vmlinux-5.10&list-type=2" -O - 2>/dev/null | grep -oP "(?<=<Key>)(firecracker-ci/v1.11/$ARCH/vmlinux-5\.10\.[0-9]{1,3})(?=</Key>)")

# Download a linux kernel binary
wget "https://s3.amazonaws.com/spec.ccfc.min/${latest}"

# Download a rootfs
wget -O ubuntu-24.04.squashfs.upstream "https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.11/${ARCH}/ubuntu-24.04.squashfs"
