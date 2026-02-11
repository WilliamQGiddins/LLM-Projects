import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """

    # Configure headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use Webdriver-manager to manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Initialize the Chrome WebDriver 
    driver = webdriver.Chrome(service=service, options=options)

    # Start WebDriver
    driver.get(url);

    # Wait for page to load
    time.sleep(5)

    # Fetch page source
    page_source = driver.page_source
    driver.quit()

    # Parse page
    soup = BeautifulSoup(page_source, 'html.parser')

    # Remove unnecesssary elements
    for irrelevant in soup.body(["scripts", "style", "img", "input"]):
        irrelevant.decompose

    # Extract content
    title = soup.title.string if soup.title else "No title found"
    text = soup.body.get_text(separator='\n', strip=True)
    links = [link.get("href") for link in soup.find_all("a")]


    return {"url": url, "title" : title, "text" : text, "links" : [link for link in links if link]}
