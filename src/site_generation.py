import shutil
import os
from block_handling import markdown_to_html_node

def copy_source_to_dest_dir(source, dest):
    if os.path.exists(dest): 
        shutil.rmtree(dest)
    if not os.path.exists(source):
        raise Exception(f"{source} does not exist")
    os.mkdir(dest)
    current_files = []
    current_dirs = []
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            current_files.append(file_path)
        if os.path.isdir(file_path):
            current_dirs.append(file_path)
    for file in current_files:
        shutil.copy(file, dest)
    for dir in current_dirs:
        _, tail = os.path.split(dir)
        new_dest = os.path.join(dest, tail)
        os.mkdir(new_dest)
        copy_source_to_dest_dir(dir, new_dest)

def extract_title(markdown):
    split_markdown = markdown.split("\n")
    split_markdown = list(filter(lambda x: x != "", split_markdown))
    for line in split_markdown:
        line = line.lstrip(" ").strip()
        if line.startswith("# "):
            return line[2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using\
    {template_path}")

    from_path_md = open(from_path, 'r').read()
    template_file = open(template_path, 'r').read()
    from_path_html = markdown_to_html_node(from_path_md).to_html()
    page_title = extract_title(from_path_md)
    print(from_path_html)
    print(page_title)
    resulting_html = template_file.replace("{{ Title }}", f"{page_title}")
    resulting_html = resulting_html.replace("{{ Content }}", f"{from_path_html}")
    print(resulting_html)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    _, tail = os.path.split(from_path)
    print(tail)
    dest_file_name, _ = tail.split(".")
    print(dest_file_name)
    dest_file_name = dest_file_name + ".html"
    dest_file_path = os.path.join(dest_path, dest_file_name)
    with open(dest_file_path, "w", encoding="utf-8") as f:
        f.write(resulting_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    if not os.path.exists(dir_path_content):
        raise Exception(f"{dir_path_content} does not exist")
    current_files = []
    current_dirs = []
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        print(filename)
        if os.path.isfile(file_path):
            print(file_path)
            current_files.append(file_path)
        if os.path.isdir(file_path):
            print(file_path)
            current_dirs.append(file_path)
    for file in current_files:
        generate_page(file, template_path, dest_dir_path)
        # shutil.copy(file, dest_dir_path)
    for dir in current_dirs:
        _, tail = os.path.split(dir)
        new_dest = os.path.join(dest_dir_path, tail)
        generate_pages_recursive(dir, template_path, new_dest)
