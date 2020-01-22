#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/admin/var/www/portofolio
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop testchallenge
docker rm testchallenge
docker rmi hamdiranu/containerd:be2
docker run -d --name testchallenge -p 5000:5000 hamdiranu/containerd:be2