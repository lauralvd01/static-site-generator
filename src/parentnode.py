from htmlnode import HTMLNode

"""
A ParentNode is a type of HTMLNode that represents a node with nested children.
It is an HTMLNode that is not a LeafNode.
"""
class ParentNode(HTMLNode):
    
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    """
    Returns a string that represents the HTML tag string of the node.
    """
    def to_html(self):
        if self.tag is None :
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        children_html = ''.join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"