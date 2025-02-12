# KM3NeT event data

This folder contains the data of the event. See the notebook `Reading Data.ipynb` for use of the data.

## Content

* **KM3-230213A_allhits.json.gz** and **KM3-230213A_allhits.root** contain the reconstructed track and photon hits on the individual PMTs. The ROOT-format is the native KM3NeT format, the json has been provided for convenience of use. The detector configuration is stored in a separate file available in the `/supplementary` folder.
* **KM3-230213A_voevent.xml** uses the VOEvent-format to store coordinates of the event and location of the detector.

## Creating json file

With the Julia environment used for the event display you can also reproduce the json file using the following snippet:

```
using KM3io

d = Detector("../supplementary/detector/detector.dynamical.datx")
f = ROOTFile("KM3-230213A_allhits.root")

tojson("KM3-230213A_allhits.json", f.offline[1], d)

```