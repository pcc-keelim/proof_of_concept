import os
import sys
import mimetypes
from pathlib import Path

class CodeCollector:
    def __init__(self, folders, include_extensions=None, exclude_extensions=None):
        """
        Initializes the CodeCollector.

        :param folders: List of folders to process.
        :param include_extensions: List of file extensions to include.
        :param exclude_extensions: List of file extensions to exclude.
        """
        self.folders = folders
        self.include_extensions = include_extensions if include_extensions is not None else []
        self.exclude_extensions = exclude_extensions if exclude_extensions is not None else []
        self.output_file = Path.home() / 'Downloads' / 'output.txt'

    def is_binary_file(self, filepath):
        """
        Checks if a file is binary.

        :param filepath: Path to the file.
        :return: True if the file is binary, False otherwise.
        """
        # Guess the MIME type of the file
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type is not None:
            return not mime_type.startswith('text')
        else:
            # Fallback: If MIME type is unknown, check for null bytes in the file to determine if it's binary.
            try:
                with open(filepath, 'rb') as file:
                    chunk = file.read(1024)
                    if b'\0' in chunk: # If null byte exists, it's likely a binary file.
                        return True
            except Exception as e:
                print(f"Error reading file {filepath}: {e}", file=sys.stderr)
                return True
            return False # If no null byte is found, assume it is a text file.

    def write_folder_structure(self, output_file):
        """
        Writes the structure of the directories and files (folder hierarchy) to the output file.

        :param output_file: The file object where the folder structure will be written.
        """
        for folder in self.folders:
            output_file.write(f"Folder Structure for: {folder}\n")
            for root, __, files in os.walk(folder):  # Walk through directory tree
                level = root.replace(folder, '').count(os.sep)  # Calculate depth of the folder
                indent = ' ' * 4 * level  # Create indentation based on depth
                output_file.write(f"{indent}{os.path.basename(root)}/\n")  # Write folder name with indent
                subindent = ' ' * 4 * (level + 1)  # Indentation for files within the folder
                for f in files:
                    output_file.write(f"{subindent}{f}\n")  # Write file name under corresponding folder
            output_file.write('\n')  # Add space after each folder structure

    def collect_code(self):
        """
        Collects the content of all specified files from the provided folders and writes them to the output file.
        It also includes the folder structure in the same output file.

        The process includes:
        1. Writing the folder structure of all provided directories.
        2. Writing the contents of each non-binary file in the folder, with a header indicating the file's path.
        """
        # First, open the output file for writing and write the folder structure
        with open(self.output_file, 'w', encoding='utf-8') as output:
            self.write_folder_structure(output)  # Write folder structure to output file

        # Then, open the output file in append mode to add file contents
        with open(self.output_file, 'a', encoding='utf-8') as output:
            for folder in self.folders:
                # Walk through each directory and get all files
                for root, __, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)  # Full path to the file
                        extension = os.path.splitext(file)[1].lower()  # Get file extension

                        # Skip binary files
                        if self.is_binary_file(file_path):
                            continue

                        # Skip files not in include list (if provided) and those in exclude list
                        if self.include_extensions and extension not in self.include_extensions:
                            continue
                        if extension in self.exclude_extensions:
                            continue

                        try:
                            # Read file content and write it to the output file with a header
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            # Add a header with the file path to distinguish it in the output file
                            header = f"#### {file_path} ####\n"
                            output.write(header)
                            output.write(content)
                            output.write('\n\n')  # Add extra space after file content
                        except Exception as e:
                            # Handle and report errors in case of issues reading a file
                            print(f"Could not read file {file_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Example usage: Define folders to process
    folders_to_process = [
        '/home/marckeelingiv/dev/proof_of_concept/marc/ansible_bash',
        '/home/marckeelingiv/dev/proof_of_concept/marc/py_ca'
    ]
    # Include all files by default, exclude typical binary files
    include = []  # Include all by default
    exclude = ['.exe', '.dll']  # Exclude binary files like .exe and .dll by default

    # Create a CodeCollector object with the specified folders and file types
    collector = CodeCollector(
        folders=folders_to_process,
        include_extensions=include,
        exclude_extensions=exclude
    )
     # Collect code and folder structure into the output file
    collector.collect_code()
    # Print success message with the path to the output file
    print(f"Code collected successfully to {collector.output_file}")
