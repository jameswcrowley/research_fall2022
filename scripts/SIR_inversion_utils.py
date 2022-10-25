# TODO:
#   1. assembling datasets from scans
#   2. unzipping and deleting scans
#       - problem: zips are buried in strangely named folders...
#   3. modifying EITHER initialization.input OR filenames

import numpy as np
import astropy.io.fits as fits
import os
import re
import zipfile
import shutil


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
    input_format = '.fits'

    for file in sorted(os.listdir(input_filepath)):
        if file.endswith(input_format):
            filenames.append(file)
    print(str(len(filenames)) + ' fits slits to assemble.')

    stokes = fits.open(input_filepath + filenames[0])[0].data
    SLITSIZE = stokes.shape[1]  # if the data is in a different format, this is the one to check first.
    print('Slitlength = ', SLITSIZE)
    stokes = stokes.reshape(1, 4, SLITSIZE, 112)

    filenames = filenames[1:]
    for name in filenames:
        stokes_temp = fits.open(input_filepath + name)[0].data
        stokes_temp = stokes_temp.reshape(1, 4, SLITSIZE, 112)
        stokes = np.concatenate((stokes, stokes_temp), axis=0)

    stokes = stokes.transpose(2, 0, 1, 3)
    #print(stokes.shape)

    hdu = fits.PrimaryHDU(stokes)
    hdu.header = fits.open(input_filepath + name)[0].header
    hdu.writeto(output_filepath + output_name, overwrite=True)
    print('Saved fits successfully at : ' + output_filepath + output_name)
    print('-------------------------------')


def unzip(zip_name, assembled_filepath='../assembled_fits/', remove_zips=False, path_to_zip='../'):

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
        temp_slit_folder_name = 'temp'
        # create a temporary folder to put fits slits into:
        try:
            os.mkdir(path_to_zip + temp_slit_folder_name)
        except:
            print('Temp folder already exists.')
        zip_ref.extractall(path_to_zip + temp_slit_folder_name)

    try:
        os.mkdir(assembled_filepath)
    except:
        print('Assembled Fits Folder Already Exits.')

    # find the filepath to the .fits slits
    all_sp3d_dirs, all_data_dirs = get_data_path(path_to_zip + temp_slit_folder_name)

    for data_dir_i in range(len(all_data_dirs)):
        data_dir = all_data_dirs[data_dir_i]
        name = all_data_dirs[data_dir_i][-15:]

        hinode_assemble(output_name=name + '.fits',
                        input_filepath=data_dir + '/',
                        output_filepath=assembled_filepath)
    #remove the slits:
    try:
        shutil.rmtree(path_to_zip + temp_slit_folder_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    # remove the zips if remove_zips is true :
    if remove_zips:
        try:
            shutil.rmtree(path_to_zip + zip_name)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

def get_data_path(path_to_unzipped_directories):
    """
    Get Data Path:

    - parameters:
        1. path_to_unzipped_directories:
    -returns:
        1. list of all sp3d directories
        2. list of all data (fits) directories
    """
    all_sp3d_dirs = [''] # all directories
    all_data_dirs = ['']
    # insert the appropriate path, relative or absolute, to where the data are stored
    for root, dirs, files in os.walk(path_to_unzipped_directories):
        #print(root, dirs, files)
        if root.endswith("SP3D"):
            all_sp3d_dirs += [root]
            for subdir in dirs:
                # this is the regular expression to find directories
                #     of the type [YYYYMMDDHHMMSS]
                if bool(re.search('20[012][0-9]+[012]+',subdir)):
                    all_data_dirs += [os.path.join(root, subdir)]
    # trim off the first null record in each list
    all_sp3d_dirs = all_sp3d_dirs[1:]
    all_data_dirs = all_data_dirs[1:]
    #print("SP3D Directories\n", "\n".join(all_sp3d_dirs))
    #print("Data Directories\n", "\n".join(all_data_dirs))

    return all_sp3d_dirs, all_data_dirs


def assemble_many(filepath_to_zips, assembled_fits_path):
    """ Assemble Many: CSAC zips contain many datasets in a single fits file,
                       so this function should unzip one zip and assemble all contained datasets,
                       naming them appropriately and deleting the fits slits.

                       Inputs: 1. filepath_to_zip
                               3. assembled_fits_path
    """
    zips = []
    for file in sorted(os.listdir(filepath_to_zips)):
        if file.endswith(".zip"):
            print('Zipped File: ' + str(file))
            zips.append(file)
    print(len(zips))

    for zip in zips:
        # for zip names, I want to call zip for each, which should
        # and then assemble slits into a DIFFERENT directory each file
        unzip(zip_name=zip, path_to_zip=filepath_to_zips)


