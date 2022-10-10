## Research Scripts: Fall 2022

Small, useful research scripts focusing on assembling & formatting HINODE data, & 
feeding them into SIR to invert these datasets. 

### File Descriptions:

1. scripts/SIR_inversion_utils.py:
   1. hinode_assemble: assembles & normalizes raw HINODE scans to SIR format
   2. unzip: I want this to unzip CSAC zips and assemble them using hinode_assemble, and finally delete the raw scans
   3. assemble_many: given a folder containing many zips, pass each into unzip.
   4. sir_single: edits an initialization.input file and starts an instance of a SIR inversion
   5. sir_many: given a text file of initialization parameters, calls sir_single multiple times to invert 
      multiple datasets. 

TODO:
   - get unzip working with nested folders 
   - get sir_single bugs worked out and add to git 
   - 