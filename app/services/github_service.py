# github_service.py v1.0

import requests
from flask import current_app

class GitHubService:
    def __init__(self):
        self.token = current_app.config["GITHUB_TOKEN"]

    def validate_repo(self, repo_url):
        """
        Validates a GitHub repository URL.
        - repo_url: The URL of the repository (e.g., https://github.com/username/repo).
        Returns True if the repo exists and is accessible, False otherwise.
        """
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            owner, repo = repo_path.split("/", 1)
            repo = repo.rstrip(".git")
            headers = {"Authorization": f"token {self.token}"}
            response = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=headers
            )
            return response.status_code == 200
        except Exception:
            return False

    def check_commit(self, repo_url, commit_sha):
        """
        Checks if a specific commit exists in the repository.
        - repo_url: The URL of the repository.
        - commit_sha: The SHA of the commit to check.
        Returns True if the commit exists, False otherwise.
        """
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            owner, repo = repo_path.split("/", 1)
            repo = repo.rstrip(".git")
            headers = {"Authorization": f"token {self.token}"}
            response = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}",
                headers=headers
            )
            return response.status_code == 200
        except Exception:
            return False