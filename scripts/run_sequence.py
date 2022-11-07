import SIR_inversion_utils as u
import argparse

def main():
    parser = argparse.ArgumentParser()
    # we learned in lecture that argparse gives helpful errors.
    # so not putting a try/except block around this part intentionally
    parser.add_argument('--zip_name',
                        dest='zip_name',
                        type=str,
                        required=True,
                        help='zip name.')
    parser.add_argument('--zip_filepath',
                        dest='zip_filepath',
                        type=str,
                        required=True,
                        help='zip name.')
    parser.add_argument('--assembled_filepath',
                        dest='assembled_filepath',
                        type=str,
                        required=True,
                        help='Path to save assembled fits.')
    parser.add_argument('--remove_zip',
                        dest='remove_zip',
                        type=str,
                        required=False,
                        help='do you want to remove zip?')

    arg = parser.parse_args()

    zip_name = arg.zip_name
    zip_filepath = arg.zip_filepath
    assembled_filepath = arg.assembled_filepath

    u.unzip(zip_name, assembled_filepath, zip_filepath)

    u.quicklook(assembled_filepath)