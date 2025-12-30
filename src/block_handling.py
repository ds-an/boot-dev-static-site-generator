from enum import Enum
import re

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
    print(split_markdown_block)
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
