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
    auth = ("Your_GitHub_Username", "Your_GitHub_Password")

    def getIssues(self, url):

        self.issues_payload = {
        "per_page": 100,
        "page": 1,
        "state": "all",
        }

        self.raw = []

        r = requests.get(url, params=self.issues_payload, auth=self.auth).json()

        while (True):
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                r = requests.get(url, params=self.issues_payload, auth=self.auth).json()
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

            labels = []

            for label in e["labels"]:
                 labelIssue = collections.OrderedDict()
                 labelIssue["issue_repo_url"] = e["repository_url"]
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


    apps = open('github_issues_url.csv', encoding='utf-8',)
    csv_apps = csv.reader(apps)

    for row in csv_apps:
        try:
            app_source = row[0].replace("//github.com", "//api.github.com/repos")
        except:
            pass

        print("=============================")
        print(app_source)
        print("=============================")

        api = GithubAPI()

        print("Getting issues...")
        try:
            issues = api.getIssues(app_source)
        except:
            pass

        print ("Creating issues.csv ...")

        #  create csv file
    with open("issues.csv", 'a', encoding='utf-8' ,newline="") as file:
        writer = csv.writer(file)

        writer.writerow(("id", "number", "issue_url", "repo_url", "events_url", "state", "html_url",
        "milestone", "title", "comments", "created_at", "uploaded_at", "closed_at"))

        for issue in issues:
            writer.writerow((issue["id"], issue["number"], issue["issue_url"], issue["repo_url"], issue["events_url"], issue["state"],
            issue["html_url"], issue["milestone"], issue["title"],
            issue["comments"], issue["created_at"], issue["updated_at"], issue["closed_at"]))


        # =======================================================================================
        print ("Creating labels.csv...")

    with open("labels.csv", 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file)

        writer.writerow(("issue_repo_url", "issue_id","issue_number", "label_id", "label"))

        for issue in issues:
            labels = issue["labels"]
            for label in labels:
                writer.writerow(( label["issue_repo_url"], label["issue_id"], label["issue_number"], label["label_id"], label["label"] ))