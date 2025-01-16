# Master Project - School of Applied Mathematics, FGV RJ
## A Network Medicine Approach to Predict Antibiotical Resistance

This is the README file for my Master Project repository. In this document, I'll provide an overview of each file and directory included in the repository.

## Introduction

This study investigated the potential of a network medicine approach for predicting antibiotic resistance using conserved genes in bacterial protein-protein interaction (PPI) networks.
Using kernel methods on PPI networks, we selected sets of conserved genes based on their proximity to AMR genes and evaluated their predictive performance using a machine learning model based on decision trees
The project is implemented using Python and R. 

## Required Data

The required data is available through the PATRIC FTP (ftp://ftp.patricbrc.org/datasets/). To download it, copy and paste this link in your file explorer and copy the file Nguyen_et_al_2020.tar.gz to a local directory. After extract, the gene sets used in this project can be found in Nguyen_et_al_2020 > Salmonella > fasta.500.0. Note that the Salmonella directory has a file named Sal.sir.filt.plf.tab. This is the raw AMR metadata for each species and it is necessary to copy this file to the directory where you have created a gene set and you will be able to run the model with your dataset.

## Predicting using the generated sets of genes

The model can be executed following the instructions in [this repository](https://github.com/jimdavis1/Core-Gene-AMR-Models).

## License

This project is licensed under the [MIT License](LICENSE).
