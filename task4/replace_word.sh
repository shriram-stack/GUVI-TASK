#!/bin/bash

input_file="input.txt"
output_file="output.txt"

# Backup the original file
cp "$input_file" "${input_file}.bak"

awk 'NR<5 { print; next }
     /welcome/ { gsub("give", "learning"); print; next }
     { print }' "$input_file" > "$output_file"

echo "✅ Replacement done. Output saved to $output_file"
