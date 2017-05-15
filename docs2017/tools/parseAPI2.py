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
            posn = cleanText(docLink)
    if (dbName in wherePresent):
        shortName = dbName.replace(' ', '')
        if (shortName == "CouchDB2.0"):
            shortName = "CouchDB2"
        if (shortName == "CouchDB1.6"):
            shortName = "CouchDB1"
        print "<a href='" + posn + "' target='_blank'><img src='../images/verySmall" + shortName + ".png' alt='" + dbName + "'/></a>"

def cleanText(content):
    tmp = content
    tmp = tmp.replace(u"\u2019", "\'").replace("_", "\\_").replace("\n", " ")
    tmp = tmp.replace("new\_window", "new_window")
    tmp = tmp.replace("https://docs.cloudant.com/advanced.html", "advanced.html")
    tmp = tmp.replace("https://docs.cloudant.com/active\_tasks.html", "active_tasks.html")
    tmp = tmp.replace("https://docs.cloudant.com/attachments.html", "attachments.html")
    tmp = tmp.replace("https://docs.cloudant.com/authentication.html", "authentication.html")
    tmp = tmp.replace("https://docs.cloudant.com/authorization.html", "authorization.html")
    tmp = tmp.replace("https://docs.cloudant.com/cloudant\_query.html", "cloudant_query.html")
    tmp = tmp.replace("https://docs.cloudant.com/cors.html", "cors.html")
    tmp = tmp.replace("https://docs.cloudant.com/creating\_views.html", "creating_views.html")
    tmp = tmp.replace("https://docs.cloudant.com/database.html", "database.html")
    tmp = tmp.replace("https://docs.cloudant.com/design\_documents.html", "design_documents.html")
    tmp = tmp.replace("https://docs.cloudant.com/document.html", "document.html")
    tmp = tmp.replace("https://docs.cloudant.com/geo.html", "cloudant-geo.html")
    tmp = tmp.replace("https://docs.cloudant.com/monitoring.html", "monitoring.html")
    tmp = tmp.replace("https://docs.cloudant.com/replication.html", "replication.html")
    tmp = tmp.replace("https://docs.cloudant.com/search.html", "search.html")
    tmp = tmp.replace("https://docs.cloudant.com/vhosts.html", "vhosts.html")
    tmp = tmp.replace("https://docs.cloudant.com/", "../cloudant.html")
    return tmp

with open('cloudant-couchdb-api-ref.json') as json_data_file:
    data = load(json_data_file)

print "<table border='1'>\n"

for row in data:
    linkArray = row["links"]
    linkArray.append("")
    linkArray.append("")
    linkArray.append("")
    wherePresent = row["database"]

    print "<tr>\n<td><code>" + cleanText(row["method"]) + "&nbsp;" + cleanText(row["endpoint"]) + "</code><p>"
    outputDatabase("Cloudant", "https://docs.cloudant.com/")
    outputDatabase("CouchDB 2.0", "http://docs.couchdb.org/en/2.0.0/")
    outputDatabase("CouchDB 1.6", "http://docs.couchdb.org/en/1.6.0/")
    outputLine = "</p></td><td>" + cleanText(row['summary'])
    if (row['comment'] != ""):
        outputLine += "<p>" + cleanText(row['comment']) +"</p>"
    print outputLine + "</td>\n</tr>"

print "</table>\n"
