#!/usr/bin/env python

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials



def __main__():
  '''
  Create the processing infrastructure for running BWA on a set of FASTQ files.

  Notes:
    - Input is the same fastq.list used with GotCloud align.

    - Paired fastq files are going to piped in from an HTTP server. See:http://kevin-gattaca.blogspot.com/2013/02/bio-bwa-help-new-alignment-algorithm.html for 'advanced piping'

  '''

  default_project='friendly-medley-91616'
  default_zone='us-central1-a'

  #### fastq setup
  ## TODO: replace this with a fastq.list parser

  #### google compute engine setup
  # using application default credentials
  credentials = GoogleCredentials.get_application_default()
  # register an instance of the google compute engine service
  compute = discovery.build('compute', 'v1', credentials=credentials)

  #### stage bwa step
  # create instance for each readGroup
  # attach reference data disk in ro mode
  # create and attach output persistent disk 

  #### execute bwa step
  # upload and execute script to each execution node

  #### cleanup bwa step
  # detach output data disks
  # detach reference data disk
  # destroy all bwa worker instances
 
  ### stage merge bam step
  
  ### execute merge bam step

  ### cleanup merge bam step
  

if __name__ == '__main__':
 __main__()
