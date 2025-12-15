#!/usr/bin/env python3
"""
Temporary script to download all markdown files from SFTP.
This script will be deleted after use.
"""
import os
import paramiko
from pathlib import Path

# SFTP Configuration
SFTP_HOSTS = [
    ("localhost", 2222),  # From host machine
    ("sftp-server", 22),  # From within docker network
]
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")
SFTP_BASE_PATH = "/data"

# Output directory
OUTPUT_DIR = Path(__file__).parent / "sftp-markdown-files"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_sftp_client(host, port):
    """Create SFTP connection."""
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        return paramiko.SFTPClient.from_transport(transport), transport
    except Exception as e:
        print(f"Failed to connect to {host}:{port} - {e}")
        return None, None

def find_markdown_files(sftp, path="/data", found_files=None, max_depth=20, current_depth=0):
    """Recursively find all .md files."""
    if found_files is None:
        found_files = []
    
    if current_depth > max_depth:
        return found_files
    
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            item_path = f"{path}/{item.filename}".replace("//", "/")
            
            # Check if it's a directory
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            if is_dir:
                # Skip common system directories
                if item.filename in ['.', '..', '.git', '__pycache__', 'node_modules']:
                    continue
                # Recursively search directories
                print(f"  Searching in: {item_path}")
                find_markdown_files(sftp, item_path, found_files, max_depth, current_depth + 1)
            elif item.filename.endswith('.md'):
                found_files.append(item_path)
                print(f"  ✓ Found: {item_path}")
    except PermissionError as e:
        print(f"  Permission denied: {path}")
    except Exception as e:
        print(f"  Error accessing {path}: {e}")
    
    return found_files

def download_file(sftp, remote_path, local_path):
    """Download a file from SFTP."""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        sftp.get(remote_path, str(local_path))
        return True
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")
        return False

def main():
    import time
    import subprocess
    
    # Check if Docker is running
    print("Checking Docker status...")
    docker_ready = False
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
        docker_ready = result.returncode == 0
    except:
        docker_ready = False
    
    if not docker_ready:
        print("⚠️  Docker is not running. Starting SFTP server...")
        print("   (If this fails, please start Docker Desktop manually)")
        try:
            subprocess.run(["docker-compose", "up", "-d", "sftp-server"], 
                         cwd=Path(__file__).parent, timeout=30)
            print("   Waiting for SFTP server to start...")
            time.sleep(5)
        except Exception as e:
            print(f"   Could not start Docker containers: {e}")
            print("\nPlease:")
            print("  1. Start Docker Desktop")
            print("  2. Run: docker-compose up -d sftp-server")
            print("  3. Run this script again")
            return
    
    print("Connecting to SFTP server...")
    
    sftp = None
    transport = None
    
    # Try to connect to any available SFTP server
    for host, port in SFTP_HOSTS:
        print(f"Trying {host}:{port}...")
        sftp, transport = get_sftp_client(host, port)
        if sftp:
            print(f"✓ Connected to {host}:{port}")
            break
    
    if not sftp:
        print("\n❌ ERROR: Could not connect to SFTP server.")
        print("\nPlease ensure:")
        print("  1. Docker Desktop is running")
        print("  2. Run: docker-compose up -d sftp-server")
        print("  3. SFTP server is accessible on port 2222")
        print("  4. SFTP credentials are correct")
        return
    
    try:
        # First, let's see what's in the directory
        print(f"\nListing contents of {SFTP_BASE_PATH}...")
        try:
            items = sftp.listdir_attr(SFTP_BASE_PATH)
            print(f"Found {len(items)} items:")
            for item in items[:20]:  # Show first 20
                item_type = "DIR" if (item.st_mode & 0o40000) else "FILE"
                print(f"  [{item_type}] {item.filename}")
            if len(items) > 20:
                print(f"  ... and {len(items) - 20} more items")
        except Exception as e:
            print(f"Error listing directory: {e}")
        
        # Explore the entire SFTP filesystem to find markdown files
        print(f"\nExploring SFTP filesystem structure...")
        
        # Try to get the current working directory
        try:
            cwd = sftp.getcwd()
            print(f"Current working directory: {cwd}")
        except:
            print("Could not get current directory")
        
        # List root directory
        print("\nExploring root directory (/):")
        try:
            root_items = sftp.listdir_attr("/")
            for item in root_items:
                item_type = "DIR" if (item.st_mode & 0o40000) else "FILE"
                print(f"  [{item_type}] /{item.filename}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Also check the home directory and other common locations
        search_paths = [SFTP_BASE_PATH]
        
        # Try to find any directories that might contain data
        try:
            root_items = sftp.listdir_attr("/")
            for item in root_items:
                if item.st_mode is not None and (item.st_mode & 0o40000):
                    search_paths.append(f"/{item.filename}")
        except:
            pass
        
        # Find all markdown files in all search paths
        all_md_files = []
        for search_path in search_paths:
            try:
                print(f"\nSearching for markdown files in {search_path}...")
                md_files = find_markdown_files(sftp, search_path)
                all_md_files.extend(md_files)
            except Exception as e:
                print(f"Could not search {search_path}: {e}")
        
        md_files = list(set(all_md_files))  # Remove duplicates
        
        if not md_files:
            print("No markdown files found.")
            return
        
        print(f"\nFound {len(md_files)} markdown file(s). Downloading...")
        
        # Download each file
        downloaded = 0
        for remote_path in md_files:
            # Create local path preserving directory structure
            relative_path = remote_path.replace(SFTP_BASE_PATH, "").lstrip("/")
            local_path = OUTPUT_DIR / relative_path
            
            if download_file(sftp, remote_path, local_path):
                downloaded += 1
                print(f"  ✓ {relative_path}")
        
        print(f"\n✓ Downloaded {downloaded}/{len(md_files)} files to {OUTPUT_DIR}")
        
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()

if __name__ == "__main__":
    main()

