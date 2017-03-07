# -*- coding: utf-8 -*-

import sys
import requests
import collections
from openpyxl import Workbook
import csv

class GithubAPI:
    results = []
    raw = []
    issues_payload = {
        "per_page": 100,
        "page": 1,
        "state": "all",
    }
    auth = ("theeibwen", "09196db17fc3dda1cfddb5a60f1516e5309d623b")

    def __init__(self, user, repo):
        self.repos_api_url = "https://api.github.com/repos/" + user + "/" + repo
        self.issues_api_url = self.repos_api_url + "/issues"

    def getIssues(self):
        r = requests.get(self.issues_api_url, params=self.issues_payload, auth=self.auth).json()

        while (True):
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                r = requests.get(self.issues_api_url, params=self.issues_payload, auth=self.auth).json()
            else:
                break

        for e in self.raw:
            print("Checking issue " + str(e["number"]))

            issue = collections.OrderedDict()
            issue["id"] = e["id"]
            issue["number"] = e["number"]
            issue["repo_url"] = e["repository_url"]
            issue["issue_url"] = e["url"]
            issue["events_url"] = e["events_url"]
            issue["state"] = e["state"]
            issue["html_url"] = e["html_url"]
            issue["title"] = e["title"]
            # issue["description"] = e["body"]
            issue["comments"] = e["comments"]
            issue["created_at"] = e["created_at"]
            issue["updated_at"] = e["updated_at"]
            issue["closed_at"] = e["closed_at"]
            if not e["milestone"]:
                 issue["milestone"] = "null"
            else:
                 issue["milestone"] = e["milestone"]["title"]


                
            # if e["milestone"] == 0:
            #     print("===================")

            labels = []

            for label in e["labels"]:
                 labelIssue = collections.OrderedDict()
                 labelIssue["issue_id"] = e["id"]
                 labelIssue["issue_number"] = e["number"]
                 labelIssue["label_id"] = label["id"]
                 labelIssue["label"] = label["name"]
                 labels.append(labelIssue)
                 # self.results.append(labelIssue)

            issue["labels"] = labels

            self.results.append(issue)

        return self.results


if __name__ == "__main__":
    api = GithubAPI(sys.argv[1], sys.argv[2])

    print("Getting issues...")
    issues = api.getIssues()

    print ("Creating issues.csv ...")

    # for i in issues:
    #     print(issues)
    #     print(type(i))
    #     print(i.keys())
    #     print("=================================")

    # wb = Workbook()

    # ws = wb.active

    # headers = ["id", "number", "issue_url", "repo_url", "events_url", "state", "html_url", 
    # "milestone", "title", "description", "comments", "created_at", "uploaded_at", "closed_at"]
    # ws.append(headers)

    # for issue in issues:
    #     ws.append([issue["id"], issue["number"], issue["issue_url"], issue["repo_url"], issue["events_url"], issue["state"],
    #     issue["html_url"], issue["milestone"], issue["title"], issue["description"], 
    #     issue["comments"], issue["created_at"], issue["updated_at"], issue["closed_at"]])

    # wb.save("issues.xlsx")

    #  create csv file
with open("issues.csv", 'w', encoding='utf-8' ,newline="") as file:
    writer = csv.writer(file)

    writer.writerow(("id", "number", "issue_url", "repo_url", "events_url", "state", "html_url", 
    "milestone", "title", "comments", "created_at", "uploaded_at", "closed_at"))

    for issue in issues:
        writer.writerow((issue["id"], issue["number"], issue["issue_url"], issue["repo_url"], issue["events_url"], issue["state"],
        issue["html_url"], issue["milestone"], issue["title"], 
        issue["comments"], issue["created_at"], issue["updated_at"], issue["closed_at"]))

# =======================================================================================
    print ("Creating labels.csv...")

with open("labels.csv", 'w', newline="") as file:
    writer = csv.writer(file)

    writer.writerow(("issue_id","issue_number", "label_id", "label"))

    for issue in issues:
        labels = issue["labels"]
        for label in labels:
            writer.writerow(( label["issue_id"], label["issue_number"], label["label_id"], label["label"] ))

    # wb = Workbook()

    # ws = wb.active

    # headers = ["issue_id","issue_number", "label_id", "label"]
    # ws.append(headers)

    # for issue in issues:
    #     labels = issue["labels"]

    #     for label in labels:
    #         ws.append([ label["issue_id"], label["issue_number"], label["label_id"], label["label"]])

    # wb.save("labels.xlsx")
