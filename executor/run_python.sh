#!/bin/bash

# Check if the first argument (Python script path) is provided
if [ $# -lt 1 ]; then
  echo "Usage: $0 <python_script_path>"
  exit 1
fi

# Get the current working directory
current_path=$(pwd)

# Get the absolute path of the Python script
python_script_path=$(realpath "$1")

# Determine the relative path of the Python script to the current working directory
relative_path=$(realpath --relative-to="$current_path" "$python_script_path")

# Replace '/' characters with '.' characters in the relative path
relative_path=${relative_path//\//.}

# Remove the '.py' extension from the relative path
relative_path=${relative_path%.py}
echo $relative_path

# Run the Python script using the -m syntax and the modified relative path
python3 -m "$relative_path"
