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

        # Extract the title from the <h2> tag and strip any surrounding whitespace
        title = div.find('h2').text.strip()

        instance['Summary'] = title
        # Find the <a> tag that contains the href attribute
        link_tag = div.find('a', href=True)

        if link_tag:  # Ensure that the <a> tag was found
            url = link_tag['href']  # Get the value of the href attribute from the <a> tag
            instance['URL'] = url
        else:
            instance['URL'] = None  # If no <a> tag was found, set url to None

        # Find the <div> with class "item-label" within the outer div
        label_date_div = div.find('div', class_='item-label')

        # Extract date and label
        date = label_date_div.find('span', class_='h-datetime').text.strip()
        label = label_date_div.find('span', class_='h-tags').text.strip()
        instance['Date'] = date
        instance['Final Label'] = label

        url_list.append(instance)


def parse_news_page(hacker_news_page_html_path, hacker_url_list_csv_path):
    """
    Parse the Hacker News page HTML content and extract the details of news items.

    Args:
        hacker_news_page_html_path (str): The file path of the Hacker News page HTML.
        hacker_url_list_csv_path (str): The file path to save the extracted news details in CSV format.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: Executing parse_news_page...")

    try:
        # Read the HTML content of the news page
        with open(hacker_news_page_html_path, "r") as file:
            html_content = file.read()
        # Parse the HTML content and extract the news details
        soup = BeautifulSoup(html_content, 'html.parser')

        position_div_list = soup.find_all("div", class_="body-post clear")

        url_list = []
        get_url_list(url_list, position_div_list)
        df = pd.DataFrame(url_list)

        # Check if the CSV file already exists
        if os.path.exists(hacker_url_list_csv_path):
            # Read the existing CSV to get its columns
            existing_df = pd.read_csv(hacker_url_list_csv_path)

            # Reorder the new DataFrame's columns to match the existing CSV
            df = df.reindex(columns=existing_df.columns)

            # Append the new data to the existing file
            df.to_csv(path_or_buf=hacker_url_list_csv_path, mode="a", index=False, header=False)
        else:
            # If it does not exist, create a new file and add data
            df.to_csv(path_or_buf=hacker_url_list_csv_path, mode="w", index=False)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"{timestamp}: Success - parse_news_page completed successfully, URL list saved to {hacker_url_list_csv_path}.")

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
    hacker_news_page_html_path = f"./Data/hacker_news_{today_str}.html"
    hacker_url_list_csv_path = f"./Data/{today_str}_final.csv"
    parse_news_page(hacker_news_page_html_path, hacker_url_list_csv_path)

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"{self_name} took time: {duration}")
    print("----------" * 10)
