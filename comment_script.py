import os  
import argparse  
import subprocess  
import sys
from pdb import set_trace
  
def generate_keywords(prefix):  
    return [f"gc__{prefix}_offset", f"gc__{prefix}_reg", f"gc__{prefix}_"]  
  
def p4_edit(file_path):  
    try:  
        subprocess.run(['p4', 'edit', file_path], check=True)  
    except subprocess.CalledProcessError as e:  
        print(f"Failed to edit file {file_path}: {e}")  
  
def search_and_comment(directory, prefix):  
    keywords = generate_keywords(prefix)  

    # add the extensions
    comment_symbols = {  
        '.h': '//',  
        '.cpp': '//',  
        '.vh': '//',  
        '.svh': '//',  
        '.v': '//',  
        '.sv': '//',  
        '.c': '//',
        'dpl': '//',
        '.txt': '#',    
    }  
  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            file_path = os.path.join(root, file)  
            file_extension = os.path.splitext(file)[1]  
            
            if file_extension in comment_symbols:  
                try:  
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:  
                        lines = f.readlines()  
                except Exception as e:  
                    print(f"Error reading file {file_path}: {e}")  
                    continue  
  
                contains_keyword = any(any(keyword in line for keyword in keywords) for line in lines)  
  
                if contains_keyword:  
                    p4_edit(file_path)  
  
                    with open(file_path, 'w', encoding='utf-8') as f:  
                        for line in lines:  
                            if any(keyword in line for keyword in keywords) and not line.lstrip().startswith(comment_symbols[file_extension]):  
                                line = comment_symbols[file_extension] + ' ' + line  
                            f.write(line)  
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Search files and comment lines containing specific keywords.')  
    parser.add_argument('-d', '--directory', type=str, required=True, help='The directory to search for files.')  
    parser.add_argument('-b', '--block', type=str, required=True, help='The prefix to generate keywords.')  
  
    args = parser.parse_args()  
  
    search_and_comment(args.directory, args.block)  
