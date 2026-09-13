
This folder contains the data and code for the implementation of Stabl used in the paper "Integrated spatial proteomics of human PDAC uncovers an expanded tumour–immune–stroma spectrum with genomic associations", with these results specifically visualized in Figure 6.

Stabl_Binary_Predictions_LateFusions_for_Boxplot.ipynb contains the script for running each omics dataset separately to determine the relative AUROC distributions possible with each dataset. The comparison between models built on Clinical, IMC, Genomic, or All Omics datasets is shown in the boxplot in Figure 6c.

Stabl_Binary_Predictions_LateFusion_then_EarlyFusion.ipynb contains the script for running Late Fusion to select the most informative features from each dataset. Features selected in >20% of models from this run were stored in EarlyFusion_Crossomics.csv. Then Early Fusion is run on EarlyFusion_Crossomics.csv, creating the final ranking of features, the top >20% of which are shown in Figure 6f.

