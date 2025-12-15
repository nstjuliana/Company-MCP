#!/usr/bin/env python3
"""
Download all markdown files from all git branches via SFTP.
Navigates each branch, finds markdown files, and downloads them.
"""
import os
import subprocess
import paramiko
from pathlib import Path
import shutil

# SFTP Configuration
SFTP_HOST = "localhost"
SFTP_PORT = 2222
SFTP_USER = os.getenv("SFTP_USER", "datauser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "changeme")
SFTP_BASE_PATH = "/data"

# Output directory
OUTPUT_DIR = Path(__file__).parent / "sftp-markdown-files"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_sftp_client():
    """Create SFTP connection."""
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
        return paramiko.SFTPClient.from_transport(transport), transport
    except Exception as e:
        print(f"Failed to connect to SFTP: {e}")
        return None, None

def get_all_branches():
    """Get all git branches (local and remote)."""
    try:
        # Get local branches
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        branches = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line and not line.startswith('*'):
                # Skip HEAD references
                if 'HEAD ->' in line or line.endswith('HEAD'):
                    continue
                # Remove 'remotes/origin/' prefix
                if 'remotes/origin/' in line:
                    branch = line.replace('remotes/origin/', '').strip()
                    if branch:
                        branches.append(branch)
                elif not line.startswith('remotes/'):
                    branches.append(line)
        
        # Remove duplicates and sort
        branches = sorted(set(branches))
        return branches
    except Exception as e:
        print(f"Error getting branches: {e}")
        return []

def find_markdown_files_in_path(path):
    """Find all markdown files in a local path."""
    md_files = []
    path_obj = Path(path)
    if path_obj.exists():
        for md_file in path_obj.rglob("*.md"):
            if md_file.is_file():
                md_files.append(md_file)
    return md_files

def download_file_from_sftp(sftp, remote_path, local_path):
    """Download a file from SFTP."""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        sftp.get(remote_path, str(local_path))
        return True
    except Exception as e:
        print(f"  Error downloading {remote_path}: {e}")
        return False

def find_markdown_files_sftp(sftp, path="/data", found_files=None, max_depth=20, current_depth=0):
    """Recursively find all .md files via SFTP."""
    if found_files is None:
        found_files = []
    
    if current_depth > max_depth:
        return found_files
    
    try:
        items = sftp.listdir_attr(path)
        for item in items:
            item_path = f"{path}/{item.filename}".replace("//", "/")
            
            is_dir = item.st_mode is not None and (item.st_mode & 0o40000)
            
            if is_dir:
                if item.filename in ['.', '..', '.git', '__pycache__', 'node_modules']:
                    continue
                find_markdown_files_sftp(sftp, item_path, found_files, max_depth, current_depth + 1)
            elif item.filename.endswith('.md'):
                found_files.append(item_path)
    except Exception as e:
        pass  # Skip errors
    
    return found_files

def main():
    repo_root = Path(__file__).parent
    
    print("Step 1: Getting all git branches...")
    branches = get_all_branches()
    if not branches:
        print("No branches found. Checking current branch...")
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=repo_root
            )
            current_branch = result.stdout.strip()
            if current_branch:
                branches = [current_branch]
        except:
            branches = ["master", "main"]
    
    print(f"Found {len(branches)} branch(es): {', '.join(branches)}")
    
    # Store current branch and stash changes
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        original_branch = result.stdout.strip()
        
        # Check if there are uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        has_changes = bool(result.stdout.strip())
        
        if has_changes:
            print("Stashing local changes...")
            subprocess.run(
                ["git", "stash", "push", "-m", "Temporary stash for branch navigation"],
                capture_output=True,
                cwd=repo_root
            )
            stashed = True
        else:
            stashed = False
    except:
        original_branch = None
        stashed = False
    
    all_downloaded_files = []
    
    # Process each branch
    for branch in branches:
        print(f"\n{'='*60}")
        print(f"Processing branch: {branch}")
        print(f"{'='*60}")
        
        try:
            # Checkout branch
            print(f"  Checking out branch: {branch}")
            result = subprocess.run(
                ["git", "checkout", branch],
                capture_output=True,
                text=True,
                cwd=repo_root
            )
            if result.returncode != 0:
                print(f"  ⚠️  Could not checkout {branch}: {result.stderr}")
                continue
            
            # Wait a moment for filesystem to sync
            import time
            time.sleep(1)
            
            # Connect to SFTP
            print(f"  Connecting to SFTP...")
            sftp, transport = get_sftp_client()
            if not sftp:
                print(f"  ⚠️  Could not connect to SFTP, skipping branch {branch}")
                continue
            
            try:
                # Find markdown files via SFTP
                print(f"  Searching for markdown files in {SFTP_BASE_PATH}...")
                md_files = find_markdown_files_sftp(sftp, SFTP_BASE_PATH)
                
                if not md_files:
                    print(f"  No markdown files found in {branch}")
                else:
                    print(f"  Found {len(md_files)} markdown file(s)")
                    
                    # Download each file
                    branch_dir = OUTPUT_DIR / branch.replace("/", "_")
                    branch_dir.mkdir(exist_ok=True)
                    
                    for remote_path in md_files:
                        # Create local path preserving structure
                        relative_path = remote_path.replace(SFTP_BASE_PATH, "").lstrip("/")
                        local_path = branch_dir / relative_path
                        
                        if download_file_from_sftp(sftp, remote_path, local_path):
                            all_downloaded_files.append((branch, str(local_path)))
                            print(f"    ✓ {relative_path}")
            
            finally:
                sftp.close()
                transport.close()
        
        except Exception as e:
            print(f"  ⚠️  Error processing branch {branch}: {e}")
    
    # Restore original branch and unstash if needed
    if original_branch:
        print(f"\nRestoring original branch: {original_branch}")
        subprocess.run(
            ["git", "checkout", original_branch],
            capture_output=True,
            cwd=repo_root
        )
        if stashed:
            print("Restoring stashed changes...")
            subprocess.run(
                ["git", "stash", "pop"],
                capture_output=True,
                cwd=repo_root
            )
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Processed {len(branches)} branch(es)")
    print(f"Downloaded {len(all_downloaded_files)} markdown file(s)")
    print(f"Files saved to: {OUTPUT_DIR}")
    
    if all_downloaded_files:
        print(f"\nDownloaded files:")
        for branch, file_path in all_downloaded_files:
            print(f"  [{branch}] {file_path}")

if __name__ == "__main__":
    main()
