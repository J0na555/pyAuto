# pyAuto — Automate Your Project Creation Workflow

**pyAuto** is a simple CLI tool that automates the tedious process of starting a new project. It creates a local project folder, initializes a Git repo, creates a remote GitHub repository, and opens the project in VS Code — all with a single command.

<br>

##  What It Does

- ✅ Creates a local project folder
- ✅ Creates a GitHub repository using your personal access token
- ✅ Initializes Git in the local folder and connects it to the remote repo
- ✅ Makes an initial commit with a `README.md`
- ✅ Pushes to GitHub
- ✅ Opens the project in VS Code
- ✅ All in one go.

<br>

## Folder Structure

```
pyAuto/
├── pyauto.py       # Main Python script that handles repo creation
├── create.sh       # Bash script that ties everything together
├── .env            # Environment variables (not included in repo)
```

<br>

## 🛠️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/J0na555/pyAuto.git
   cd pyAuto
   ```

2. **Install Dependencies**
   You need Python, `python-dotenv`, and `PyGithub`:

   ```bash
   pip install python-dotenv PyGithub
   ```

3. **Create your `.env` file**
   Inside the `pyAuto` directory:

   ```env
   FILEPATH=/your/local/projects/directory/
   GITHUB_TOKEN=ghp_YourPersonalAccessTokenHere
   USERNAME=yourGitHubUsername
   ```

4. **Make the Bash script executable**

   ```bash
   chmod +x create.sh
   ```

<br>

## Usage

From your terminal:

```bash
./create.sh my-cool-project
```

This will:

* Create a local directory: `$FILEPATH/my-cool-project`
* Create a remote GitHub repo: `https://github.com/<USERNAME>/my-cool-project`
* Initialize Git, make an initial commit, and push to main
* Open the project in VS Code



<br>

Tired of repeating the same steps every time you start a project? `pyAuto` was built to **cut setup time to seconds** and let you focus on building.

