from pocketflow import Flow
from nodes import CurateSources, FilterStories, SummarizeStories, FormatNewsletter

def create_newsletter_flow():
    """
    Create a linear newsletter curation pipeline.

    The flow works like this:
    1. CurateSources searches the web for multiple topics
    2. FilterStories picks the 4 most interesting stories
    3. SummarizeStories writes punchy newsletter blurbs
    4. FormatNewsletter creates a formatted markdown newsletter

    Returns:
        Flow: A complete newsletter generation flow
    """
    # Create node instances
    curate = CurateSources()
    filter_node = FilterStories()
    summarize = SummarizeStories()
    format_node = FormatNewsletter()

    # Connect the linear chain
    curate >> filter_node >> summarize >> format_node

    return Flow(start=curate)
