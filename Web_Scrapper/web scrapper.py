import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def scrape_website(url, max_depth=10, item_selector='p'):
    visited = set()  # To keep track of visited URLs
    queue = deque([(url, 0)])  # Queue holds tuples of (URL, current_depth)
    scraped_items = []  # To store scraped content

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    while queue:
        current_url, depth = queue.popleft()

        # Skip if we have already visited this URL or reached max depth
        if current_url in visited or depth >= max_depth:
            continue
        
        # Send HTTP request to the URL
        try:
            response = requests.get(current_url, headers=headers, timeout=5)
            response.raise_for_status()
            print(f"Scraping: {current_url} (Depth: {depth})")  # Debugging
            scraped_items.extend(f"\n\nScraping: {current_url} (Depth: {depth})\n\n")
        except requests.RequestException as e:
            print(f"Failed to scrape {current_url}: {e}")
            scraped_items.extend(f"\n\nFailed to scrape {current_url}: {e}\n\n")
            continue
        
        # Mark the URL as visited
        visited.add(current_url)
        
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape items (e.g., paragraphs or other content based on item_selector)
        items = [item.get_text(strip=True) for item in soup.select(item_selector)]
        scraped_items.extend(items)
        
        # Print the content from the current page (optional)
        '''print("\nScraped Content:")
        for item in items:
            print(item)'''
        
        # Find and enqueue all the hyperlinks (<a> tags) on the page
        for link in soup.find_all('a', href=True):
            next_url = urljoin(current_url, link['href'])  # Get the full URL
            if next_url not in visited:
                queue.append((next_url, depth + 1))  # Add the link to the queue with incremented depth
    
    return scraped_items

def save_to_file(scraped_items, filename="scraped_content.txt"):
    # Open a file in write mode and store the scraped items
    with open(filename, 'w', encoding='utf-8') as file:
        for item in scraped_items:
            file.write(item + "\n")  # Write each item in a new line

    print(f"Content saved to {filename}")

if __name__ == "__main__":
    start_url = "https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU"
    max_depth = 3  # You can change this to whatever depth you need
    scraped_data = scrape_website(start_url, max_depth=max_depth)
    
    '''print("\nFinal Scraped Items:")
    for item in scraped_data[:20]:  # Print first 20 items as a sample
        print(item)'''
    
    save_to_file(scraped_data, "scraped_content.txt")

    print("Scraping completed.")




'''
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    # Get the Content-Type from the response headers
    content_type = response.headers.get('Content-Type', '').lower()

    # Check if the content is HTML or XML
    if 'html' in content_type:
        print("Content is HTML")
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse as HTML
    elif 'xml' in content_type or 'xhtml' in content_type:
        print("Content is XML or XHTML")
        soup = BeautifulSoup(response.text, 'xml')  # Parse as XML
    else:
        print("Unknown content type")
        return
    
    # Now you can continue with your scraping logic
    items = soup.find_all('p')  # Example: looking for <p> tags
    for item in items:
        print(item.get_text())

# Example usage
scrape_website("https://job-boards.greenhouse.io/opensesame/jobs/6560064?gh_jid=6560064&gh_src=997b50af1us")'''

