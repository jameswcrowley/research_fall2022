import numpy as np
import astropy.io.fits as fits
import os
import re
import zipfile
import shutil
import matplotlib.pyplot as plt


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
    # print(stokes.shape)

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
    # remove the slits:
    try:
        shutil.rmtree(path_to_zip + temp_slit_folder_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    # remove the zips if remove_zips is true :
    if remove_zips:
        try:
            shutil.rmtree(path_to_zip + zip_name)
            print('Successfully removed slit scan folder: ' + str(path_to_zip) + 'temp')
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
    all_sp3d_dirs = ['']  # all directories
    all_data_dirs = ['']
    # insert the appropriate path, relative or absolute, to where the data are stored
    for root, dirs, files in os.walk(path_to_unzipped_directories):
        # print(root, dirs, files)
        if root.endswith("SP3D"):
            all_sp3d_dirs += [root]
            for subdir in dirs:
                # this is the regular expression to find directories
                #     of the type [YYYYMMDDHHMMSS]
                if bool(re.search('20[012][0-9]+[012]+', subdir)):
                    all_data_dirs += [os.path.join(root, subdir)]
    # trim off the first null record in each list
    all_sp3d_dirs = all_sp3d_dirs[1:]
    all_data_dirs = all_data_dirs[1:]
    # print("SP3D Directories\n", "\n".join(all_sp3d_dirs))
    # print("Data Directories\n", "\n".join(all_data_dirs))

    return all_sp3d_dirs, all_data_dirs


def normalize(input_dataname, output_datapath, output_dataname, remove_original=True):
    """
    normalize: normalizes data already in the right SIR shape
    _____________
    Parameters:
        - input_data: the filepath/name of a fits cube to normalze.
                      (in the shape (x, y, s, l))
        - output_data: the filepath/name of the output fits cube
        - remove_original: if the original fits file should be removed
    _____________
    Outputs:
        - normalized data: the filepath
    """

    input_data = fits.open(input_dataname)[0].data
    try:
        assert (input_data.shape[2] == 4)
    except Exception as err:
        print('Input data is incorrect format:', err)

    continuum = np.mean(input_data[:, :, 0, :10])
    normalized_data = np.true_divide(input_data, continuum)

    hdu = fits.PrimaryHDU(normalized_data)
    hdu.header = fits.open(input_dataname)[0].header
    hdu.writeto(output_datapath, output_dataname, overwrite=True)

    if remove_original:
        os.remove(input_dataname)


def quicklook(input_filepath):
    data_list = os.listdir(input_filepath + '*.fits')
    N = len(data_list)

    for i in range(N):
        temp_data = fits.open(input_filepath + data_list[i])[0].data

        plt.subplots(1, N, i+1)
        plt.imshow(temp_data[:, :, 0, 10], cmap = 'magma'); plt.colorbar()
        plt.title(data_list[i])

    plt.savefig(input_filepath + 'quicklook.png')


def quickcheck(input_filepath):
    data_list = os.listdir(input_filepath + '*.fits')
    N = len(data_list)

    good_data = []

    for i in range(N):
        temp_data = fits.open(input_filepath + data_list[i])[0].data

        if np.min(temp_data[:, :, 0, 10]) > 0:
            good_data.append(data_list[i])

        elif np.np.min(temp_data[:, :, 0, 10]) < 0:
            print(data_list[i] + ' is corrupted.')

    print(good_data)

