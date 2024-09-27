#!/bin/bash  

concat_files() {  
  output_file="output.txt"  
    
  # Empty the output file if it already exists  
  > "$output_file"  
  
  for file in "$@"; do  
    if [[ -f "$file" ]]; then  # Check if the file exists
      echo "Processing $file"  
      echo "$file" >> "$output_file"  
      cat "$file" >> "$output_file"  
      echo "<<<----END OF FILE---->>>" >> "$output_file"
      echo "" >> "$output_file"
    else
      echo "Warning: $file does not exist."  # Warn if the file doesn't exist
    fi
  done  
    
  echo "Concatenation done. Output: $output_file"  
}  

# Call the function with a list of files passed as arguments
concat_files "$@"
