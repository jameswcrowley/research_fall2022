# testing assembler utilities on a test of 3 zipped files:
# ideally, I would make 3 really small

import SIR_inversion_utils as u

path_to_zips = '/Volumes/EDRIVE/Fall_2022/research/data/assembling_test/'

u.assemble_many(path_to_zips)