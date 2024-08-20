#!/usr/bin/python

"""
Function:
    1. Download title page html.

I/O:
    1. Input:
        1.1 title page url (str)
        1.2 title page html file storage path (str)
    2. Output:
        2.1 title page html file (html file)


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
    title_page_url = "https://www.cyber.gov.au/about-us/view-all-content/news-and-media"
    title_page_html_path = f"./Data/cyber_gov_{today_str}.html"
    download_html(title_page_url, title_page_html_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"{self_name} takes time: {duration}")
    print("----------"*10)