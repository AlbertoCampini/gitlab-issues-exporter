from dotenv import load_dotenv
import os
import yaml
from gitlab_client import GitLabClient
from exporter import export_issues

# Load environment variables from .env file
load_dotenv()

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    gitlab_token = os.getenv("GITLAB_PRIVATE_TOKEN")

    if not gitlab_token:
        print("Error: GITLAB_PRIVATE_TOKEN not found in .env file.")
        return

    client = GitLabClient(
        api_base_url=config['gitlab']['api_base_url'],
        project_id=config['gitlab']['project_id'],
        private_token=gitlab_token
    )

    output_dir = config['export']['output_dir']
    issues_to_export = config['export']['issues_to_export']

    if issues_to_export == 'all':
        state = config['export'].get('state', 'all')
        print(f"Exporting all issues with state: {state}")
        issues = client.list_all_issues(state=state)
        issue_iids = [issue['iid'] for issue in issues]
        export_issues(client, issue_iids, output_dir)
    elif isinstance(issues_to_export, list):
        print(f"Exporting specific issues: {issues_to_export}")
        export_issues(client, issues_to_export, output_dir)
    else:
        print("Invalid value for 'issues_to_export' in config.yaml. Please use 'all' or a list of issue IDs.")

if __name__ == '__main__':
    main()