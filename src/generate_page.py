
import os
from textnode import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):

    """
Create a generate_page(from_path, template_path, dest_path) function. It should:
Print a message like "Generating page from from_path to dest_path using template_path".
Read the markdown file at from_path and store the contents in a variable.
Read the template file at template_path and store the contents in a variable.
Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
Use the extract_title function to grab the title of the page.
Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
"""
    
    # Resolve paths: accept relative template or content paths and try common locations
    src_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(src_dir)

    # Resolve markdown source
    if not os.path.isabs(from_path):
        candidate = os.path.join(project_root, from_path)
        if os.path.exists(candidate):
            from_path = candidate

    # Read markdown content
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown source not found: {from_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Resolve template: try provided path, then src/template.html, then project_root/template.html
    resolved_template = template_path
    if not os.path.isabs(resolved_template):
        candidates = [
            os.path.join(src_dir, resolved_template),
            os.path.join(project_root, resolved_template),
            os.path.join(src_dir, 'template.html'),
            os.path.join(project_root, 'template.html'),
            resolved_template,
        ]
    else:
        candidates = [resolved_template]

    template_content = None
    for cand in candidates:
        if cand and os.path.exists(cand):
            resolved_template = cand
            with open(cand, 'r', encoding='utf-8') as f:
                template_content = f.read()
            break

    if template_content is None:
        raise FileNotFoundError(f"Template not found. Tried: {candidates}")

    # Convert markdown to HTML
    md_node = markdown_to_html_node(md_content)
    html_content = md_node.to_html()
    # Extract just the inner content from the div if present
    if html_content.startswith('<div>') and html_content.endswith('</div>'):
        html_content = html_content[5:-6]  # strip <div> and </div>

    # Extract title
    title = extract_title(md_content)

    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    # Write the full HTML to destination path
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
