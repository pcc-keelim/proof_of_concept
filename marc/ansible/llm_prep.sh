#!/bin/bash  
  
concat_files() {  
  output_file="output.txt"  
    
  # Empty the output file if it already exists  
  > $output_file  
  
  for file in "$@"; do  
    echo "Processing $file"  
    echo "$file" >> $output_file  
    cat "$file" >> $output_file  
    echo "<<<----END OF FILE---->>>" >> $output_file
    echo "" >> $output_file

  done  
    
  echo "Concatenation done. Output: $output_file"  
}  
  
# Call the function with a list of files  
concat_files .env Dockerfile docker-compose.yaml
