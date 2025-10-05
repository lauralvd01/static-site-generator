import re

from textnode import TextType, TextNode

############################################ Split inline elements

"""
Takes a list of 'old nodes', a delimiter and a text type.
Returns a new list of nodes, where any old node that contains 
a portion of the given text type, delimited by the given delimiter,
are split into the correspondant nodes.
"""
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : TextType) :
    new_list = []
    for old_node in old_nodes :
        text = old_node.text
        parts = text.split(delimiter)
        
        for index, part in enumerate(parts):
            if len(part) > 0 :
                if index % 2 == 0:
                    new_list.append(TextNode(part,old_node.text_type,old_node.url))
                else:
                    new_list.append(TextNode(part,text_type))
    return new_list

"""
Takes raw markdown text.
Returns a list of tuples. 
Each tuple contains the alt text and the URL of any markdown images as ![alt text](url).
"""
def extract_markdown_images(text):
    return re.findall(r"!\[(.+?)\]\((.+?)\)",text)

"""
Takes raw markdown text.
Returns a list of tuples. 
Each tuple contains the anchor text and the URL of any markdown links as [anchor text](url).
Don't extract markdown images (i.e a ! character before the link).
"""
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)",text)

"""
Takes a list of 'old nodes'.
Returns a new list of nodes, where any old node that contains 
a markdown image are split into the correspondant nodes.
"""
def split_nodes_image(old_nodes):
    new_list = []
    for old_node in old_nodes :
        text = old_node.text
        images = extract_markdown_images(text)
        
        i = 0
        while len(text) > 0 and i < len(images):
            img = images[i]
            parts = text.split(f'![{img[0]}]({img[1]})')
            if len(parts[0]) > 0:
                new_list.append(TextNode(parts[0],old_node.text_type,old_node.url))
            new_list.append(TextNode(img[0],TextType.IMAGE,img[1]))
            if len(parts) > 1:
                text = parts[1]
            else: 
                text = ''
            i += 1
        if len(text) > 0:
            new_list.append(TextNode(text,old_node.text_type,old_node.url))
    return new_list

"""
Takes a list of 'old nodes'.
Returns a new list of nodes, where any old node that contains 
a markdown link are split into the correspondant nodes.
"""
def split_nodes_link(old_nodes):
    new_list = []
    for old_node in old_nodes :
        text = old_node.text
        links = extract_markdown_links(text)
        
        i = 0
        while len(text) > 0 and i < len(links):
            link = links[i]
            parts = text.split(f'[{link[0]}]({link[1]})')
            if len(parts[0]) > 0:
                new_list.append(TextNode(parts[0],old_node.text_type,old_node.url))
            new_list.append(TextNode(link[0],TextType.LINK,link[1]))
            if len(parts) > 1:
                text = parts[1]
            else: 
                text = ''
            i += 1
        if len(text) > 0:
            new_list.append(TextNode(text,old_node.text_type,old_node.url))
    return new_list

"""
Takes inline markdown as input.
Returns the list of tje textnodes correponding to the inline elements.
"""
def text_to_textnodes(text):
    with_bold = split_nodes_delimiter([TextNode(text,TextType.TEXT)],'**',TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold,'_',TextType.ITALIC)
    with_code = split_nodes_delimiter(with_italic,'`',TextType.CODE)
    with_images = split_nodes_image(with_code)
    with_links = split_nodes_link(with_images)
    return with_links



############################################ Split block elements

"""
Takes a raw Markdown string (representing a full document).
Returns a list of "block" strings.
"""
def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split('\n\n') if len(block.strip()) > 0]

from enum import Enum
class BlockType(Enum):
    PARAGRAPH = 'paragraph_bloc'
    HEADING = 'heading_block'
    CODE = 'code_block'
    QUOTE = 'quote_block'
    UNORDERED_LIST = 'unordered_list_block'
    ORDERED_LIST = 'ordered_list_block'

"""
Takes a single block of markdown text.
Returns the correspondant BlockType.
Assumes all leading and trailing whitespace were already stripped.
"""
def block_to_block_type(text):
    # Headings are a one-line block, start with 1-6 # characters, followed by a space and then the heading text.
    pattern = r"^#{1,6} .*"
    match = re.findall(pattern,text)
    if len(match) == 1 and match[0] == text:
        return BlockType.HEADING
    
    # Code blocks can be a several-lines block, must start with 3 backticks and end with 3 backticks.
    pattern = r"^`{3}[\s\S]*`{3}$"
    match = re.findall(pattern,text)
    if len(match) == 1 and match[0] == text:
        return BlockType.CODE
    
    # Every line in a quote block must start with a > character.
    pattern = r"^>(?:.*\n>)*.*"
    match = re.findall(pattern,text)
    if len(match) == 1 and match[0] == text:
        return BlockType.QUOTE
    
    # Every line in an unordered list block must start with a - character, followed by a space.
    pattern = r"^- (?:.*\n- )*.*"
    match = re.findall(pattern,text)
    if len(match) == 1 and match[0] == text:
        return BlockType.UNORDERED_LIST
    
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    # Check the format each-line-begins-with-a-digit-a-dot-and-a-space
    pattern = r"^\d\. (?:.*\n\d\. )*.*"
    match = re.findall(pattern,text)
    if len(match) == 1 and match[0] == text:
        # Retrieve the digits list and check that its ordered and start at 1
        pattern = r"^(\d)\. .*"
        matches = re.findall(pattern,text,re.MULTILINE)
        ordered_range = [f'{i+1}' for i in range(len(matches))]
        if ordered_range == matches :
            return BlockType.ORDERED_LIST
    
    # Every other block are paragraph block
    return BlockType.PARAGRAPH