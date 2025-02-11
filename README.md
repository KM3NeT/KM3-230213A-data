# Data for the KM3-230213A high energy event observation

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgit.km3net.de%2Fopen-data%2Fpublic-candidates%2Fvhe-event/HEAD?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2FReading+Data.ipynb)

This repository contains open data and methods to supplement the publication *Observation of an Ultra-high-energy Cosmic Neutrino with KM3NeT*, available at XXX.

In this publication, the observation of an exceptionally high-energy neutrino event in the PeV-range by the KM3NeT neutrino telescope is reported. Here, you can find supplementary information to reproduce and reuse selected outcomes cited in the publication.

## Overview

The repository is mainly based on the use of Jupyter notebooks and provides an interactive event display. You can find the relevant notebooks in the `notebooks` folder, which also exemplifies how to read the data provided in `data`, and the event display in èvent-display`. As some analyses require special dependencies, ensure that you set up the environment accordingly as explained below in *Getting started*.

### Project Structure
- `data/`: Input data for the notebooks, supplementary data and single hit information for the event
- `event-display/`: Interactive event display of the event based on Julia
- `notebooks/`: Jupyter notebooks to document the final analysis steps and produce outcomes shown in the publication
- `src/`: Supplementary scripts and functions

### Contents

The following parts of the publication can be reproduced here:

#### Figures
- Julia-based event display (Figure 1): `/event-display` in a specialized Julia environment
- Distribution of number of hits for simulation of neutrinos of 10, 100 and 1000 PeV (Figure 2): `/notebooks/Simulated number of PMTs.ipynb`
- Skymap in the direction of KM3-230213A (Figure 4): `/notebooks/Skymap.ipynb`
- Comparison of the astrophysical flux with measurements and theoretical predictions, (Figure 5): `/notebooks/Astrophysical flux comparions.ipynb`
- Time residual distribution of the event hits (Extended Data, Figure 7): `/notebooks/Hit distributions.ipynb`
- Topography in the direction of the event (Extended Data, Figure 9): `/notebooks/Site topography.ipynb`
- Emission point of photons along the reconstructed muon trajectory (Extended Data, Figure 11): `/notebooks/Hit distributions.ipynb`

#### Tables
- Expected number of track events for a variety of diffuse astrophysical fluxes (Table 4): `/notebooks/Expected events per flux.ipynb`

## Getting started

You can run the repository locally on your machine (recommended in venv or conda environment) or on binder.

### Adding full data

For the full use of all notebooks, you have to retrieve the full dataset for `/data` from the KM3NeT Open Data Center, as explained in `/notebooks/Reading Data.ipynb`. A download function is provided, or you can directly download larger files from the [data set](https://opendata.km3net.de/dataset.xhtml?persistentId=doi%3A10.5072%2FFK2%2FJW72C9).

### Using mybinder

Launch the repository on mybinder following this link: [https://mybinder.org/v2/gh/https://git.km3net.de/open-data/public-candidates/vhe-event/HEAD?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2FReading+Data.ipyn](https://mybinder.org/v2/gh/https://git.km3net.de/open-data/public-candidates/vhe-event/HEAD?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2FReading+Data.ipyn).

### Run the repository locally

Firstly, download the whole content of the repository using `git` or just directly from the download function:
```sh
git clone git@git.km3net.de:open-data/public-candidates/uhe-event.git
```

then change into the code repository:
```sh
cd uhe-event/
```

#### Creating the environment

##### Using conda
In order to use conda to build the environment, conda has to be installed. To see how, use these [Installation instructions](https://docs.anaconda.com/free/anaconda/install/).

Build environment using `conda` from `_environment.yml` file:
```sh
conda env create -f _environment.yml
conda activate uhe_event
```

##### Using venv

It requires to build a dedicated environment.
Build environment using `pip`:
```sh
pip install virtualenv

virtualenv venv

```
acitvate `venv`:
```sh
# on Windows
.\venv\Scripts\activate.ps1
# on Linux
source venv/bin/activate
```
Install necessary packages:
```sh
pip install -r requirements.txt
```

#### Using Jupyter
In order to run the notebooks, you need to have Jupyter installed. You can install it using `pip install jupyter` or following the instructions at the [Juypter website](https://jupyter.org/install).

##### Running the Jupyter kernel

Jupyter notebook kernel and launch your notebook:
```sh
python -m ipykernel install --user --name=uhe_event
jupyter-notebook
```
And for `zsh` shell, you need to execute these lines first before installation of the kernel
```zsh
conda install -c conda-forge notebook
conda install -c conda-forge nb_conda_kernels
```

## License and Disclaimer

This project is licensed under the terms of the [BSD 3-clause](/LICENSE) license. Be aware that KM3NeT is currently under construction and data taking and processing are still under development. The presented data have been tested to the best current standards. However, the KM3NeT collaboration gives no warranty for the re-use of the data and does not endorse any third-party scientific findings based on the use of the presented data.

