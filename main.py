#!/home/zabana/projects/willy/ENV__willy/bin/python

import csv
import os
from helpers import *

def build_startups_list():

    cities = [ "berlin", "hong-kong", "london", "melbourne",
                "sao-paulo", "stockholm", "sydney", "toronto",
                "vancouver" ]

    startups_list = []

    for city in cities:
        website     = "http://{}.startups-list.com".format(city)

        print("Scraping {}".format(website))
        soup        = soupify_website(site_url=website)

        print("Getting startups info ...")
        startups    = get_all_startups(soup, city)

        startups_list.append(startups)
        print("Done !")
        print("")

    print("Saving startupsinfo ...")
    for city_startups in startups_list:

        for startup in city_startups:
            startup_name = startup[0]
            save_startups_info_to_csv(startup, "startups.csv")
            print("{} saved.".format(startup_name))

def get_startup_jobs():

    with open("startups.csv", "r") as startups_file:

        all_startups        = csv.reader(startups_file)
        hiring_startups     = 0
        google_sheet_index  = 1

        print("Scraping Jobs ...")

        for startup in all_startups:

            startup_name  = startup[0]
            startup_site  = startup[1]
            startup_city  = startup[2]

            try:
                startup_soup = soupify_website(site_url=startup_site)
            except requests.exceptions.ConnectionError:
                continue
            except Exception as e:
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
            except requests.exceptions.ConnectionError:
                error = "Could not connect to {}. URL: {}".format(startup_name, jobs_page)
                print(colored(error, "red"))
                continue

            hiring_swd, job_title   = startup_is_hiring_software_devs(jobs_page_soup)

            if not hiring_swd:
                continue

            message = "{} is hiring software devs ! Job title: {}"
            print(colored(message.format(startup_name, job_title), "green"))

            hiring_startup_info = [startup_city, startup_name, job_title, jobs_page]

            save_startups_info_to_csv(hiring_startup_info, "hiring_startups.csv")
            hiring_startups += 1

        startups_file.close()
        print("A total of {} startups are actively looking for software developers".format(hiring_startups))

if __name__ == "__main__":

    if not os.path.exists("./startups.csv"):
        build_startups_list()
        get_startup_jobs()
    else:
        get_startup_jobs()
