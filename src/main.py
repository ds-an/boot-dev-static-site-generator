from site_generation import copy_source_to_dest_dir, generate_page, generate_pages_recursive

def main():
    copy_source_to_dest_dir("static", "public")
    # generate_page("content/index.md", "template.html", "public")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty")
    # generate_page("content/contact/index.md", "template.html", "public/contact")
    generate_pages_recursive("content", "template.html", "public")
    
main()
