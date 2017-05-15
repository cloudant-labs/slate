from json import load
import csv

linkArray = []
outputLine = ""
wherePresent = ""

def outputDatabase(dbName, default):
    global outputLine
    global wherePresent
    global linkArray
    posn = default
    for docLink in linkArray:
        if (default in docLink):
            posn = docLink
    if (dbName in wherePresent):
        shortName = dbName.replace(' ', '')
        if (shortName == "CouchDB2.0"):
            shortName = "CouchDB2"
        if (shortName == "CouchDB1.6"):
            shortName = "CouchDB1"
        outputLine += "[![small" + shortName + "](../images/small" + shortName + ".png)](" + posn + "){:new_window} | "
    else:
        outputLine += " | "

with open('cloudant-couchdb-api-ref.json') as json_data_file:
    data = load(json_data_file)

print("Endpoint | Method | Cloudant | CouchDB 2.0 | CouchDB 1.6 | Summary | Notes")
print("---------|--------|----------|-------------|-------------|---------|------")

for row in data:
    linkArray = row["links"]
    linkArray.append("")
    linkArray.append("")
    linkArray.append("")
    outputLine = row["endpoint"] + " | "
    outputLine += row["method"] + " | "
    wherePresent = row['database']
    outputDatabase("Cloudant", "https://docs.cloudant.com/")
    outputDatabase("CouchDB 2.0", "http://docs.couchdb.org/en/2.0.0/")
    outputDatabase("CouchDB 1.6", "http://docs.couchdb.org/en/1.6.0/")
    outputLine += row['summary'] + " | "
    if (row['comment'] != ""):
        outputLine += row['comment']
    outputLine = outputLine.replace(u"\u2019", "\'").replace("_", "\\_").replace("\n", " ")
    outputLine = outputLine.replace("new\_window", "new_window")
    outputLine = outputLine.replace("https://docs.cloudant.com/advanced.html", "advanced.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/active\_tasks.html", "active_tasks.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/attachments.html", "attachments.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/authentication.html", "authentication.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/authorization.html", "authorization.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/cloudant\_query.html", "cloudant_query.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/cors.html", "cors.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/creating\_views.html", "creating_views.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/database.html", "database.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/design\_documents.html", "design_documents.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/document.html", "document.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/geo.html", "cloudant-geo.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/monitoring.html", "monitoring.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/replication.html", "replication.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/search.html", "search.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/vhosts.html", "vhosts.html")
    outputLine = outputLine.replace("https://docs.cloudant.com/", "../cloudant.html")
    print outputLine
