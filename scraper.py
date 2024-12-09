import requests
from bs4 import BeautifulSoup
import re
import csv
import argparse
import json
import logging

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# A function to fetch and parse a page
def fetch_page(url, session, referring_page=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = session.get(url, headers=headers, allow_redirects=True)  # Use session for persistent headers and cookies
        if response.history:
            print(f"Request to {url} was redirected to {response.url}")
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Failed to fetch {url}: Status {response.status_code}. Referring page: {referring_page}")
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}. Referring page: {referring_page}")
    return None

# A function to find keywords in a page
def find_keywords(content, keywords):
    found = []
    for keyword in keywords:
        if re.search(rf"\b{keyword}\b", content, re.IGNORECASE):
            found.append(keyword)
    return found

# A function to recursively crawl pages
def crawl_site(base_url, keywords, visited, results, session):
    to_visit = [base_url]

    while to_visit:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        print(f"Crawling: {current_url}")
        visited.add(current_url)
        html_content = fetch_page(current_url, session, referring_page=None)
        
        if not html_content:
            continue

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for keywords
        keywords_found = find_keywords(html_content, keywords)
        if keywords_found:
            results.append({"url": current_url, "keywords": keywords_found})

        # Find links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith("/"):
                href = base_url.rstrip("/") + href
            elif not href.startswith("http"):
                href = base_url.rstrip("/") + "/" + href
            if href.startswith(base_url) and href not in visited:
                if not fetch_page(href, session, referring_page=current_url):
                    logging.error(f"Broken link found: {href}. Referring page: {current_url}")
                to_visit.append(href)

# Load configuration from a file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config.get("base_urls", []), config.get("keywords", [])
    except Exception as e:
        logging.error(f"Error loading configuration file: {e}")
        return [], []

# Main function
def main():
    parser = argparse.ArgumentParser(description="Web scraper to find pages with specific keywords.")
    parser.add_argument('base_urls', nargs='*', help="Base URLs to start crawling from.")
    parser.add_argument('-k', '--keywords', help="Comma-separated list of keywords to search for.")
    parser.add_argument('-c', '--config', help="Path to a JSON configuration file containing base URLs and keywords.")
    args = parser.parse_args()

    base_urls = []
    keywords = []

    # Load from config file if provided
    if args.config:
        config_urls, config_keywords = load_config(args.config)
        base_urls.extend(config_urls)
        keywords.extend(config_keywords)

    # Override with command-line arguments if provided
    if args.base_urls:
        base_urls.extend(args.base_urls)
    if args.keywords:
        keywords.extend(args.keywords.split(','))

    if not base_urls or not keywords:
        logging.error("Error: No base URLs or keywords provided.")
        print("Error: No base URLs or keywords provided. Check errors.log for details.")
        return

    visited = set()
    results = []

    # Use requests.Session for persistent headers and cookies
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    # Start crawling for each base URL
    for base_url in base_urls:
        print(f"Starting crawl at: {base_url}")
        crawl_site(base_url, keywords, visited, results, session)

    # Write results to CSV
    output_file = "pages_with_keywords.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({"url": result["url"], "keywords": ", ".join(result["keywords"])})

    print(f"Crawling complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
