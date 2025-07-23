import os
from gitlab_client import GitLabClient
from html_renderer import render_issue_html, render_index_html, find_attachment_paths
import emoji

def export_issues(client: GitLabClient, issue_iids, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    index_entries = []
    for iid in issue_iids:
        print(f"Processing issue {iid}...")
        try:
            details = client.get_issue_details(iid)
            notes = client.get_issue_notes(iid)

            issue_folder = os.path.join(output_dir, str(iid))
            os.makedirs(issue_folder, exist_ok=True)

            # Render issue HTML
            html_content = render_issue_html(details, notes)
            html_filename = f"issue_{iid}.html"
            html_path = os.path.join(issue_folder, html_filename)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Saved HTML for issue {iid}: {html_path}")

            # Download attachments
            combined_md = details.get('description', '') + '\n'.join(n['body'] for n in notes)
            attachment_paths = find_attachment_paths(emoji.emojize(combined_md, language='alias'))

            for att_name, att_path in attachment_paths:
                try:
                    # Modify the path to be relative to the HTML file
                    local_path = client.download_attachment(att_path, issue_folder)
                    # We need to replace the gitlab upload path with the local path
                    html_content = html_content.replace(att_path, os.path.basename(local_path))
                except Exception as e:
                    print(f"Failed to download attachment {att_path}: {e}")
            
            # Save the HTML again with updated attachment links
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            index_entries.append({
                'iid': iid,
                'title': details.get('title', ''),
                'state': details.get('state'),
                'file': f"{iid}/{html_filename}",
                'gitlab_link': details.get('web_url')
            })

        except Exception as e:
            print(f"Failed to process issue {iid}: {e}")

    # Generate index HTML
    index_html = render_index_html(index_entries)
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Generated index file: {index_path}")