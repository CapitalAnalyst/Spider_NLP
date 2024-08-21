import datetime
import os
import requests
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

        # Extract the title from the <div> with the appropriate class
        title_div = div.find('div', class_='field--name-node-title')
        if title_div:
            title = title_div.text.strip()
            instance['Summary'] = title
        else:
            instance['Summary'] = None

        # Find the <a> tag that contains the href attribute
        link_tag = div.find('a', href=True)

        if link_tag:  # Ensure that the <a> tag was found
            url = link_tag['href']  # Get the value of the href attribute from the <a> tag
            instance['URL'] = "https://afp.gov.au" + url
        else:
            instance['URL'] = None  # If no <a> tag was found, set url to None

        # Find the <div> with class "card--date"
        date_div = div.find('div', class_='card--date')
        if date_div:
            date = date_div.text.strip()
            instance['Date'] = date
        else:
            instance['Date'] = None

        instance['Final Label'] = 'cyber'

        url_list.append(instance)

def parse_news_page(search_term, afp_url_list_csv_path):
    """
    Parse the AFP news page by sending a request with the search term and extract the details of news items.

    Args:
        search_term (str): The search term to use in the request.
        afp_url_list_csv_path (str): The file path to save the extracted news details in CSV format.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: Executing parse_news_page...")

    try:
        # Define the URL and the search parameters
        url = 'https://www.afp.gov.au/news-centre'
        params = {'title': search_term}

        # Send the GET request to the website
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check that the request was successful

        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the divs that contain the news items
        position_div_list = soup.find_all("div", class_="node--type-article")

        url_list = []
        get_url_list(url_list, position_div_list)
        df = pd.DataFrame(url_list)

        # Check if the CSV file already exists
        if os.path.exists(afp_url_list_csv_path):
            # Read the existing CSV to get its columns
            existing_df = pd.read_csv(afp_url_list_csv_path)

            # Reorder the new DataFrame's columns to match the existing CSV
            df = df.reindex(columns=existing_df.columns)

            # Append the new data to the existing file
            df.to_csv(path_or_buf=afp_url_list_csv_path, mode="a", index=False, header=False)
        else:
            # If it does not exist, create a new file and add data
            df.to_csv(path_or_buf=afp_url_list_csv_path, mode="w", index=False)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"{timestamp}: Success - parse_news_page completed successfully, URL list saved to {afp_url_list_csv_path}.")

    except requests.exceptions.RequestException as ex:
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
    search_term = 'cyber'
    afp_url_list_csv_path = f"./Data/{today_str}_final.csv"
    parse_news_page(search_term, afp_url_list_csv_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"{self_name} took time: {duration}")
    print("----------" * 10)
