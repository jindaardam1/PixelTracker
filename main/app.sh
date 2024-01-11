#!/bin/bash

# Function to install Python packages
function install_package {
    local packageName=$1
    local packageVersion=$2

    # Check if the package is already installed
    if ! python3 -m pip show "$packageName" &>/dev/null; then
        # Install the package with the specified version
        pip3 install "$packageName==$packageVersion"
    else
        # Print a message if the package is already installed
        echo "$packageName is ready to use"
    fi
}

# Set console window size
printf '\e[8;50;140t'

# Set console code page to UTF-8 for better character support
export LANG=en_US.UTF-8

# List of packages to install (format: "package_name:version")
packages=("colorama:0.4.6" "waitress:2.1.2" "Flask:3.0.0" "tabulate:0.9.0" "requests:2.31.0")

# Install the specified packages
for package in "${packages[@]}"; do
    IFS=':' read -ra parts <<< "$package"
    install_package "${parts[0]}" "${parts[1]}"
done

# Execute the specified executables in the background
for executable in "PixelTrackerDBQuery" "EmailServerPlaceHolder"; do
    ./"$executable" &
done

# Change to the parent directory
cd ..

# Use Waitress to serve the Flask app on all available network interfaces on port 5000
waitress-serve --listen=0.0.0.0:5000 src.core.main_tracker:app


# Pause to keep the console window open after the script finishes
read -r -p "Press Enter to exit"
