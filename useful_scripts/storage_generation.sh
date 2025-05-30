#!/bin/bash

# === Inputs ===
read -p "Filesitze (e.g. 100Mb): " FILESIZE
read -p "Filesystem (e.g. ext4): " FILESYSTEM
read -p "Filename (e.g. virtual_disk): " FILENAME
read -p "Payload directory (the folder with files you'll feed your newly created filesystem): " PAYLOAD_DIR

# === Creating empty image from specs ===
echo "[+] Creating empty disk image of size $FILESIZE..."
DISK_IMAGE="${FILENAME}.img"
dd if=/dev/zero of=${FILENAME}.img bs=1M count=$(echo $FILESIZE | sed 's/M//') status=progress

# === Creating loop-back-device ===
echo "[+] Attaching to loop device..."
LOOPDEV=$(losetup --find --show $DISK_IMAGE)
echo "[+] Attached at $LOOPDEV"

# === Formatting the Filesystem ===
echo "[+] Formatting with $FILESYSTEM..."
mkfs.$FILESYSTEM $LOOPDEV

# === Mounting ===
MOUNT_DIR="./mnt_${FILENAME}"
mkdir -p $MOUNT_DIR

echo "[+] Mounting..."
mount $LOOPDEV $MOUNT_DIR

# === Bringing in data ===
echo "[+] Copying files from $PAYLOAD_DIR to disk image..."
cp -r $PAYLOAD_DIR/* $MOUNT_DIR/

# === Interactive menu after setup stage ===
while true; do
        echo ""
        echo "=== MENU ==="
        echo "1) Unmount and detach disk"
        echo "2) Create dump/backup of image"
        echo "3) Check remaining space on mounted image"
        echo "4) Run Foremost"
        echo "5) Run Scalpel"
        echo "6) Generate SHA256 checksums of payload"
        echo "7) Exit"
        echo "==========="
        read -p "Choose an option: " option

        case $option in
                1)
                        echo "[+] Unmounting and detaching..."
                        sync
                        umount $MOUNT_DIR
                        losetup -d $LOOPDEV
                        echo "[+] Done."
                        ;;
                2)
                        echo "[+] Creating image dump.."
                        DUMP_DIR="./dumps"
                        mkdir -p $DUMP_DIR
                        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                        cp ${FILENAME}.img $DUMP_DIR/${FILENAME}_$TIMESTAMP.img
                        echo "[+] Dump saved to $DUMP_DIR/${FILENAME}_$TIMESTAMP.img"
                        ;;
                3)
                        echo "[+] Checking space..."
                        df -h $MOUNT_DIR
                        ;;
                4)
                        echo "[+] Running Foremost..."
                        mkdir -p output_foremost
                        foremost -i ${FILENAME}.img -o output_foremost
                        echo "[+] Foremost done. Output in output_foremost/"
                        ;;
                5)
                        echo "[+] Running Scalpel..."
                        mkdir -p output_scalpel
                        scalpel -c /etc/scalpel/scalpel.conf -o output_scalpel ${FILENAME}.img
                        echo "[+] Scalpel done. Output in output_scalpel/"
                        ;;
                6)
                        echo "[+] Generating SHA256 checksums of payloads..."
                        find $PAYLOAD_DIR -type f -exec sha256sum {} \; > checksums_${FILENAME}.txt
                        echo "[+] Checksums saved in checksums_${FILENAME}.txt"
                        ;;
                7)
                        echo "Have a nice day! Dring some water!"
                        break
                        ;;
        esac
done