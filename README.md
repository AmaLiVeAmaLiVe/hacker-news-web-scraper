# My Scraping Project

This project scrapes GitHub links from the latest posts on Hacker News.

## Features

- Scrapes the newest posts on Hacker News
- Extracts and logs GitHub links
- Handles HTTP errors and retries failed requests
- Configurable through command-line arguments

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AmaLiVeAmaLiVe/hacker-news-web-scraper.git
    cd my-scraping-project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with default settings:
```bash
python src/news_scraper.py
