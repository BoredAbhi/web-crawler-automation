# Web Crawler Automation

A multi-threaded Python crawler with retry logic, rate limiting, and export to JSON/CSV. Useful for mapping endpoint structures during CTFs, bug bounties, or internal app testing.

## Features
- Threaded crawling (5 threads)
- Depth-limited (default: 2)
- Rate limiting (1 request/sec/thread)
- Output: `output.json`, `output.csv`

## Usage
```bash
python web_crawler.py
```
Enter a seed URL when prompted

## Dependencies
- requests
- beautifulsoup4
