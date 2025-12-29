from textnode import TextType, TextNode
from text_extraction import extract_markdown_images, extract_markdown_links
import re

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        images_links = extract_markdown_images(node.text)
        if not images_links:
            new_nodes.append(node)
            continue
        image_link = images_links[0]
        split_node = node.text.split(f"![{image_link[0]}]({image_link[1]})", 1)
        if split_node[0] == "":
            new_node = TextNode(image_link[0], TextType.IMAGE, image_link[1])
            new_nodes.append(new_node)
        else:
            new_node = TextNode(split_node[0], TextType.PLAIN)
            new_nodes.append(new_node)
            new_node = TextNode(image_link[0], TextType.IMAGE, image_link[1])
            new_nodes.append(new_node)
        if split_node[1] == "":
            continue
        new_nodes += split_nodes_image([TextNode(split_node[1], TextType.PLAIN)])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        alts_links = extract_markdown_links(node.text)
        if not alts_links:
            new_nodes.append(node)
            continue
        alt_link = alts_links[0]
        split_node = node.text.split(f"[{alt_link[0]}]({alt_link[1]})", 1)
        if split_node[0] == "":
            new_node = TextNode(alt_link[0], TextType.LINK, alt_link[1])
            new_nodes.append(new_node)
        else:
            new_node = TextNode(split_node[0], TextType.PLAIN)
            new_nodes.append(new_node)
            new_node = TextNode(alt_link[0], TextType.LINK, alt_link[1])
            new_nodes.append(new_node)
        if split_node[1] == "":
            continue
        new_nodes += split_nodes_link([TextNode(split_node[1], TextType.PLAIN)])
    return new_nodes

def text_to_textnodes(text):
    main_node = TextNode(text, TextType.PLAIN)
    new_nodes = split_nodes_link([main_node])
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes 
