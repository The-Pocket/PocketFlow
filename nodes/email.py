"""Email-related node classes."""

import logging
from pocketflow import Node
from utils.generators import generate_email

class GenerateEmail(Node):
    """Generates a personalized email based on analysis of lead data."""
    def prep(self, shared):
        """Prepare context for email generation."""
        # Gather all context for email creation
        context = {
            "lead_first_name": shared.get('lead_first_name', ''),
            "lead_last_name": shared.get('lead_last_name', ''),
            "company_name": shared.get('company_name', ''),
            "product_service": shared.get('product_service', ''),
            "company_website": shared.get('company_website', ''),
            "linkedin_url": shared.get('linkedin_url', ''),
            "website_report": shared.get('website_report', ''),
            "linkedin_report": shared.get('linkedin_report', ''),
            "precision_intelligence_report": shared.get('precision_intelligence_report', ''),
            "dev_local_mode": shared.get("dev_local_mode", False) # Pass dev mode flag
        }
        
        # Check if we have enough data to generate a meaningful email
        if not context["lead_first_name"] and not context["lead_last_name"]:
            logging.warning("Missing lead name for email generation")
            return None
            
        # Check if we have at least one report
        has_reports = any([
            bool(context["website_report"]) and not str(context["website_report"]).startswith("Analysis failed") and not str(context["website_report"]).startswith("Error"),
            bool(context["linkedin_report"]) and not str(context["linkedin_report"]).startswith("Analysis failed") and not str(context["linkedin_report"]).startswith("Error"),
            bool(context["precision_intelligence_report"]) and not str(context["precision_intelligence_report"]).startswith("Analysis failed") and not str(context["precision_intelligence_report"]).startswith("Error")
        ])
        
        if not has_reports:
            logging.warning("No valid analysis reports available for email generation")
            # Continue anyway, but with limited personalization
            
        logging.info("Preparing context for email generation")
        return context
        
    def exec(self, context):
        """Generate email using LLM."""
        if not context:
            return {"subject": "Error: Insufficient data", "body": "Could not generate email due to insufficient lead data."}
            
        # Call the specific generator function, passing context directly
        email_result = generate_email(
            lead_first_name=context.get("lead_first_name", ""),
            lead_last_name=context.get("lead_last_name", ""),
            company_name=context.get("company_name", ""),
            product_service=context.get("product_service", ""),
            company_website=context.get("company_website", ""),
            linkedin_url=context.get("linkedin_url", ""),
            website_report=context.get("website_report", ""),
            linkedin_report=context.get("linkedin_report", ""),
            precision_intelligence_report=context.get("precision_intelligence_report", ""),
            dev_local_mode=context.get("dev_local_mode", False) # Pass dev mode flag
        )
        
        # Error handling is now within generate_email, just return the result
        return email_result
        # Removed the redundant try/except block and validation
    
    def post(self, shared, prep_res, exec_res):
        """Store the generated primary and follow-up email details in shared."""
        if not exec_res or not isinstance(exec_res, dict) or "primary_subject" not in exec_res or "primary_line1" not in exec_res:
            logging.warning(f"Email generation produced no result or invalid format: {exec_res}")
            shared['email_subject'] = "Error: Email generation failed"
            shared['email_body'] = "The system could not generate an email with the provided information."
            shared['followup_subject'] = ""
            shared['followup_body'] = ""
        else:
            # Store primary email parts
            shared['email_subject'] = exec_res.get("primary_subject", "")
            # Combine lines for the body (handle potential missing lines gracefully)
            body_lines = [
                exec_res.get("primary_line0", f"Hi {shared.get('lead_first_name', 'there')},"), # Add default line 0 if missing
                exec_res.get("primary_line1", ""),
                exec_res.get("primary_line2", ""),
                exec_res.get("primary_line3", "")
            ]
            shared['email_body'] = "\n\n".join(line for line in body_lines if line) # Join non-empty lines with double newline
            
            # Store follow-up email parts (optional, could be empty)
            shared['followup_subject'] = exec_res.get("followup_subject", "")
            followup_body_lines = [
                exec_res.get("followup_line1", ""),
                exec_res.get("followup_line2", ""),
                exec_res.get("followup_line3", "")
            ]
            shared['followup_body'] = "\n\n".join(line for line in followup_body_lines if line)
            
            logging.info(f"Generated email with subject: {shared['email_subject']}")
            if shared['followup_subject']:
                logging.info(f"Generated follow-up email with subject: {shared['followup_subject']}")
            
        return "default"  # Continue flow 