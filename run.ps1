$dir = ".\output"
if (Test-Path $dir -PathType Container) {
    Remove-Item $dir -Recurse -Force
}

docker build -t script-docker-image .
docker run -d --name script-docker-container script-docker-image
docker logs -f script-docker-container
docker wait script-docker-container > $null 2>&1
docker cp script-docker-container:/script/output $dir > $null 2>&1
docker rm -f script-docker-container > $null 2>&1

pause