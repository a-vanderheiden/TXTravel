# TAMU Geography Texas Travel Competition

This repo contains a jupyter notebook to figure out how an individual stacks up in the various sub-competitions of the Geography Department Summer Travel competition. 

The subcompetions can be assessed on either a list of county names or `.kmz` file(s) of travel routes.
If kmz files are provided, the notebook will derive the counties visited via intersection.

Alternatively, if you do not wish to use kmz files of your travel routes, you can simply list the county names you visited at the top of the notebook. 
These names will be used to query a TX County shapefile stored in the `data` folder. 

The notebook will then assess each sub-competion from the list of counties porvided (either from the kmz intersections or those listed by you). 

Your results for each of the sub-competions will be summarized at the end and an interactive map will visualize these results.   

## Downloading kmz travel routes
You can generate and download kmz files of Google Maps driving routes from the [My Maps](https://www.google.com/maps/d/) website created by Google. 

To download a kmz of a Google Maps route, follow the steps below:
1. Open the [My Maps](https://www.google.com/maps/d/) page
2. Click "Create New Map" in the top left corner
3. On the new map, click the Add Directions button below the Search Field at the top of the page
4. Name the new layer that appears on the left hand side of the page
5. Add the start and end points of your route next to "A" and "B"
6. To export the layer, select the 3 dots to the right of the map name, then select "Export to KML/KMZ"
7. In the pop-up menu, select your layer instead of "Entire map" in the drop-down
8. Click "Download"
9. Move this downloaded kmz to the `data` folder in this repo
10. Repeat steps 3-10 for each route you want to add

## Running the notebook
This notebook needs to be ran in an environment with these specific libraries installed (listed below).
- jupyter
- geopandas
- libkml

To create a `conda` environment with these libaries, run the following command:

```shell
# Navigate to where this repo was installed
$ cd path/to/this/repo/TXTravel 

# Create the environment
$ conda env create --file environment.yml
```
This process may take a couple minutes.

Once completed, you can activate the environment and start jupyter with...
```shell
$ conda activate tx_travel
$ jupyter notebook
```
... then select the file `TXTravel.ipynb`.

Once the notebook is running, enter your information in the top cell and select "Run All Cells". 
Your info will be summarized at the bottom of the page.

