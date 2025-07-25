
# GitLab Issues Exporter

## Overview

GitLab Issues Exporter is a Python tool that allows you to export issues from a GitLab project to HTML files, including all comments and attachments. The tool automates technical documentation and collaboration by generating navigable HTML and downloading all related attachments.

## Features

- **Flexible export:** Export all issues or only selected ones via configuration.
- **HTML rendering:** Converts Markdown from issues and comments to HTML.
- **Attachment download:** Downloads all files linked to issues and comments.
- **Navigable index:** Creates an `index.html` file for browsing exported issues.
- **Simple configuration:** All options managed via `config.yaml` and environment variables in `.env`.
- **Detailed logging:** Provides logs for monitoring and troubleshooting.

## Prerequisites

- Python >= 3.10
- A GitLab Private Access Token
- Internet connection to access GitLab APIs

## Installation

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd issues_exporter
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up environment files:**
    - Copy `.env.example` to `.env` and add your GitLab token:
      ```
      GITLAB_PRIVATE_TOKEN=your_gitlab_private_token
      ```

2. **Configure `config.yaml`:**
    - Set your project ID, issue selection, and output directory. Example:
      ```yaml
      gitlab:
        api_base_url: "https://gitlab.com/api/v4"
        project_id: 12345678

      export:
        output_dir: "exported_issues"
        issues_to_export: "all" # or [1, 2, 3]
        state: "opened" # "closed" or "all"

      html:
        css_file: "styles.css"
      ```

## How to Use

1. **Run the main script:**
    ```bash
    python main.py
    ```
    The tool will read configuration from `config.yaml` and `.env`, exporting the selected issues.

2. **Check outputs:**
    - HTML files and attachments will be saved in the specified output directory (`output_dir`).
    - Each issue will have its own folder with `issue_{iid}.html` and attachments.
    - An `index.html` file will be generated for navigation.

## Project Structure

```
issues_exporter/
├── config.yaml
├── config.example.yaml
├── .env
├── .env.example
├── .gitignore
├── exporter.py
├── gitlab_client.py
├── html_renderer.py
├── main.py
├── requirements.txt
├── README.md
└── __pycache__/
```

## Configuration Details

### config.yaml

| Section   | Parameter            | Description                                              | Example                        |
|-----------|----------------------|----------------------------------------------------------|--------------------------------|
| gitlab    | api_base_url         | Base URL for GitLab API                                  | https://gitlab.com/api/v4      |
|           | project_id           | GitLab project ID                                        | 12345678                       |
| export    | output_dir           | Output directory for exported files                      | exported_issues                |
|           | issues_to_export     | "all" or list of issue IIDs to export                   | "all" / [1, 2, 3]              |
|           | state                | Issue state to export ("opened", "closed", "all")        | opened                         |
| html      | css_file             | CSS file for custom HTML styling                         | styles.css                     |

### .env

| Variable               | Description                                 | Example                        |
|------------------------|---------------------------------------------|--------------------------------|
| GITLAB_PRIVATE_TOKEN   | Private access token for GitLab API         | glpat-xxxxxxxxxxxxxxxxxxxx     |

## Troubleshooting

- **Invalid token:** Make sure the token in `.env` is correct and has the required permissions.
- **Wrong project ID:** Ensure `project_id` in `config.yaml` matches your GitLab project.
- **Path issues on Windows:** Use forward slashes (`/`) or double backslashes (`\\`) in paths.
- **Check logs:** Logs are generated in the output directory to help diagnose errors.

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

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