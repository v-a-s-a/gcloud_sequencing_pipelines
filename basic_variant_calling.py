#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import itertools

bam_list = 'data/2-sample_1000G_phase3_low-cov_gcs.list'

def __main__():
  '''
  The most basic variant calling pipeline:

  BAM -> GLF -> VCF

  This is parallelized by sample and region.

  Assuming:
    * one BAM per sample
    * no error handling
  '''

  ## setup
  # register a compute engine service
  credentials = GoogleCredentials.get_application_default()
  compute = discovery.build('compute', 'v1', credentials=credentials)

  # read in bam files
  sample_bams = { x.strip().split()[0]:x.strip().split()[1] for x in open(bam_list) }

  # set up regions
  #   we are testing with two random 5MB regions
  regions = [ {'chr':'chr20', 'start':11000001, 'end':16000000},
              {'chr':'chr20', 'start':36000001, 'end':41000001} ]

  ## pileup
  ##    inputs: BAMs in GCS, reference material on PD
  ##    outputs: PD with GLF for each sample x region

  region_names = [ '{0}-{1}-{2}'.format(x['chr'], str(x['start']), str(x['end'])) for x in regions ]
  output_disks = [ '{0}-{1}'.format(x) for x in itertools.product(sample_bams.keys(), region_names) ]

  # write startup script for each sample x region node
  #   startup script:
  #     1. create and attach output disk
  #     2. attach disk with reference data 
  #     3. execute pileup command
  #     4. detach output and reference disks
  #     5. destroy yourself

  # create instances for each sample x region

  

  ## glfmultiples
  ##    inputs: glf for each sample x region on separate PD
  ##    outputs: PD with vcf for each region

  # write startup script for each region
  #   startup script:
  #     1. attach input disk for each sample in RO mode
  #     2. create and attach output disk
  #     3. execute glfmultiples command 
  #     4. detach input and output disks
  #     5. destroy input disks
  #     6. destroy yourself

  # create instances for each region

if __name__ == '__main__':
  __main__()
