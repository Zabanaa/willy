import csv
import requests
from bs4            import BeautifulSoup
from termcolor      import colored
from collections    import namedtuple

def soupify_website(site_url=None):

    if site_url is not None:
        sauce   = requests.get(site_url).text
        return BeautifulSoup(sauce, "html.parser")
    else:
        raise ValueError("Argument site_url is required.")

def get_all_startups(soup, city):

    startups_list   = soup.find_all("div", class_="startup")
    all_startups        = []

    for startup in startups_list:
        startup_name    = startup["data-name"]
        startup_url     = startup["data-href"]
        all_startups.append([startup_name, startup_url, city])

    return all_startups

def startup_has_open_jobs(soup):

    StartupSituation = namedtuple("StartupSituation", ["hiring", "href"])

    links       = soup.find_all("a")

    keywords    = [ "jobs", "join us", "careers", "work for us", "work with us",
            "we are hiring"]

    if len(links) >= 1:

        for link in links:

            link_text = link.text.strip().lower()

            if link_text in keywords:
                href = link.get("href")

                if href is not None:
                    return StartupSituation(hiring=True, href=href)
                else:
                    return StartupSituation(hiring=False, href=None)
                    break
        else:
            return StartupSituation(hiring=False, href=None)

    else:
        # The page doesn't even have links
        # so ... not hiring
        return StartupSituation(hiring=False, href=None)

def startup_is_hiring_software_devs(soup):

    HiringSWD       = namedtuple("HiringSWD", ["hiring", "job_title"])
    jobs_page_body  = soup.body.text.lower()

    job_titles      = [ "python", "nodejs", "node.js", "django", "flask",
                       "full stack", "fullstack", "full stack", "backend",
                       "back end", "back-end", "software developer",
                       "software engineer"]

    if jobs_page_body is not None:

        for job_title in job_titles:

            if jobs_page_body is not None and job_title in jobs_page_body:
                return HiringSWD(hiring=True, job_title=job_title)
                break
        else:
            return HiringSWD(hiring=False, job_title=job_title)

    else:
        return HiringSWD(hiring=False, job_title=job_title)

def save_startups_info_to_csv(startup_info, file):

    with open(file, "a") as startup_file:

        writer  = csv.writer(startup_file)
        writer.writerow(startup_info)

    startup_file.close()
    return True
