# Python Web Scraper

I built this Python-based web scraper to help identify pages on a website that contain specific keywords (e.g., product names). The scraper crawls through the site recursively, searches for occurrences of the keywords, and outputs the results to a CSV file. It also outputs  a list of broken links to a separate `errors.log` file.

## Features
- Recursively crawls a website starting from a base URL.
- Identifies and lists pages containing specified keywords.
- Supports configuration through command-line arguments or a JSON config file.
- Logs errors and broken links in a separate `errors.log` file for debugging.
- Uses persistent sessions to manage headers and cookies efficiently.
- Saves results to a CSV file for easy analysis.

## Requirements
- Python 3.10+
- `requests`
- `beautifulsoup4`

Install the dependencies with:
```bash
pip install -r requirements.txt
```

## Configuration
The scraper supports two methods for providing the base URLs and keywords:

1. **Command-Line Arguments**
   - **Base URLs**: Provide one or more base URLs separated by spaces.
   - **Keywords**: Provide a comma-separated list of keywords.

   Example:
   ```bash
   python scraper.py https://example.com https://another-site.com -k "keyword1,keyword2"
   ```

2. **Configuration File**
   - Copy the provided `config.json-example` file to `config.json` and edit it with your settings, specifically:
     - `base_urls`
     - `keywords`

   Example `config.json`:
   ```json
   {
       "base_urls": [
           "https://example.com",
           "https://another-example.com"
       ],
       "keywords": [
           "ProductName1",
           "ProductName2",
           "Keyword3"
       ]
   }
   ```
   Run the scraper with the configuration file:
   ```bash
   python scraper.py -c config.json
   ```

## Logging
The scraper logs errors and broken links to an `errors.log` file, capturing details such as the URL that failed to load and the referring page.

## Usage
1. [Fork](https://github.com/jerdog/web-scraper/fork) and Clone this repository:
   ```bash
   git clone <repository_url>
   cd web-scraper
   ```
2. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```
3. Run the scraper using either command-line arguments or a configuration file:
   - Command-line arguments:
     ```bash
     python scraper.py https://example.com https://another-site.com -k "product1,product2"
     ```
   - Configuration file:
     ```bash
     python scraper.py -c config.json
     ```
4. Check the output in `pages_with_keywords.csv`.

## Output
The script generates a CSV file with the following columns:
- **URL**: The URL of the page where keywords were found.
- **Keywords**: The keywords that were matched on the page.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions
Feel free to open issues or submit pull requests to improve the scraper.
