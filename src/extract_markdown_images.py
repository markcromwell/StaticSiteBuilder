import re

def extract_markdown_images(markdown_text):
    """
    Takes raw markdown text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images. For example:
text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print(extract_markdown_images(text))
# [("rick roll",
    

    Args:
        markdown_text (str): The markdown text to extract images from.

    Returns:
        list: A list of tuples (alt_text, image URL) found in the markdown text.
    """
    # Regular expression to match markdown image syntax ![alt text](image_url)
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # Find all matches using the regex pattern
    matches = re.findall(image_pattern, markdown_text)
    
    return matches

def extract_markdown_links(markdown_text):
    """
    Extracts all link URLs from the given markdown text.

    Args:
        markdown_text (str): The markdown text to extract links from.

    Returns:
        list: A list of link URLs found in the markdown text.
    """
    import re

    # Regular expression to match markdown link syntax [link text](link_url)
    link_pattern = r'\[.*?\]\((.*?)\)'
    
    # Find all link URLs using the regex pattern
    link_urls = re.findall(link_pattern, markdown_text)
    
    return link_urls

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

