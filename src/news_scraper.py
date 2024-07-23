import random
import time
from bs4 import BeautifulSoup
import requests
import logging
import argparse
from requests.exceptions import RequestException, HTTPError, Timeout, TooManyRedirects
    

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = requests.Session()


def get_page_content(url, headers):
    """
    Make a request to the given URL and parse it into a BeautifulSoup object
    """
    try:
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, "html.parser")
            return soup
        else:
            logger.warning(f"Request has failed with status code: {request.status_code}")
            return None
    except (RequestException, HTTPError, Timeout, TooManyRedirects) as ex:
        logger.error(f"Request error: {ex}")
        return None
    except Exception as ex:
        logger.error(f"An error occurred :{ex}")
        return None


def maintain_themes(soup, file):
    """
    Process the themes from the parsed HTML content and log the GitHub links
    """
    themes = soup.find_all("td", class_="title")

    for theme in themes:
        theme = theme.find("span", {'class': 'titleline'})
        if theme is not None:
            link_tag = theme.select_one('.titleline > a')
            if link_tag and 'github.com' in str(link_tag):
                link = link_tag.get('href')

                logger.info(f"{theme.text.strip()}: {link}")
                logger.info("====")

                save_links(theme.text.strip(), link, file)


def get_next_page(soup):
    """
    Extract the suffix for the next page
    """
    next_page = soup.find(class_="morelink")
    if next_page:
        next_link = next_page.get('href')
        return next_link[6:]
    else:
        return None


def save_links(text, link, outputfile):
    """
    Save the links and its associated text to a file
    """
    with open(outputfile, 'a') as file:
        file.write(f"{text}: {link}\n\n")


def main(url, max_retries, retry_delay, file):
    """
    Main function to control the flow of the script
    """
    suffix = ""

    # Configuration
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://news.ycombinator.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive'
    }

    while True:
        time.sleep(3)
        delay = retry_delay
        attempt = 0
        for attempt in range(max_retries):
            page = url + suffix
            logger.info(page)

            soup = get_page_content(page, headers)
            if soup:
                maintain_themes(soup, file)
                suffix = get_next_page(soup)
                break  # Successful request, break the inner for loop

            # Calculate next retry delay
            time.sleep(delay)
            jitter = random.uniform(0, delay * 0.1)
            delay = min(delay * 2, 120) + jitter

        if attempt + 1 == max_retries:
            logger.error("Max retries reached. Exiting.")
            break  # Error request, break the outer while loop


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape GitHub links from Hacker News.")
    parser.add_argument("--url", type=str, default="https://news.ycombinator.com/newest", help="Base URL to start scraping from")
    parser.add_argument("--max_retries", type=int, default=7, help="Maximum number of retries for failed requests")
    parser.add_argument("--retry_delay", type=int, default=7, help="Initial delay between retries")
    parser.add_argument("--file", type=str, default="links.txt", help="File to save the extracted links")
    parser.add_argument("--log_level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")
    args = parser.parse_args()

    logger.setLevel(getattr(logging, args.log_level.upper()))

    main(args.url, args.max_retries, args.retry_delay, args.file)
