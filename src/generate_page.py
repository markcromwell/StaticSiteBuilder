
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
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Read template content
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Convert markdown to HTML
    md_node = markdown_to_html_node(md_content)
    html_content = md_node.to_html()
    print("DEBUG - Generated HTML:", html_content)
    # Extract just the inner content from the div
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
