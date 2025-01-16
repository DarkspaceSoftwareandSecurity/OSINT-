import os
import subprocess
import sys
import requests
import webbrowser
import json
import argparse
import pandas as pd
import urllib.parse
from datetime import datetime

# Automatically install missing dependencies
def install_dependencies():
    try:
        import pandas
        import requests
    except ImportError:
        print("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pandas", "openpyxl"])

# Function to fetch latitude and longitude for the given postcode
def get_coordinates(postcode):
    geocode_url = f"https://nominatim.openstreetmap.org/search?postalcode={postcode}&format=json"
    headers = {
        'User-Agent': 'OSINT-Automation-Script (your_email@example.com)'
    }
    response = requests.get(geocode_url, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        latitude = data['lat']
        longitude = data['lon']
        return latitude, longitude
    else:
        raise ValueError(f"Could not find location for postcode: {postcode}")

# Function to open Google Earth Pro for a given location (latitude, longitude)
def open_google_earth_pro(latitude, longitude):
    try:
        # Command to open local Google Earth Pro with latitude and longitude
        google_earth_command = f"google-earth-pro --latlon={latitude},{longitude}"
        subprocess.run(google_earth_command, check=True)
        print(f"Opened Google Earth Pro for location ({latitude}, {longitude})")
    except FileNotFoundError:
        print("Google Earth Pro is not installed or not found in the system PATH.")

# Function to perform a Shodan search
def shodan_search(api_key, query):
    url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        result = json.dumps(response.json(), indent=4)
        print("Shodan Results:\n", result)
        return response.json()  # Return JSON for report
    else:
        raise ValueError("Error fetching results from Shodan")

# Function to perform a HaveIBeenPwned email search
def haveibeenpwned_search(api_key, email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'OSINT-Automation-Script'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("HaveIBeenPwned Results:\n", json.dumps(response.json(), indent=4))
        return response.json()  # Return JSON for report
    elif response.status_code == 404:
        return "No breaches found for this email."
    else:
        raise ValueError("Error fetching results from HaveIBeenPwned")

# Function to create folder structure and save OSINT report in Excel format
def save_report(postcode, shodan_data=None, hibp_data=None):
    # Create a directory for reports with the timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = f"OSINT_Reports/{timestamp}_{postcode}"
    os.makedirs(report_dir, exist_ok=True)

    # Create an Excel writer object
    report_path = f"{report_dir}/OSINT_Report_{postcode}_{timestamp}.xlsx"
    writer = pd.ExcelWriter(report_path, engine='openpyxl')

    # Shodan data report
    if shodan_data:
        shodan_df = pd.DataFrame(shodan_data['matches'])
        shodan_df.to_excel(writer, sheet_name="Shodan Results", index=False)

    # HIBP data report
    if hibp_data and isinstance(hibp_data, list):
        hibp_df = pd.DataFrame(hibp_data)
        hibp_df.to_excel(writer, sheet_name="HaveIBeenPwned Results", index=False)

    # Save the Excel file
    writer.save()
    print(f"OSINT report saved at {report_path}")

# Main function to automate the process
def main(postcode, shodan_key, hibp_key, shodan_query=None, hibp_email=None):
    try:
        # Step 1: Get coordinates from the postcode
        latitude, longitude = get_coordinates(postcode)
        print(f"Postcode {postcode} found at coordinates: Latitude: {latitude}, Longitude: {longitude}")

        # Step 2: Open local Google Earth Pro for the location
        open_google_earth_pro(latitude, longitude)

        # Step 3: Perform OSINT searches (Shodan and HaveIBeenPwned)
        shodan_results = None
        hibp_results = None
        if shodan_query:
            print("\nPerforming Shodan Search...")
            shodan_results = shodan_search(shodan_key, shodan_query)
        
        if hibp_email:
            print("\nPerforming HaveIBeenPwned Search...")
            hibp_results = haveibeenpwned_search(hibp_key, hibp_email)
        
        # Step 4: Save detailed OSINT report to Excel
        save_report(postcode, shodan_results, hibp_results)

    except ValueError as ve:
        print(str(ve))

if __name__ == "__main__":
    # Automatically install missing dependencies
    install_dependencies()

    # Argument parsing for command-line interaction
    parser = argparse.ArgumentParser(description="Automate OSINT by Postcode with Google Earth Pro Integration and OSINT Queries.")
    
    parser.add_argument("--postcode", type=str, required=True, help="Postcode to perform OSINT on (e.g., 90210).")
    parser.add_argument("--shodan_key", type=str, required=True, help="Shodan API key.")
    parser.add_argument("--hibp_key", type=str, required=True, help="HaveIBeenPwned API key.")
    
    # Optional arguments
    parser.add_argument("--shodan_query", type=str, help="Shodan search query (e.g., 'apache').")
    parser.add_argument("--hibp_email", type=str, help="Email address to check for breaches using HaveIBeenPwned.")

    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.postcode, args.shodan_key, args.hibp_key, args.shodan_query, args.hibp_email)
