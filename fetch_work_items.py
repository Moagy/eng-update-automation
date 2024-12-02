import requests
from requests.auth import HTTPBasicAuth
import os
import logging
from datetime import datetime
import json
import pyjokes
import random

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('azure_devops_report.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AzureDevOpsReport:
    def __init__(self, organization, project):
        self.organization = organization
        self.project = project
        self.pat = self.get_pat_from_file()
        self.base_url = f"https://dev.azure.com/{organization}/{project}"
        self.status_comments = {
            'Done': [
                "🎉 Another one bites the dust!",
                "✨ Crushed it!",
                "🚀 Mission accomplished!",
                "🌟 Nailed it!"
            ],
            'Live Testing': [
                "🔍 Let's hunt those bugs!",
                "🎯 Testing in progress...",
                "🧪 Lab work ongoing",
                "🔬 Under the microscope"
            ],
            'Ready for Release': [
                "🚦 Ready for takeoff!",
                "📦 Packed and ready to go",
                "🎁 Fresh out of the oven",
                "🔥 Hot and ready!"
            ],
            'In Development': [
                "⚡ Code wizards at work",
                "🛠️ Building something awesome",
                "💻 Cooking up some code",
                "🔨 Hammering out the details"
            ],
            'Ready': [
                "🎬 Action stations!",
                "⭐ Time to shine",
                "🎯 Target acquired",
                "🔋 Charged up and ready"
            ],
            'Refinement': [
                "🎨 Making it beautiful",
                "✨ Adding some sparkle",
                "🔧 Fine-tuning in progress",
                "💎 Polishing to perfection"
            ]
        }

    def get_random_emoji(self):
        emojis = ["🚀", "💻", "⚡", "🎯", "✨", "🔥", "💪", "🎨", "🎉", "🌟"]
        return random.choice(emojis)

    def get_random_greeting(self):
        greetings = [
            "Hey team! Here's what's cooking",
            "Greetings, fellow developers!",
            "Welcome to this week's update",
            "Another exciting week in the books",
            "Time for your weekly dose of progress"
        ]
        return random.choice(greetings)

    def get_random_status_comment(self, status):
        if status in self.status_comments:
            return random.choice(self.status_comments[status])
        return f"{self.get_random_emoji()} Status: {status}"

    def get_pat_from_file(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "pat.txt")
        try:
            with open(desktop_path, "r") as file:
                pat = file.read().strip()
                logging.info("PAT successfully retrieved")
                return pat
        except FileNotFoundError:
            logging.error("PAT file not found on desktop")
            raise
        except Exception as e:
            logging.error(f"Error reading PAT: {e}")
            raise

    def get_work_items(self):
        url = f"{self.base_url}/_apis/wit/wiql?api-version=7.0"
        query = {
            "query": (
                "SELECT [System.Id], [System.Title], [System.State], "
                "[System.AssignedTo], [System.Tags], [System.BoardColumn] "
                "FROM WorkItems "
                "WHERE [System.TeamProject] = @project "
                "AND [System.WorkItemType] <> '' "
                "AND ("
                "    ([System.BoardColumn] = 'Done' AND [System.ChangedDate] > @Today - 7) "
                "    OR [System.BoardColumn] IN ('Live Testing', 'Ready for Release', 'DoD', 'Dev Testing', 'In Development', 'Ready', 'Refinement')"
                ") "
                "ORDER BY [System.BoardColumn] ASC"
            )
        }

        try:
            response = requests.post(url, json=query, auth=HTTPBasicAuth('', self.pat))
            response.raise_for_status()
            work_items = response.json().get('workItems', [])
            logging.info(f"Successfully retrieved {len(work_items)} work items")
            return work_items
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching work items: {e}")
            raise

    def get_work_item_details(self, work_item_id):
        url = f"{self.base_url}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
        try:
            response = requests.get(url, auth=HTTPBasicAuth('', self.pat))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching details for work item {work_item_id}: {e}")
            raise

    def generate_weekly_report(self):
        try:
            work_items = self.get_work_items()
            report_data = {
                'Done': [],
                'Live Testing': [],
                'Ready for Release': [],
                'DoD': [],
                'Dev Testing': [],
                'In Development': [],
                'Ready': [],
                'Refinement': []
            }

            for item in work_items:
                details = self.get_work_item_details(item['id'])
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

            self.save_report(report_data)
            logging.info("Weekly report generated successfully")
            
        except Exception as e:
            logging.error(f"Error generating weekly report: {e}")
            raise

    def save_report(self, report_data):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON for data processing
        json_path = os.path.join(desktop_path, f"weekly_report_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

        # Save as formatted text file for reading
        txt_path = os.path.join(desktop_path, f"weekly_report_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("🌟 AZURE DEVOPS WEEKLY STATUS REPORT 🌟\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Add a random greeting
            f.write(f"{self.get_random_greeting()}\n\n")

            # Add a random programming joke
            f.write("😄 Developer's Corner 😄\n")
            f.write(f"Today's Programming Joke: {pyjokes.get_joke()}\n")
            f.write("-" * 40 + "\n\n")

            for status, items in report_data.items():
                if items:  # Only show sections with items
                    status_comment = self.get_random_status_comment(status)
                    f.write(f"\n{status.upper()} - {status_comment}\n")
                    f.write("-" * len(status) + "\n")
                    for item in items:
                        f.write(f"\n{self.get_random_emoji()} ID: {item['ID']}\n")
                        f.write(f"Title: {item['Title']}\n")
                        f.write(f"Assigned To: {item['Assigned To']}\n")
                        f.write(f"State: {item['State']}\n")
                        if item['Tags']:
                            f.write(f"Tags: {item['Tags']}\n")
                        f.write("\n" + "-" * 40 + "\n")

            # Add a random closing message
            closing_messages = [
                "Keep crushing it! 💪",
                "Another great week in the books! 🎉",
                "Until next time, happy coding! 💻",
                "Stay awesome, team! ⭐",
                "Let's keep the momentum going! 🚀"
            ]
            f.write(f"\n{random.choice(closing_messages)}\n")

        logging.info(f"Report saved as JSON: {json_path}")
        logging.info(f"Report saved as TXT: {txt_path}")

def main():
    try:
        reporter = AzureDevOpsReport("dorset-ics", "DiiS%20Development%20Team")
        reporter.generate_weekly_report()
        print("Weekly report generated successfully!")
    except Exception as e:
        logging.error(f"Application failed: {e}")
        print("An error occurred. Check azure_devops_report.log for details.")

if __name__ == "__main__":
    main()