# OSINT-
ONGOING PROJECTS I AM WORKING ON WILL BE RELEASING THIS SOON TO THE DARKSPACE SOFTWARE AND SECURITY REPOSITORY USE WITH RESPONSIBILITY  

OSINT Automation Script Documentation
Introduction
This script automates OSINT (Open Source Intelligence) operations by fetching geographic coordinates, performing Shodan searches, querying HaveIBeenPwned, and generating detailed reports in Excel format.
Installation
Ensure you have Python 3.x installed. The script automatically installs required dependencies such as pandas, requests, and openpyxl if they are missing.
Functions
install_dependencies
Automatically installs the required Python packages: pandas, requests, and openpyxl.
get_coordinates
Fetches the latitude and longitude for a given postcode using Nominatim's API.
Parameters:
  - postcode (str): The postal code to search for.
Returns:
  - latitude (str): The latitude of the location.
  - longitude (str): The longitude of the location.
open_google_earth_pro
Opens Google Earth Pro with the provided latitude and longitude.
Parameters:
  - latitude (str): The latitude of the location.
  - longitude (str): The longitude of the location.
shodan_search
Performs a Shodan search using the provided API key and query.
Parameters:
  - api_key (str): Shodan API key.
  - query (str): The search query to perform on Shodan.
Returns:
  - dict: The JSON response from Shodan.
haveibeenpwned_search
Checks if an email address has been part of any data breaches using HaveIBeenPwned API.
Parameters:
  - api_key (str): HaveIBeenPwned API key.
  - email (str): The email address to search for breaches.
Returns:
  - dict or str: JSON response if breaches are found, or a string indicating no breaches.
save_report
Creates a folder structure and saves the OSINT report in Excel format.
Parameters:
  - postcode (str): The postcode used for OSINT.
  - shodan_data (dict, optional): Shodan results data.
  - hibp_data (dict or list, optional): HaveIBeenPwned results data.
main
Main function that orchestrates the OSINT process by calling the other functions. It fetches coordinates, opens Google Earth Pro, performs Shodan and HaveIBeenPwned searches, and saves the report.
Parameters:
  - postcode (str): The postcode for OSINT.
  - shodan_key (str): Shodan API key.
  - hibp_key (str): HaveIBeenPwned API key.
  - shodan_query (str, optional): Query for Shodan search.
  - hibp_email (str, optional): Email address for HaveIBeenPwned search.
Usage
The script can be run from the command line with the following arguments:
  --postcode: Postcode to perform OSINT on (required).
  --shodan_key: Shodan API key (required).
  --hibp_key: HaveIBeenPwned API key (required).
Optional arguments:
  --shodan_query: Shodan search query.
  --hibp_email: Email address to check for breaches.
Example command:
  python osint_script.py --postcode 90210 --shodan_key your_shodan_key --hibp_key your_hibp_key --shodan_query apache --hibp_email example@example.com

https://github.com/DarkspaceSoftwareandSecurity
