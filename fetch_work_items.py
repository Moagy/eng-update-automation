import requests
from requests.auth import HTTPBasicAuth
import os

# Define your organization, project, and PAT
organization = "dorset-ics"
project = "DiiS%20Development%20Team"
pat = ''

# WIQL query URL (fetching work items)
url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.0"

# Define the WIQL query to fetch all work items (you can modify the query)
query = {
    "query": (
        "SELECT  [System.Id], "
        "FROM WorkItems "
        "WHERE [System.TeamProject] = @project "
        "AND [System.WorkItemType] <> '' "
        "AND (([System.BoardColumn] = 'Done' AND [System.ChangedDate] < DATEADD(DD, GETDATE() - 7)) "
            "OR () "
        "AND [System.Id] = 20750 "
        "ORDER BY [System.ChangedDate] DESC "
        "ASOF '01-01-2024"
    )
}

# Make the API request
response = requests.post(url, json=query, auth=HTTPBasicAuth('', pat))

# Check if the request was successful
if response.status_code == 200:
    # Extract and format work items data
    work_items = response.json().get('workItems', [])
    
    # Specify path to save .txt file to desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "work_items.txt")

    # Write data to the .txt file
    with open(desktop_path, "w") as file:
        for item in work_items:
            file.write(f"ID: {item['id']}\n")
            file.write(f"Title: {item.get('fields', {}).get('System.Title')}\n")
            file.write(f"Assigned To: {item.get('fields', {}).get('System.AssignedTo')}\n")
            file.write(f"State: {item.get('fields', {}).get('System.State')}\n")
            file.write(f"Tags: {item.get('fields', {}).get('System.Tags')}\n")
            file.write("-" * 40 + "\n")
    
    print(f"Work items successfully saved to {desktop_path}")
else:
    print(f"Error: {response.status_code}, {response.text}")
