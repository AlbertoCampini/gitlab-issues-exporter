import requests
import os

class GitLabClient:
    def __init__(self, api_base_url, project_id, private_token):
        self.api_base_url = api_base_url
        self.project_id = project_id
        self.session = requests.Session()
        self.session.headers.update({'PRIVATE-TOKEN': private_token})

    def get_issue_details(self, issue_iid):
        url = f"{self.api_base_url}/projects/{self.project_id}/issues/{issue_iid}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_issue_notes(self, issue_iid):
        url = f"{self.api_base_url}/projects/{self.project_id}/issues/{issue_iid}/notes"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_all_issues(self, state=None):
        """Fetch all issues for a project, optionally filtering by state."""
        issues = []
        page = 1
        per_page = 100
        while True:
            params = {'page': page, 'per_page': per_page}
            if state and state != 'all':
                params['state'] = state
            url = f"{self.api_base_url}/projects/{self.project_id}/issues"
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            issues.extend(batch)
            page += 1
        return issues

    def download_attachment(self, rel_path, dest_folder):
        subpath = rel_path.replace('/uploads', '')
        url = f"{self.api_base_url}/projects/{self.project_id}/uploads{subpath}"
        resp = self.session.get(url, stream=True)
        resp.raise_for_status()
        filename = os.path.basename(rel_path)
        dest_path = os.path.join(dest_folder, filename)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded attachment: {filename}")
        return dest_path