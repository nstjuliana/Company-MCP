#!/usr/bin/env python3
"""
Download synthetic_250_postgres and synthetic_250_snowflake files/directories from SFTP
to the sftp-markdown-files directory.
"""
import os
import paramiko
from pathlib import Path

# SFTP Configuration
SFTP_HOST = "localhost"
SFTP_PORT = 2222
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")
# SFTP server is chrooted to /home/datauser/data, which appears as /data
# But we should also check the actual mount point
SFTP_BASE_PATHS = ["/data", "/home/datauser/data", "."]

# Output directory
OUTPUT_DIR = Path(__file__).parent / "sftp-markdown-files"
OUTPUT_DIR.mkdir(exist_ok=True)

# Files/directories to download
TARGET_FILES = [
    "synthetic_250_postgres",
    "synthetic_250_snowflake"
]

def get_sftp_client():
    """Create SFTP connection."""
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        return paramiko.SFTPClient.from_transport(transport), transport
    except Exception as e:
        print(f"Failed to connect to SFTP: {e}")
        return None, None

def find_target_paths(sftp, path="/data", found_paths=None, max_depth=10, current_depth=0):
    """Recursively find target files/directories."""
    if found_paths is None:
        found_paths = []
    
    if current_depth > max_depth:
        return found_paths
    
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            item_path = f"{path}/{item.filename}".replace("//", "/")
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            # Check if this matches any target (case-insensitive, partial match)
            item_lower = item.filename.lower()
            for target in TARGET_FILES:
                if target.lower() in item_lower or item_lower in target.lower():
                    found_paths.append({
                        "path": item_path,
                        "name": item.filename,
                        "is_dir": is_dir
                    })
                    print(f"  Found match: {item_path}")
            
            # Recursively search directories
            if is_dir:
                if item.filename in ['.', '..', '.git', '__pycache__', 'node_modules']:
                    continue
                find_target_paths(sftp, item_path, found_paths, max_depth, current_depth + 1)
    except PermissionError:
        pass  # Skip permission errors
    except Exception as e:
        print(f"  Warning: Could not access {path}: {e}")
    
    return found_paths

def download_file_from_sftp(sftp, remote_path, local_path):
    """Download a file from SFTP."""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        sftp.get(remote_path, str(local_path))
        return True
    except Exception as e:
        print(f"  Error downloading {remote_path}: {e}")
        return False

def download_directory_from_sftp(sftp, remote_path, local_path, max_depth=20, current_depth=0):
    """Recursively download a directory from SFTP."""
    if current_depth > max_depth:
        return
    
    try:
        items = sftp.listdir_attr(remote_path)
        local_path.mkdir(parents=True, exist_ok=True)
        
        for item in items:
            item_remote_path = f"{remote_path}/{item.filename}".replace("//", "/")
            item_local_path = local_path / item.filename
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            if is_dir:
                if item.filename in ['.', '..']:
                    continue
                download_directory_from_sftp(sftp, item_remote_path, item_local_path, max_depth, current_depth + 1)
            else:
                if download_file_from_sftp(sftp, item_remote_path, item_local_path):
                    print(f"    ✓ {item_remote_path.replace(SFTP_BASE_PATH, '').lstrip('/')}")
    except Exception as e:
        print(f"  Error downloading directory {remote_path}: {e}")

def main():
    print("=" * 60)
    print("Downloading synthetic_250_postgres and synthetic_250_snowflake")
    print("=" * 60)
    
    # Connect to SFTP (first attempt)
    print("\n[Attempt 1] Connecting to SFTP server...")
    sftp, transport = get_sftp_client()
    if not sftp:
        print("❌ Could not connect to SFTP server")
        print("\nPlease ensure:")
        print("  1. Docker is running")
        print("  2. SFTP server is running: docker-compose up -d sftp-server")
        print("  3. SFTP server is accessible on port 2222")
        return
    
    print("✓ Connected to SFTP server")
    
    # Close connection
    sftp.close()
    transport.close()
    print("  Closed connection")
    
    # Wait a moment
    import time
    time.sleep(1)
    
    # Reconnect to SFTP (fresh connection)
    print("\n[Attempt 2] Reconnecting to SFTP server...")
    sftp, transport = get_sftp_client()
    if not sftp:
        print("❌ Could not reconnect to SFTP server")
        return
    
    print("✓ Reconnected to SFTP server")
    
    try:
        # Find target files/directories - search all possible base paths
        all_found_paths = []
        for base_path in SFTP_BASE_PATHS:
            print(f"\nSearching for target files in {base_path}...")
            try:
                # Test if path exists
                sftp.listdir_attr(base_path)
                found = find_target_paths(sftp, base_path)
                if found:
                    all_found_paths.extend(found)
                    print(f"  Found {len(found)} matches in {base_path}")
            except Exception as e:
                print(f"  Path {base_path} not accessible: {e}")
        
        found_paths = all_found_paths
        # Remove duplicates
        seen = set()
        unique_paths = []
        for path_info in found_paths:
            path_key = path_info["path"]
            if path_key not in seen:
                seen.add(path_key)
                unique_paths.append(path_info)
        found_paths = unique_paths
        
        if not found_paths:
            print("⚠️  No matching files/directories found")
            print(f"\nSearched for: {', '.join(TARGET_FILES)}")
            print("\nListing available files for reference:")
            # Try all base paths
            for base_path in SFTP_BASE_PATHS:
                try:
                    items = sftp.listdir_attr(base_path)
                    print(f"\n{base_path}: Found {len(items)} items")
                    for item in items[:30]:
                        item_type = "DIR" if (item.st_mode & 0o40000) else "FILE"
                        size = f" ({item.st_size} bytes)" if not (item.st_mode & 0o40000) else ""
                        print(f"  [{item_type}] {item.filename}{size}")
                    if len(items) > 30:
                        print(f"  ... and {len(items) - 30} more items")
                    
                    # Also check subdirectories
                    print(f"\nChecking subdirectories in {base_path}...")
                    for item in items:
                        if item.st_mode is not None and (item.st_mode & 0o40000):
                            item_path = f"{base_path}/{item.filename}".replace("//", "/")
                            try:
                                sub_items = sftp.listdir_attr(item_path)
                                print(f"  {item.filename}/ ({len(sub_items)} items)")
                                for sub_item in sub_items[:10]:
                                    sub_type = "DIR" if (sub_item.st_mode & 0o40000) else "FILE"
                                    if 'synthetic' in sub_item.filename.lower() or '250' in sub_item.filename:
                                        print(f"    → [{sub_type}] {sub_item.filename} ⭐")
                            except:
                                pass
                    break  # Found a working path, no need to check others
                except Exception as e:
                    print(f"  {base_path}: Error - {e}")
                    continue
            return
        
        print(f"✓ Found {len(found_paths)} matching path(s)")
        
        # Download each found path
        downloaded_count = 0
        for found in found_paths:
            remote_path = found["path"]
            name = found["name"]
            is_dir = found["is_dir"]
            
            print(f"\nDownloading: {name} ({'DIRECTORY' if is_dir else 'FILE'})")
            print(f"  Remote: {remote_path}")
            
            # Create local path - handle different base paths
            relative_path = remote_path
            for base_path in SFTP_BASE_PATHS:
                if remote_path.startswith(base_path):
                    relative_path = remote_path.replace(base_path, "").lstrip("/")
                    break
            local_path = OUTPUT_DIR / relative_path
            
            if is_dir:
                print(f"  Local: {local_path}/")
                download_directory_from_sftp(sftp, remote_path, local_path)
                downloaded_count += 1
            else:
                print(f"  Local: {local_path}")
                if download_file_from_sftp(sftp, remote_path, local_path):
                    downloaded_count += 1
                    print(f"    ✓ {relative_path}")
        
        # Summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Found: {len(found_paths)} path(s)")
        print(f"Downloaded: {downloaded_count} path(s)")
        print(f"Output directory: {OUTPUT_DIR}")
        
    finally:
        sftp.close()
        transport.close()

if __name__ == "__main__":
    main()
