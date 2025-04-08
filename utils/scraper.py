"""
Utility functions for scraping websites and LinkedIn profiles.
This module serves as a unified interface to various specialized scrapers.
"""

import logging
from typing import Dict, Any, Optional
import utils.web_scraper as web
import utils.linkedin_scraper as linkedin

def scrape_website(url: str) -> Optional[str]:
    """
    Scrape content from a website URL.
    
    Args:
        url: The URL of the website to scrape
        
    Returns:
        String containing the scraped content, or None if scraping failed
    """
    logging.info(f"Scraping website content from: {url}")
    return web.call_firecrawl(url)

def scrape_linkedin(url: str) -> Optional[str]:
    """
    Scrape content from a LinkedIn profile or company page.
    
    Args:
        url: The URL of the LinkedIn profile/company to scrape
        
    Returns:
        String containing the structured LinkedIn data, or None if scraping failed
    """
    logging.info(f"Scraping LinkedIn content from: {url}")
    result = linkedin.call_apify_linkedin_profile(url)
    
    # If there was an error, return None
    if isinstance(result, dict) and "error" in result:
        logging.error(f"LinkedIn scraping failed: {result['error']}")
        return None
        
    # Format the LinkedIn data as text for LLM consumption
    try:
        formatted_data = format_linkedin_data(result)
        return formatted_data
    except Exception as e:
        logging.error(f"Error formatting LinkedIn data: {e}")
        return None

def format_linkedin_data(data: Dict[str, Any]) -> str:
    """
    Format raw LinkedIn profile data as a structured text.
    
    Args:
        data: Raw LinkedIn profile data dictionary
        
    Returns:
        Formatted text containing key LinkedIn profile information
    """
    if not data:
        return "No data available"
        
    sections = []
    
    # Basic profile info
    basic_info = []
    if data.get("fullName"):
        basic_info.append(f"Name: {data['fullName']}")
    if data.get("title"):
        basic_info.append(f"Title: {data['title']}")
    if data.get("location"):
        basic_info.append(f"Location: {data['location']}")
    if data.get("summary"):
        basic_info.append(f"Summary: {data['summary']}")
        
    if basic_info:
        sections.append("PROFILE INFORMATION\n" + "\n".join(basic_info))
    
    # Work experience
    experience = data.get("experience", [])
    if experience:
        exp_items = []
        for job in experience:
            job_desc = []
            company = job.get("companyName", "Unknown Company")
            title = job.get("title", "Unknown Title")
            dates = f"{job.get('dateRange', 'Unknown dates')}"
            
            job_desc.append(f"- {title} at {company} ({dates})")
            if job.get("description"):
                job_desc.append(f"  Description: {job['description']}")
                
            exp_items.append("\n".join(job_desc))
            
        sections.append("WORK EXPERIENCE\n" + "\n".join(exp_items))
    
    # Education
    education = data.get("education", [])
    if education:
        edu_items = []
        for school in education:
            school_name = school.get("schoolName", "Unknown School")
            degree = school.get("degree", "")
            field = school.get("fieldOfStudy", "")
            dates = school.get("dateRange", "")
            
            edu_info = f"- {school_name}"
            if degree and field:
                edu_info += f", {degree} in {field}"
            elif degree:
                edu_info += f", {degree}"
            if dates:
                edu_info += f" ({dates})"
                
            edu_items.append(edu_info)
            
        sections.append("EDUCATION\n" + "\n".join(edu_items))
    
    # Skills
    skills = data.get("skills", [])
    if skills:
        skill_items = [f"- {skill}" for skill in skills]
        sections.append("SKILLS\n" + "\n".join(skill_items))
    
    # Combine all sections
    return "\n\n".join(sections) 