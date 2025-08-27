#!/bin/bash

# Greenhouse API Proxy Development Setup Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Setting up development environment for Greenhouse API Proxy..."

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    print_error "Pipenv is not installed. Please install it first:"
    echo "pip install pipenv"
    exit 1
fi

# Install dependencies
print_status "Installing Python dependencies..."
pipenv install --dev

# Install pre-commit hooks
print_status "Installing pre-commit hooks..."
pipenv run pre-commit install
pipenv run pre-commit install --hook-type commit-msg

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_warning "Creating .env file from template..."
    cat > .env << EOF
# API Configuration
GREENHOUSE_API_KEY=your_api_key_with_colon
GREENHOUSE_API_URL=https://harvest.greenhouse.io/v1

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO

# Storage Configuration
DATA_DIR=data
BATCH_SIZE=100
EOF
    print_warning "Please update the .env file with your actual API key before continuing."
fi

# Create data directories
print_status "Creating data directories..."
mkdir -p data/json data/csv data/logs

# Run initial pre-commit check
print_status "Running initial pre-commit check..."
pipenv run pre-commit run --all-files || true

print_success "Development environment setup completed! 🚀"
print_status "Next steps:"
echo "1. Update .env file with your Greenhouse API key"
echo "2. Activate virtual environment: pipenv shell"
echo "3. Run the application: uvicorn main:app --reload"
echo "4. Or use Docker: docker-compose up --build"
