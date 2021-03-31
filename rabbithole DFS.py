# Import shit
import requests  
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama # Just used for diff colors while outputting

# Timeout func imports


# Need this global variable. 
external_urls = set() 
# Colorama stuff
colorama.init()
GREEN = colorama.Fore.GREEN

# Since not all links in <a> tags are valid, some link to parts of site, others are JS. This validates those URLs
def valid_url(url):
    # Makes sure there's an existing protocol and domain name exists in the URL
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_links(url, *connections):
    global total_urls_visited

    # Used set datatype to prevent useless links and potential duplicates
    urls = set()
    # Extract the domain name from the URL, to check if the link is external or internal
    domain_name = urlparse(url).netloc
    # Some sites load their shit using JS, so this try except and session code will account for JS
    session = HTMLSession()
    response = session.get(url)
    try:
        response.html.render()
    except: 
        pass
    # Parse the messy HTML content into nice, readable SouP
    soup = BeautifulSoup(response.html.html, "html.parser")
    # Get all <a> tags of HTML, and check if they're empty or not
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href== "" or href is None:
            continue
        # Since some links are not absolute, join the relative URL with its domain to get absolute url 
        href = urljoin(url,href)
        # Remove URL GET params and fragments of other urls, make urls clean and not redundant
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        # Check if urls are valid. If it's not, continue to next link.
        if not valid_url(href): 
            continue
        # Check if domain name exists in href or not, add it to external links
        if domain_name not in href:
            if href not in external_urls:
                total_urls_visited +=1
                print(f"{GREEN} New link: {href}")
                external_urls.add(href)
                while True:
                    try:
                        get_links(href)
                    except:
                        exit()
            continue
    
        urls.add(href)
    return urls

total_urls_visited = 0
# Crawls the site, gets all links and recursively visits those links, grabs the links etc. To prevent recursion error,
# max urls is defined as 78. 
def crawler(url, max_urls=78):
    
    links = get_links(url)
    for link in links:
        if total_urls_visited > max_urls: break
        crawler(link, max_urls=total_urls_visited)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Enter a value for max urls")
    parser.add_argument("url")
    parser.add_argument("-m", "--max-urls", default=78,type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    crawler(url, max_urls=max_urls) 

    print("Total External links:", len(external_urls))
    domain_name = urlparse(url).netloc

    """with open(f"{domain_name} links.txt","w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)
"""