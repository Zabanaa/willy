#!/home/zabana/projects/willy/ENV__willy/bin/python

import csv
import os
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from termcolor import colored

def get_all_startups(soup, city):

    startups_list   = soup.find_all("div", class_="startup")
    startups        = []

    for startup in startups_list:
        startup_name    = startup["data-name"]
        startup_url     = startup["data-href"]
        startups.append({
            "name": startup_name,
            "url": startup_url,
            "location": city
        })

    return startups

def soupify_website(site_url=None):

    if site_url is not None:
        sauce   = requests.get(site_url).text
        return BeautifulSoup(sauce, "html.parser")
    else:
        raise ValueError("Argument site_url is required.")

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

    for job_title in job_titles:

        if jobs_page_body is not None and job_title in jobs_page_body:
            return HiringSWD(hiring=True, job_title=job_title)
            break
    else:
        return HiringSWD(hiring=False, job_title=job_title)

def save_startups_info_to_csv(startups):

    with open("startups.csv", "a") as startup_file:

        writer  = csv.writer(startup_file)

        for startup in startups:

            startup_name = startup.get("name")
            startup_url  = startup.get("url")
            startup_city = startup.get("location")

            writer.writerow([startup_name, startup_url, startup_city])

    startup_file.close()
    return True

def build_startups_list():

    cities = [ "berlin", "hong-kong", "london", "melbourne",
                "sao-paulo", "stockholm", "sydney", "toronto",
                "vancouver" ]

    for city in cities:
        website     = "http://{}.startups-list.com".format(city)

        print("Scraping {}".format(website))
        soup        = soupify_website(site_url=website)

        print("Getting startups info ...")
        startups    = get_all_startups(soup, city)

        print("Saving startups info to file ...")
        save_startups_info_to_csv(startups)
        print("Info Saved")
        print("")

if not os.path.exists("./startups.csv"):
    build_startups_list()
else:
    with open("startups.csv", "r") as startups_file:

        all_startups = csv.reader(startups_file)
        print("Scraping Jobs ...")

        for startup in all_startups:

            startup_name  = startup[0]
            startup_site  = startup[1]
            startup_city  = startup[2]

            try:
                startup_soup = soupify_website(site_url=startup_site)
                # print("Scraping {} in {}".format(startup_name, startup_city))
            except requests.exceptions.ConnectionError:
                # print(colored("Not reachable, skipping ...\n", "grey"))
                continue
            except Exception as e:
                # print("There's something wrong with this website")
                continue

            has_open_jobs, jobs_page = startup_has_open_jobs(startup_soup)

            if not has_open_jobs:
                continue

            if jobs_page.startswith("/"):
                jobs_page = "{}{}".format(startup_site, jobs_page)

            try:
                jobs_page_soup          = soupify_website(site_url=jobs_page)
                pass
            except requests.exceptions.MissingSchema:
                # jobs page does not start with / ex: jobs.html instead of jobs.html
                jobs_page = "{}/{}".format(startup_site, jobs_page)
                jobs_page_soup          = soupify_website(site_url=jobs_page)

            hiring_swd, job_title   = startup_is_hiring_software_devs(jobs_page_soup)

            if not hiring_swd:
                continue

            message = "{} is hiring software devs ! Job title: {}"
            print(colored(message.format(startup_name, job_title), "green"))

        startups_file.close()
