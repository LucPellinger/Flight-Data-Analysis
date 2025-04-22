"""
This module contains a class for processing flight data, including downloading and parsing
flight-related data and plotting flight routes.
"""

import sys

# Modify sys.path to include the parent directory for imports
sys.path.append("..")

# pylint: disable=wrong-import-position
import folium
import matplotlib.pyplot as plt
import pandas as pd
from branca.element import Element
from IPython.display import Markdown, display
from pydantic import BaseModel, Field

from Functions.distances import distance
from Functions.download_zip import download_file
from Functions.reading_zip import unzip
from langchain_openai import ChatOpenAI

# pylint: disable=R0903
# pylint: disable=R0914
class FlightData(BaseModel):
    """
    A class for processing flight data, including downloading
    and parsing flight-related data and plotting flight routes.

    Attributes
    ------------
    url: str
        The URL to download the flight data from.
    file: str
        The name of the downloaded zip file.
    airlines_df: pandas.DataFrame
        A DataFrame containing airline data.
    airplanes_df: pandas.DataFrame
        A DataFrame containing airplane data.
    airports_df: pandas.DataFrame
        A DataFrame containing airport data.
    routes_df: pandas.DataFrame
        A DataFrame containing route data.

    Methods
    ---------
    plot_airports(country: str) -> folium.Map:
        Plots the airports from a specified country on a map.
    distance_analysis() -> None:
        Plots the distribution of flight distances.
    plot_airport_flights(airport_code: str, internal: bool = False) -> folium.Map:
        Plots the flight routes from a specified airport on a map.
    plot_top_models(countries: list = None, top_n: int = 10) -> None:
        Plots the N most used airplane models by number of routes.
    plot_country_flights(country_name: str,
                        threshold: int = 1000,
                        internal: bool = False) -> folium.Map:
        Plots the flight routes from all airports in a specified country on a map.
    aircrafts() -> list:
        Print the list of unique airplane models in the data.
    aircraft_info(aircraft_name: str):
        Print the specifications of a specific airplane model.
    airports():
        Print the list of unique airports in the data.
    airport_info(airport_name: str):
        Print the specifications of a specific airport.
    """

    url: str = Field(
        default="https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false"
    )
    file: str = Field(default="downloads/flight_data.zip")
    airlines_df: pd.DataFrame = pd.DataFrame()
    airplanes_df: pd.DataFrame = pd.DataFrame()
    airports_df: pd.DataFrame = pd.DataFrame()
    routes_df: pd.DataFrame = pd.DataFrame()

    class Config:
        """
        This class is used to configure the Pydantic model.

        Attributes
        ------------
        arbitrary_types_allowed: bool
            A boolean indicating whether arbitrary types are allowed for the model.
        """

        arbitrary_types_allowed = True  # To allow Pandas DataFrame as a type

    def __init__(self, **data):
        """
        Initialize the class with default or passed values.
        Downloads the zip file, unzips it, and loads the CSVs into DataFrames.

        Parameters
        ------------
        data: dict
            A dictionary containing the data to initialize the class with.

        Returns
        ---------
        None
        """
        super().__init__(**data)  # Initialize with defaults or passed values

        download_file(self.url, self.file)  # Downloading the zip file
        dataframes_dict = unzip(self.file)  # Unzipping and loading CSVs into DataFrames

        # Directly setting the DataFrame attributes and removing superfluous columns
        if "airlines_df" in dataframes_dict:
            allowed_columns_airlines = [
                "Airline ID",
                "Name",
                "Alias",
                "IATA",
                "ICAO",
                "Callsign",
                "Country",
                "Active",
            ]
            self.airlines_df = dataframes_dict["airlines_df"][allowed_columns_airlines]
        if "airplanes_df" in dataframes_dict:
            allowed_columns_airplanes = ["Name", "IATA code", "ICAO code"]
            self.airplanes_df = dataframes_dict["airplanes_df"][
                allowed_columns_airplanes
            ]
        if "airports_df" in dataframes_dict:
            allowed_columns_airports = [
                "Airport ID",
                "Name",
                "City",
                "Country",
                "IATA",
                "ICAO",
                "Latitude",
                "Longitude",
                "Altitude",
                "Timezone",
                "DST",
                "Tz database time zone",
                "Type",
                "Source",
            ]
            self.airports_df = dataframes_dict["airports_df"][allowed_columns_airports]
        if "routes_df" in dataframes_dict:
            allowed_columns_routes = [
                "Airline",
                "Airline ID",
                "Source airport",
                "Source airport ID",
                "Destination airport",
                "Destination airport ID",
                "Codeshare",
                "Stops",
                "Equipment",
            ]
            self.routes_df = dataframes_dict["routes_df"][allowed_columns_routes]

            # Adding "lat" and "long" columns of source airport from airports_df to routes_df
            self.routes_df = self.routes_df.merge(
                self.airports_df[["Latitude", "Longitude", "IATA"]],
                left_on="Source airport",
                right_on="IATA",
                how="left",
            )
            # rename columns
            self.routes_df.rename(
                columns={
                    "Latitude": "Source latitude",
                    "Longitude": "Source longitude",
                },
                inplace=True,
            )

            # Adding "lat" and "long" columns of dest. airport from airports_df to routes_df
            self.routes_df = self.routes_df.merge(
                self.airports_df[["Latitude", "Longitude", "IATA"]],
                left_on="Destination airport",
                right_on="IATA",
                how="left",
            )
            # rename columns
            self.routes_df.rename(
                columns={
                    "Latitude": "Destination latitude",
                    "Longitude": "Destination longitude",
                },
                inplace=True,
            )
            # Calculate the distance in km between source and destination airports
            self.routes_df["distance_km"] = self.routes_df.apply(
                lambda row: distance(
                    row["Source latitude"],
                    row["Source longitude"],
                    row["Destination latitude"],
                    row["Destination longitude"],
                ),
                axis=1,
            )

    def plot_airports(self, country: str) -> folium.Map:
        """
        Plots the airports from a specified country on a map using the Folium library.
        Utilizes the class's DataFrame

        Parameters
        ------------
        country: str
            The name of the country to plot airports for.

        Returns
        ---------
        folium.Map
            A map object with plotted airports.

        Raises
        ------------
        ValueError
            If the specified country does not exist in the provided data.
        """

        # Check if the country exists in the DataFrame
        if country not in self.airports_df["Country"].values:
            raise ValueError(
                f"The specified country '{country}' does not exist in the provided data."
            )

        # Filter the dataframe for the specified country
        country_airports = self.airports_df[self.airports_df["Country"] == country]

        # Calculate the mean latitude and longitude to center the map
        mean_lat = country_airports["Latitude"].mean()
        mean_long = country_airports["Longitude"].mean()

        # Create a map centered at the mean latitude and longitude with a simple tileset
        country_map = folium.Map(
            location=[mean_lat, mean_long], tiles="CartoDB positron", zoom_start=6
        )

        # Add a circle marker for each airport
        for _, row in country_airports.iterrows():
            folium.Circle(
                location=[row["Latitude"], row["Longitude"]],
                radius=25,
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="red",
                fill=True,
                tooltip=row["Name"],
            ).add_to(country_map)

        # Return the map object
        return country_map

    def distance_analysis(self) -> None:
        """
        Plots the distribution of flight distances.

        Parameters
        ------------
        self: FlightData

        Returns
        ---------
        None
        """
        # Plot the distribution of flight distances
        plt.figure(figsize=(10, 6))
        plt.hist(
            self.routes_df["distance_km"], bins=100, color="blue", edgecolor="black"
        )
        plt.title("Distribution of Flight Distances")
        plt.xlabel("Distance (km)")
        plt.ylabel("Number of Flights")
        plt.grid(True)
        plt.show()

    def plot_airport_flights(self, airport_code: str, internal=False) -> folium.Map:
        """
        Plots the flight routes from a specified airport on a map.

        Parameters
        ------------
        airport_code: str
            The IATA code of the airport to plot flights from.
        internal: bool, optional
            Whether to only include flights within the same country.

        Returns
        ---------
        folium.Map
            A map object with plotted flight routes.

        Raises
        ------------
        ValueError
            If the specified airport does not exist in the provided data.
        """
        # Check if the airport exists in the DataFrame
        source_airport_info = self.airports_df[self.airports_df["IATA"] == airport_code]
        if source_airport_info.empty:
            print(f"No information found for airport code {airport_code}.")
            return None

        # Filter the routes DataFrame for flights departing from the specified airport
        departing_flights = self.routes_df[
            self.routes_df["Source airport"] == airport_code
        ]
        # Create a map centered at the source airport with a simple tileset
        source_lat = source_airport_info.iloc[0]["Latitude"]
        source_long = source_airport_info.iloc[0]["Longitude"]
        flight_map = folium.Map(location=[source_lat, source_long], zoom_start=5)

        # Add a line for each flight route
        for _, flight in departing_flights.iterrows():
            destination_airport_code = flight["Destination airport"]
            destination_airport_info = self.airports_df[
                self.airports_df["IATA"] == destination_airport_code
            ]
            # Skip if the destination airport does not exist in the data
            if destination_airport_info.empty:
                continue
            # Get the latitude and longitude of the destination airport
            destination_lat = destination_airport_info.iloc[0]["Latitude"]
            destination_long = destination_airport_info.iloc[0]["Longitude"]
            # Skip if internal and the source and destination airports are in different countries
            if internal and (
                source_airport_info.iloc[0]["Country"]
                != destination_airport_info.iloc[0]["Country"]
            ):
                continue
            # Set the line color to blue for internal flights and red for international flights
            color = (
                "blue"
                if source_airport_info.iloc[0]["Country"]
                == destination_airport_info.iloc[0]["Country"]
                else "red"
            )
            # Add the line to the map
            folium.PolyLine(
                locations=[
                    (source_lat, source_long),
                    (destination_lat, destination_long),
                ],
                color=color,
            ).add_to(flight_map)

        return flight_map

    def plot_top_models(self, countries: list = None, top_n: int = 10) -> None:
        """
        Plots the N most used airplane models by number of routes.

        Parameters
        ------------
        countries: list, optional
            A list of country names to filter the routes by.
        top_n: int, optional
            The number of top airplane models to plot.

        Returns
        ---------
        None

        Raises
        ------------
        ValueError
            If the specified country does not exist in the provided data.
        """
        # Use self.routes_df directly, ensuring 'routes' is always defined
        routes = self.routes_df.copy()

        # Check if the countries exist in the airports_df
        if countries is not None:
            if isinstance(countries, str):
                countries = [countries]

            # Get unique countries from airports_df
            valid_countries = set(self.airports_df["Country"].unique())
            invalid_countries = [
                country for country in countries if country not in valid_countries
            ]

            if invalid_countries:
                invalid_countries_str = ", ".join(invalid_countries)
                raise ValueError(
                    f"The following countries do not exist in the data: {invalid_countries_str}"
                )

            # Filter airports to those in the specified countries
            airports_in_countries = self.airports_df[
                self.airports_df["Country"].isin(countries)
            ]
            # Filter routes where either source or destination airport is in the specified countries
            routes = routes[
                (routes["Source airport"].isin(airports_in_countries["IATA"]))
                | (routes["Destination airport"].isin(airports_in_countries["IATA"]))
            ]

        # Expand 'Equipment' field into separate rows for accurate counting
        expanded_equipment = (
            routes["Equipment"]
            .str.split(" ", expand=True)
            .stack()
            .reset_index(level=1, drop=True)
        )
        # Count the number of routes for each airplane model
        route_counts = (
            expanded_equipment.value_counts()
            .rename_axis("IATA code")
            .reset_index(name="Counts")
        )

        # Merge with airplanes_df to get model names, sort by 'Counts', and select top n
        model_counts = route_counts.merge(self.airplanes_df, on="IATA code")
        model_counts = (
            model_counts.groupby("Name")
            .sum()
            .sort_values(by="Counts", ascending=False)
            .head(top_n)
        )

        # Plot
        plt.figure(figsize=(10, 6))
        plt.bar(model_counts.index, model_counts["Counts"])
        plt.xlabel("Airplane Model")
        plt.ylabel("Number of Routes")
        plt.title(
            f"Top {top_n} Most Used Airplane Models"
            + (" Worldwide" if not countries else f' in {", ".join(countries)}')
        )
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def plot_country_flights(
        self,
        country_name: str,
        threshold: int = 1000,
        internal: bool = False,
        train_plane_ratio: float = 3 / 25,
    ) -> folium.Map:
        """
        Plots the flight routes from all airports in a specified country on a map.

        Parameters
        ------------
        country_name: str
            The name of the country to plot flights for.
        threshold: int, optional
            The distance threshold in kilometers to distinguish short-haul from long-haul flights.
        internal: bool, optional
            Whether to only include flights within the same country.
        train_plane_ratio: float, optional
            The ratio of train to plane emissions for short-haul flights.

        Returns
        ---------
        folium.Map
            A map object with plotted flight routes.

        Raises
        ------------
        ValueError
            If the specified country does not exist in the provided data.

        Notes
        ------------
        The train_plane_ratio is used to calculate the potential reduction in CO2 emissions
        if short-haul flights were replaced with train services. The default value of 3/25
        is based on the average CO2 emissions per passenger-kilometer for trains and planes.

        The map also includes a legend with the total distance and count of short-haul and
        long-haul flights, as well as the potential reduction in CO2 emissions.

        The map is colored blue for short-haul flights and red for long-haul flights.
        """
        # Check if the country exists in the DataFrame
        country_airports = self.airports_df[self.airports_df["Country"] == country_name]
        # If the country does not exist in the DataFrame, raise a ValueError
        if country_airports.empty:
            raise ValueError(
                f"The specified country '{country_name}' does not exist in the provided data."
            )
        # Calculate the mean latitude and longitude to center the map
        mean_lat = country_airports["Latitude"].mean()
        mean_long = country_airports["Longitude"].mean()
        flight_map = folium.Map(location=[mean_lat, mean_long], zoom_start=5)

        # Initialize variables to store the total distance and count of short- and long-haul flights
        sh_dist = 0
        sh_count = 0
        lh_dist = 0
        lh_count = 0

        # Iterate over the airports in the specified country
        for _, source_airport in country_airports.iterrows():
            source_airport_code = source_airport["IATA"]
            departing_flights = self.routes_df[
                self.routes_df["Source airport"] == source_airport_code
            ]
            # Iterate over the departing flights from the current airport
            for _, flight in departing_flights.iterrows():
                destination_airport_code = flight["Destination airport"]
                destination_airport_info = self.airports_df[
                    self.airports_df["IATA"] == destination_airport_code
                ]
                # Skip if the destination airport does not exist in the data
                if destination_airport_info.empty:
                    continue

                destination_lat = destination_airport_info.iloc[0]["Latitude"]
                destination_long = destination_airport_info.iloc[0]["Longitude"]
                # If internal source and destination airports are in different countries, skip
                if internal and (
                    source_airport["Country"]
                    != destination_airport_info.iloc[0]["Country"]
                ):
                    continue
                # Increment the total distance and count of short-haul and long-haul flights
                # Set the line color to blue for internal flights and red for international flights
                if flight["distance_km"] < threshold:
                    sh_dist += flight["distance_km"]
                    sh_count += 1
                    color = "blue"
                else:
                    lh_dist += flight["distance_km"]
                    lh_count += 1
                    color = "red"

                # Add the line to the map
                folium.PolyLine(
                    locations=[
                        (source_airport["Latitude"], source_airport["Longitude"]),
                        (destination_lat, destination_long),
                    ],
                    color=color,
                ).add_to(flight_map)

        # If one was to replace short-haul flights with trains
        emission_reduction = (
            (train_plane_ratio * sh_dist + lh_dist)
            / (sh_dist + lh_dist)
            * 100
        )

        # Create a legend with the total distance and count of short-haul and long-haul flights
        legend_html = (
            f"<div style=\"position: fixed; "
            f"bottom: 20px; left: 20px; width: 320px; height: 200px; "
            f"border:2px solid grey; z-index:9999; font-size:14px; "
            f"background-color:white; "
            f"opacity: 0.95; "
            f"padding: 10px; "
            f"\">&nbsp;<b>Flight Legend</b><br>"
            f"&nbsp;<span style='color: blue;'>Short-haul flights</span><br>"
            f"&nbsp;Count: <b>{sh_count}</b> - Total distance: <b>{sh_dist:.2f}</b> km<br>"
            f"&nbsp;<span style='color: red;'>Long-haul flights</span><br>"
            f"&nbsp;Count: <b>{lh_count}</b> - Total distance: <b>{lh_dist:.2f}</b> km<br><br>"
            f"&nbsp;If we were to replace short-haul flights with<br>"
            f"&nbsp;rail services, we could reduce CO2<br>"
            f"&nbsp;emissions to <b>{emission_reduction:.2f}</b>% of the current emissions."
            f"</div>"
        )

        # Add the HTML code to the Folium map
        legend = Element(legend_html)
        flight_map.get_root().html.add_child(legend)

        return flight_map

    def aircrafts(self) -> list:
        """
        Print the list of unique airplane models in the data.
        Uses the airplanes_df attribute from the class and
        prints the unique airplane models using the attribute
        Name from the dataframe.

        Parameters
        ------------
        self: FlightData

        Returns
        ---------
        unique_aircrafts: list
            A list of unique airplane models.

        Example
        ------------
        flight_data = FlightData()
        flight_data.aircrafts()

        """
        # Get the unique airplane models from the airplanes_df attribute
        unique_aircrafts = self.airplanes_df["Name"].unique()
        print("List of airplane models:")
        print(list(unique_aircrafts))

        return list(unique_aircrafts)

    def aircraft_info(self, aircraft_name: str):
        """

        Print the specifications of a specific airplane model.
        Uses the airplanes_df attribute from the class and prints the specifications of
        the airplane model using the attribute Name from the dataframe.
        The method accesses ChatOpenAI to get the information about the airplane model.

        Parameters
        ------------
        self            : FlightData
        aircraft_name   : str = the name of the airplane model

        Returns
        ------------
        aircraft_info: A table of specifications about the airplane in Markdown.

        Example
        ------------
        flight_data = FlightData()
        flight_data.aircraft_info("Boeing 737-800")
        """
        # Check if the airplane model exists in the DataFrame
        if self.airplanes_df[self.airplanes_df.Name == aircraft_name].empty:
            # If the airplane model does not exist in the DataFrame, raise a ValueError
            raise ValueError(
                f"Aircraft {aircraft_name} not found in the data."
                f"Choose one of the following: {self.aircrafts()}"
            )
        # Access ChatOpenAI to get the information about the airplane model
        llm = ChatOpenAI(temperature=0.1)
        aircraft_info = llm.invoke(f"Tell me about the airplane {aircraft_name}")
        # Print the specifications of the airplane model in Markdown
        display(
            Markdown(
                aircraft_info.content.replace(aircraft_name, ("**" + aircraft_name + "**"))
            )
        )

    def airports(self):
        """
        Print the list of unique airports in the data.
        Uses the airports_df attribute from the class and
        prints the unique airports using the attribute
        Name from the dataframe.

        Parameters
        ------------
        self: FlightData

        Returns
        ---------
        unique_airports: list
            A list of unique airports.

        Example
        ------------
        flight_data = FlightData()
        flight_data.airports()
        """
        # Get the unique airports from the airports_df attribute
        unique_airports = self.airports_df["Name"].unique()
        print("List of airports in the data:")
        print(list(unique_airports))

        return list(unique_airports)

    def airport_info(self, airport_name: str):
        """

        Print the specifications of a specific airport.
        Uses the airports_df attribute from the class and prints the specifications of the airport
        using the attribute Name from the dataframe.
        The method accesses ChatOpenAI to get the information about the airport.

        Parameters
        ------------
        self            : FlightData
        airport_name    : str = the name of the airport

        Returns
        ------------
        airport_info: A table of specifications about the airport in Markdown.

        Example
        ------------
        flight_data = FlightData()
        flight_data.airport_info("Schiphol Airport")
        """
        # Check if the airport exists in the DataFrame
        if self.airports_df[self.airports_df.Name == airport_name].empty:
            # If the airport does not exist in the DataFrame, raise a ValueError
            raise ValueError(
                f"Aircraft {airport_name} not found in the data."
                f"Choose one of the following: {self.airports()}"
            )
        # Access ChatOpenAI to get the information about the airport
        llm = ChatOpenAI(temperature=0.1)
        airport_info = llm.invoke(f"Tell me about the airplane {airport_name}")
        # Print the specifications of the airport in Markdown
        display(
            Markdown(
                airport_info.content.replace(airport_name, ("**" + airport_name + "**"))
            )
        )
