# Set console window size
[console]::SetWindowSize(140, 50)

# Set console code page to UTF-8 for better character support
chcp 65001 | Out-Null

# Change directory to the parent directory using Set-Location
Set-Location ..

# Use Waitress to serve the Flask app on all available network interfaces at port 5000
waitress-serve --listen=0.0.0.0:5000 src.main:app

# Pause to keep the console window open after the script finishes
Pause
