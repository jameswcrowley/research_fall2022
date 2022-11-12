# TODO:
#   1. automate calling of SIR, moving and checking outputs.

def check_output(output_text, N=30):
    """
    Given an output SIR inversion text file, check whether it has error-ed.
    If it has, return -1, if not, return 0.
    """
    head = ''
    with open(output_text) as file:
        n = 0
        while n <= N:
            for line in file:
                if 'error' in line.lower():
                    return -1
                n += 1
        return 0


def edit_initialization():
    return 0

# def call_SIR(x, T_nodes?, initialization_path, ...):

# def move_output():

# def
