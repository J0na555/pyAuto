import sys
import os
import subprocess
import shutil
from github import Github
from dotenv import load_dotenv
from github.GithubException import GithubException

load_dotenv()

def get_editor_choice():
    """Get editor choice from command line argument or prompt user"""
    # Check for --editor argument
    if "--editor" in sys.argv:
        try:
            editor_index = sys.argv.index("--editor")
            if editor_index + 1 < len(sys.argv):
                editor = sys.argv[editor_index + 1].lower()
                if editor in ["code", "cursor", "nvim"]:
                    return editor
                else:
                    print(f"Invalid editor '{editor}'. Must be one of: code, cursor, nvim")
                    print("Prompting for editor choice...")
            else:
                print("--editor flag requires a value (code, cursor, or nvim)")
                print("Prompting for editor choice...")
        except ValueError:
            pass
    
    # If no valid argument, prompt user
    print("\nChoose an editor to open:")
    print("1. VS Code (code)")
    print("2. Cursor (cursor)")
    print("3. Neovim (nvim)")
    print("4. Skip (don't open any editor)")
    
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            return "code"
        elif choice == "2":
            return "cursor"
        elif choice == "3":
            return "nvim"
        elif choice == "4":
            return None
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

def open_editor(project_path, editor):
    """Open the project in the specified editor"""
    editor_commands = {
        "code": "code",
        "cursor": "cursor",
        "nvim": "nvim"
    }
    
    if editor not in editor_commands:
        return
    
    command = editor_commands[editor]
    editor_names = {
        "code": "VS Code",
        "cursor": "Cursor",
        "nvim": "Neovim"
    }
    
    try:
        subprocess.run([command, project_path], check=False)
        print(f"Opened project in {editor_names[editor]}")
    except FileNotFoundError:
        print(f"{editor_names[editor]} not found in PATH. Skipping...")
    except Exception as e:
        print(f"Failed to open {editor_names[editor]}: {e}")

def create():
    # Get project name (first non-flag argument)
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("ERROR: Project name is required")
        print("Usage: python pyauto.py <project_name> [--editor code|cursor|nvim]")
        return
    
    folder_name = args[0]
    base_path = os.getenv("FILEPATH")
    token = os.getenv("GITHUB_TOKEN") 

    if not base_path or not token:
        print("ERROR: FILEPATH or GITHUB_TOKEN not set in .env")
        return

    project_path = os.path.join(base_path, folder_name)

    # Create local directory
    try:
        os.makedirs(project_path)
        print(f"Created local directory: {project_path}")
    except FileExistsError:
        print(f"Directory {project_path} already exists")
        return

    # Create GitHub repository
    repo = None
    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(folder_name, private=True)
        print(f"Successfully created GitHub repo: {folder_name}")
    except GithubException as e:
        print(f"Failed to create repo: {e}")
        # Cleanup: remove local directory if GitHub creation fails
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            print("Cleaned up local directory")
        return

    # Initialize git repository
    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True, 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Initialized git repository")
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize git: {e}")
        cleanup_on_error(project_path, repo)
        return

    # Create README.md
    try:
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# {folder_name}\n\n")
        print("Created README.md")
    except Exception as e:
        print(f"Failed to create README.md: {e}")
        cleanup_on_error(project_path, repo)
        return

    # Add remote, commit, and push
    try:
        # Set remote URL with token for authentication
        remote_url = repo.clone_url.replace("https://", f"https://{token}@")
        subprocess.run(["git", "remote", "add", "origin", remote_url], 
                      cwd=project_path, check=True,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "add", "."], cwd=project_path, check=True,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "Initial commit"], 
                      cwd=project_path, check=True,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "branch", "-M", "main"], cwd=project_path, check=True,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", "main"], 
                      cwd=project_path, check=True,
                      env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        print("Note: Repository created on GitHub, but local git operations failed")
        # Don't cleanup here since repo exists on GitHub

    # Open editor
    editor = get_editor_choice()
    if editor:
        open_editor(project_path, editor)

def cleanup_on_error(project_path, repo=None):
    """Remove project directory and optionally delete GitHub repo if something goes wrong"""
    if os.path.exists(project_path):
        try:
            shutil.rmtree(project_path)
            print(f"Cleaned up {project_path}")
        except Exception as e:
            print(f"Warning: Could not clean up {project_path}: {e}")
    
    if repo:
        try:
            repo.delete()
            print("Deleted GitHub repository")
        except Exception as e:
            print(f"Warning: Could not delete GitHub repository: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pyauto.py <project_name> [--editor code|cursor|nvim]")
        print("  --editor: Optional. Choose editor to open (code, cursor, or nvim)")
        print("           If not specified, you'll be prompted to choose.")
    else:
        create()
        
