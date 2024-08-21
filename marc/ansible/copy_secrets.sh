#!/bin/bash

# Define the source and destination paths
SOURCE_PATH_pub="$HOME/.ssh/id_rsa.pub"
SOURCE_PATH_private="$HOME/.ssh/id_rsa"
DESTINATION_PATH="./.ssh"

# Check if the source file exists
if [ -f "$SOURCE_PATH_pub" ] && [ -f "$SOURCE_PATH_private" ]; then
    # Create the destination directory if it doesn't exist
    mkdir -p "$DESTINATION_PATH"
    
    # Copy the file
    cp "$SOURCE_PATH_pub" "$DESTINATION_PATH"
    echo "id_rsa.pub has been copied to $DESTINATION_PATH"
    cp "$SOURCE_PATH_private" "$DESTINATION_PATH"
    echo "id_rsa has been copied to $DESTINATION_PATH"
    
else
    echo "Source file $SOURCE_PATH does not exist."
fi
