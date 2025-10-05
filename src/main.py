import os
import shutil

from textnode import TextNode, TextType

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

def main():
    copy_from_to("static","public")
    

main()