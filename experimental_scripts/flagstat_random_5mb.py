#!/usr/bin/env python

import random
import os
import argparse


def __main__(vm_name, instance_num, num_regions):
    """
    Simple script to process a set of random 5MB regions on across the genome using samtools flagstat.

    This script is a part of testing multiple persistent disk connections

    Returns: None

    """

    for i in xrange(num_regions):
        # select a random 5MB region to pull reads from
        regions = {line.split()[0]:line.split()[1] for line in open('data/hs37d5.fa.fai')}
        rnd_chr = random.choice([str(x) for x in xrange(1,23)])
        rnd_start = random.randrange(1, regions[rnd_chr])
        rnd_end = rnd_start + 10000000

        # create and execute samtools command
        region = '{chr}:{start}-{end}'.format(chr=rnd_chr, start=str(rnd_start), end=str(rnd_end))
        samtools_bin = '/home/trubetsk/samtools'
        bam_path = '/home/trubetsk/input-data/HG00096.chrom11.ILLUMINA.bwa.GBR.low_coverage.20120522.bam'
        gcs_log = 'gs://variant-calling/{run_id}_{region}_{num_jobs}-instance.log'.format(run_id=vm_name,
                                                                                          num_jobs=instance_num,
                                                                                          region=i)
        samtools_cmd = ('{samtools_bin} view -bh {bam_path} {region} | '
                        '/usr/bin/time -f "realtime:%es\nCPU:%P" -o /dev/stdout {samtools_bin} flagstat - | '
                        'gsutil cp - {gcs_log} ')
        os.system(samtools_cmd.format(region=region,samtools_bin=samtools_bin, bam_path=bam_path, gcs_log=gcs_log))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--vm-name', dest='vm_name', help='The name of the VM on which the command is executed.')
    parser.add_argument('--instance-number', dest='instance_num', help='Number of concurrent instances being tested.')
    parser.add_argument('--region-number', dest='num_regions', help='Number of regions to sequentially read from.')
    args = parser.parse_args()
    __main__(args.vm_name, args.instance_num, args.num_regions)