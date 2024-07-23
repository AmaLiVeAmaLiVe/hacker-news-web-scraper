import unittest
from unittest.mock import patch, mock_open, MagicMock
from bs4 import BeautifulSoup
import sys

sys.path.insert(0, 'D:\Pet projects\Web Scraper\src')

import news_scraper


class TestScraper(unittest.TestCase):

    @patch('news_scraper.requests.get')
    def test_get_page_content_success(self, mock_get):
        # Mock the response of requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = "https://example.com"
        result = news_scraper.get_page_content(url, headers)
        self.assertIsInstance(result, BeautifulSoup)

    @patch('news_scraper.requests.get')
    def test_get_page_content_failure(self, mock_get):
        # Mock the response of requests.get
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = "https://example.com"
        result = news_scraper.get_page_content(url, headers)
        self.assertIsNone(result)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_links(self, mock_file):
        text = "Test Title"
        link = "https://github.com/test"
        output_file = "test_links.txt"

        news_scraper.save_links(text, link, output_file)
        mock_file().write.assert_called_once_with(f"{text}: {link}\n\n")

    def test_get_next_page(self):
        html_content = '<a class="morelink" href="newest?p=2">More</a>'
        soup = BeautifulSoup(html_content, "html.parser")
        result = news_scraper.get_next_page(soup)
        self.assertEqual(result, "?p=2")

    @patch('news_scraper.save_links')
    def test_maintain_themes(self, mock_save_links):
        html_content = '''
        <tr class='athing'>
            <td class='title'>
                <span class='titleline'>
                    <a href='https://github.com/test'>Test Title</a>
                </span>
            </td>
        </tr>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        output_file = "test_links.txt"

        news_scraper.maintain_themes(soup, output_file)
        mock_save_links.assert_called_once_with("Test Title", "https://github.com/test", output_file)


if __name__ == "__main__":
    unittest.main()
