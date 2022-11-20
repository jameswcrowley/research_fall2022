import os
import time
import glob


# TODO:
#   1. automate calling of SIR, moving and checking outputs.

# PSUEDOCODE:
#   I want to invert with same wrappers, and move input/outputs
#   Check that output didn't error, then move all to it's own folder in scratch/alpine.

def check_output(bash_output_filapath, N=30):
    """
    Given an output SIR inversion text file, check whether it has error-ed.
    If it has, return -1, if not, return 0.
    """
    latest_bash_out = max(glob.glob(bash_output_filapath + '*.out'))
    head = ''
    with open(latest_bash_out) as file:
        n = 0
        while n <= N:
            for line in file:
                if 'error' in line.lower():
                    return -1
                n += 1
        return 0


def edit_initialization(path_to_wrapper, atmos, n_cores):
    """
    NO LONGER USING - I don't want to edit input/output, just move inversions between wrappers.
    """
    # with path_to_wrapper + 'initialization.input' as initialization


# def call_SIR(path_to_wrapper):


def move_output(wrapper_path, final_path, final_folder_name):
    """
    Moves the output of inversions to its own folder, with a specified name.
    _____________
    Inputs:
        1. wrapper_path: path to SIR wrapper (where moving the data from)
        2. final_path: where to stick the final folder/inverison results
        3. final_folder_name: what to call the final folder.
    """
    # make output folder:
    try:
        os.mkdir(final_path + final_folder_name)
    except:
        print('Final output Folder Already Exits.')

    # move output to that new folder:
    os.rename(wrapper_path + 'output/*', final_path + final_folder_name)
    # don't need to delete output from wrapper - SIR will do it automatically


def edit_summary(summary_file, iteration, error, data_name):
    """
    Creates a file for each inverison, summarizing time it took to invert,
    where results are saved, and whether it errored.
    """
    current_time = str(time.asctime())
    summary = open(summary_file, 'a')
    if iteration == 0:  # if it's the first iteration
        header = (
            'Inversion of dataset ' + data_name + '\n', '------------', 'Iteration 0 completed at: ' + current_time)
        summary.writelines(header)
        if not error:
            summary.write('Inversion errored.')
        else:
            summary.write('Inversion completed without error.')
    else:
        lines = ('------------', 'Iteration ' + str(iteration) + 'completed at: ' + current_time)
        summary.writelines(lines)
    summary.close()


def create_list(path_to_assembled_fits):
    """
    Creates a list of all assembled fits files in a given directory.
    _____________
    Inputs:
        1. Path to assembled fits files
    _____________
    Outputs:
        1. saves a text file with all the assembled fits files, to be iterated through for inversions.
    """
    assembled_data = [os.path.basename(x + '\n') for x in glob.glob(path_to_assembled_fits + 'a.*.fits')]
    data_list_exits = glob.glob(path_to_assembled_fits + 'data_list')
    if data_list_exits == []:
        data_list = open(path_to_assembled_fits + 'data_list', 'w')
        for i in range(len(assembled_data)):
            data_list.write(assembled_data[i])
        data_list.close()
    else:
        pass


def find_latest_data(path_to_assembled_fits):
    """
    Prints the first line of data_list that has not been inverted (i.e. without an i. )
    _____________
    Inputs:
        1. path_to_assembled_fits
    _____________
    Outputs:
        1. prints the first instance of a non-inverted dataset to the screen,
           so it can be saved in bash files.
    """
    data_list = open(path_to_assembled_fits + 'data_list', 'r')
    for line in data_list:
        first_char = line[0]
        if first_char != 'i':
            print(line)
            break
        else:
            pass


def edit_latest_data(path_to_assembled_fits, latest_data_name):
    """
    For a given dataset, edits the data_list to append an i. on the front of that line.
    (for usage after that dataset has been inverted without erroring)
    _____________
    Inputs:
        1. path_to_assembled_fits
        2. latest_data_name
    _____________
    Outputs:
        1. edits only the line of data_list with latest_data_name to append an i. on front.
    """
    data_list = open(path_to_assembled_fits + 'data_list', 'w')
    for line in data_list:
        if latest_data_name in line.rstrip():  # doing in in case of weird spaces, etc...
            data_list.write('i' + line)
        else:
            data_list.write(line)
    data_list.close()

def print_inversion(inversion_num):
    """ super simple function: just prints the inversion number for use in bash scripts"""
    print(inversion_num)
