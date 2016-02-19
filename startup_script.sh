#!/bin/bash

# Get our start-up variables from the meta-data server
IMAGE_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/image-name -H "X-Google-Metadata-Request: True")
ZONE=$(curl http://metadata/computeMetadata/v1/instance/attributes/zone -H "X-Google-Metadata-Request: True")
PROJECT=$(curl http://metadata/computeMetadata/v1/instance/attributes/project -H "X-Google-Metadata-Request: True")

INPUT_DISK_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/input-disk-name -H "X-Google-Metadata-Request: True")
MOUNT_POINT=$(curl http://metadata/computeMetadata/v1/instance/attributes/mount-point -H "X-Google-Metadata-Request: True")

# attach input disk
gcloud compute instances attach-disk $IMAGE_NAME   \
    --disk $INPUT_DISK_NAME                        \
    --device-name "input"                          \
    --zone $ZONE                                   \
    --mode "ro"

# mount input disk
sudo mkdir $MOUNT_POINT
sudo mount -o ro /dev/disk/by-id/google-input $MOUNT_POINT
sudo chmod -R 777 $MOUNT_POINT

# clone our git repository
sudo apt-get install -y git
git clone https://github.com/vtrubets/gcloud_sequencing_pipelines.git /home/trubetsk/gcloud_sequencing_pipelines/
chmod -R 777 /home/trubetsk/gcloud_sequencing_pipelines/