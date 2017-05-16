import requests
from bs4 import BeautifulSoup

cities = ["berlin", "hong-kong", "london", "melbourne", "sao-paulo", "stockholm", "sydney",
"toronto", "vancouver"]

def get_all_startups(soup):

    startups_list   = soup.find_all("div", class_="startup")
    startups        = []

    for startup in startups_list:
        startup_url     = startup["data-name"]
        startup_name    = startup["data-href"]
        startups.append({"name": startup_name, "url": startup_url})

    return startups

def soupify_website(site_url=None):

    if site_url is not None:
        sauce   = requests.get(website).text
        return BeautifulSoup(sauce, "html.parser")
    else:
        raise ValueError("Argument site_url is required.")

def get_jobs():
    pass

for city in cities:
    website     = "http://{}.startups-list.com".format(city)

    print("")
    print("Scraping {}".format(website))
    print("")
    soup        = soupify_website(site_url=website)

    print("Getting startups info ...")
    print("")
    startups    = get_all_startups(soup)

    print("Found {} startups in {}".format( len(startups), city))

