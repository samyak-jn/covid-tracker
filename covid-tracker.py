import subprocess
import sys

# if package dosen't exist the script will install automatically
def install(package):
    subprocess.check_call([sys.executable, '-m', "pip", "install", package])

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("beautifulsoup4")

try:
	import requests
except ImportError:
    install("requests")

#importing the packages
from bs4 import BeautifulSoup
import requests

print("      --- Welcome to Covid-Tracker ---")
print("\n--------------------------------------------")

response=requests.get('https://www.worldometers.info/coronavirus/')
base_url='https://www.worldometers.info/coronavirus/'
check_country = input("Please enter your country name: ")
check_country = check_country.upper()
print(f"Checking data for {check_country}, please hold...")

# collecting all country data list and checking if the entered input data exists
if response.status_code==200:
    data=BeautifulSoup(response.text,'html.parser')
    country_list = {}
    for country in data.find_all(class_="mt_a"):
        country_list[(country.text).upper()] = country['href']
    if check_country in country_list.keys():
        print("Your country data is available.")
        site = base_url+country_list[check_country]
    else:
        print("Sorry, your country data is not available.")
        sys.exit(0)

# checking for country data (parsing through country website)
c_response=requests.get(site)
c_data = {}
if c_response.status_code==200:
    data=BeautifulSoup(c_response.text,'html.parser')
    info = data.find_all("div", {"id": "maincounter-wrap"})
    for div in info:
        key = div.text.split(":")[0].strip('\n')
        if(key!="Projections"):
            value = div.text.split(":")[1].strip('\n').strip()
            c_data[key] = value
    print("--------------------------------------------")
    print(f"Current status of {check_country}:\n")
    for info_text in c_data:
        print(f"{info_text}: {c_data[info_text]}")
    print(f"Active Case: {format(int(c_data['Coronavirus Cases'].replace(',', ''))-int(c_data['Recovered'].replace(',', ''))-int(c_data['Deaths'].replace(',', '')), ',')}")
print("--------------------------------------------")
print("Thank you for using covid-meter, Stay Inside, Stay Safe!")

