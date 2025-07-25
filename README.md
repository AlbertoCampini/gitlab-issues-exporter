
# GitLab Issues Exporter

## Overview

GitLab Issues Exporter is a Python tool designed to export issues from a GitLab project into a user-friendly HTML format. It captures all essential information, including issue descriptions, comments, and attachments, making it easy to create offline archives, generate technical documentation, or migrate data.

## Features

- **Flexible Export Options**: Configure the tool to export all issues or a specific list of issues by their IDs.
- **State Filtering**: Filter issues by their state (e.g., `opened`, `closed`, or `all`).
- **Complete Data Capture**: Exports issue details, comments, and downloads all associated attachments.
- **HTML Rendering**: Converts GitLab's Markdown syntax into clean, readable HTML files.
- **Navigable Index**: Automatically generates an `index.html` file for easy browsing of all exported issues.
- **Easy Configuration**: All settings are managed through a `config.yaml` file and a `.env` file for sensitive data like API tokens.

## Prerequisites

- Python 3.8 or newer.
- A GitLab Private Access Token with `api` scope.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone <your-repository-url>
    cd issues_exporter
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    # Create the virtual environment
    python -m venv .venv

    # Activate it (Windows)
    .venv\Scripts\activate

    # Activate it (macOS/Linux)
    # source .venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Configure Environment Variables:**

    Copy the example `.env` file:

    ```bash
    copy .env.example .env
    ```

    Open the new `.env` file and add your GitLab Private Access Token:

    ```
    GITLAB_PRIVATE_TOKEN="your_gitlab_token_here"
    ```

2.  **Configure the Export:**

    Copy `config.example.yaml` to `config.yaml` and customize it with your project details. You can specify the GitLab project ID and choose which issues to export.

    **Example `config.yaml`:**

    ```yaml
    gitlab:
      api_base_url: "https://gitlab.com/api/v4"
      project_id: 12345678 # Your GitLab project ID

    export:
      output_dir: "exported_issues"
      # Use "all" to export all issues or provide a list of issue IDs: [1, 5, 10]
      issues_to_export: "all"
      # Filter by state: "opened", "closed", or "all"
      state: "opened"
    ```

3.  **Run the Exporter:**

    Execute the main script from the project's root directory:

    ```bash
    python main.py
    ```

4.  **Check the Output:**

    The exported HTML files and attachments will be saved in the directory specified by `output_dir` in your configuration (e.g., `exported_issues/`).

## Project Structure

```
issues_exporter/
├── .env
├── .env.example
├── .gitignore
├── config.yaml
├── config.example.yaml
├── exporter.py
├── gitlab_client.py
├── html_renderer.py
├── main.py
├── README.md
└── requirements.txt
```

## Configuration Details

### `config.yaml`

| Section | Parameter          | Description                                       |
|---------|--------------------|---------------------------------------------------|
| `gitlab`  | `project_id`       | The ID of your GitLab project.                    |
| `export`  | `output_dir`       | The folder where exported files will be saved.    |
|         | `issues_to_export` | Set to `"all"` or a list of issue IDs (e.g., `[1, 2]`). |
|         | `state`            | Filters issues by state: `opened`, `closed`, `all`. |

### `.env`

| Variable               | Description                          |
|------------------------|--------------------------------------|
| `GITLAB_PRIVATE_TOKEN` | Your GitLab Private Access Token.    |

## Troubleshooting

-   **Authentication Errors**: Ensure your `GITLAB_PRIVATE_TOKEN` in the `.env` file is correct and has the necessary `api` permissions.
-   **Project Not Found**: Double-check that the `project_id` in `config.yaml` is correct.
-   **File Not Found Errors**: Make sure you are running `python main.py` from the root directory of the project.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request.

## License

This project is unlicensed. You are free to use, modify, and distribute it as you see fit. Consider adding a `LICENSE` file if you plan to share it publicly.