import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrapeCity(cityURL):
    ### once a city is clicked on
    # url = r"https://mailboxlocate.com/states/NJ/cities/ATLANTIC CITY"
    baseURL = "https://mailboxlocate.com"
    url = baseURL + cityURL
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    addressesRaw = soup.find_all("div", {"class":"address_1"})
    citiesRaw = soup.find_all("div", {"class":"city"})
    addresses = [a.text for a in addressesRaw]
    cities = [c.text.strip("\n").replace("\n"," ") for c in citiesRaw]
    return (addresses, cities)
    
def scrapeState(stateURL):
    baseURL = "https://mailboxlocate.com"
    url = baseURL + stateURL
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    addresses = []
    cities = []
    for link in soup.find_all("a"):
        linkHref = link.get('href')
        if "%s/cities/"%stateURL in linkHref:
            print(linkHref)
            iAddresses, iCities = scrapeCity(linkHref)
            addresses += iAddresses
            cities += iCities
    return (addresses, cities)
def scrapeHome():
    url = "https://mailboxlocate.com/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    addresses = []
    cities = []
    for link in soup.find_all("a"):
        linkHref = link.get('href')
        # if linkHref != "/states/MA":
        #     continue
        if "/states/" in linkHref and len(linkHref) == 10:
            print(linkHref)
            iAddresses, iCities = scrapeState(linkHref)
            addresses += iAddresses
            cities += iCities
    df = pd.DataFrame()
    df['address'] = addresses
    df['city'] = cities
    return df
if __name__ == '__main__':
    # scrapeState("NJ")
    df = scrapeHome()
    df.to_csv("mailboxAddresses.csv", sep="|", index=False)
    print(df.head())