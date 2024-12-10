#!/bin/bash

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Upgrade pip
pip install --upgrade pip

# Install the required libraries
pip install -r requirements.txt

echo "Virtual environment setup complete and libraries installed."

# Run following command in terminal to setup the environment
#chmod +x setup_env.sh
#./setup_env.sh
