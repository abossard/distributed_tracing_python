#!/bin/sh
for ARCH in amd64 arm64; do
    for x in $(ls -1 *.py | sed 's/\..*//'); do
        echo "Building $x"
        docker buildx build \
            --push \
            --platform linux/$ARCH \
            --tag $ACR/py/$x\:latest \
            --build-arg MODULE=$x .
    done
done