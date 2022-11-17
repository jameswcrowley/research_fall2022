import argparse
import inversion_utils as iu


# I want this script to be run at the beginning of each inversion bash.
# it should take only the path to assembled fits files.

def main():
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
