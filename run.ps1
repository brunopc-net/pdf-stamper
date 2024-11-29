$output_dir = ".\output"
if (Test-Path $output_dir -PathType Container) {
    Remove-Item $output_dir -Recurse -Force
}

docker build -t script-docker-image .
docker run -d --name script-docker-container script-docker-image
docker logs -f script-docker-container
docker wait script-docker-container > $null 2>&1
docker cp script-docker-container:/script/output $output_dir
docker rm -f script-docker-container > $null 2>&1

pause