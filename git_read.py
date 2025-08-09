from git import Repo
import os
import tempfile

# load/Clone repo from Github to a temp file

def load_repo(path_or_url):
    """
    Load or clone a Git repository from a local path or a remote URL.
    """
    try:
        if path_or_url.startswith("http"):
            temp_dir = tempfile.mkdtemp()
            print(f"Cloning repo to temp dir: {temp_dir}")
            repo = Repo.clone_from(path_or_url, temp_dir)
        else:
            repo = Repo(path_or_url)
        return repo
    except Exception as e:
        print(f"Error loading repository: {e}")
        return None

# List all file paths in the repository

def list_file_paths(repo):
    """
    List all file paths in the Git repository.
    
    Args:
        repo (Repo): The GitPython Repo object.
        
    Returns:
        list: A list of file paths in the repository.
    """
    try:
        return [item.path for item in repo.tree().traverse()]
    except Exception as e:
        print(f"Error listing file paths: {e}")
        return []
    
import os

# Read file content 

def read_file(repo, file_path):
    try:
        full_path = os.path.join(repo.working_tree_dir, file_path)
        
        # Skip folders and binary files
        if os.path.isdir(full_path) or file_path.endswith('.pyc'):
            return None
        
        # Try reading with UTF-8 first, then fallback
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(full_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

