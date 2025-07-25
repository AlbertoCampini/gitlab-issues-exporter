import markdown
import emoji
from datetime import datetime, timezone

def find_attachment_paths(text):
    import re
    # Finds markdown links pointing to /uploads/... paths
    return re.findall(r'\[(.*?)\]\((/uploads/[^)]+)\)', text)

def render_issue_html(details, notes, css=''):
    meta = {
        'ID': details.get('id'),
        'IID': details.get('iid'),
        'Project': details.get('project_id'),
        'State': details.get('state'),
        'Created At': details.get('created_at'),
        'Updated At': details.get('updated_at'),
        'Exported At': datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        'Closed At': details.get('closed_at') or '',
        'Closed By': (details.get('closed_by') or {}).get('name', ''),
        'Author': details.get('author', {}).get('name', ''),
        'Assignees': ', '.join(a.get('name') for a in details.get('assignees', [])),
        'Link': f"<a href='{details.get('web_url')}'>View on GitLab</a>"
    }
    title = details.get('title', '')
    raw_desc_md = emoji.emojize(details.get('description', '') or '', language='alias')
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    desc_html = md.convert(raw_desc_md)

    notes_sorted = sorted(notes, key=lambda n: n['created_at'])
    updates = []
    for note in notes_sorted:
        dt = datetime.fromisoformat(note['created_at'].rstrip('Z'))
        header = f"<p><strong>Update by {note['author']['name']} on {dt.strftime('%Y-%m-%d %H:%M:%S')}</strong></p>"
        raw_desc_md = emoji.emojize(note['body'], language='alias')
        body_html = markdown.markdown(raw_desc_md, extensions=['tables', 'fenced_code'])
        updates.append(f"<div class='update'>{header}{body_html}</div>")
    updates_html = '<hr/>' .join(updates)

    if not css:
        css = get_default_css()

    rows = ''.join(f"<tr><th>{key}</th><td>{value}</td></tr>" for key, value in meta.items())

    html = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
      <meta charset='UTF-8'>
      <title>Issue {details.get('iid')}</title>
      <style>{css}</style>
    </head>
    <body>
      <h1>ISSUE - {details.get('iid')} LOGS</h1>
      <table class='metadata'>
        {rows}
      </table>
      {desc_html}
      <hr/>
      <h2>Updates</h2>
      {updates_html}
    </body>
    </html>
    """
    return html

def render_index_html(issues, css=''):
    if not css:
        css = get_default_css()

    header = '<h1>Issue Export Index</h1>'
    table_rows = ''.join(
        f"<tr>"
        f"<td>{issue['iid']}</td>"
        f"<td><a href='{issue['file']}'>{issue['title']}</a></td>"
        f"<td>{issue['state']}</td>"
        f"<td><a href='{issue['gitlab_link']}'>GitLab</a></td>"
        f"</tr>" for issue in issues
    )
    table = (
        '<table>'
        '<thead><tr><th>IID</th><th>Title</th><th>State</th><th>GitLab</th></tr></thead>'
        f'<tbody>{table_rows}</tbody>'
        '</table>'
    )
    return f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Issues Index</title><style>{css}</style></head><body>{header}{table}</body></html>"""

def get_default_css():
    return '''
    body { font-family: Arial, sans-serif; margin: 2em; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 1.5em; }
    table.metadata th { background: #f0f0f0; text-align: left; width: 20%; padding: 0.5em; }
    table.metadata td { padding: 0.5em; }
    th, td { border: 1px solid #ccc; }
    .update { margin-bottom: 1em; }
    blockquote { color: #666; margin: 1em 0; padding-left: 1em; border-left: 4px solid #ccc; }
    pre { background: #f8f8f8; padding: 1em; overflow: auto; }
    a { text-decoration: none; color: #0366d6; }
    '''