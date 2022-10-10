# TODO:
#   1. assembling datasets from scans
#   2. unzipping and deleting scans
#       - problem: zips are buried in strangely named folders...
#   3. modifying EITHER initialization.input OR filenames

import numpy as np
import astropy.io.fits as fits
import os
import sys

# TODO:
#  Add output filename & filepath to hinode_assemble:
def hinode_assemble(output_name, input_filepath='.', output_filepath='.'):

    """
        Hinode Assemble: given a filepath and a filename, unzip the file, assemble the data (via calling hinode_assemble),
                         and finally, delete the folder and scans.

                Inputs: 1. output_name: the name of the saved fits file
                        2. input_filepath: the filepath to the fits slit scans. default = '.'
                        3. output_filepath: where to put saved fits file. default = '.'
                Outputs: saves an assembled fits file, normalized and in SIR format.
        """

    filenames = []
    input_format = 'S*.fits'

    for file in sorted(os.listdir(input_filepath)):
        if file.endswith(input_format):
            print(file)
            filenames.append(file)
    print(len(filenames))

    print(filenames[0])
    stokes = fits.open(filenames[0])[0].data
    print(stokes.shape)
    SLITSIZE = stokes.shape[1]  # if the data is in a different format, this is the one to check first.
    print('Slitlength = ', SLITSIZE)
    stokes = stokes.reshape(1, 4, SLITSIZE, 112)

    filenames = filenames[1:]
    for name in filenames:
        stokes_temp = fits.open(name)[0].data
        stokes_temp = stokes_temp.reshape(1, 4, SLITSIZE, 112)
        stokes = np.concatenate((stokes, stokes_temp), axis=0)

    stokes = stokes.transpose(2, 0, 1, 3)
    print(stokes.shape)

    output = sys.argv[1]
    hdu = fits.PrimaryHDU(stokes)
    hdu.header = fits.open(name)[0].header
    hdu.writeto(output, overwrite=True)


import zipfile

def unzip(zip_name, assembled_filepath='./assembed_fits/', remove_zips=False, path_to_zip='.'):

    """
    Unzip: given a filepath and a filename, unzip the file, assemble the data (via calling hinode_assemble),
            and finally, delete the folder and scans.

            Inputs: 1. assembled_filepath: filepath to send assembled to
                    2. remove_zips: whether to remove zips, default is False
                    3. directory_to_extract_to: directory to which extract slits. this needs to be removed later....
                    4. zip_name
                    5. path_to_zip
            Outputs: saves a fits file via assemble to assembled_filepath
    """

    with zipfile.ZipFile(path_to_zip + zip_name, 'r') as zip_ref:
        temp_slit_folder_name = path_to_zip + 'temp'
        # create a temporary folder to put fits slits into:
        os.mkdir(temp_slit_folder_name)
        zip_ref.extractall(temp_slit_folder_name)

    try:
        os.mkdir(assembled_filepath)
    except:
        print('Assembled Fits Folder Already Exits.')
    hinode_assemble(output_name=zip_name + '.fits',
                    input_filepath=temp_slit_folder_name,
                    output_filepath=assembled_filepath)
    # remove the slits:
    os.remove(temp_slit_folder_name)

    # remove the zips:
    if remove_zips:
        os.remove(path_to_zip + zip_name)


def assemble_many(filepath_to_zips):
    """ Assemble Many: given a folder containing many zip files,
                       unzip and assemble them all.

                       Inputs: 1. filepath_to_zips
                               2. fits_slits_path
                               3. assembled_fits_path
    """


    zips = []

    for file in sorted(os.listdir(filepath_to_zips)):
        if file.endswith(".zip"):
            print(file)
            zips.append(file)
    print(len(zips))

    for zip in zips:
        # for zip names, I want to call zip for each, which should
        # and then assemble slits into a DIFFERENT directory each file
        unzip(zip_name=zip, path_to_zip=filepath_to_zips)
