#!/bin/sh
#SBATCH --nodes=2
#SBATCH --ntasks=48
#SBATCH --time=04:00:00
#SBATCH --job-name=magnetic_nonfiltered_testing_sept8
#SBATCH --partitio=shas
#SBATCH --qos=long
#SBATCH --output=/home/jacr0382/HOP79_summary/full_wrapper_1.%j.out

module purge
module load slurm/alpine
module load gcc
module load openmpi
source /curc/sw/anaconda3/latest

path_to_single_wrapper=$/projects/jacr0382/wrapper_1/
path_to_atmos_wrapper=$/projects/jacr0382/wrapper_2/
path_to_scripts=$/home/jacr0382/research_fall2022/scripts/
path_to_data=$/scratch/alpine/jacr0382/HOP79/
path_to_temp_data=$/scratch/alpine/jacr0382/temp/

# run start inversion python:
current_data=$(python $path_to_scripts\start_inversion.py --path_to_assembled_fits $path_to_data)

# iteration 0:
mv $path_to_data\$current_data $path_to_temp_data\data.fits
python $path_to_single_wrapper\parallel_master_v0.51.py
mv $path_to_single_wrapper\results/inv_res_atmos.fits $path_to_atmos_wrapper\run_files/atmos/atmos.fits

# iteration 1:
python $path_to_atmos_wrapper\parallel_master_v0.51.py
mv $path_to_atmos_wrapper\results/inv_res_atmos.fits $path_to_atmos_wrapper\run_files/atmos/atmos.fits

# iteration 2:
python $path_to_atmos_wrapper\parallel_master_v0.51.py

python $path_to_scripts\end_inversion.py --data_name $current_data \
                                         --path_to_SIR_output $path_to_atmos_wrapper\output \
                                         --path_to_assembled_fits $path_to_data
                                         --output_folder /scratch/alpine/jacr0382/HOP79_results/
                                         --summary_file /home/jacr0382/inversion_summary_nov15.txt

sbatch full_wrapper_2







