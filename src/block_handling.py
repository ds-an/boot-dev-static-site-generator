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
        if not line.startswith(">"):
            flag_quote = False
            break
    if flag_quote:
        return BlockType.QUOTE
    flag_unordered_list = True
    for line in split_markdown_block:
        if not line.startswith("- "):
            flag_unordered_list = False
            break
    if flag_unordered_list:
        return BlockType.UNORDERED_LIST
    number = 0 
    flag_ordered_list = True
    for line in split_markdown_block:
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

def markdown_to_html_node(markdown):
    print("Markdown: " + markdown)
    markdown_blocks = markdown_to_blocks(markdown)
    print("Markdown Blocks: ")
    print(markdown_blocks)
    markdown_blocks = list(filter(lambda x: x != "", markdown_blocks))
    print("Markdown Blocks Filtered: ")
    print(markdown_blocks)
    markdown_block_types = list(map(block_to_block_type, markdown_blocks))
    markdown_blocks_and_types = list(zip(markdown_blocks, markdown_block_types))
    html_nodes = []
    for block, block_type in markdown_blocks_and_types:
        match block_type:
            case block_type.QUOTE:
                split_block = block.split("\n")
                split_block = list(filter(lambda x: x != "", split_block))
                for line in split_block:
                    line = line[:1]
                block = "\n".join(split_block)
                html_nodes.append(ParentNode("blockquote", list(map(text_node_to_html_node, text_to_textnodes(block)))))
            case block_type.PARAGRAPH:
                split_block = block.split("\n")
                split_block = [line.strip() for line in split_block]
                # split_block = list(filter(lambda x: x != "", split_block))
                block = " ".join(split_block)
                print(block)
                html_nodes.append(ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(block)))))
            case block_type.HEADING:
                heading_level = 0 
                for i in range(len(block)):
                    if block[i] == "#":
                        heading_level = heading_level + 1
                    else:
                        break
                html_nodes.append(ParentNode(f"h{heading_level}", list(map(text_node_to_html_node, text_to_textnodes(block)))))
            case block_type.CODE:
                pre_node = ParentNode("pre", ParentNode("code", text_node_to_html_node(TextNode(block, TextType.CODE))))
                html_nodes.append(pre_node)
            case block_type.UNORDERED_LIST:
                split_list = block.split("\n")
                split_list = list(filter(lambda x: x != "", split_list))
                print(split_list)
                list_items = []
                for list_item in split_list:
                    list_items.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(list_item)))))
                html_nodes.append(ParentNode("ul", list_items))
            case block_type.ORDERED_LIST:
                split_list = block.split("\n")
                split_list = list(filter(lambda x: x != "", split_list))
                list_items = []
                for list_item in split_list:
                    list_items.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(list_item)))))
                html_nodes.append(ParentNode("ol", list_items))
    # print(ParentNode("div", html_nodes).to_html())
    return ParentNode("div", html_nodes)
