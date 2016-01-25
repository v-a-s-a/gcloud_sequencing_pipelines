#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import time

def list_instances(compute, project, zone):
  response = compute.instances().list(project=project, zone=zone).execute()
  if response.get('items'):
    result = response['items']
  else:
    result = []
  return result

def create_instance(compute, project, zone, name, bucket):
  source_disk_image = \
      "projects/debian-cloud/global/images/debian-7-wheezy-v20150320"
  machine_type = "zones/%s/machineTypes/f1-micro" % zone

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
              'https://www.googleapis.com/auth/devstorage.read_write',
              'https://www.googleapis.com/auth/logging.write'
          ]
      }],

  }

  return compute.instances().insert(
      project=project,
      zone=zone,
      body=config).execute()

def delete_instance(compute, project, zone, name):
  return compute.instances().delete(
      project=project,
      zone=zone,
      instance=name).execute()

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
  __main__()
