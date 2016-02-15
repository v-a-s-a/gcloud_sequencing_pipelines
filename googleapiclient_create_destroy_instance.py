#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import time
import os


def list_instances(compute, project, zone):
    response = compute.instances().list(project=project, zone=zone).execute()
    if response.get('items'):
        result = { x['name']:x['status'] for x in response['items'] }
    else:
        result = {}
    return result

def is_input_disk_attached(name, compute, project, zone):
    response = compute.instances().list(project=project, zone=zone).execute()
    print '\tChecking disk for {name}'.format(name=name)
    if response.get('items'):
        disks = { x['name']:x['disks'] for x in response['items'] }

        for disk in disks.get(name):
            if disk.get('deviceName') == 'input':
                result = True
            else:
                result = False
    else:
        result = False
    return result

def create_instance(compute, project, zone, name, input_disk='', mount_point=''):
    source_disk_image = \
      "projects/friendly-medley-91616/global/images/random-region-reader"
    machine_type = "zones/{zone}/machineTypes/n1-standard-1".format(zone=zone)

    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup_script.sh'), 'r').read()
    shutdown_script = open(
    os.path.join(
        os.path.dirname(__file__), 'shutdown_script.sh'), 'r').read()

    config = {
    'name': name,
    'machineType': machine_type,
    # Specify the boot disk and the image to use as a source.
    'disks': [
        {
        'boot': True,
        'autoDelete': True,
        'initializeParams': {
            'sourceImage': source_disk_image,
            }
        }
    ],
    # Specify a network interface with NAT to access the public
    # internet.
    'networkInterfaces': [{
        'network': 'global/networks/default',
        'accessConfigs': [
            {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
    # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
        'email': 'default',
        'scopes': [
            'https://www.googleapis.com/auth/cloud-platform'
            ]
        }],
    # Metadata is readable from the instance and allows you to
    # pass configuration from deployment scripts to instances.
    'metadata': {
    'items': [{
        # Startup script is automatically executed by the
        # instance upon startup.
        'key': 'startup-script',
        'value': startup_script
        }, {
        'key': 'shutdown-script',
        'value': shutdown_script
        }, {
        'key': 'image-name',
        'value': name
        }, {
        'key': 'input-disk-name',
        'value': input_disk
        }, {
        'key': 'mount-point',
        'value': mount_point
        }, {
        'key': 'zone',
        'value': zone
        }, {
        'key': 'project',
        'value': project
        }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()


def attach_disk(compute, project, zone, instance_name, disk, device_name):
    config = {
    "deviceName": device_name, # Specifies a unique device name of your choice that is reflected into the /dev/disk/by-id/google-* tree of a Linux operating system running within the instance. This name can be used to reference the device for mounting, resizing, and so on, from within the instance.
    "kind": "compute#attachedDisk", # [Output Only] Type of the resource. Always compute#attachedDisk for attached disks.
    "autoDelete": False, # Specifies whether the disk will be auto-deleted when the instance is deleted (but not when the disk is detached from the instance).
    "index": 1, # Assigns a zero-based index to this disk, where 0 is reserved for the boot disk. For example, if you have many disks attached to an instance, each disk would have a unique index number. If not specified, the server will choose an appropriate value.
    "boot": False, # Indicates that this is a boot disk. The virtual machine will use the first partition of the disk for its root filesystem.
    "mode": "READ_ONLY", # The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode.
    "type": "PERSISTENT", # Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.
    "source": "https://www.googleapis.com/compute/v1/projects/{project_name}/zones/{zone_name}/disks/{disk_name}".format(project_name=project,zone_name=zone, disk_name=disk) # Specifies a valid partial or full URL to an existing Persistent Disk resource. This field is only applicable for persistent disks.
    }
    return compute.instances().attachDisk(
          instance=instance_name,
          project=project,
          zone=zone,
          body=config).execute()


def delete_instance(compute, project, zone, name):
  return compute.instances().delete(
      project=project,
      zone=zone,
      instance=name).execute()


def check_instance(name, compute, zone, project, tries = 100):
    """
    Returns: Bool. True if instance exists in zone, false if it does not.
    """
    for i in xrange(tries):
        instances = list_instances(compute=compute, project=project, zone=zone)
        for j in xrange(10):
            if instances.get(name) == 'RUNNING':
                # check whether the persistent input disk has been attached
                if is_input_disk_attached(name=name, compute=compute, project=project, zone=zone):
                    return True
        else:
            res = False
        time.sleep(1)

    return res


def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
                    project=project,
                    zone=zone,
                    operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)


def __main__():
  '''
  Create and destroy a google compute engine instance.
  '''

  default_project='friendly-medley-91616'
  default_zone='us-central1-a'

  # using application default credentials
  credentials = GoogleCredentials.get_application_default()
  
  # register an instance of the google compute engine service
  compute = discovery.build('compute', 'v1', credentials=credentials)

  # create a test instance
  print 'Creating an instance for you.'
  operation = create_instance(compute, project=default_project, zone=default_zone, name='toner-low', bucket='')
  wait_for_operation(compute, project=default_project, zone=default_zone, operation=operation['name'])
  print 'Instance created!\n'

  # list instances
  instances = list_instances(compute, project=default_project, zone=default_zone)
  print('Instances in project %s and zone %s:' % (default_project, default_zone))
  for instance in instances:
    print(' - ' + instance['name'])
  print ''

  # delete created instance
  print 'Delete the test instance.'
  operation = delete_instance(compute, project=default_project, zone=default_zone, name='toner-low')
  wait_for_operation(compute, project=default_project, zone=default_zone, operation=operation['name'])
  print 'Instance deleted.'

if __name__ == '__main__':
    pass
    #__main__()
