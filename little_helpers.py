"""_summary_
"""

import os
import numpy as np
import mne
import matplotlib.pyplot as plt

def load_connectivity_matrix(subject, condition, con_folder):
    """Loads the coherence matrix for the given subject and condition."""
    filename = f"sub-{subject}_{condition}_coh_matrix.npy"
    filepath = os.path.join(con_folder, filename)
    
    if os.path.exists(filepath):
        try:
            matrix = np.load(filepath)
            # Ensure the matrix is symmetric
            matrix = (matrix + matrix.T) - np.diag(np.diag(matrix))  
            return matrix
        except Exception as e:
            print(f"Error loading coherence matrix for {subject}_{condition}: {e}")
    else:
        print(f"Warning: Coherence matrix file not found - {filename}")
    return None

def load_correlation_matrix(subject, condition, corr_folder):
    """Loads the correlation matrix and p-values for the given subject and condition."""
    filename = f"sub-{subject}_{condition}_corr.npz"
    filepath = os.path.join(corr_folder, filename)
    
    if os.path.exists(filepath):
        try:
            data = np.load(filepath)
            correlation_matrix = data.get("correlation_matrix")
            p_values = data.get("p_values")
            return correlation_matrix, p_values
        except Exception as e:
            print(f"Error loading correlation matrix for {subject}_{condition}: {e}")
    else:
        print(f"Warning: Correlation matrix file not found - {filename}")
    return None, None

def load_channel_names(subject, condition, input_folder):
    """Loads EEG channel names for the given subject and condition."""
    eeg_filename = f"sub-{subject}_{condition}.set"
    eeg_filepath = os.path.join(input_folder, eeg_filename)
    
    if os.path.exists(eeg_filepath):
        try:
            raw_data = mne.io.read_raw_eeglab(eeg_filepath, preload=False)
            return raw_data.ch_names
        except Exception as e:
            print(f"Error loading EEG file for {subject}_{condition}: {e}")
    else:
        print(f"Warning: EEG file not found - {eeg_filepath}")
    return None

def load_data(subjects, conditions, matrix_type, con_folder, corr_folder, input_folder):
    """Loads coherence or correlation data for specified subjects and conditions, including channel names.
    
    Parameters:
    -----------
    subjects : list, optional
        List of subject IDs to load. If None, loads all subjects.
    condition : str, optional
        Specific condition to filter. If None, loads all conditions.
    matrix_type: str
        Choose matrix type to load: 'coherence' or 'correlation' 
    con_folder : str
        Path to the folder containing coherence files.    
    corr_folder : str
        Path to the folder containing correlation files.
    input_folder : str
        Path to the folder containing eeg .set files.
            
    Returns:
    --------
    dict: A dictionary with subject-condition keys and their corresponding data
          (subject, correlation matrix, p-values (for correlation), ch_names).
    """
    data = {}

    if matrix_type not in ["coherence", "correlation"]:
        raise ValueError("Invalid matrix type. Choose 'coherence' or 'correlation'.")

    for subject in subjects:
        for condition in conditions:
            condition = condition.strip()  # Remove spaces if present
            print(f"Checking: {subject}_{condition} ({matrix_type})")  # Debugging output
            
            if matrix_type == "coherence":
                matrix = load_connectivity_matrix(subject, condition, con_folder)                       
                p_values = None  # Not applicable for coherence matrices
            else:  # correlation
                matrix, p_values = load_correlation_matrix(subject, condition, corr_folder)
            
            ch_names = load_channel_names(subject, condition, input_folder)
            
            if matrix is not None:
                data[f"{subject}_{condition}"] = {
                    "subject": subject,
                    f"{matrix_type}_matrix": matrix,
                    "p_values": p_values,  # Only applies to correlation matrices
                    "channel_names": ch_names,
                }

    return data

def visualize_matrices(data, matrix_type):
    """Visualizes all loaded matrices, ensuring coherence matrices are symmetric."""
    for key, subject_data in data.items():
        subject_id, condition = key.split("_")
        matrix = subject_data.get(f"{matrix_type}_matrix", None)
        ch_names = subject_data.get("channel_names", None)

        if matrix is not None and ch_names is not None:
            plt.figure(figsize=(10, 8))
            sns.heatmap(matrix, xticklabels=ch_names, yticklabels=ch_names, cmap="coolwarm", center=0, annot=False)
            plt.title(f"{matrix_type.capitalize()} Matrix - {subject_id} {condition}")
            plt.show()
        else:
            print(f"Skipping visualization: Incomplete data for {subject_id} - {condition}")
