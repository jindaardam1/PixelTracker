# Set console window size
[console]::SetWindowSize(140, 50)

# Set console code page to UTF-8 for better character support
chcp 65001 | Out-Null

# Change directory to the parent directory using Set-Location
Set-Location ..

# Check if colorama is already installed before attempting to install it
if (-not (python -m pip show colorama)) {
    pip install colorama~=0.4.6
}
else {
    Write-Host "Colorama is ready to use"
}

# Check if waitress is already installed before attempting to install it
if (-not (python -m pip show waitress)) {
    pip install waitress==2.1.2
}
else {
    Write-Host "Waitress is ready to use"
}

# Check if Flask is already installed before attempting to install it
if (-not (python -m pip show Flask)) {
    pip install Flask==3.0.0
}
else {
    Write-Host "Flask is ready to use"
}

# Use Waitress to serve the Flask app on all available network interfaces at port 5000
waitress-serve --listen=0.0.0.0:5000 src.core.main:app

# Pause to keep the console window open after the script finishes
Pause
