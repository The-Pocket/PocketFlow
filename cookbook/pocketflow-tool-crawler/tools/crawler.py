import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set

class WebCrawler:
    """Simple web crawler that extracts content and follows links"""
    
    def __init__(self, base_url: str, max_pages: int = 10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited: Set[str] = set()
        
    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain"""
        base_domain = urlparse(self.base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain
        
    def extract_page_content(self, url: str) -> Dict:
        """Extract content from a single page"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract main content
            content = {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "text": soup.get_text(separator="\n", strip=True),
                "links": []
            }
            
            # Extract links
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    absolute_url = urljoin(url, href)
                    if self.is_valid_url(absolute_url):
                        content["links"].append(absolute_url)
            
            return content
            
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None
    
    def crawl(self) -> List[Dict]:
        """Crawl website starting from base_url"""
        to_visit = [self.base_url]
        results = []
        
        while to_visit and len(self.visited) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited:
                continue
                
            print(f"Crawling: {url}")
            content = self.extract_page_content(url)
            
            if content:
                self.visited.add(url)
                results.append(content)
                
                # Add new URLs to visit
                new_urls = [url for url in content["links"] 
                          if url not in self.visited 
                          and url not in to_visit]
                to_visit.extend(new_urls)
        
        return results
