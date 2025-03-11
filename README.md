# EEG Rest Analysis

This repository contains Jupyter notebooks for analyzing resting-state EEG data. The analysis includes power spectral density calculation, connectivity calculations, and gradient-based approaches to understand brain dynamics.

## Features

Connectivity Analysis: Calculate correlation or coherence matrices from EEG signals
Gradient Mapping: Create gradient maps from connectivity matrices
Visualization: Tools for visualizing EEG data and analysis results

## Power Spectral Density (PSD) Analysis
This script computes the power spectral density (PSD) of EEG data, allowing analysis of frequency components. It provides insights into spectral properties and can be used for basic frequency-domain investigations.
The notebook includes power spectral density analysis capabilities:
- Calculation of power spectra for individual channels
- Band-specific power estimation (delta, theta, alpha, beta, gamma)
- Topographic mapping of spectral power
- Statistical analysis of spectral features

Example Output:
![Image](https://github.com/MarianSimarro/EEG/blob/main/assets/exxample_psd.png)

## Coherence Analysis
Computes coherence between EEG channels, offering a measure of functional connectivity. This analysis helps assess synchronization between different brain regions.

Example Output:
![Image](https://github.com/MarianSimarro/EEG/blob/main/assets/example_connectivity.png)

## Correlation Analysis
Performs correlation analysis on EEG data, examining relationships between signals from different electrodes. Useful for investigating connectivity patterns in EEG recordings.

Example Output:
![Image](https://github.com/MarianSimarro/EEG/blob/main/assets/example_correlation.png)

## Gradient Analysis
The repository includes tools for gradient analysis of EEG connectivity data, providing a low-dimensional representation of brain connectivity patterns. This approach leverages the BrainSpace library to map EEG connectivity patterns to cortical surfaces.
Key features include:
- Loading connectivity matrices (correlation or coherence)
- Creating surface-based parcellation for EEG electrodes
- Computing connectivity gradients using diffusion mapping
- Mapping gradient values to the cortical surface
- Visualizing the principal gradients on an interactive 3D brain model

## Usage
These scripts require preprocessed EEG data and provide a basic analysis framework. They can be modified for more advanced analyses.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Citation
If you use this code in your research, please cite:
Simarro, M. (2025). EEG: A Python package for EEG connectivity and gradient analysis.
GitHub repository: https://github.com/MarianSimarro/EEG

## Contact
For questions or collaboration, feel free to reach out to: gonzalez@cbs.mpg.de


---

March 2025, Marian Simarro

