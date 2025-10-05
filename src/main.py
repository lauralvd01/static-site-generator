import os
import shutil

import splitmarkdown as sp

"""
Takes a source directory and a destination directory.
Deletes all the contents of the destination directory and
copies each file of the source directory in the destination directory.
"""
def copy_from_to(source : str, destination : str, start : bool = True):
    if not os.path.exists(source) or not os.path.exists(destination):
        raise Exception
    
    if start:
        print("Destination directory content :")
        print(" - ",destination," - ")
        print(os.listdir(destination))
        shutil.rmtree(destination)
        os.mkdir(destination)
        print("Content removed :")
        print(" - ",destination," - ")
        print(os.listdir(destination))
    
    listdir = os.listdir(source)
    files = [os.path.join(source,file) for file in listdir if os.path.isfile(os.path.join(source,file))]
    dirs = [dir for dir in listdir if os.path.isdir(os.path.join(source,dir))]
    print("Files to copy from "+source+" to "+destination+" :")
    print(files)
    print("Directories to copy from "+source+" to "+destination+" :")
    print(dirs)
    
    print("Copying files...")
    for file in files:
        shutil.copy(file,destination)
        print(file+" copied from "+source+" to "+destination)
    print("Files copied.")
    
    print("Creating directories...")
    for dir in dirs:
        new_dir = os.path.join(destination,dir)
        os.mkdir(new_dir)
        print(new_dir+" created")
        copy_from_to(os.path.join(source,dir),new_dir,False)
    
    print(source+" fully copied to "+destination+".")
    return

"""
Takes the path of the markdown file to read, of the template html to use and of the html destination file.
Reads the markdown and the template files,
converts the markdown to html and create the
destination file with the template filled with
the markdown title and its translated content.
"""
def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    markdown = ""
    with open(from_path,"r") as markdown_file:
        markdown = markdown_file.read()
    
    template_html = ""
    with open(template_path,"r") as html_file:
        template_html = html_file.read()
    
    markdown_to_node = sp.markdown_to_html_node(markdown)
    markdown_to_html = markdown_to_node.to_html()
    
    title = sp.extract_title(markdown)
    
    template_html = template_html.replace("{{ Title }}",title)
    template_html = template_html.replace("{{ Content }}",markdown_to_html)
    
    os.makedirs(os.path.dirname(dest_path),exist_ok=True)
    with open(dest_path,"w") as final_html_file:
        final_html_file.write(template_html)

def main():
    copy_from_to("static","public")
    generate_page("content/index.md","template.html","public/index.html")
    generate_page("content/blog/glorfindel/index.md","template.html","public/blog/glorfindel/index.html")
    generate_page("content/blog/tom/index.md","template.html","public/blog/tom/index.html")
    generate_page("content/blog/majesty/index.md","template.html","public/blog/majesty/index.html")
    generate_page("content/contact/index.md","template.html","public/contact/index.html")

main()