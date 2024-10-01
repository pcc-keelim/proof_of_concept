#!/bin/bash  

concat_files() {  
  output_file="output.txt"  
    
  # Empty the output file if it already exists  
  > "$output_file"  
  
  for path in "$@"; do  
    if [[ -f "$path" ]]; then  # Check if the path is a file
      echo "Processing $path"  
      echo "$path" >> "$output_file"  
      cat "$path" >> "$output_file"  
      echo "<<<----END OF FILE---->>>" >> "$output_file"
      echo "" >> "$output_file"
    elif [[ -d "$path" ]]; then  # Check if the path is a directory
      echo "Processing directory $path"
      find "$path" -type f | while read -r file; do
        echo "Processing $file"
        echo "$file" >> "$output_file"
        cat "$file" >> "$output_file"
        echo "<<<----END OF FILE---->>>" >> "$output_file"
        echo "" >> "$output_file"
      done
    else
      echo "Warning: $path does not exist."  # Warn if the path doesn't exist
    fi
  done  
    
  echo "Concatenation done. Output: $output_file"  
}  

# Call the function with a list of files and/or directories passed as arguments
concat_files "$@"