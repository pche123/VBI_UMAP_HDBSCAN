# VBI_UMAP_HDBSCAN

This repository presents a python implentation of the code used to generate the images in paper **XXXXX** for the section relying upon the usage of Uniform Manifold Approximation and Projection (UMAP), and Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN). 

The primary workflow consisted of using UMAP to project the data to a lower dimensional space, and then relying upon HDBSCAN for non-parametric clustering. Although care should be taken in such a workflow since methods like t-SNE and UMAP are primarily used for the purpose of visualization in lower dimensional spaces, if one is careful with the pre-processing steps, UMAP has been noted to be able to used for such a purpose:

https://umap-learn.readthedocs.io/en/latest/clustering.html

In particular we show this workflow sucessfully being implemented on a subset of data generated for the purpose of simulating vehicle bridge interaction (VBI). This data is publically available at: **XXXXXX**.

## Required Libraries

```
TESTING
python          3.9.12
matplotlib      3.5.1
hdbscan         0.8.29
umap-learn      0.5.3           
scikit-learn    1.0.2
```

The code was written on a macOS Monterey Version 12.4.

## Quick Explanation

The function ```HDBSCAN_UMAP_Application```, located in the ```methodology``` module, will be the main function to use for analysis. Ideally the code ill be pre-processed according to the Jupyter Notebook ```test```. In order to compare your results with the theoretical clustering results, you can call ```theoretical_clustering```, once again located in the ```methodology``` module. 


