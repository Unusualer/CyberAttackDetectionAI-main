#!/bin/bash

# Install Poetry (Python dependency management)
curl -sSL https://install.python-poetry.org | python3 -

# Install Node.js and npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 16
nvm use 16

# Install C++ build tools
sudo apt-get update
sudo apt-get install -y build-essential cmake

# Set up backend
cd backend
poetry install

# Set up frontend
cd ../frontend
npm install

# Set up database
cd ../backend
poetry run alembic upgrade head

# Build agent
cd ../agent
mkdir build && cd build
cmake ..
make 