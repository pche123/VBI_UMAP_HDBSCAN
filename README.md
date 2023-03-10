# VBI_UMAP_HDBSCAN

This repository presents a python implentation of the code used to generate the images in paper **XXXXX** for the section relying upon the usage of Uniform Manifold Approximation and Projection (UMAP), and Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN). 

The primary workflow consisted of using UMAP to project the data to a lower dimensional space, and then relying upon HDBSCAN for non-parametric clustering. Although care should be taken in such a workflow since methods like t-SNE and UMAP are primarily used for the purpose of visualization in lower dimensional spaces, if one is careful with the pre-processing steps, UMAP has been noted to be able to used for such a purpose:

https://umap-learn.readthedocs.io/en/latest/clustering.html

In particular we show this workflow sucessfully being implemented on a subset of data generated for the purpose of simulating vehicle bridge interaction (VBI). This data is publically available at: **XXXXXX**.

## Required Libraries

aiohttp                       3.8.1
aiosignal                     1.2.0
alabaster                     0.7.12
anaconda-client               1.9.0
anaconda-navigator            2.2.0
anaconda-project              0.10.2
anyio                         3.5.0
appdirs                       1.4.4
applaunchservices             0.2.1
appnope                       0.1.2
appscript                     1.1.2
argon2-cffi                   21.3.0
argon2-cffi-bindings          21.2.0
arrow                         1.2.2
astroid                       2.6.6
astropy                       5.0.4
asttokens                     2.0.5
async-timeout                 4.0.1

The code was tested on a Macbook....

## Example Usage

Function **XXXX** will be the main thing to call, and is available in folder etc ... etc.... 

``` python
main(x,y,z)
```

