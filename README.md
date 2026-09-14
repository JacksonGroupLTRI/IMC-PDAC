# IMC-PDAC

![PDAC cores with background](PDAC_cores_with_background.png)

This repository includes code and data used in the paper "Integrated spatial proteomics of human PDAC uncovers an expanded tumour–immune–stroma spectrum with genomic associations".

### Summary

For this project, three serial sections of a pancreatic ductal adenocarcinoma tumour microarray were acquired using imaging mass cytometry. Each serial section was stained with a 40-43 antibody panel focused on a different cellular compartment, either epithelial, immune, or stroma. Each serial section was segmented into individual cells, and cell types were annotated according to their protein expression using that serial section's marker panel (see Cell Phenotyping folder for code). Relationships between epithelial cell phenotypes were visualized using PHATE and PAGA (see PHATE-PAGA folder for code). The serial sections were then computationally overlaid (see Serial Section Overlay folder for code). Cross-section microenvironments were then clustered and annotated by the cellular content surrounding each patch of epithelial from all three aligned sections (see Microenvironment Phenotyping for code). We leveraged laser capture microdissection-coupled mass spectrometry to conduct an unbiased, deep proteomic profiling of the identified microenvironments (see LCM-MS folder for code used to process resulting data). Finally, we combined multiple data sources from these PDAC patients and implemented Stabl from Hédou et al. 2024 to compare predictive ability across omics and across features (see Stabl_implementation folder). 

### Directory of analyses

1. Cell phenotyping
2. PHATE/PAGA visualization of epithelial cell phenotypes
3. Serial section overlay
4. Microenvironment phenotyping
5. LCM-MS
6. Stabl implementation for dataset and feature ranking

### Data

DOI for data archive: 10.5281/zenodo.17534881

Full Link: 
https://zenodo.org/records/17534881?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjM4YmMxMDA1LTRiZTMtNDkyNi1hMTEyLTgyMGQ3MmQyYmMxYyIsImRhdGEiOnt9LCJyYW5kb20iOiI3YjFmZTRlMzU3ZjY2NWE0ODg5YzZhOGQ2NzdhNzM0NiJ9.jVN35VD8B-yjc81a8j9pHt5Uul4Ae6OhSwSsOZ9bOUgQmUD4xN4sDLtxYYdg9LkWEarV9t2wXClQ1E3X2Gf-TQ 

The data folders on Zenodo are structured as follows:

1. MCDs
2. Tiffs with all channels
3. Single cell segmented masks
4. Three RDS files of cell type data, one for each serial section (tumour/immune/stroma-focused)
5. Clinical Data
