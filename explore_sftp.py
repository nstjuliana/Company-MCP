#!/usr/bin/env python3
"""
Comprehensive SFTP exploration script to find synthetic_250 files.
"""
import paramiko
import os
from pathlib import Path

SFTP_HOST = "localhost"
SFTP_PORT = 2222
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")

def get_sftp_client():
    """Create SFTP connection."""
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        return paramiko.SFTPClient.from_transport(transport), transport
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None, None

def explore_recursive(sftp, path, max_depth=10, current_depth=0, indent=""):
    """Recursively explore directory structure."""
    if current_depth > max_depth:
        return
    
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            item_path = f"{path}/{item.filename}".replace("//", "/")
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            # Check for synthetic files
            if 'synthetic' in item.filename.lower() or '250' in item.filename:
                marker = "⭐" * 3
                print(f"{indent}{marker} FOUND: {item_path} ({'DIR' if is_dir else 'FILE'})")
            
            # Recursively explore directories
            if is_dir and item.filename not in ['.', '..']:
                explore_recursive(sftp, item_path, max_depth, current_depth + 1, indent + "  ")
    except Exception as e:
        pass

def main():
    print("=" * 70)
    print("Comprehensive SFTP Exploration")
    print("=" * 70)
    
    # Close any existing connections
    print("\n[Step 1] Closing any existing connections...")
    # (Nothing to close initially)
    
    print("\n[Step 2] Connecting to SFTP server...")
    sftp, transport = get_sftp_client()
    if not sftp:
        print("❌ Failed to connect")
        return
    
    print("✓ Connected")
    
    try:
        # Get current working directory
        try:
            cwd = sftp.getcwd()
            print(f"\nCurrent working directory: {cwd}")
        except:
            print("\nCould not get CWD (may be chrooted)")
        
        # List root
        print("\n[Step 3] Exploring root directory...")
        try:
            items = sftp.listdir_attr("/")
            print(f"Root (/) contains {len(items)} items:")
            for item in items[:20]:
                item_type = "DIR" if (item.st_mode & 0o40000) else "FILE"
                print(f"  [{item_type}] {item.filename}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Check /data
        print("\n[Step 4] Exploring /data directory...")
        try:
            items = sftp.listdir_attr("/data")
            print(f"/data contains {len(items)} items:")
            for item in items:
                item_type = "DIR" if (item.st_mode & 0o40000) else "FILE"
                print(f"  [{item_type}] {item.filename}")
            
            # Recursively explore /data
            if items:
                print("\n[Step 5] Recursively searching /data for synthetic files...")
                explore_recursive(sftp, "/data", max_depth=15)
        except Exception as e:
            print(f"  Error accessing /data: {e}")
        
        # Try to change directory
        print("\n[Step 6] Trying to change directory...")
        for test_path in ["/data", ".", "/", "/home/datauser/data"]:
            try:
                sftp.chdir(test_path)
                print(f"✓ Successfully changed to: {test_path}")
                items = sftp.listdir_attr(".")
                print(f"  Contains {len(items)} items")
                for item in items[:10]:
                    if 'synthetic' in item.filename.lower() or '250' in item.filename:
                        print(f"    ⭐ {item.filename}")
                break
            except Exception as e:
                print(f"  Could not chdir to {test_path}: {e}")
        
    finally:
        print("\n[Step 7] Closing connection...")
        sftp.close()
        transport.close()
        print("✓ Connection closed")
        
        # Reconnect
        print("\n[Step 8] Reconnecting...")
        import time
        time.sleep(1)
        sftp2, transport2 = get_sftp_client()
        if sftp2:
            print("✓ Reconnected")
            try:
                items = sftp2.listdir_attr("/data")
                print(f"\nAfter reconnect, /data contains {len(items)} items")
                if items:
                    for item in items:
                        if 'synthetic' in item.filename.lower() or '250' in item.filename:
                            print(f"  ⭐ FOUND: {item.filename}")
            except:
                pass
            sftp2.close()
            transport2.close()

if __name__ == "__main__":
    main()
