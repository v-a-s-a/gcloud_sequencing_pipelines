#!/usr/bin/env python

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

def __main__():
  '''
  Trying out the basics of apache libcloud with google.

  The idea behind using libcloud is it provides a uniform interface to amazon and
  google. The only thing to check is that the storage services can be swapped out
  in a similar way.
  '''
  ## try registering your service account
  ComputeEngine = get_driver(Provider.GCE)
  gce_driver = ComputeEngine('1008716305589-i8l6q0q8d8egnmbklpnbqll1vikgppb3@developer.gserviceaccount.com',
     '/Users/vasya/Projects/boehnkelab/google-gotcloud/auth/gotGoogleCloud-7882344317db.pem',
     project='friendly-medley-91616',
     datacenter='us-central1-a')

  ## try creating and a toy instance
  base_name = 'libcloud-test'
  size = next((size for size in gce_driver.list_sizes() if size.name == 'f1-micro'))
  location = next((location for location in gce_driver.list_locations() if location.name == 'us-central1-a' ))
  image = gce_driver.ex_get_image('debian-7')
  number = 2
  multi_nodes = gce_driver.ex_create_multiple_nodes(base_name=base_name,
                                                    size=size,
                                                    image=image,
                                                    number=number,
                                                    location=location,
                                                    ex_tags=['libcloud'],
                                                    ex_disk_auto_delete=True)
  for node in multi_nodes:
    if node.error:
      print 'Failed to create node {0}s '.format(node.name)
      print '\tMessage: {message}'.format(**node.error)

  ## try creating/attaching a persistent disk
  
  ## try detaching/destroying a persistent disk

  ## destroy the toy instance
  result = gce.ex_destroy_multiple_nodes(multi_nodes)
  for i, success in enumerate(result):
    if success:
        display('   Deleted %s' % del_nodes[i].name)
    else:
        display('   Failed to delete %s' % del_nodes[i].name)
  


if __name__ == '__main__':
  __main__()

