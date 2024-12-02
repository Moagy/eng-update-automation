from config import get_pat_from_file
from api_client import AzureDevOpsClient
from report_generator import ReportGenerator
import logging

def main():
    try:
        pat = get_pat_from_file()
        api_client = AzureDevOpsClient(pat)
        reporter = ReportGenerator(api_client)
        reporter.generate_report()
        print("Weekly report generated successfully!")
    except Exception as e:
        logging.error(f"Application failed: {e}")
        print("An error occurred. Check azure_devops_report.log for details.")

if __name__ == "__main__":
    main()