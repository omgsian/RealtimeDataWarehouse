# Default recipe to display when just is called without arguments
default: 
    just --list

# Build with progress output
build-progress: 
    docker-compose build --no-cache --progress=plain

# Stop and remove containers, networks, volumes, and images created by up
down: 
    docker-compose down --volumes

# Run the cluster in detached mode
upb:
    docker-compose up --build -d
    
up:
    docker-compose up -d
# Stop services
stop: 
    docker-compose stop
