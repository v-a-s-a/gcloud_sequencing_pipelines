#!/bin/bash

# Get our start-up variables from the meta-data server
IMAGE_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/image-name -H "X-Google-Metadata-Request: True")
ZONE=$(curl http://metadata/computeMetadata/v1/instance/attributes/zone -H "X-Google-Metadata-Request: True")
PROJECT=$(curl http://metadata/computeMetadata/v1/instance/attributes/project -H "X-Google-Metadata-Request: True")

INPUT_DISK_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/input-disk-name -H "X-Google-Metadata-Request: True")
MOUNT_POINT=$(curl http://metadata/computeMetadata/v1/instance/attributes/mount-point -H "X-Google-Metadata-Request: True")

# unmount input disk
sudo umount $MOUNT_POINT

# detach input disk
gcloud compute instances detach-disk $IMAGE_NAME   \
    --disk $INPUT_DISK_NAME                        \
    --zone $ZONE

