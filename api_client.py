import requests
from requests.auth import HTTPBasicAuth
import logging
from config import BASE_URL

class AzureDevOpsClient:
    def __init__(self, pat):
        self.pat = pat
        self.auth = HTTPBasicAuth('', pat)

    def get_work_items(self):
        url = f"{BASE_URL}/_apis/wit/wiql?api-version=7.0"
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
            response = requests.post(url, json=query, auth=self.auth)
            response.raise_for_status()
            work_items = response.json().get('workItems', [])
            logging.info(f"Successfully retrieved {len(work_items)} work items")
            return work_items
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching work items: {e}")
            raise

    def get_work_item_details(self, work_item_id):
        url = f"{BASE_URL}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching details for work item {work_item_id}: {e}")
            raise