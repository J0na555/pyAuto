import sys
import os
from github import Github
from dotenv import load_dotenv
from github.GithubException import GithubException

load_dotenv()

def create():
    folder_name = str(sys.argv[1])
    base_path = os.getenv("FILEPATH")
    token = os.getenv("GITHUB_TOKEN") 

    if not base_path or not token:
        print("ERROR: FILEPATH or GITHUB_TOKEN not set in .env")
        return

    project_path = os.path.join(base_path, folder_name)

    try:
        os.makedirs(project_path)
        print(f"Created local directory: {project_path}")
    except FileExistsError:
        print(f" Directory {project_path} already exists")

    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(folder_name, private=True)
        print(f"Successfully created GitHub repo: {folder_name}")
    except GithubException as e:
        print(f"Failed to create repo: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create.py <project_name>")
    else:
        create()
