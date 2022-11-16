import inversion_utils as iu
import argparse

# idea: I want to call this script for each iteration of the inverison.
# this means this won't include wrapper, just moving files, renaming, etc...
# I'll need: 1. data name
#            2. path to SIR output
#            3. path to where to save outputs
#            4. Summary folder
#            5. iteration # (for the summary file)
#            6. SIR summry file (to check whether errored.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_name',
                        dest='data_name',
                        type=str,
                        required=True,
                        help='name of inversion for naming.')
    parser.add_argument('--path_to_SIR_output',
                        dest='path_to_SIR_output',
                        type=str,
                        required=True,
                        help='path to SIR output.')
    parser.add_argument('--path_to_assembled_fits',
                        dest='path_to_assembled_fits',
                        type=str,
                        required=True,
                        help='path to SIR output.')
    parser.add_argument('--output_folder',
                        dest='output_folder',
                        type=str,
                        required=True,
                        help='output folder for inversion results')
    parser.add_argument('--sir_summary_file',
                        dest='sir_summary_file',
                        type=str,
                        required=True,
                        help='SIR summary filepath and file.')

    arg = parser.parse_args()

    data_name = arg.data_name
    path_to_assembled_fits = arg.path_to_assembled_fits
    path_to_SIR_output = arg.path_to_SIR_output
    output_folder = arg.output_folder
    summary_folder = arg.sir_summary_file

    # idea with this script: I want this to run after 2x inversions. it should move output,

    iu.move_output(path_to_SIR_output,
                   output_folder,
                   data_name)
    iu.edit_latest_data(path_to_assembled_fits,
                        data_name)
    iu.edit_summary(summary_folder=summary_folder,
                    summary_file='inversion_summary.txt',
                    iteration=2,
                    error=False,
                    data_name=data_name)


if __name__ == '__main__':
    main()
