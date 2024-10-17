# key-api

### Running in docker
Docker is run by following command on Unraid server:

---
```
docker run
  -d
  --name='key-api'
  --net='reverseproxy'
  -e TZ="Europe/Warsaw"
  -e HOST_OS="Unraid"
  -e HOST_HOSTNAME="nas"
  -e HOST_CONTAINERNAME="key-api"
  -l net.unraid.docker.managed=dockerman
  -l net.unraid.docker.icon='https://d1q6f0aelx0por.cloudfront.net/product-logos/library-python-logo.png'
  -v '/mnt/user/appdata/key-api':'/app':'rw' 'python:latest' /bin/bash /app/init.sh
```
---

According to above it is required to add following options in Unraid docker configuration:
```
Repository: python:latest
Icon URL: https://d1q6f0aelx0por.cloudfront.net/product-logos/library-python-logo.png
Post Arguments: /bin/bash /app/init.sh
mount folder -v: /mnt/user/appdata/key-api to: /app inside docker
```
