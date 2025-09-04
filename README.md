# IMC-PDAC

This repository includes code and data used in the paper "Integrated spatial proteomics of human PDAC uncovers an expanded tumour–immune–stroma spectrum with genomic associations".

### Summary

For this project, three serial sections of a pancreatic ductal adenocarcinoma tumour microarray were acquired using imaging mass cytometry. Each serial section was stained with a 40-43 antibody panel focused on a different cellular compartment, either epithelial, immune, or stroma. Each serial section was segmented into individual cells, and cell types were annotated according to their protein expression using that serial section's marker panel (see Cell Phenotyping folder for code). The serial sections were then computationally overlaid (see Serial Section Overlay folder for code). Cross-section microenvironments were then annotated by measuring cellular content surrounding each patch of epithelial from all three aligned sections (see Microenvironment Phenotyping for code). 

### Directory of analyses

1. Cell phenotyping
2. Serial section overlay
3. Microenvironment phenotyping

### Data

***Zenodo DOI goes here***

The data folders on Zenodo are structured as follows:

1. MCDs
2. Tiffs with all channels
3. Segmented masks
4. Three RDS files of cell type data, one for each serial section (tumour/immune/stroma-focused)
5. Clinical Data