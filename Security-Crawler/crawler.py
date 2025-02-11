import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from urllib.robotparser import RobotFileParser
from collections import deque
import os

class Crawler:
    """
    A scalable web crawler for security-focused data collection.
    """

    USER_AGENT = "SecurityLLMCrawler/1.2 (+your-email@example.com)"  # Replace with your contact
    DEFAULT_CRAWL_DELAY = 2  # seconds

    def __init__(self, seed_urls, allowed_domains, output_dir="crawled_data"):
        """
        Initialize the Crawler.

        Args:
            seed_urls (list): List of starting URLs.
            allowed_domains (list): List of domains to stay within.
            output_dir (str, optional): Directory to save crawled data. Defaults to "crawled_data".
        """
        self.seed_urls = seed_urls
        self.allowed_domains = allowed_domains
        self.output_dir = output_dir
        self.url_queue = deque(seed_urls)
        self.visited_urls = set()
        self.crawl_delay = self.DEFAULT_CRAWL_DELAY
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def get_robots_url(url):
        """
        Construct the robots.txt URL for a given website URL.

        Args:
            url (str): Website URL.

        Returns:
            str: robots.txt URL.
        """
        parsed_url = urllib.parse.urlparse(url)
        return urllib.parse.urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")

    def can_crawl(self, url):
        """
        Check if crawling is allowed by robots.txt for the given URL.

        Args:
            url (str): URL to check.

        Returns:
            bool: True if crawling is allowed, False otherwise.
        """
        robots_url = self.get_robots_url(url)
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()  # Might raise errors if robots.txt is unavailable
            return rp.can_fetch(self.USER_AGENT, url)
        except Exception as e:
            print(f"Error reading robots.txt from {robots_url}: {e}")
            return True  # Be permissive if robots.txt is unavailable (or handle more strictly)

    def crawl_page(self, url):
        """
        Crawl a single web page, extract text and links, and save the data.

        Args:
            url (str): URL of the page to crawl.
        """
        if url in self.visited_urls:
            return

        if not any(domain in url for domain in self.allowed_domains):
            print(f"Skipping URL outside allowed domains: {url}")
            self.visited_urls.add(url)
            return

        if not self.can_crawl(url):
            print(f"Robots.txt disallows crawling: {url}")
            self.visited_urls.add(url)
            return

        try:
            print(f"Crawling: {url}")
            headers = {'User-Agent': self.USER_AGENT}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text

            soup = None
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
            except Exception as soup_error:
                print(f"Error parsing HTML with BeautifulSoup for {url}: {soup_error}")
                soup = None

            article_text = "" # Initialize outside the if soup block

            if soup:
                # **--- Conditional Text Extraction based on Website ---**
                if "thehackernews.com" in url:
                    # For thehackernews.com, extract titles and descriptions
                    titles = soup.find_all('h2', class_='home-title')
                    descriptions = soup.find_all('div', class_='home-desc')

                    for title in titles:
                        article_text += title.text.strip() + "\n"
                    for desc in descriptions:
                        article_text += desc.text.strip() + "\n"

                elif "securityweek.com" in url: # Example for securityweek.com - adjust selectors based on inspection
                    # Add specific selectors for securityweek.com if needed, else fall through to default
                    paragraphs = soup.find_all('p') # Default to <p> tags for securityweek.com for now

                elif "nist.gov" in url: # Example for nist.gov - adjust selectors based on inspection
                    # Add specific selectors for nist.gov if needed, else fall through to default
                    paragraphs = soup.find_all('p') # Default to <p> tags for nist.gov for now

                elif "darkreading.com" in url: # Example for darkreading.com - adjust selectors based on inspection
                    # Add specific selectors for darkreading.com if needed, else fall through to default
                    paragraphs = soup.find_all('p') # Default to <p> tags for darkreading.com for now

                else:
                    # Default: Extract <p> tags (for other websites, adjust as needed)
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        article_text += p.text.strip() + "\n"

                if "thehackernews.com" not in url: # Only loop through paragraphs if not thehackernews (already handled titles/descriptions)
                    if 'paragraphs' in locals(): # Check if paragraphs variable is defined (might not be in all conditions)
                        for p in paragraphs:
                            article_text += p.text.strip() + "\n"

                # Save the extracted text
                filename = os.path.join(self.output_dir, f"page_{len(self.visited_urls) + 1}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n\n")
                    f.write(article_text)

                # **--- Extract Links (No changes needed here) ---**
                links = soup.find_all('a', href=True)
                for link in links:
                    absolute_url = urllib.parse.urljoin(url, link['href'])
                    if any(domain in absolute_url for domain in self.allowed_domains) and absolute_url not in self.visited_urls:
                        self.url_queue.append(absolute_url)
            else:
                print(f"Skipping text/link extraction for {url} due to BeautifulSoup parsing error.")

            self.visited_urls.add(url)
            time.sleep(self.crawl_delay)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling (request failed) {url}: {e}")
        except Exception as e:
            print(f"Error processing (other) {url}: {e}")

    def run_crawler(self):
        """
        Run the main crawling loop.
        """
        while self.url_queue:
            current_url = self.url_queue.popleft()
            self.crawl_page(current_url)
        print("Crawling finished.")


if __name__ == "__main__":
    seed_urls = [
        "https://www.securityweek.com/",
        "https://thehackernews.com/",
        "https://www.nist.gov/nvd",
        "https://www.darkreading.com/"
    ]
    allowed_domains = [
        "securityweek.com",
        "thehackernews.com",
        "nist.gov",
        "nvd.nist.gov",
        "darkreading.com"
    ]

    crawler = Crawler(seed_urls, allowed_domains, output_dir="security_crawl_data_oop")
    crawler.run_crawler()