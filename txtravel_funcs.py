from pathlib import Path
import geopandas as gpd
from geopandas import GeoDataFrame
import pandas as pd
from shapely.geometry import LineString
from itertools import combinations

def check_kmz(data_dir="data"):
    """Check the data folder for kmz routes. Provide feedback if none are found"""

    # List all kmz in the data folder
    data_path = Path(data_dir)
    kmz_files = list(data_path.glob("*.kmz"))

    if len(kmz_files)>0:
        print("KMZ files found")
        [print(f" - {kmz.name}") for kmz in kmz_files]
    else:
        print("No kmz files provided or they are in the wrong folder.")
    
    return kmz_files


def check_county_names(counties, county_list):
    """Check the names in county_list against the official names in the counties gdf"""

    # Check if names aren't in the county shapefile
    bad_names = [name for name in county_list if name not in counties["CNTY_NM"].values]

    if bad_names:
        print("The following county names could not be found in the county shapefile from TXDOT:")
        [print(f" - {name}") for name in bad_names]
        print("\n")
        print("Check the spelling and capitalization of the names above. Once changes are made to USER_COUNTIES, re-run the notebook.")
        print("The official county names are listed below:")
        [print(f" - {name}") for name in counties["CNTY_NM"].sort_values().values]
    else:
        print("No incorrect county names entered.")


def load_routes(kmz_files):
    """ Load the kmz files"""
    # Open kmz routes
    kmz = [gpd.read_file(f) for f in kmz_files]
    routes = pd.concat(kmz, ignore_index=True)
    
    # Filter out the point data
    routes = routes[routes.geometry.type == "LineString"]

    return routes


def intersecting_counties(clipped_routes, counties):
    """
    Find which counties are intersected by the routes
    """

    # Get names of intersecting counties and append to county list
    itx_county_names = list(clipped_routes.overlay(counties)["CNTY_NM"])

    return itx_county_names


class CountyProcessor():
    """
    Scores the user based on the counties and other information provided. 
    The provided counties should be a goedataframe filtered to just the counties the user has visited.

    All methods return the information needed to calculate whatever value is needed, not the value itself.
    This way, the user can validate and feel more confident in the metrics generated
    """
    def __init__(self, counties: GeoDataFrame, routes: GeoDataFrame, 
                 years_of_res: int, vehicle_age: int, tx_utm):
        self.counties = counties
        self.routes = routes
        self.years_of_res = int(years_of_res)
        self.vehicle_age = int(vehicle_age)
        self.tx_utm = tx_utm
    
    def counties_per_yr_tx_res(self):
        """
        Divide the number of counties by the number of years.
        counties can be any kind of iterable
        num_years is an int
        """
   
        return (len(self.counties), self.years_of_res)

    def greatest_distance_between_counties(self):
        """
        Measures the distance between county centroids.
        Returns the greatest distance. 
        """

        # Project the gdf for distance calculations
        vc_proj = self.counties.to_crs(self.tx_utm)

        # Calculate the centroid of every county
        vc_proj["centroid"] = vc_proj.centroid

        # Create LineStrings of every combination of centroid
        coord_combos = combinations(vc_proj["centroid"].values, 2)
        linestrings = [LineString(combo) for combo in coord_combos]

        # Return the longest LineString
        sorted_linestrings = sorted(linestrings, key=lambda x: x.length, reverse=True)
        gdf = gpd.GeoDataFrame(geometry = sorted_linestrings, crs=self.tx_utm)


        return gdf.loc[[0]]
    
    def longest_boundary(self):
        """
        Dissolve the boundaries of the counties provided, then calculate the perimeter of each separate area.
        Return the area with the longest perimeter.
        """

        # Project the dataset
        proj = self.counties.to_crs(self.tx_utm)
        proj["geometry"] = proj.buffer(1) # Buffer the dataset by 1m to ensure boundary overlaps of the projected counties

        # Dissolve the county boundaries
        dissolved = proj.dissolve()

        # Break apart the dissolved boundaries into their separate areas
        sep_areas = dissolved.explode(index_parts=True)

        # Calculate the length of each polgon exterior
        perimeters = sep_areas.exterior.length
        
        # Return the area with the highest length
        longest_border = sep_areas[perimeters == perimeters.max()]

        return longest_border

    def boldest_mile(self):
        """
        Multiply the route length (in km) by the age of the vehicle.
        Returns the length in miles
        """

        if self.routes.empty:
            return (0, 0)
        
        proj = self.routes.to_crs(self.tx_utm)
        total_length = proj.length.sum() / 1609 # convert m to miles

        return (total_length, self.vehicle_age)
    
    def alphabet_bingo(self):
        '''Loops through county names, slices the first letter of each county
        Returns a set of unique county first letters'''

        countylist = []
        for i in self.counties['CNTY_NM']:
            countylist.append(i[0])
        countyset = set(countylist)

        return countyset
    
    def county_names(self):
        """Return a list of all the county names"""
        return list(self.counties["CNTY_NM"].sort_values())