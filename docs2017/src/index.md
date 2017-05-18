---

copyright:
  years: 2015, 2017
lastupdated: "2017-05-18"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}
{:tip: .tip}

# Getting started tutorial
{: #getting-started-with-cloudant}

In this {{site.data.keyword.cloudantfull}} getting started tutorial
we'll use Python to create a {{site.data.keyword.cloudant}} database
and populate that database with a simple collection of data.
{:shortdesc}

## Prerequisites
{: #prereqs}

You'll need a [Bluemix account](https://console.ng.bluemix.net/registration/),
an instance of the {{site.data.keyword.cloudant}} service, and the following Python requirements:

*	Install the latest version of the
	[Python programming language ![External link icon](../images/launch-glyph.svg "External link icon")](https://www.python.org/){:new_window} on your system.
	
	To check this, run the following command at a prompt:
	```sh
	python --version
	```
	{:pre}

*	Install the [Python library](../libraries/supported.html#python)
	to enable your Python applications to work with
	{{site.data.keyword.cloudant_short_notm}} on {{site.data.keyword.Bluemix_notm}}.
	
	To check that you have the client library installed successfully,
	run the following command at a prompt:
	```sh
	pip freeze
	```
	{:pre}

## 1. Connect to your {{site.data.keyword.cloudant_short_notm}} service instance on {{site.data.keyword.Bluemix_notm}}

1.	Run the following '`import`' statements of the {{site.data.keyword.cloudant_short_notm}}
	Client Library components to enable your Python application to connect to
	the {{site.data.keyword.cloudant_short_notm}} service instance.
	```python
	from cloudant.client import Cloudant
	from cloudant.error import CloudantException
	from cloudant.result import Result, ResultByKey
	```
	{:pre}

2. Identify the {{site.data.keyword.cloudant_short_notm}} service credentials:
  1. In the {{site.data.keyword.Bluemix_notm}} console, open the dashboard for your service instance.
  2. In the left navigation, click **`Service credentials`**.
  3. Click **`View credentials`** under **`ACTIONS`**.

3.	Establish a connection to the service instance by running the following command.
	Replace your service credentials from step 2:
	```python
	client = Cloudant(username, password, url=url)
	client.connect()
	```
	{:pre}

If you run into '`can't read`' errors,
prefix `#!/usr/bin/env python` to each command to instruct your shell to execute through python.
{: tip}

## 2. Create a database

1. Define a variable in the Python application:
  ```python
  databaseName = "your_database_name"
  ```
  {:pre}

  Your database name must begin with a letter and can include only lowercase characters (a-z), 
  numerals (0-9),
  and any of the following characters `_`, `$`, `(`, `)`, `+`, `-`, and `/`.
  {: tip}

2. Create the database:
  ```python
  myDatabase = client.create_database(your_database_name)
  ```
  {:pre}

3. Confirm the database was created successfully:
  ```python
  if your_database_name.exists():
      print "'{0}' successfully created.\n".format(databaseName)
  ```
  {:pre}

## 3. Store a small collection of data as documents within the database

1. Define a collection of data:
  ```python
  sampleData = [
      [1, "one", "boiling", 100],
      [2, "two", "hot", 40],
      [3, "three", "warm", 20],
      [4, "four", "cold", 10],
      [5, "five", "freezing", 0]
    ]
  ```
  {:pre}

2. Use Python code to 'step' through the data and convert it into JSON documents.
  Each document is stored in the database:

  ```python
  # Create documents using the sample data.
  # Go through each row in the array
  for document in sampleData:
    # Retrieve the fields in each row.
    number = document[0]
    name = document[1]
    description = document[2]
    temperature = document[3]

    # Create a JSON document that represents
    # all the data in the row.
    jsonDocument = {
        "numberField": number,
        "nameField": name,
        "descriptionField": description,
        "temperatureField": temperature
    }

    # Create a document using the Database API.
    newDocument = myDatabaseDemo.create_document(jsonDocument)

    # Check that the document exists in the database.
    if newDocument.exists():
        print "Document '{0}' successfully created.".format(number)
  ```
  {:pre}

Notice that we check that each document was successfully created.
{: tip}

## 4. Retrieving data through queries

At this point,
a small collection of data has been stored as documents within the database.
You can do a minimal or full retrieval of that data from the database.

* To perform a minimal retrieval:
  1. First, request a list of all documents within the database.
    ```python
    result_collection = Result(YourDatabaseName.all_docs)
    ```      
    {:pre}

    This list is returned as an array.

  2. Display the content of an element in the array.
    ```python
    print "Retrieved minimal document:\n{0}\n".format(result_collection[0])
    ```
    {:pre}

    The result is similar to the following example:
    ```json
    [
        {
            "value": {
                "rev": "1-b2c48b89f48f1dc172d4db3f17ff6b9a"
            },
            "id": "14746fe384c7e2f06f7295403df89187",
            "key": "14746fe384c7e2f06f7295403df89187"
        }
    ]
    ```
    {:screen}

  The nature of NoSQL databases,
  such as {{site.data.keyword.cloudant_short_notm}},
  means that simple notions such as the first document stored in a database is always
  the first one returned in a list of results,
  do not necessarily apply.
  {: tip}

* To perform a full retrieval,
  request a list of all documents within the database,
  and specify that the document content must also be returned
  by providing the `include_docs` option.
  ```python
  result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
  print "Retrieved minimal document:\n{0}\n".format(result_collection[0])
  ```
  {:pre}

  The result is similar to the following example:
  ```json
  [
      {
          "value": {
          "rev": "1-b2c48b89f48f1dc172d4db3f17ff6b9a"
          },
          "id": "14746fe384c7e2f06f7295403df89187",
          "key": "14746fe384c7e2f06f7295403df89187",
          "doc": {
            "temperatureField": 10,
            "descriptionField": "cold",
            "numberField": 4,
            "nameField": "four",
            "_id": "14746fe384c7e2f06f7295403df89187",
            "_rev": "1-b2c48b89f48f1dc172d4db3f17ff6b9a"
          }
      }
  ]
  ```
  {:screen}

## 5. Retrieving data through the {{site.data.keyword.cloudant_short_notm}} API endpoint

You can also request a list of all documents and their contents by
invoking the Cloudant [`/_all_docs` endpoint](../api/database.html#get-documents).

1. Identify the endpoint to contact, and any parameters to supply along with the call:
  ```python
  end_point = '{0}/{1}'.format(serviceURL, databaseName + "/_all_docs")
  params = {'include_docs': 'true'}
  ```
  {:pre}

2. Send the request to the service instance,
  then display the results:
  ```python
  response = client.r_session.get(end_point, params=params)
  print "{0}\n".format(response.json())
  ```
  {:pre}

The result is similar to the following _abbreviated_ example:

```json
{
    "rows": [
        {
            "value": {
              "rev": "1-b2c48b89f48f1dc172d4db3f17ff6b9a"
            },
            "id": "14746fe384c7e2f06f7295403df89187",
            "key": "14746fe384c7e2f06f7295403df89187",
            "doc": {
                "temperatureField": 10,
                "descriptionField": "cold",
                "numberField": 4,
                "nameField": "four",
                "_id": "14746fe384c7e2f06f7295403df89187",
                "_rev": "1-b2c48b89f48f1dc172d4db3f17ff6b9a"
            }
        },
        ...
        {
            "value":
            {
              "rev": "1-7130413a8c7c5f1de5528fe4d373045c"
            },
            "id": "49baa66cc66b4dda86ffb2852ae78eb8",
            "key": "49baa66cc66b4dda86ffb2852ae78eb8",
            "doc": {
                "temperatureField": 40,
                "descriptionField": "hot",
                "numberField": 2,
                "nameField": "two",
                "_id": "49baa66cc66b4dda86ffb2852ae78eb8",
                "_rev": "1-7130413a8c7c5f1de5528fe4d373045c"
            }
        }
    ],
    "total_rows": 5,
    "offset": 0
}
```
{:screen}

## 6. Delete the database

When you are finished with the database,
it can be deleted.

```python
try :
    client.delete_database(databaseName)
except CloudantException:
    print "There was a problem deleting '{0}'.\n".format(databaseName)
else:
    print "'{0}' successfully deleted.\n".format(databaseName)
```
{:pre}

We have included some basic error handling
to illustrate how problems might be caught and addressed.

## 7. Close the connection to the service instance

The final step is to disconnect the Python client application from the service instance:

```python
client.disconnect()
```
{:pre}

## Next steps

For more information on all the {{site.data.keyword.cloudant_short_notm}} offerings,
see the main [{{site.data.keyword.cloudant_short_notm}} ![External link icon](images/launch-glyph.svg "External link icon")](http://www.ibm.com/analytics/us/en/technology/cloud-data-services/cloudant/){:new_window} site.
For more details and tutorials on {{site.data.keyword.cloudant_short_notm}} concepts,
tasks and techniques,
see the [{{site.data.keyword.cloudant_short_notm}} documentation](cloudant.html).