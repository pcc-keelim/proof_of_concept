import os
import argparse

# Function to get user's Downloads directory
def get_downloads_directory():
    """
    Returns the path to the user's 'Downloads' directory.

    This function constructs the full path to the 'Downloads' folder 
    for the current user based on the home directory.

    Returns:
        str: Full path to the user's 'Downloads' directory.
    """
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Function to print the directory tree using relative paths
def print_directory_tree(target_folder):
    """
    Generates a directory tree of the target folder using relative paths.

    This function recursively walks through the target folder, printing 
    directories and their files in a hierarchical structure.

    Args:
        target_folder (str): The target folder to generate the directory tree for.

    Returns:
        str: A formatted string representing the directory tree with relative paths.
    """
    tree = ""
    for root, _, files in os.walk(target_folder):
        # Get the relative path of the current directory
        relative_root = os.path.relpath(root, target_folder)
        if relative_root == ".":
            relative_root = os.path.basename(target_folder)

        # Print directories and files with relative paths
        level = relative_root.count(os.sep)
        indent = ' ' * 4 * level
        tree += f"{indent}{relative_root}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            tree += f"{sub_indent}{f}\n"
    return tree

# Function to recursively gather file contents using relative paths
def gather_files_contents(target_folder, output_file):
    """
    Gathers the contents of all files in a folder recursively and combines them 
    into a single output file. It also prints the directory tree at the top of 
    the output file.

    Args:
        target_folder (str): The target folder from which to gather file contents.
        output_file (str): The output file where the combined contents will be saved.

    Returns:
        None
    """
    with open(output_file, 'w', encoding='utf-8') as combined_file:
        # Print directory tree at the top of the output file
        combined_file.write("Directory Tree:\n")
        combined_file.write(print_directory_tree(target_folder))
        combined_file.write("\n\n")

        for root, _, files in os.walk(target_folder):
            for file_name in files:
                # Get the relative file path
                file_path = os.path.relpath(os.path.join(root, file_name), target_folder)

                # Skip hidden files
                if file_name.startswith('.'):
                    continue

                # Write a header with the relative file path for clarity
                combined_file.write(f"\n\n# FILE: {file_path}\n")
                combined_file.write("#" * (len(file_path) + 7) + "\n\n")

                # Open and write the content of each file
                try:
                    with open(os.path.join(root, file_name), 'r', encoding='utf-8') as file:
                        combined_file.write(file.read())
                        combined_file.write("\n\n")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue

if __name__ == "__main__":
    # Main entry point for the script.

    # This block handles command-line arguments for specifying the target
    # folder and output file. If no arguments are provided, it defaults
    # to the current directory as the target and the '~/Downloads/output.txt'
    # as the output file.

    # The script then verifies that the target folder exists and proceeds
    # to gather the file contents if it does.

    # Set up argument parsing for command-line usage
    parser = argparse.ArgumentParser(
        description="""Gather all files in a folder recursively and
        combine their contents into a single file.""")
    parser.add_argument(
        "target_folder",
        nargs='?',
        default=os.getcwd(),
        help="""Path to the target folder where files are located.
        Defaults to the current directory.""")
    parser.add_argument(
        "output_file", 
        nargs='?',
        default=os.path.join(get_downloads_directory(), "output.txt"),
        help="""Path to the output file where contents will be
        saved. Defaults to '~/Downloads/output.txt'.""")

    args = parser.parse_args()

    # Ensure the target folder exists
    if not os.path.exists(args.target_folder):
        print(f"Error: The folder '{args.target_folder}' does not exist.")
        exit(1)

    # Run the function to gather file contents
    gather_files_contents(args.target_folder, args.output_file)

    print(f"Combined contents of all files from '{args.target_folder}' into '{args.output_file}'.")
