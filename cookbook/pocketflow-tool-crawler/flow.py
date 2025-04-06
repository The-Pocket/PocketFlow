from pocketflow import Flow
from nodes import CrawlWebsiteNode, AnalyzeContentBatchNode, GenerateReportNode

def create_flow() -> Flow:
    """Create and configure the crawling flow
    
    Returns:
        Flow: Configured flow ready to run
    """
    # Create nodes
    crawl = CrawlWebsiteNode()
    analyze = AnalyzeContentBatchNode()
    report = GenerateReportNode()
    
    # Connect nodes
    crawl >> analyze >> report
    
    # Create flow starting with crawl
    return Flow(start=crawl)
