#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from googleapiclient_create_destroy_instance import create_instance
from googleapiclient_create_destroy_instance import check_instance

import subprocess
import time

# number of concurrent instances reading from a disk
instance_num = 100

def __main__():
    """
    Test how read performance for a persistent disk scales as it is attached to more
    and more virtual machines.

    Input: 1 low-coverage chr11 BAM file on a 200GB standard persistent disk
    Metrics: time samtools flagstat on random5MB region access

    Try 1 attached machine, 10 attached machines, and 100 attached machines

    Consider google cloud monitoring tools for performance metrics.

    Helpful Documentation:
    * https://google-api-client-libraries.appspot.com/documentation/compute/v1/python/latest/
    * https://developers.google.com/api-client-library/python/
    """

    # instantiate our google services
    default_project = 'friendly-medley-91616'
    default_zone = 'us-central1-a'
    credentials = GoogleCredentials.get_application_default()
    gce = discovery.build('compute', 'v1', credentials=credentials)

    print 'Provisioning machines...'

    # create instances
    instances = list()
    for reader_vm in xrange(instance_num):
        # create instance with startup script
        #   attach input disk
        #   format and mount disk
        instance_name = 'reader-{}'.format(reader_vm)
        create_operation = create_instance(compute=gce,
                                           project=default_project,
                                           zone=default_zone,
                                           name=instance_name,
                                           input_disk='hg00096-chr20-bam',
                                           mount_point='/home/trubetsk/input-data/')
        instances.append(instance_name)
        time.sleep(1)


    for instance in instances:
        instance_found = check_instance(name=instance, compute=gce, project=default_project, zone=default_zone)
        if not instance_found:
            Exception('Instance not found.')
    print '\t Done.'

    print 'Executing samtools on each machine...'
    # execute our samtools command on each instance
    for instance in instances:
        flagstat_cmd = ('/home/trubetsk/flagstat_random_5mb.py '
                    '--vm-name {vm_name} --instance-number {instance_num} '.format(vm_name=instance, instance_num=instance_num))
        gcloud_cmd = 'gcloud compute ssh trubetsk@{instance} --project {project} --zone {zone} --command \'{command}\' &'.format(instance=instance,
                                                                                                        project=default_project,
                                                                                                        zone=default_zone,
                                                                                                        command=flagstat_cmd)
        print gcloud_cmd
        subprocess.call(gcloud_cmd, shell=True)

    print '\t Done'

if __name__ == '__main__':
    __main__()

