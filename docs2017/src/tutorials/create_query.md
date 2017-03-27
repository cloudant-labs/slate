---

copyright:
  years: 2015, 2017
lastupdated: "2017-01-06"

---
{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Creating a Cloudant Query

This tutorial demonstrates how to create an index and extract specific data from the database using a query.

[Description of query elements.]

Create a database
Database contains JSON documents and design documents.
    JSON documents - description
    Design documents - description 
Describe Views and their elements
Describe Indexes and their elements
    Each database automatically includes a design document. Indexes are created in the design document. To create an index of type JSON, make a POST request to the database. 
Describe queries and their elements

## Creating a database using the Cloudant Dashboard

This tutorial is based on the simple `rolodex` database. Each index and query that you create will use this database. 

1.  Create a Cloudant account here, https://cloudant.com/sign-in/. 
2.  Log in to the Cloudant Dashboard. 
3.  Verify that the Databases tab is selected in the left navigation. 
4.  Click **Create Database**. 
5.  Enter `rolodex` as the name for the database and click **Create**. 
    The `rolodex` database is automatically opened. 
6.  Click **Add New** (+) next to All Documents and select **New Doc**.
    The New Document window opens. 
7.  Create a new document by adding the following text after the "_id" line and inside the brackets.   


**Example document 1
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "Sally",
  "lastname": "Brown",
  "sex": "female",
  "address": "122 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-9354"
}    
```


8. Create nine more documents using the following text by inserting the text after the "_id" line and inside the brackets. 


**Example document 2
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "John",
  "lastname": "Smith",
  "sex": "male",
  "address": "123 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4614"
}
```

**Example document 3
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "Greg",
  "lastname": "Mason",
  "sex": "male",
  "address": "124 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4445"
}
```

**Example document 4
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "Dan",
  "lastname": "Brown",
  "sex": "male",
  "address": "125 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4275"
}
```

**Example document 5
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "firstname": "Janine",
    "lastname": "Lee",
    "sex": "female",
    "address": "126 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "726-9938"
}
```

**Example document 6
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "Sam",
  "lastname": "Harris",
  "sex": "male",
  "address": "125 Second Street",
  "city": "San Mateo",
  "state": "CA",
  "zipcode": 94401,
  "areacode": 650,
  "phonenumber": "225-4444"
}
```

Example document 7
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "firstname": "Amanda",
  "lastname": "Greene",
  "sex": "female",
  "address": "124 Second Street",
  "city": "San Mateo",
  "state": "CA",
  "zipcode": 94401,
  "areacode": 650,
  "phonenumber": "613-8462"
}
```

Example document 8
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "firstname": "Tammy",
    "lastname": "Smith",
    "sex": "female",
    "address": "122 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "333-7310"
}
```

Example document 9
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "firstname": "Patricia"”",
    "lastname": "Jones",
    "sex": "female"
    "address": "125 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "336-4003"  
}
```

Example document 10
```json
{
  "_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "firstname": "Nick",
    "lastname": "Brown",
    "sex": "male",
    "address": "126 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "334-4841"
}
```

The `rolodex` database now contains ten JSON documents. 

## Creating an index 
With Cloudant Query, you can use the Primary Index out-of-the-box. You can also build indexes using MapReduce 
Views (type=json) and Search Indexes (type=text). Index specifics are stored in design documents. 
When you change the design document, the index is overwritten and recreated from scratch.

When you create an index, you must select the columns 
from the database table that you want to search. For example, the `rolodex` database contains the following 
columns:

*   Firstname
*   Lastname
*   Sex
*   Address
*   City
*   State
*   Zipcode
*   Areacode
*   Phone number

When you create an index, it is important to select the columns that will improve your searches. The following
examples show how to create an index to reduce your data set and the load on your environment. 



###Creating a "type=json" index
If you know the type of data you want to search for or if you want to minimize storage and 
processing requirements, you can use a "type=json" index and specify how to create 
the index. 
  
1.  Create a JSON index in the `rolodex` database.
2.  Make a `POST` request to the `_index` endpoint. 
3.  In the request body for the JSON object, specify the `state` and `area code` fields.   
4.  Set the `type` field equal to `json`. 


```json
POST /rolodex/_index HTTP/1.1
Content-Type: application/json
    {
        "index": {
            "fields": [
                {
                   "state", "area code"
                    }
                ]                    
        },
        "name" : "rolodex-json",
        "type" : "json"
}
```

Return JSON confirms the index was created successfully.

```
    {
        "result" : "created"
    }
NOT A TRUE RESPONSE    
    {"total_rows":2,"indexes":[{"ddoc":null,"name":"_all_docs",
    "type":"special","def":{"fields":[{"_id":"asc"}]}},{"ddoc":
    "_design/a7ee061f1a2c0c6882258b2f1e148b714e79ccea","name":
    "a7ee061f1a2c0c6882258b2f1e148b714e79ccea","type":"json",
    "def":{"fields":[{"foo":"asc"}]}}]}
```

[Describe index and fields fields.] The `index` field contains the settings that are specific to [NO IDEA-page 4 on queries.]

###Creating a design document
[DESCRIPTION OF Design Doc here]

1.  From the Dashboard, open the `rolodex` database.
2.  On the Design Doc tab, click the create icon, +, and select New Doc. 
3.  Replace the `_id` with `rolodex-index-design-doc` and click **Save Changes**.

The index information will be stored in this design document.  

####Creating a "type=text" index
If you want the flexibility to search all your data, you can create a "type=text" index. 
This index type automatically indexes all the fields of the documents in your database providing
the ability to query and retrieve information from all the data in your database. This 
flexibility requires more storage resources and can take longer to create than a JSON index. 

1.  Create a text index in the `rolodex` database.
2.  Make a `POST` request to the `_index` endpoint.  
3.  In the request body for the JSON object, specify the `sex`, `lastname`, and `areacode` fields.   
4.  Set the `type` field equal to `text`. 
 
```json
POST /rolodex/_index HTTP/1.1
Content-Type: application/json
{
    "type": "text" 
    "name": "rolodex-text",
    "ddoc": "rolodex-index-design-doc",            
    "index": {
       "default_field": {
            "enabled": true,
            "analyzer": "standard"
            },            
        "selector": {},
                "fields": [
                    {"name": "sex", "type": "string"},
                    {"name": "lastname", "type": "string"},
                    {"name": "areacode", "type": "number"}
               ]
        }   
}
```
[Describe why the type, name, ddoc, and index are in their current order. 
Describe how to create a design doc that includes this index info. Describe default_field and selector.]


### Listing Cloudant Query indexes 

You can list all the indexes in a database by using the GET endpoint. 

```
    GET /rolodex/_index
```

Return JSON lists the index in the database in the following manner.

```
[VERIFY content]
{"total_rows":2,"indexes":[{"ddoc":null,"name":"_all_docs","type":"special","def":{"fields":[{"_id":"asc"}]}},{"ddoc":"_design/a7ee061f1a2c0c6882258b2f1e148b714e79ccea","name":"a7ee061f1a2c0c6882258b2f1e148b714e79ccea","type":"json","def":{"fields":[{"foo":"asc"}]}}]}
```


### Deleting an index

Indexes are saved to the design document. Therefore, the index must be deleted from the design document. You delete the index from the design document using the DELETE endpoint.

To delete the index we created, use the following DELETE request.

```
    DELETE /rolodex/_index/$DDOC/JSON/$INDEX_NAME
```    

Return JSON [shows the index was deleted].

```
     [INSERT RETURN JSON]
``` 


## Creating a query 






### Querying the rolodex database using selector syntax
To build a query that searches for a document in the database when you have a 
few specifics, you can include the fields in the query to retrieve it. For example, 
in the `rolodex` database, if you know the state and last name included in one 
of the documents, search for the state and last name in the query as is written
in the example below. You can also include the fields you want returned in the 
response and which of the return fields to sort by. 

1.  Make a POST request and include the fields to search in the `selector` 
    syntax as shown in the example below.
2.  In the `fields` field, type in the name of the fields you want to see when
    the response is returned.
3.  Enter the value you want to sort by, limit the number of documents to 
    search, and the number of documents to skip [true?] before the search 
    aborts. 

```
POST /rolodex/_find
{
    "selector": {
        "state": "CA"
        "last name": "Greene"
        }
         "fields": ["first name", "last name", "address", "area code", "phone number"],
         "sort": ["last name"],
         "limit": 10
         "skip": 0
    }        
```

### Querying the rolodex database using operators
[Search for people who live in California and have a 650 area code.]

    

