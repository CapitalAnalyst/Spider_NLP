#!/usr/bin/python

"""
Function:
    1. Parse the HTML of the Cyber.gov.au news page and extract the details of each news item,
       including the date, title, content, and URL, and save them as a CSV file.

I/O:
    1. Input:
        1.1 HTML file path of the Cyber.gov.au news page (str)
        1.2 CSV file path to save the extracted news details (str)
    2. Output:
        2.1 CSV file containing the extracted news details (date, title, content, URL)

"""

import datetime, os, json
from bs4 import BeautifulSoup
import pandas as pd


def get_url_list(url_list, position_div_list):
    """
    Extracts the date, title, content, and URL from a list of news item divs
    and adds them to the url_list dictionary.

    Args:
        url_list (list): A list to store the extracted details (date, title, content, URL).
        position_div_list (list): A list of div elements containing the news item details.
    """

    for div in position_div_list:
        instance = dict()

        date = div.find('header').text.strip()
        content = div.find('p').text.strip()
        title = div.find('h3').text.strip()
        url = div['href']

        # Store the extracted information in the dictionary
        instance['Date'] = date
        instance['Title'] = title
        instance['URL'] = url
        instance['Content'] = content

        url_list.append(instance)


def parse_news_page(cyber_news_page_html_path, cyber_url_list_csv_path):
    """
    Parse the Cyber.gov.au news page HTML content and extract the details of news items.

    Args:
        cyber_news_page_html_path (str): The file path of the Cyber.gov.au news page HTML.
        cyber_url_list_csv_path (str): The file path to save the extracted news details in CSV format.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: Executing parse_news_page...")

    try:
        # Read the HTML content of the news page
        with open(cyber_news_page_html_path, "r") as file:
            html_content = file.read()
        # Parse the HTML content and extract the news details
        soup = BeautifulSoup(html_content, 'html.parser')

        position_div_list = soup.find_all("a",
                                          class_="card--alert flex flex-col w-full h-full px-6 pt-6 pb-[56] border relative rounded-sm size--small rating-- color--white")

        url_list = []
        get_url_list(url_list, position_div_list)
        df = pd.DataFrame(url_list)

        # Save the extracted information to a CSV file
        df.to_csv(path_or_buf=cyber_url_list_csv_path, mode="w", index=False)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"{timestamp}: Success - parse_news_page completed successfully, URL list saved to {cyber_url_list_csv_path}.")

    except Exception as ex:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp}: Error - parse_news_page encountered an error. Details: {ex}")


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    self_name = os.path.basename(__file__)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("----------" * 10)
    print(f"{timestamp}: {self_name} started to run.")

    # Run the function
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    cyber_news_page_html_path = f"./Data/cyber_gov_{today_str}.html"
    cyber_url_list_csv_path = f"./Data/cyber_gov_{today_str}.csv"
    parse_news_page(cyber_news_page_html_path, cyber_url_list_csv_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"{self_name} took time: {duration}")
    print("----------" * 10)
