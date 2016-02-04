#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

bam_list = 'data/2-bam.list'

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

  ## pileup
  ##    inputs: BAMs in GCS, reference material on PD
  ##    outputs: PD with GLF for each sample x region

  # write startup script for each sample x region node

  # create instances for each sample x region
  #   startup script:
  #     1. create and attach output disk
  #     2. attach disk with reference data 
  #     3. execute pileup command
  #     4. detach output and reference disks
  #     5. destroy yourself

  

  ## glfmultiples
  ##    inputs: glf for each sample x region on separate PD
  ##    outputs: PD with vcf for each region

  # write startup script for each region

  # create instances for each region
  #   startup script:
  #     1. attach input disk for each sample in RO mode
  #     2. create and attach output disk
  #     3. execute glfmultiples command 
  #     4. detach input and output disks
  #     5. destroy input disks
  #     6. destroy yourself

if __name__ == '__main__':
  __main__()
