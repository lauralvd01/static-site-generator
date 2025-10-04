import re

from textnode import TextType, TextNode

"""
Takes a list of 'old nodes', a delimiter and a text type.
Returns a new list of nodes, where any old node that has type TextType.TEXT
and contains a portion of the given text type, delimited by the given delimiter,
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
                    new_list.append(TextNode(part,old_node.text_type))
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
"""
def extract_markdown_links(text):
    return re.findall(r"\[(.+?)\]\((.+?)\)",text)