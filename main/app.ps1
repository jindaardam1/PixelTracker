function Install-Package {
    param(
        [string]$packageName,
        [string]$packageVersion
    )

    if (-not (python -m pip show $packageName)) {
        pip install "$packageName==$packageVersion"
    }
    else {
        Write-Host "$packageName is ready to use"
    }
}

# Set console window size
[console]::SetWindowSize(140, 50)

# Set console code page to UTF-8 for better character support
chcp 65001 | Out-Null

# Change directory to the parent directory using Set-Location
Set-Location ..

# Using the function to install Colorama
Install-Package -packageName "colorama" -packageVersion "0.4.6"

# Using the function to install Waitress
Install-Package -packageName "waitress" -packageVersion "2.1.2"

# Using the function to install Flask
Install-Package -packageName "Flask" -packageVersion "3.0.0"

# Using the function to install tabulate
Install-Package -packageName "tabulate" -packageVersion "0.9.0"

# Using the function to install tabulate
Install-Package -packageName "pythonnet" -packageVersion ""


# Use Waitress to serve the Flask app on all available network interfaces at port 5000
waitress-serve --listen=0.0.0.0:5000 src.core.main:app

# Pause to keep the console window open after the script finishes
Pause