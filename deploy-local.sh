#!/bin/bash

echo "🚀 Starting AI Personal Assistant with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker is installed"
echo "📦 Building and starting the application..."

# Build and start with docker-compose
docker-compose up -d --build

echo ""
echo "✅ Application is starting!"
echo ""
echo "🌐 Access your app at: http://localhost:8000"
echo ""
echo "📝 Next steps:"
echo "  1. Open http://localhost:8000 in your browser"
echo "  2. Click '⚙️ Settings' in the navigation"
echo "  3. Enter your API keys"
echo "  4. Click 'Save Configuration'"
echo "  5. Start using your AI assistant!"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop app: docker-compose down"
echo ""
