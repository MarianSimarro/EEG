import os

matrix_type = "coherence"

# Set paths
input_folder = 'C:/Users/Marianne/Downloads/Lemon/subjects/ses-01' # Folder with subject files
output_folder = 'C:/Users/Marianne/Downloads/Lemon/subjects/Results'

psd_folder = os.path.join(output_folder, "psd") # output directory for PSDs
con_folder = os.path.join(output_folder, "connectivity") # Folder for connectivity matrices
corr_folder = os.path.join(output_folder, "correlation") # Folder for correlation matrices

subjects_list = [
    'sub-032304',
    'sub-032305',
    'sub-032306',
    'sub-032307',
    'sub-032308',
    'sub-032310'
    ]

subjects = subjects_list

original_ch_names = ('Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'CP5', 'CP1', 'CP2', 'CP6', 'AFz', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'AF7', 'AF3', 'AF4', 'AF8', 'F5', 'F1', 'F2', 'F6', 'FT7', 'FC3', 'FC4', 'FT8', 'C5', 'C1', 'C2', 'C6', 'TP7', 'CP3', 'CPz', 'CP4', 'TP8', 'P5', 'P1', 'P2', 'P6', 'PO7', 'PO3', 'POz', 'PO4', 'PO8')

conditions = ["EC, EO"]

