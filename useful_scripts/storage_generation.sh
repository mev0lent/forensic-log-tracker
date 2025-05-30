#!/bin/bash
set -e  # stop script on any error

# === checking root rights ===
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run this script as root (sudo)."
  exit 1
fi

# === Inputs ===
read -p "Filesize (e.g. 100M): " FILESIZE
read -p "Filesystem (e.g. ext4, fat): " FILESYSTEM
read -p "Filename (e.g. virtual_disk): " FILENAME
read -p "Payload directory (the folder with files you'll feed your newly created filesystem): " PAYLOAD_DIR

# === Ensure payload directory exists ===
if [ ! -d "$PAYLOAD_DIR" ]; then
  echo "[!] Payload directory '$PAYLOAD_DIR' does not exist. Creating it..."
  mkdir -p "$PAYLOAD_DIR"
  echo "[i] Payload directory created. Please add your files before running the script again."
  exit 0
fi

# === Creating empty image from specs ===
echo "[+] Creating empty disk image of size $FILESIZE..." 
DISK_IMAGE="${FILENAME}.img"
dd if=/dev/zero of="$DISK_IMAGE" bs=1M count=$(echo "$FILESIZE" | sed 's/M//') status=progress

# === Creating loop-back-device ===
echo "[+] Attaching to loop device..."
LOOPDEV=$(losetup --find --show "$DISK_IMAGE")
if [ -z "$LOOPDEV" ]; then
  echo "[!] Failed to create loop device."
  exit 1
fi
echo "[+] Attached at $LOOPDEV"

# === Formatting the Filesystem ===
echo "[+] Formatting with $FILESYSTEM..."
mkfs."$FILESYSTEM" "$LOOPDEV"

# === Mounting ===
MOUNT_DIR="./mnt_${FILENAME}"
mkdir -p "$MOUNT_DIR"

echo "[+] Mounting..."
mount "$LOOPDEV" "$MOUNT_DIR"

# === Bringing in data ===
echo "[+] Copying files from $PAYLOAD_DIR to disk image..."
cp -r "$PAYLOAD_DIR"/* "$MOUNT_DIR"/

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
            umount "$MOUNT_DIR"
            losetup -d "$LOOPDEV"
            echo "[+] Done."
            ;;
        2)
            echo "[+] Creating image dump..."
            DUMP_DIR="./dumps"
            mkdir -p "$DUMP_DIR"
            TIMESTAMP=$(date +%Y%m%d_%H%M%S)
            cp "$DISK_IMAGE" "$DUMP_DIR/${FILENAME}_$TIMESTAMP.img"
            echo "[+] Dump saved to $DUMP_DIR/${FILENAME}_$TIMESTAMP.img"
            ;;
        3)
            echo "[+] Checking space..."
            df -h "$MOUNT_DIR"
            ;;
        4)
            echo "[+] Running Foremost..."
            mkdir -p output_foremost
            foremost -i "$DISK_IMAGE" -o output_foremost
            echo "[+] Foremost done. Output in output_foremost/"
            ;;
        5)
            echo "[+] Running Scalpel..."
            mkdir -p output_scalpel
            scalpel -c /etc/scalpel/scalpel.conf -o output_scalpel "$DISK_IMAGE"
            echo "[+] Scalpel done. Output in output_scalpel/"
            ;;
        6)
            echo "[+] Generating SHA256 checksums of payloads..."
            find "$PAYLOAD_DIR" -type f -exec sha256sum {} \; > "checksums_${FILENAME}.txt"
            echo "[+] Checksums saved in checksums_${FILENAME}.txt"
            ;;
        7)
            echo "[✓] Exiting. Have a productive day & drink water!"
            break
            ;;
        *)
            echo "[!] Invalid option. Try again."
            ;;
    esac
done
