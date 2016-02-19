#!/usr/bin/env python

import random
import os
import argparse
import subprocess as sp

def __main__(vm_name, instance_num):
    """
    Simple script to process a set of random 5MB regions on across the genome using samtools flagstat.

    This script is a part of testing multiple persistent disk connections

    Returns: None

    """
    rnd_start = random.randrange(1, 130006516)
    rnd_end = rnd_start + 5000000
    region = '11:{start}-{end}'.format(start=str(rnd_start), end=str(rnd_end))
    samtools_bin = '/home/trubetsk/samtools'
    bam_path = '/home/trubetsk/input-data/HG00096.chrom11.ILLUMINA.bwa.GBR.low_coverage.20120522.bam'
    gcs_log = 'gs://variant-calling/{run_id}_{num_jobs}-instance.log'.format(run_id=vm_name, num_jobs=instance_num)
    samtools_cmd = '{samtools_bin} view -bh {bam_path} {region} | /usr/bin/time -f "realtime:%es\nCPU:%P" -o /dev/stdout {samtools_bin} flagstat - | gsutil cp - {gcs_log} &'.format(region=region,
                                                                                                  samtools_bin=samtools_bin,
                                                                                              bam_path=bam_path,
                                                                                              gcs_log=gcs_log)
    os.system(samtools_cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--vm-name', dest='vm_name', help='The name of the VM on which the command is executed.')
    parser.add_argument('--instance-number', dest='instance_num', help='Number of concurrent instances being tested.')
    args = parser.parse_args()
    __main__(args.vm_name, args.instance_num)