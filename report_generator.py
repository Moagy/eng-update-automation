import os
from datetime import datetime
import json
import logging
import pyjokes
from message_templates import (
    get_random_emoji, get_random_greeting,
    get_random_status_comment, get_random_closing_message
)

class ReportGenerator:
    def __init__(self, api_client):
        self.api_client = api_client

    def generate_report(self):
        try:
            work_items = self.api_client.get_work_items()
            report_data = self._process_work_items(work_items)
            self._save_report(report_data)
            logging.info("Weekly report generated successfully")
        except Exception as e:
            logging.error(f"Error generating weekly report: {e}")
            raise

    def _process_work_items(self, work_items):
        report_data = {
            'Done': [], 'Live Testing': [], 'Ready for Release': [],
            'DoD': [], 'Dev Testing': [], 'In Development': [],
            'Ready': [], 'Refinement': []
        }

        for item in work_items:
            details = self.api_client.get_work_item_details(item['id'])
            fields = details.get('fields', {})
            
            status = fields.get('System.BoardColumn', 'Unknown')
            item_data = {
                'ID': item['id'],
                'Title': fields.get('System.Title', 'No Title'),
                'Assigned To': fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned'),
                'State': fields.get('System.State', 'Unknown'),
                'Tags': fields.get('System.Tags', ''),
                'Description': fields.get('System.Description', 'No description available')
            }
        
            if status in report_data:
                report_data[status].append(item_data)

        return report_data
    
    def _save_report(self, report_data):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON report
        json_path = os.path.join(desktop_path, f"weekly_report_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

        # Save formatted text report
        txt_path = os.path.join(desktop_path, f"weekly_report_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("🌟 AZURE DEVOPS WEEKLY STATUS REPORT 🌟\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"{get_random_greeting()}\n\n")
            f.write("😄 Developer's Corner 😄\n")
            f.write(f"Today's Programming Joke: {pyjokes.get_joke()}\n")
            f.write("-" * 40 + "\n\n")

            for status, items in report_data.items():
                if items:
                    status_comment = get_random_status_comment(status)
                    f.write(f"\n{status.upper()} - {status_comment}\n")
                    f.write("-" * len(status) + "\n")
                    for item in items:
                        f.write(f"\n{get_random_emoji()} ID: {item['ID']}\n")
                        f.write(f"Title: {item['Title']}\n")
                        f.write(f"Assigned To: {item['Assigned To']}\n")
                        f.write(f"State: {item['State']}\n")
                        if item['Tags']:
                            f.write(f"Tags: {item['Tags']}\n")
                        f.write("\n" + "-" * 40 + "\n")

            f.write(f"\n{get_random_closing_message()}\n")

        logging.info(f"Report saved as JSON: {json_path}")
        logging.info(f"Report saved as TXT: {txt_path}")