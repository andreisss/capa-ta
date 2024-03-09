#!/bin/bash

# Install necessary tools
sudo apt-get update
sudo apt-get install -y jq unzip wget git

# Check for Python3 and Pip3 installation
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Python3 or Pip3 is not installed. Installing them now."
    sudo apt-get install -y python3 python3-pip
fi

echo "Python3 and Pip3 are installed."

# Fetch the latest release of CAPA from GitHub
LATEST_CAPA_URL=$(curl -s https://api.github.com/repos/mandiant/capa/releases/latest | \
                  jq -r '.assets[] | select(.name | endswith("linux.zip")) | .browser_download_url' | \
                  head -n 1)

if [ -z "$LATEST_CAPA_URL" ]; then
    echo "Failed to find the latest CAPA release."
    exit 1
fi

echo "Downloading CAPA from $LATEST_CAPA_URL"

# Download and install CAPA if not already installed
CAPA_BIN="/usr/local/bin/capa"
if [ ! -f "$CAPA_BIN" ]; then
    echo "Downloading CAPA from $LATEST_CAPA_URL"
    wget "$LATEST_CAPA_URL" -O capa-latest-linux.zip
    if [ $? -eq 0 ]; then
        sudo unzip capa-latest-linux.zip -d /usr/local/bin/
        sudo chmod +x /usr/local/bin/capa
        rm capa-latest-linux.zip
        echo "CAPA installed successfully."
    else
        echo "Failed to download CAPA."
    fi
else
    echo "CAPA is already installed."
fi

# Create necessary directories if they do not exist
DIRECTORIES=("/tempone" "/opt/capa-rules" "/analysis" "/opt/capa-ta" "/opt/capa-ta/analysis_files")
for DIR in "${DIRECTORIES[@]}"; do
    if [ ! -d "$DIR" ]; then
        echo "Creating directory: $DIR"
        sudo mkdir -p "$DIR"
    else
        echo "Directory $DIR already exists."
    fi
done

# Fetch and install the latest CAPA rules if not already present
if [ ! -d "/opt/capa-rules/.git" ]; then
    echo "Downloading CAPA rules to /opt/capa-rules."
    sudo git clone https://github.com/mandiant/capa-rules.git /opt/capa-rules
else
    echo "CAPA rules are already downloaded."
fi

# Clone your application code into /opt/capa-ta if not already present
if [ ! -d "/opt/capa-ta/.git" ]; then
    echo "Cloning application code to /opt/capa-ta."
    sudo git clone https://github.com/andreisss/capa-ta.git /opt/capa-ta
else
    echo "Application code is already cloned."
fi

# Install Gunicorn and Python requirements if requirements.txt is present
if [ -f "/opt/capa-ta/requirements.txt" ]; then
    echo "Installing Python requirements from requirements.txt"
    pip3 install -r /opt/capa-ta/requirements.txt
else
    echo "No requirements.txt found, skipping Python package installation."
fi

sudo apt install gunicorn -y
echo "Gunicorn installed."

# Reminder to configure and launch the application
echo "Please configure your application with the appropriate paths."
echo "To launch your application with Gunicorn, use: gunicorn -w 4 -b <your_ip>:7665 app:app"
