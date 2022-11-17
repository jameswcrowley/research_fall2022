import argparse
import inversion_utils as iu


def main():
    """
    This script is run at the beginning of each inversion. It does the following:
    1. if a data_list of all assembled fits files had not been created yet, make it.
    2. find the last non-inverted dataset

    --------------------
    Inputs:
    1. path to assembled fits: this is where the data_list and data is.
    --------------------
    Outputs:
    1. prints the last non-inverted dataset to screen, so it can be saved as a var in bash scripts.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_assembled_fits',
                        dest='path_to_assembled_fits',
                        type=str,
                        required=True,
                        help='Path to assembled fits.')

    arg = parser.parse_args()

    path_to_assembled_fits = arg.path_to_assembled_fits
    # this will only create a list if there isn't one yet.
    iu.create_list(path_to_assembled_fits)

    # get the latest, un-inverted dataset:
    iu.find_latest_data(path_to_assembled_fits)

if __name__ == '__main__':
    main()
