"""
An HTMLNode "HTMLNode" represents a node in an HTML document tree.
For example : a <p> tag and its contents, or an <a> tag and its contents. 
It can be block level or inline, and is designed to only output HTML.
"""
class HTMLNode :
    
    """
    Each node has a tag, value, children, and properties.
    The tag is a string representing the HTML tag name (e.g., 'p', 'a', 'h1', etc.).
    The value is a string representing the value of the HTML tag (e.g. the text inside a paragraph).
    Children are a list of HTMLNode objects representing the children ot this node
    Properties are a dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}.
    """
    def __init__(self, tag : str = None, value : str = None, children : list = None, props : dict = None):
        self.tag = tag  # if None, it renders as raw text
        self.value = value # if None, assuming to have children
        self.children = children # if None, assuming to have a value
        self.props = props # if None, assuming to have no attributes
    
    """
    Returns a string that represents the HTML attributes of the node.
    """
    def props_to_html(self):
        if self.props is None:
            return ""
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string
    
    """
    Print method for debugging purposes.
    """
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})'
        # if self.tag is None:
        #     return f"Raw text : value={self.value}, props={self.props_to_html()}"
        # if self.value is not None:
        #     return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        # if self.children is not None:
        #     children_html = ''.join([repr(child) for child in self.children])
        #     return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        # return f"<{self.tag}{self.props_to_html()} />"