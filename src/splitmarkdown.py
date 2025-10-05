import re

from textnode import TextType, TextNode
from parentnode import ParentNode

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
    # Headings are a one-line block, start with 1-6 # characters, followed by a space and then the heading text (at least one character).
    pattern = r"^#{1,6} .+"
    matches = re.findall(pattern,text)
    if len(matches) == 1 and matches[0] == text:
        return BlockType.HEADING
    
    # Code blocks can be a several-lines block, must start with 3 backticks and end with 3 backticks.
    pattern = r"^`{3}[\s\S]*`{3}$"
    matches = re.findall(pattern,text)
    if len(matches) == 1 and matches[0] == text:
        return BlockType.CODE
    
    # Every line in a quote block must start with a > character.
    pattern = r"^>(?:.*\n>)*.*"
    matches = re.findall(pattern,text)
    if len(matches) == 1 and matches[0] == text:
        return BlockType.QUOTE
    
    # Every line in an unordered list block must start with a - character, followed by a space, and have at least one character on each line.
    pattern = r"^- (?:.+\n- )*.+"
    matches = re.findall(pattern,text)
    if len(matches) == 1 and matches[0] == text:
        return BlockType.UNORDERED_LIST
    
    # Every line in an ordered list block must start with a number followed by a . character and a space, and have at least one character on each line. The number must start at 1 and increment by 1 for each line.
    # Check the format each-line-begins-with-a-digit-a-dot-and-a-space
    pattern = r"^\d+\. (?:.+\n\d\. )*.+"
    matches = re.findall(pattern,text)
    if len(matches) == 1 and matches[0] == text:
        # Retrieve the digits list and check that its ordered and start at 1
        pattern = r"^(\d+)\. .+"
        matches = re.findall(pattern,text,re.MULTILINE)
        ordered_range = [f'{i+1}' for i in range(len(matches))]
        if ordered_range == matches :
            return BlockType.ORDERED_LIST
    
    # Every other block are paragraph block
    return BlockType.PARAGRAPH

"""
Takes a string of inline text.
Returns a list of HTMLNodes that represent the inline markdown.
"""
def text_to_children(text):
    children = []
    texnodes = text_to_textnodes(text)
    for textnode in texnodes:
        children.append(textnode.text_node_to_html_node())
    return children

"""
Takes a markdown block and its block type.
Returns the correspondant HTMLNode.
"""
def block_to_html_node(block_text,block_type):
    if block_type == BlockType.HEADING:
        pattern = r"^(\S+) "
        matches = re.findall(pattern,block_text)
        raw_text = block_text.split(matches[0] + ' ')[1]
        children = text_to_children(raw_text)
        return ParentNode(tag=f'h{len(matches[0])}',children=children)
    
    if block_type == BlockType.CODE:
        pattern = r"^`{3}\n([\s\S]*)`{3}$"
        matches = re.findall(pattern,block_text)
        textnode = TextNode(text=matches[0],type=TextType.CODE)
        children = [textnode.text_node_to_html_node()]
        return ParentNode(tag='pre',children=children)
    
    if block_type == BlockType.QUOTE:
        raw_text = block_text.replace('>','').strip()
        raw_text = raw_text.replace('\n','')
        children = text_to_children(raw_text)
        return ParentNode(tag='blockquote',children=children)
    
    if block_type == BlockType.UNORDERED_LIST:
        items = block_text.split('- ')
        children = []
        for item in items:
            if len(item) > 0:
                raw_text = item.strip()
                nested_children = text_to_children(raw_text)
                children.append(ParentNode(tag='li',children=nested_children))
        return ParentNode(tag='ul',children=children)
    
    if block_type == BlockType.ORDERED_LIST:
        items = block_text.split('\n')
        children = []
        for item in items:
            if len(item) > 0:
                pattern = r"^\d+\. (.+)"
                matches = re.findall(pattern,item)
                raw_text = matches[0].strip()
                nested_children = text_to_children(raw_text)
                children.append(ParentNode(tag='li',children=nested_children))
        return ParentNode(tag='ol',children=children)
    
    children = text_to_children(block_text.strip())
    return ParentNode(tag='p',children=children)


"""
Takes a raw Markdown string, representing a full document.
Returns a single HTMLNode that contains all the child HTMLNodes
representing the nested elements of the document.
"""
def markdown_to_html_node(markdown):
    children = []
    
    markdown_blocks = markdown_to_blocks(markdown)
    for md_block in markdown_blocks:
        block_type = block_to_block_type(md_block)
        block_htmlnode = block_to_html_node(md_block,block_type)
        children.append(block_htmlnode)
    
    parent_htmlnode = ParentNode(tag="div",children=children)
    return parent_htmlnode

"""
Takes a raw Markdown string, representing a full document.
Returns the content of the h1 header of the file.
Raise an exception if there is no h1 header.
"""
def extract_title(markdown):
    pattern = r"# (.+)"
    matches = re.findall(pattern,markdown)
    if len(matches) == 0:
        raise Exception
    return matches[0].strip()