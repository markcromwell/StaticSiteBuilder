def extract_title(markdown):
    """
    Extracts the title from the given markdown content.
    The title is defined as the first level 1 heading (i.e., a line starting with '# ').
    If no level 1 heading is found, returns 'Untitled'.
    """
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return 'Untitled'
