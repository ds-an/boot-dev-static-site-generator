from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from node_operations import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    split_markdown_block = markdown_block.split("\n")
    split_markdown_block = list(filter(lambda x: x != "", split_markdown_block))
    if re.match(r"^#{1,6} .+", split_markdown_block[0]):
        return BlockType.HEADING
    if markdown_block.startswith("```")\
        and markdown_block.endswith("```"):
        return BlockType.CODE
    flag_quote = True
    for line in split_markdown_block:
        line = line.lstrip(" ").strip()
        if not line.startswith(">"):
            flag_quote = False
            break
    if flag_quote:
        return BlockType.QUOTE
    flag_unordered_list = True
    for line in split_markdown_block:
        line = line.lstrip(" ").strip()
        if not line.startswith("- "):
            flag_unordered_list = False
            break
    if flag_unordered_list:
        return BlockType.UNORDERED_LIST
    number = 0 
    flag_ordered_list = True
    for line in split_markdown_block:
        line = line.lstrip(" ").strip()
        number = number + 1
        if not line.startswith(f"{number}. "):
            flag_ordered_list = False
            break
    if flag_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for line in split_markdown:
        if line == "":
            del line
            continue
        line = line.strip("\n")
        line = line.strip()
        blocks.append(line)
    return blocks

def quote_block_to_html_node(block):
    split_block = block.split("\n")
    for i in range(len(split_block)):
        split_block[i] = split_block[i].lstrip(" ").strip()
        split_block[i] = split_block[i].lstrip(">").strip()
    block = " ".join(split_block)
    return ParentNode("blockquote", list(map(text_node_to_html_node, text_to_textnodes(block))))

def paragraph_block_to_html_node(block):
    split_block = block.split("\n")
    split_block = [line.strip() for line in split_block]
    block = " ".join(split_block)
    return ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(block))))

def heading_block_to_html_node(block):
    heading_level = 0 
    for i in range(len(block)):
        if block[i] == "#":
            heading_level = heading_level + 1
        else:
            break
    block = block[heading_level + 1:]
    return ParentNode(f"h{heading_level}", list(map(text_node_to_html_node, text_to_textnodes(block))))

def code_block_to_html_node(block):
    block = block[4:-3]
    block = block.strip(" ")
    split_block = block.split("\n")
    split_block = [line.strip() for line in split_block]
    block = "\n".join(split_block)
    pre_node = ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))])
    return pre_node

def unordered_list_block_to_html_node(block):
    split_block = block.split("\n")
    for i in range(len(split_block)):
        split_block[i] = split_block[i].lstrip(" ").strip()
        split_block[i] = split_block[i].lstrip("- ").strip()
    list_items = []
    for list_item in split_block:
        list_items.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(list_item)))))
    return ParentNode("ul", list_items)

def ordered_list_block_to_html_node(block):
    split_block = block.split("\n")
    number = 0
    for i in range(len(split_block)):
        number = number + 1
        split_block[i] = split_block[i].lstrip(" ").strip()
        split_block[i] = split_block[i].lstrip(f"{number}. ").strip()
    list_items = []
    for list_item in split_block:
        list_items.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(list_item)))))
    return ParentNode("ol", list_items)

def block_to_html_node(block, block_type):
    match block_type:
        case block_type.QUOTE:
            return quote_block_to_html_node(block)
        case block_type.PARAGRAPH:
            return paragraph_block_to_html_node(block)
        case block_type.HEADING:
            return heading_block_to_html_node(block)
        case block_type.CODE:
            return code_block_to_html_node(block)
        case block_type.UNORDERED_LIST:
            return unordered_list_block_to_html_node(block)
        case block_type.ORDERED_LIST:
            return ordered_list_block_to_html_node(block)

def markdown_to_blocks_and_types(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    markdown_blocks = list(filter(lambda x: x != "", markdown_blocks))
    markdown_block_types = list(map(block_to_block_type, markdown_blocks))
    markdown_blocks_and_types = list(zip(markdown_blocks, markdown_block_types))
    return markdown_blocks_and_types


def markdown_to_html_node(markdown):
    markdown_blocks_and_types = markdown_to_blocks_and_types(markdown)
    html_nodes = []
    for block, block_type in markdown_blocks_and_types:
        html_nodes.append(block_to_html_node(block, block_type))
    return ParentNode("div", html_nodes)
