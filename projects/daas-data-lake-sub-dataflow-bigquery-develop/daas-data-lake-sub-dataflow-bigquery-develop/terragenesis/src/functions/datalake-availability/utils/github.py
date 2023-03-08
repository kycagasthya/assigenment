from io import BytesIO
import os, requests, zipfile


def download_repo(token: str, repo: str) -> str:

    url = f"https://api.github.com/repos/{repo}/zipball/main"
    directory = repo.split('/')[-1]
    response = requests.get(
        url,
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}"
        }
    )

    archive = zipfile.ZipFile(BytesIO(response.content))
    archive.extractall(f"/tmp/{directory}")

    path = f"/tmp/{directory}/" + os.listdir(f'/tmp/{directory}')[0]
    return path if os.path.isdir(path) else None

def check_workflow_run(token: str, repo: str) -> bool:

    url = f"https://api.github.com/repos/{repo}/actions/runs?status=in_progress&branch=main"
    response = requests.get(
        url,
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}"
        }
    )
    
    return True if _validate_runs(response.json()) == True else False


def _validate_runs(content: dict) -> bool:

    in_progress = False
    for run in content['workflow_runs']:
        if run['name'] == "CI/CD - GCP smart deployment":
            in_progress = True
            break
        else:
            continue

    return True if in_progress == True else False
    