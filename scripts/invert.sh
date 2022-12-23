#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --time=04:00:00
#SBATCH --partition=amilan
#SBATCH --account=ucb-general
#SBATCH --job-name=invert_1_test_v1
#SBATCH --output=/home/jacr0382/HOP79_results/invert_test_v1.%j.out

module purge
module load gcc
module load openmpi
source /curc/sw/anaconda3/latest

path_to_single_wrapper=/projects/jacr0382/wrapper_1/
path_to_atmos_wrapper=/projects/jacr0382/wrapper_2/
path_to_scripts=/home/jacr0382/research_fall2022/scripts/
path_to_data=/scratch/alpine/jacr0382/HOP79/
path_to_temp_data=/scratch/alpine/jacr0382/temp/

# Start Scripts
current_data=$(python /home/jacr0382/research_fall2022/scripts/start_inversion.py --path_to_assembled_fits /scratch/alpine/jacr0382/HOP79/)


# ITERATION 0:
# ------------

# 1. renaming selected dataset as temporary dataset:
mv /scratch/alpine/jacr0382/HOP79/"$current_data" /scratch/alpine/jacr0382/temp/data.fits

# 2. running first inversion:
python /projects/jacr0382/wrapper_1/parallel_master_v0.51.py

# 3. median filtering output:
python /projects/jacr0382/median.py /projects/jacr0382/wrapper_1/results/inv_res_mod.fits /projects/jacr0382/wrapper_2/run_files/atmos/atmos.fits

# ITERATION 1:
# ------------

# 1. running inversion:
python /projects/jacr0382/wrapper_2/parallel_master_v0.51.py

# 2. median filtering output:
python /projects/jacr0382/median.py /projects/jacr0382/wrapper_2/results/inv_res_mod.fits /projects/jacr0382/wrapper_2/run_files/atmos/atmos.fits

# ITERATION 2:
# ------------

# 1. running inversion:
python /projects/jacr0382/wrapper_2/parallel_master_v0.51.py


# End Scripts:
# ------------
python /home/jacr0382/research_fall2022/scripts/end_inversion.py --data_name "$current_data" \
                                                                 --path_to_SIR_output $path_to_atmos_wrapper\output \
                                                                 --path_to_assembled_fits $path_to_data \
                                                                 --output_folder /scratch/alpine/jacr0382/HOP79_results/ \
                                                                 --summary_file /home/jacr0382/HOP79_results/

sbatch invert_2.sh