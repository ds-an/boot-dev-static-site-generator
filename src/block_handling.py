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
