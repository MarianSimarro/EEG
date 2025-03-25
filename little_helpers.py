"""_summary_
"""

import os
import numpy as np
import mne
import matplotlib.pyplot as plt

def load_correlation_matrix(subject, condition, corr_folder):
    """Loads the correlation matrix and p-values for the given subject and condition."""
    filename = f"{subject}_{condition}_corr.npz"
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
    eeg_filename = f"{subject}_{condition}.set"
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

def load_data(subjects, conditions, matrix_type, con_folder, corr_folder, input_folder, frequency_band=None):
    """Loads coherence or correlation data for specified subjects and conditions, including channel names.
    
    Parameters:
    -----------
    subjects : list
        List of subject IDs to load.
    conditions : list
        List of conditions to load.
    matrix_type : str
        Choose matrix type to load: 'coherence' or 'correlation'.
    con_folder : str
        Path to the folder containing coherence files.    
    corr_folder : str
        Path to the folder containing correlation files.
    input_folder : str
        Path to the folder containing EEG .set files.
    frequency_band : str, optional
        Frequency band to filter coherence matrices ('delta', 'theta', 'alpha', 'beta', or None for full-band).
            
    Returns:
    --------
    dict: A dictionary with subject-condition keys and their corresponding data
          (subject, correlation/coherence matrix, p-values (for correlation), ch_names).
    """
    data = {}

    if matrix_type not in ["coherence", "correlation"]:
        raise ValueError("Invalid matrix type. Choose 'coherence' or 'correlation'.")

    for subject in subjects:
        for condition in conditions:
            condition = condition.strip()  # Remove extra spaces

            if isinstance(condition, str) and "," in condition:
                condition_list = [c.strip() for c in condition.split(",")]  # Clean spaces
            else:
                condition_list = [condition]  # Keep as a list

            for cond in condition_list:
                print(f"Checking: {subject}_{cond} ({matrix_type})")  # Debugging output

                if matrix_type == "coherence":
                    suffix = "_coh_matrix.npy" if frequency_band is None else f"_coh_matrix_{frequency_band}.npy"
                    filename = os.path.join(con_folder, f"{subject}_{cond}{suffix}")

                    if not os.path.exists(filename):
                        print(f"File missing: {filename}")
                        continue  # Skip to the next condition if the file doesn't exist

                    matrix = np.load(filename)
                  # Ensure the matrix is symmetric
                    matrix = (matrix + matrix.T) - np.diag(np.diag(matrix))  
                    p_values = None
                else:
                    matrix, p_values = load_correlation_matrix(subject, cond, corr_folder)

                ch_names = load_channel_names(subject, cond, input_folder)

                if matrix is not None:
                    data[f"{subject}_{cond}"] = {
                        "subject": subject,
                        f"{matrix_type}_matrix": matrix,
                        "p_values": p_values,
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

def plot_connectivity_matrix(matrix, title, ax=None, vmin=None, vmax=None, cmap='viridis'):
    """
    Plot a single connectivity matrix with proper formatting.
    
    Parameters:
    -----------
    matrix : numpy.ndarray
        The connectivity matrix to plot
    title : str
        Title of the plot
    ax : matplotlib.axes, optional
        Axes to plot on, if None a new figure is created
    vmin, vmax : float, optional
        Min and max values for color scaling
    cmap : str, optional
        Colormap to use
    
    Returns:
    --------
    ax : matplotlib.axes
        The axes with the plot
    im : matplotlib.image.AxesImage
        The image for colorbar creation
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    # Plot the matrix
    im = ax.imshow(matrix, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax)
    
    # Add labels and title
    ax.set_title(title)
    ax.set_xlabel('Channels')
    ax.set_ylabel('Channels')

    """
     # Add grid lines
    n_channels = matrix.shape[0]
    ax.set_xticks(np.arange(-.5, n_channels, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n_channels, 1), minor=True)
    ax.grid(which='minor', color='w', linestyle='-', linewidth=0.5)
    
    # Set ticks
    if n_channels <= 25:  # Only show all ticks for small matrices
        ax.set_xticks(np.arange(n_channels))
        ax.set_yticks(np.arange(n_channels))
    else:
        # For larger matrices, show fewer ticks
        step = max(1, n_channels // 10)
        ax.set_xticks(np.arange(0, n_channels, step))
        ax.set_yticks(np.arange(0, n_channels, step))"""
    
    return ax, im

def plot_subject_comparison(ec_matrix, eo_matrix, subject_id, ch_names=None, output_dir=None):
    """
    Plot comparison of EC and EO connectivity matrices for a single subject.
    
    Parameters:
    -----------
    ec_matrix : numpy.ndarray
        Eyes closed connectivity matrix
    eo_matrix : numpy.ndarray
        Eyes open connectivity matrix
    subject_id : str
        Subject identifier
    ch_names : list, optional
        Channel names
    output_dir : str, optional
        Directory to save plot, if None plot is not saved
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Find global min and max for consistent color scaling
    vmin = min(np.min(ec_matrix), np.min(eo_matrix))
    vmax = max(np.max(ec_matrix), np.max(eo_matrix))
    
    # Plot each matrix
    ax1, im1 = plot_connectivity_matrix(ec_matrix, f"Subject {subject_id} - Eyes Closed", 
                                        ax=axes[0], vmin=vmin, vmax=vmax, cmap='viridis')
    ax2, im2 = plot_connectivity_matrix(eo_matrix, f"Subject {subject_id} - Eyes Open", 
                                        ax=axes[1], vmin=vmin, vmax=vmax, cmap='viridis')
    
    # Calculate and plot difference
    diff_matrix = ec_matrix - eo_matrix
    diff_vmax = max(abs(np.min(diff_matrix)), abs(np.max(diff_matrix)))
    ax3, im3 = plot_connectivity_matrix(diff_matrix, f"Difference (EC - EO)", 
                                        ax=axes[2], vmin=-diff_vmax, vmax=diff_vmax, cmap='coolwarm')
    
    # Add colorbars
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04, label='Coherence')
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04, label='Coherence')
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04, label='Difference')
    
    # Add channel labels if provided
    if ch_names is not None and len(ch_names) == ec_matrix.shape[0]:
        if len(ch_names) <= 25:  # Only show all labels for small matrices
            for ax in axes:
                ax.set_xticks(np.arange(len(ch_names)))
                ax.set_yticks(np.arange(len(ch_names)))
                ax.set_xticklabels(ch_names, rotation=45, ha="right")
                ax.set_yticklabels(ch_names)

    plt.tight_layout()
    
    # Save figure if output directory is provided
    if output_dir is not None:
        plt.savefig(os.path.join(output_dir, f"subject_{subject_id}_connectivity.png"), 
                   dpi=300, bbox_inches='tight')
    plt.show()    
    return fig

def plot_group_average(ec_conn_list, eo_conn_list, ch_names=None, output_dir=None):
    """
    Plot group-level average connectivity matrices.
    
    Parameters:
    -----------
    ec_conn_list : list of numpy.ndarray
        List of eyes closed connectivity matrices
    eo_conn_list : list of numpy.ndarray
        List of eyes open connectivity matrices
    ch_names : list, optional
        Channel names
    output_dir : str, optional
        Directory to save plot, if None plot is not saved
    """
    # Calculate averages
    ec_avg = np.mean(np.array(ec_conn_list), axis=0)
    eo_avg = np.mean(np.array(eo_conn_list), axis=0)
    
    np.save("ec_avg_matrix_filled.npy", ec_avg)
    np.save("eo_avg_matrix_filled.npy", eo_avg)

    # Calculate statistical difference (t-test)
    t_values = np.zeros_like(ec_avg)
    p_values = np.zeros_like(ec_avg)
    
    for i in range(ec_avg.shape[0]):
        for j in range(ec_avg.shape[1]):
            ec_values = [mat[i, j] for mat in ec_conn_list]
            eo_values = [mat[i, j] for mat in eo_conn_list]
            t, p = stats.ttest_rel(ec_values, eo_values)
            t_values[i, j] = t
            p_values[i, j] = p
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Find global min and max for consistent color scaling for the averages
    vmin = min(np.min(ec_avg), np.min(eo_avg))
    vmax = max(np.max(ec_avg), np.max(eo_avg))
    
    # Plot average matrices
    ax1, im1 = plot_connectivity_matrix(ec_avg, "Group Average - Eyes Closed", 
                                       ax=axes[0, 0], vmin=vmin, vmax=vmax)
    ax2, im2 = plot_connectivity_matrix(eo_avg, "Group Average - Eyes Open", 
                                       ax=axes[0, 1], vmin=vmin, vmax=vmax)
    
    # Plot difference
    diff_avg = ec_avg - eo_avg
    diff_vmax = max(abs(np.min(diff_avg)), abs(np.max(diff_avg)))
    ax3, im3 = plot_connectivity_matrix(diff_avg, "Average Difference (EC - EO)", 
                                        ax=axes[1, 0], vmin=-diff_vmax, vmax=diff_vmax, cmap='coolwarm')
    
    # Plot p-values (with threshold)
    p_threshold = 0.05
    p_values_masked = np.ma.masked_where(p_values > p_threshold, p_values)
    ax4, im4 = plot_connectivity_matrix(-np.log10(p_values), "Statistical Significance (-log10(p))", 
                                       ax=axes[1, 1], vmin=0, vmax=4, cmap='plasma')
    
    # Add p-value threshold line to colorbar
    cbar4 = plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04, label='-log10(p-value)')
    cbar4.ax.axhline(-np.log10(p_threshold), color='r', lw=2)
    
    # Add other colorbars
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04, label='Coherence')
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04, label='Coherence')
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04, label='Difference')
    
    # Add channel labels if provided
    if ch_names is not None and len(ch_names) == ec_avg.shape[0]:
        if len(ch_names) <= 25:  # Only show all labels for small matrices
            for ax in axes.flat:
                ax.set_xticks(np.arange(len(ch_names)))
                ax.set_yticks(np.arange(len(ch_names)))
                ax.set_xticklabels(ch_names, rotation=45, ha="right")
                ax.set_yticklabels(ch_names)
    
    plt.tight_layout()
    
    # Save figure if output directory is provided
    if output_dir is not None:
        plt.savefig(os.path.join(output_dir, "group_average_connectivity.png"), 
                   dpi=300, bbox_inches='tight')
    plt.show()    
    return fig

def plot_all_subjects_and_group(ec_conn_list, eo_conn_list, subjects, ch_names=None, output_dir=None):
    """
    Plot individual subjects and group average in one workflow.
    
    Parameters:
    -----------
    ec_conn_list : list of numpy.ndarray
        List of eyes closed connectivity matrices
    eo_conn_list : list of numpy.ndarray
        List of eyes open connectivity matrices
    subjects : list of str
        List of subject identifiers
    ch_names : list, optional
        Channel names
    output_dir : str, optional
        Directory to save plots, if None plots are not saved
    """
    # Create output directory if needed
    if output_dir is not None and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Plot each subject
    for i, subject in enumerate(subjects):
        plot_subject_comparison(ec_conn_list[i], eo_conn_list[i], subject, ch_names, output_dir)
    
    # Plot group average
    plot_group_average(ec_conn_list, eo_conn_list, ch_names, output_dir)

    print(f"Plotting complete! {len(subjects)} subjects processed.")


def fill_missing_channels(data, subjects, conditions, original_ch_names):
    """
    Ensure all subjects have the same channel set by filling missing channels with zeros.
    
    Parameters:
    -----------
    data : dict
        Dictionary containing connectivity matrices and channel names for each subject-condition.
    subjects : list
        List of subject IDs.
    conditions : list
        List of conditions (e.g., "EC", "EO").
    original_ch_names : list
        Full list of expected channel names.
    
    Returns:
    --------
    updated_data : dict
        Data dictionary with all subjects having the same channels (missing ones filled with zeros).
    """
    updated_data = {}

    for subject in subjects:
        for condition in conditions:
            key = f"{subject}_{condition}"

            if key in data:
                subject_data = data[key]
                matrix = subject_data.get(f"{matrix_type}_matrix", None)
                ch_names = subject_data.get("channel_names", None)

                if matrix is not None and ch_names is not None:
                    # Create full-size zero matrix
                    full_size = len(original_ch_names)
                    full_matrix = np.zeros((full_size, full_size))

                    # Find indices of existing channels
                    existing_indices = [original_ch_names.index(ch) for ch in ch_names if ch in original_ch_names]
                    
                    # Insert existing matrix values into the correct positions
                    for i, old_i in enumerate(existing_indices):
                        for j, old_j in enumerate(existing_indices):
                            full_matrix[old_i, old_j] = matrix[i, j]

                    # Update subject's data with the filled matrix
                    updated_data[key] = {
                        f"{matrix_type}_matrix": full_matrix,
                        "channel_names": original_ch_names
                    }

                    print(f"Updated matrix for {subject} - {condition}: {full_matrix.shape}")
                else:
                    print(f"Incomplete data for {subject} - {condition}, skipping.")

    return updated_data

def extract_filled_matrices(data_filled, subjects, conditions, matrix_type):
    """
    Extracts matrices from the filled data dictionary.

    Parameters:
    -----------
    data_filled : dict
        Dictionary with subject-condition keys and matrices.
    subjects : list
        List of subject IDs.
    conditions : list
        List of conditions (e.g., "EC", "EO").
    matrix_type : str
        Type of matrix (e.g., 'conn', 'coherence').

    Returns:
    --------
    matrices : list
        List of connectivity matrices.
    """
    matrices = []
    
    for subject in subjects:
        for condition in conditions:
            key = f"{subject}_{condition}"
            if key in data_filled:
                matrices.append(data_filled[key][f"{matrix_type}_matrix"])
    
    return matrices

def align_filled_matrices(conn_list, ch_names):
    """
    Align matrices without removing channels (since all have the same shape).

    Parameters:
    -----------
    conn_list : list of numpy arrays
        List of connectivity matrices for each subject.
    ch_names : list of str
        List of channel names (already standardized).

    Returns:
    --------
    aligned_matrices : list of numpy arrays
        Connectivity matrices with consistent channels.
    aligned_ch_names : list of str
        Channel names (unchanged).
    """
    # Ensure all matrices have the same shape (which they do after filling)
    shape_set = {mat.shape for mat in conn_list}
    if len(shape_set) > 1:
        raise ValueError("Mismatch in matrix shapes even after filling. Check your data.")

    return conn_list, ch_names  # No channels are removed