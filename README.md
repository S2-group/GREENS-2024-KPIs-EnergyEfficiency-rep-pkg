<!-- This repository is a companion page for the following thesis / publication:
> Author Names. Publication year. Thesis / Paper title. Publication venue / proceedings.

It contains all the material required for replicating the study, including: X, Y, and Z.

## How to cite us
The scientific article describing design, execution, and main results of this study is available [here](https://www.google.com).<br>
If this study is helping your research, consider to cite it is as follows, thanks!

```
@article{,
  title={},
  author={},
  journal={},
  volume={},
  pages={},
  year={},
  publisher={}
}
``` -->

## Unveiling Key Performance Indicators for the Energy Efficiency of Cloud Data Storage - Replication Package

This repository provides the replication package for our study "Unveiling Key Performance Indicators for the Energy Efficiency of Cloud Data Storage", submitted to the GREENS Workshop at ICSA 2024

## Repository Structure
This is the root directory of the repository. The directory is structured as follows:

    template-replication-package
     .
     |
     |--- src/                             Source code (Python) used in the paper to generate graphs
     |
     |--- documentation/                   NA
     |
     |--- data/                            Data collected via NetApp, used to generate graphs


     # consumption_patterns script
     This script contains the analysis and visualisation conducted for identifying patterns of power consumption across different models. The visualisation of power consumption and capacity per watt ratio metrics can also be found in this script.

     # capacity_utilisation script
     This script contains analysis and visualisation of the capacity utilisation of the storage environment in the period of 2022 to 2023. For filtering the node models when observing the capacity utilisation values per node, use the code in the Filtering Section with a specific node model.

     # space_saving scriot
     This script includes analysis and visualisation of space saving techniques provided by NetApp. The share of the techniques on space saving and their efficiency is compared in this analysis.

     # environmental_indicators script
     This script contains analysis and visualisation of the relation between data on different environmental inidicators provided by NetApp.

     # dc_consumption script
     This script contains an approximate estimation of the share of SBP's data storage in terms of energy impact compared to the golbal energy consumption of data centers based on the estimations from the literature.

     # data files

     - data.xlsx file contains company's data regarding the performance of the storage environment (capacity utilisation, space saving, etc)
     - workingenvironment.csv file contains sustainability data provided by NetApp
