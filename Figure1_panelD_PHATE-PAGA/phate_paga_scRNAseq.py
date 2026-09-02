import re

import numpy as np
import pandas as pd
import anndata as ad
import scanpy as sc
import phate
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ---------------------------------------------------------------------------
# Load and filter data
# ---------------------------------------------------------------------------
adata = sc.read_h5ad("ductal_malignant_lognorm_20270728.h5ad")
adata = adata[adata.obs['cell_type'].notna()].copy()
adata = adata[adata.obs['cell_type'] != "Tuft"].copy()
adata.obs['cell_type'] = adata.obs['cell_type'].cat.remove_unused_categories()

# ---------------------------------------------------------------------------
# PHATE embedding + PAGA graph
# ---------------------------------------------------------------------------
phate_operator = phate.PHATE(knn=25, n_jobs=1, verbose=True, mds_solver='smacof')
adata.obsm['X_phate'] = phate_operator.fit_transform(adata.obsm['corrected'])

sc.pp.neighbors(adata, n_neighbors=15, use_rep='corrected')
sc.tl.paga(adata, groups='cell_type')

# ---------------------------------------------------------------------------
# Color mapping for cell types
# ---------------------------------------------------------------------------
target_categories = [
    "Basal",
    "tumor-associated normal",
    "edTFnull_Classical",
    "S100A4+_Classical-like",
    "edTFhigh_Classical",
    "edTFlow_Classical",
    "Hybrid"
]
new_colors = [
    "#8A181A",
    "#FDD700",
    "#196533",
    "#C05127",
    "#282A74",
    "#3A53A4",
    "#683B87"
]

all_categories = list(adata.obs["cell_type"].cat.categories)
color_dict = {}
for cat, col in zip(target_categories, new_colors):
    color_dict[cat] = col
for cat in all_categories:
    if str(cat).isdigit():
        color_dict[cat] = "#BDBDBD"
for cat in all_categories:
    if cat not in color_dict:
        color_dict[cat] = "#BDBDBD"

adata.uns["cell_type_colors"] = [
    color_dict[cat] for cat in all_categories
]

# ---------------------------------------------------------------------------
# PAGA + PHATE comparison plot
# ---------------------------------------------------------------------------
sc.pl.paga_compare(
    adata,
    basis="phate",
    color="cell_type",
    node_size_scale=1,
    alpha=0.5,
    edge_width_scale=0.3,
    show=False,
    size=3,
    labels=[""] * len(all_categories)  # remove all labels
)

fig = plt.gcf()
# axes[0] is the embedding (PHATE) panel, axes[1] is the PAGA graph panel
ax_phate, ax_paga = fig.axes[0], fig.axes[1]
ax_paga.set_title("PAGA", fontsize=16, pad=20)
ax_phate.set_title("PHATE", fontsize=16, pad=20)
fig.set_size_inches(30, 15)
for ax in (ax_paga, ax_phate):
    ax.set_box_aspect(1)

cats = adata.obs["cell_type"].cat.categories
colors = adata.uns["cell_type_colors"]
handles = [mpatches.Patch(color=colors[i], label=cats[i]) for i in range(len(cats))]
plt.legend(
    handles=handles,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    borderaxespad=0.
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
    "paga_phate_scRNAseq_malignant.pdf",
    format="pdf",
    dpi=600,
    bbox_inches="tight"
)
plt.close(fig)

# ---------------------------------------------------------------------------
# PAGA connectivity heatmap
# ---------------------------------------------------------------------------
clusters = adata.obs["cell_type"].cat.categories
row_order = col_order = [
    'tumor-associated normal',
    'edTFhigh_Classical',
    'edTFlow_Classical',
    'edTFnull_Classical',
    'S100A4+_Classical-like',
    'Hybrid',
    'Basal'
]

conn = adata.uns["paga"]["connectivities"].toarray()
conn_df = pd.DataFrame(conn, index=clusters, columns=clusters)
conn_reordered = conn_df.loc[row_order, col_order].copy()

arr = conn_reordered.values.copy()
np.fill_diagonal(arr, np.nan)
conn_reordered = pd.DataFrame(arr, index=conn_reordered.index, columns=conn_reordered.columns)

mask = np.triu(np.ones_like(conn_reordered, dtype=bool), k=0)

plt.figure(figsize=(12, 8))
sns.heatmap(conn_reordered, mask=mask, cmap="viridis", annot=True, fmt=".2f")
plt.tight_layout()
plt.savefig("paga_connectivity_heatmap.pdf", format="pdf", bbox_inches="tight")
plt.close()
