import requests
from bs4 import BeautifulSoup

cities = ["berlin", "hong-kong", "london", "melbourne", "sao-paulo", "stockholm", "sydney",
"toronto", "vancouver"]

for city in cities:
    website     = "http://{}.startups-list.com".format(city)
    soup        = soupify_website(site_url=website)
    startups    = get_all_startups(soup)



def soupify_website(site_url=None):

    if site_url is not None:
        sauce   = requests.get(website).text
        return BeauitulSoup(sauce, "html.parser")
    else:
        raise ValueError("Argument site_url is required.")

def get_jobs():
    pass
