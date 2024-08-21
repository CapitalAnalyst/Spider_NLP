#!/usr/bin/python

"""
Function:
    1. Download the AFP News homepage HTML.

I/O:
    1. Input:
        1.1 title page URL (str)
        1.2 file path for storing the HTML content (str)
    2. Output:
        2.1 HTML file of the AFP News homepage (html file)

"""
import datetime, os, requests


def download_html(url, html_path):
    """
    Downloads the HTML content from the given URL and saves it to the specified file path.

    Args:
        url (str): The URL to download the HTML content from.
        html_path (str): The file path to save the downloaded HTML content.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: Executing download_html for {url}")

    try:
        r = requests.get(url)
        html_doc = r.text
        with open(html_path, "w") as file:
            file.write(html_doc)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp}: Success - download_html run to success - {url} is saved to {html_path}.")

    except Exception as ex:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp}: Error - download_html run to error. Details: {ex}")


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    self_name = os.path.basename(__file__)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("----------"*10)
    print(f"{timestamp}: {self_name} started to run.")

    # Run the function
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    afp_news_homepage_url = "https://www.afp.gov.au/news-centre"
    afp_news_html_path = f"./Data/afp_news_{today_str}.html"
    download_html(afp_news_homepage_url, afp_news_html_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"{self_name} took time: {duration}")
    print("----------"*10)
