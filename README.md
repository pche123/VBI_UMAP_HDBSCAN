# VBI_UMAP_HDBSCAN

This repository presents a python implentation of the code used to generate the images in paper **XXXXX** for the section relying upon the usage of Uniform Manifold Approximation and Projection (UMAP), and Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN). 

The primary workflow consisted of using UMAP to project the data to a lower dimensional space, and then relying upon HDBSCAN for non-parametric clustering. Although care should be taken in such a workflow since methods like t-SNE and UMAP are primarily used for the purpose of visualization in lower dimensional spaces, if one is careful with the pre-processing steps, UMAP has been noted to be able to used for such a purpose:

https://umap-learn.readthedocs.io/en/latest/clustering.html

In particular we show this workflow sucessfully being implemented on a subset of data generated for the purpose of simulating vehicle bridge interaction (VBI). This data is publically available at: **XXXXXX**.

## Required Libraries

```
python          3.9.12
matplotlib      3.5.1
hdbscan         0.8.29
umap-learn      0.5.3           
scikit-learn    1.0.2
scipy           1.7.3
numpy           1.21.5
```

The code was written on a macOS Monterey Version 12.4.

## Quick Explanation

The function ```HDBSCAN_UMAP_Application```, located in the ```methodology``` module within the ```src``` folder, will be the main function to use for algorithm. However extra utility functions are located in the ```utils``` and ``` processing``` modules also.

Example useage of these modules for the proposed data pipeline can be found in the ```notebooks``` folder, within the notebook file named: ```Example_Usage.ipnyb```. Further explanation, and a note on any assumptions made is also located in this notebook file.


