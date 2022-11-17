#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --partition=amilan
#SBATCH --account=ucb-general
#SBATCH --time=01:30:00
#SBATCH --job-name=unpacking_nov15
#SBATCH --output=/projects/jacr0382/out/unzip_v1.%j.out

module purge
source /curc/sw/anaconda3/latest


# note for self: takes ~45 min to do a 'full' zip.

# unpack all the data: run only once
python run_sequence.py --zip_name "fg_download.php?cmd=download&zip=635858ae18ad9.zip&uid=1227" \
                       --zip_filepath "/scratch/alpine/jacr0382/HOP79_zips/" \
		       --assembled_filepath "/scratch/alpine/jacr0382/HOP79/"

