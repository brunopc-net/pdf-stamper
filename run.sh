#!/bin/bash

output_dir="./output"

# Check if the output_directory exists, and if it does, remove it
if [ -d "$output_dir" ]; then
    rm -rf "$output_dir"
fi

docker build -t script-docker-image .
docker run -d --name script-docker-container script-docker-image
docker logs -f script-docker-container
docker wait script-docker-container > /dev/null 2>&1
docker cp script-docker-container:/script/output "$output_dir" > /dev/null 2>&1
docker rm -f script-docker-container > /dev/null 2>&1

read -p "Press any key to continue..."
