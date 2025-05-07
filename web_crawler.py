import requests
from bs4 import BeautifulSoup
import threading
import time
import json
import csv
from urllib.parse import urljoin, urlparse
from queue import Queue

visited = set()
lock = threading.Lock()
output = []
q = Queue()

MAX_THREADS = 5
MAX_DEPTH = 2
RATE_LIMIT = 1  # seconds between requests per thread

def crawl(url, depth):
    try:
        time.sleep(RATE_LIMIT)
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        with lock:
            output.append({'url': url, 'title': soup.title.string if soup.title else ''})

        if depth < MAX_DEPTH:
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                parsed = urlparse(absolute_url)
                if parsed.scheme.startswith('http'):
                    with lock:
                        if absolute_url not in visited:
                            visited.add(absolute_url)
                            q.put((absolute_url, depth + 1))

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

def worker():
    while not q.empty():
        url, depth = q.get()
        crawl(url, depth)
        q.task_done()

def start_crawl(seed_url):
    visited.add(seed_url)
    q.put((seed_url, 0))
    threads = []

    for _ in range(MAX_THREADS):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    for t in threads:
        t.join()

    print("Crawling completed.")

    # Save to JSON
    with open('output.json', 'w') as f:
        json.dump(output, f, indent=2)

    # Save to CSV
    with open('output.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title'])
        writer.writeheader()
        writer.writerows(output)

if __name__ == "__main__":
    seed = input("Enter the seed URL: ").strip()
    start_crawl(seed)
