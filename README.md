# GitLab Issues Exporter

This tool allows you to export issues from a GitLab project to HTML files, including all comments and attachments.

## Features

- Export specific issues or all issues from a project.
- Renders issues and comments from Markdown to HTML.
- Downloads all attachments linked in the issues and comments.
- Creates a main index file to navigate through the exported issues.
- Configuration via `config.yaml` and `.env` file for security.

## Project Structure

```
issues_exporter/
├── .env.example
├── .gitignore
├── config.yaml
├── get_all_issues.py
├── get_issues.py
├── requirements.txt
└── README.md
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd issues_exporter
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Set up the environment file:**

    Create a `.env` file by copying the example file:

    ```bash
    cp .env.example .env
    ```

    Open the `.env` file and add your GitLab Private Access Token:

    ```
    GITLAB_PRIVATE_TOKEN=your_gitlab_private_token
    ```

2.  **Configure `config.yaml`:**

    Open `config.yaml` and set your GitLab project ID and other settings:

    ```yaml
    gitlab:
      api_base_url: "https://gitlab.com/api/v4"
      project_id: 12345678  # Your project ID

    export:
      output_dir: "exported_issues"
      # Issue selection: 
      # 'all' to export all issues, or a list of IIDs like [1, 2, 3]
      issues_to_export: [185] # or [1, 2, 3]
      output_dir: "exported_issues"

    html:
      css_file: "styles.css" # Optional: for custom styling
    ```

## Usage

To run the exporter, simply execute the `main.py` script:

```bash
python main.py
```

The script will read the configuration from `config.yaml` to determine which issues to export.

### Configuration Examples

**To export all issues:**

```yaml
# in config.yaml
export:
  # ...
  issues_to_export: "all"
  state: "opened" # or "closed", "all"
```

**To export specific issues:**

```yaml
# in config.yaml
export:
  # ...
  issues_to_export: [123, 456, 789]
```

## Output

The exported files will be saved in the directory specified by `output_dir` in your `config.yaml` (e.g., `exported_issues/`).

Each issue will have its own folder containing the `issue_{iid}.html` file and any downloaded attachments.

An `index.html` file will be created in the root of the output directory, providing a list of all exported issues.