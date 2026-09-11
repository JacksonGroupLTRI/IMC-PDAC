import pandas as pd
import phate
import numpy as np
import anndata as ad
import scanpy as sc
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# 1. Load data, build AnnData, filter, save
# ---------------------------------------------------------------------------
df = pd.read_csv("2026Feb4_PDAC_TMA_Epithelial_Panel_compensated_ungated_cells_noslide6_raw_expression_labelannotated_with_neoadj_noProblemCases.csv")
df = df.iloc[:, 1:]
df = df[df["Epithelial_Cell_Annotations"].notna()]

numeric_cols = df.columns[: df.columns.get_loc("SMA") + 1]
cols_to_remove = [
    "SMA", "INS", "FAP", "CD45", "CD31", "PDPN", "MKI67", "CASP3", "BMP4", "CAIX",
]
numeric_cols = [col for col in numeric_cols if col not in cols_to_remove]

numeric_matrix = df[numeric_cols]
metadata_cols = [col for col in df.columns if col not in numeric_cols]
metadata = df[metadata_cols]

adata = ad.AnnData(
    X=numeric_matrix.values,
    obs=metadata,
    var=pd.DataFrame(index=numeric_cols),
)
del df, numeric_matrix, metadata

# Remove cells where any marker exceeds 1.2x the 3rd-highest value for that marker
third_highest = np.partition(adata.X, -3, axis=0)[-3, :]
thresholds = 1.2 * third_highest
mask = (adata.X > thresholds).any(axis=1)
adata = adata[~mask].copy()

cat_cols = ["clinical_info", "High_Stage", "Neoadjuvant", "Slide", "Genomic"]
for col in cat_cols:
    adata.obs[col] = adata.obs[col].astype("category")

ad.settings.allow_write_nullable_strings = True
adata.write_h5ad("adata_epithelialIMC.h5ad")

# ---------------------------------------------------------------------------
# 2. Normalize, transform, compute PHATE embedding, neighbors graph, PAGA
# ---------------------------------------------------------------------------
GROUPS_KEY = "Epithelial_Cell_Annotations"

# Min-max normalize per feature, then sqrt-transform
adata.X = adata.X / adata.X.max(axis=0)
adata.X = np.sqrt(adata.X)

# Compute PHATE embedding
phate_operator = phate.PHATE(
    knn=25,
    n_jobs=1,
    verbose=True,
    mds_solver="smacof",
)
adata.obsm["X_phate"] = phate_operator.fit_transform(adata.X)

# Compute neighbors graph and PAGA
sc.pp.neighbors(adata, use_rep="X")
sc.tl.paga(adata, groups=GROUPS_KEY)

# ---------------------------------------------------------------------------
# 3. Plot PAGA-compare (PHATE embedding + PAGA graph) and save as high-res PDF
# ---------------------------------------------------------------------------
new_colors = [
    "#8A181A",
    "#FDD700",
    "#683B87",
    "#196533",
    "#C05127",
    "#282A74",
    "#3A53A4",
]
adata.uns["Epithelial_Cell_Annotations_colors"] = new_colors

sc.pl.paga_compare(
    adata,
    basis="phate",
    color="Epithelial_Cell_Annotations",
    node_size_scale=0.5,
    show=False,
)

fig = plt.gcf()
ax_phate, ax_paga = fig.axes[0], fig.axes[1]
ax_phate.set_title("PHATE", fontsize=16, pad=20)
ax_paga.set_title("PAGA", fontsize=16, pad=20)

cats = adata.obs["Epithelial_Cell_Annotations"].cat.categories
colors = adata.uns["Epithelial_Cell_Annotations_colors"]
handles = [mpatches.Patch(color=colors[i], label=cats[i]) for i in range(len(cats))]
plt.legend(
    handles=handles,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    borderaxespad=0.0,
)

for ax in fig.axes:
    for txt in ax.texts:
        txt.set_visible(False)

for ax in fig.axes:
    for artist in ax.get_children():
        try:
            artist.set_rasterized(True)
        except Exception:
            pass

plt.savefig(
    "paga_compare_highres.pdf",
    format="pdf",
    dpi=600,
    bbox_inches="tight",
)
