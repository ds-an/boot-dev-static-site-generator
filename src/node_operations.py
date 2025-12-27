from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown")
        split_text = node.text.split(delimiter)
        for i, item in enumerate(split_text):
            if item != "":
                if i % 2 != 0:
                    new_node = TextNode(item, text_type)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(item, TextType.PLAIN)
                    new_nodes.append(new_node)
    return new_nodes
