#!/bin/bash
# Fix permissions on mounted data directory for SFTP user
# This script is run by atmoz/sftp from /etc/sftp.d/ on startup

DATA_DIR="/home/${SFTP_USER:-datauser}/data"
SFTP_UID="${SFTP_UID:-1001}"
SFTP_GID="${SFTP_GID:-1001}"

# Ensure the data directory exists and is writable by the SFTP user
if [ -d "$DATA_DIR" ]; then
    chown "${SFTP_UID}:${SFTP_GID}" "$DATA_DIR"
    chmod 755 "$DATA_DIR"
    echo "[sftp-init] Fixed permissions on $DATA_DIR for uid:gid ${SFTP_UID}:${SFTP_GID}"
fi
