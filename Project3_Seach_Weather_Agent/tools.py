from langchain_nimble import NimbleSearchTool       # This module is used to perform a Google search for real-time information based on the user's query. 
from langchain.tools import tool
import os
import requests         # This module is used to make HTTP requests to the weather API to get real-time weather data for a given city.


# Create a NimbleSearchTool instance with the specified parameters.
search_tool = NimbleSearchTool(
    k = 5,
    deep_search = True,
    parsing_type="markdown"     
)

# Create the 1st tool for the agent to perform a Google search :
def google_search(query:str):
    """
    Search anything on google for real time information.
    Args:
        query - user search query for google search
        
    Return - result from google search
    """
    res = search_tool.invoke(query)
    return res


# Create the 2nd tool for the agent to get real-time weather details for a given city:
@tool
def weather_tool(city:str):
    """
        Get real time weather details like temperature, humidity and others.
        Args:
            city - city name for weather details
        Return -> Weather data from the api response.
    """

    # This part of the code constructs the API URL using the city name and the API key stored in the environment variable "WEATHR_API_KEY". 
    # It then makes a GET request to the OpenWeatherMap API to retrieve the weather data for the specified city. 
    # If the request is successful (status code 200), it returns the JSON response containing the weather data. If the request fails, it returns an error message indicating that the details for the specified city could not be found.
    API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv("WEATHR_API_KEY")}"
    res = requests.get(API_URL)
    if res.status_code == 200:
        return res.json()
    return "Unable to find details for this city"


# This list contains all the tools that the agent can use to perform specific tasks.
ALL_TOOLS = [google_search, weather_tool]