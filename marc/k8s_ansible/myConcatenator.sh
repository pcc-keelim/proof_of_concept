#!/bin/bash

# Check if at least one file is provided
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 output_file file1 [file2 ... fileN]"
  exit 1
fi

# Output file
output_file="$1"
shift  # Remove output file from the arguments list

# Create or clear the output file
> "$output_file"

# Iterate through all the input files
for file in "$@"; do
  if [ -f "$file" ]; then
    # Add file delimiter and file name at the beginning
    echo "======" >> "$output_file"
    echo "File: $file" >> "$output_file"
    echo "======" >> "$output_file"

    # Concatenate the content of the file
    cat "$file" >> "$output_file"

    # Add file delimiter and file name at the end
    echo "" >> "$output_file"  # New line before the footer
    echo "======" >> "$output_file"
    echo "End of: $file" >> "$output_file"
    echo "======" >> "$output_file"
    echo "" >> "$output_file"  # New line after the footer
  else
    echo "File $file not found, skipping..."
  fi
done

echo "All files concatenated into $output_file"
