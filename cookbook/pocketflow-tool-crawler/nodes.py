from tools.crawler import WebCrawler
from tools.parser import analyze_site

from pocketflow import BatchNode, Node


class CrawlWebsiteNode(Node):
    """Node to crawl a website and extract content"""
    
    def prep(self, shared):
        return shared.get("base_url"), shared.get("max_pages", 10)
        
    def exec(self, prep_res):
        base_url, max_pages = prep_res
        if not base_url:
            return []
            
        crawler = WebCrawler(base_url, max_pages)
        return crawler.crawl()
        
    def post(self, shared, prep_res, exec_res):
        shared["crawl_results"] = exec_res
        return "default"

class AnalyzeContentBatchNode(BatchNode):
    """Node to analyze crawled content in batches"""
    
    def prep(self, shared):
        results = shared.get("crawl_results", [])
        # Process in batches of 5 pages
        batch_size = 5
        return [results[i:i+batch_size] for i in range(0, len(results), batch_size)]
        
    def exec(self, prep_res):
        return analyze_site(prep_res)
        
    def post(self, shared, prep_res, exec_res):
        # Flatten results from all batches
        all_results = []
        for batch_results in exec_res:
            all_results.extend(batch_results)
            
        shared["analyzed_results"] = all_results
        return "default"

class GenerateReportNode(Node):
    """Node to generate a summary report of the analysis"""
    
    def prep(self, shared):
        return shared.get("analyzed_results", [])
        
    def exec(self, prep_res):
        if not prep_res:
            return "No results to report"
            
        report = []
        report.append("Analysis Report\n")
        report.append(f"Total pages analyzed: {len(prep_res)}\n")
        
        for page in prep_res:
            report.append(f"\nPage: {page['url']}")
            report.append(f"Title: {page['title']}")
            
            analysis = page.get("analysis", {})
            report.append(f"Summary: {analysis.get('summary', 'N/A')}")
            report.append(f"Topics: {', '.join(analysis.get('topics', []))}")
            report.append(f"Content Type: {analysis.get('content_type', 'unknown')}")
            report.append("-" * 80)
            
        return "\n".join(report)
        
    def post(self, shared, prep_res, exec_res):
        shared["report"] = exec_res
        print("\nReport generated:")
        print(exec_res)
        return "default"
