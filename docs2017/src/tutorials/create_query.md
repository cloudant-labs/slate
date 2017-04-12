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

This tutorial demonstrates how to create a design document, index and use Cloudant Query to extract specific data 
from the database.



## Creating a database using the Cloudant Dashboard

This tutorial is based on the `rolodex` [database](database.html#create) that you create using these steps. 

1.  Create a Cloudant account [here](https://cloudant.com/sign-in/) if you do not already have one.
2.  Log in to the Cloudant Dashboard. 
3.  Verify that the Databases tab is selected in the left navigation. 
4.  Click **Create Database**. 
5.  Enter `rolodex` as the name for the database and click **Create**. 
    The `rolodex` database automatically opens. 
6.  Click the Create icon, **+**, next to All Documents and select **New Doc**.
    The new document opens. 
7.  Add the text for Document 1 below after the `_id` line and inside the brackets. 
8.  Repeat steps 6 and 7 for documents 2 - 10.   



Document 1

```json
  "firstname": "Sally",
  "lastname": "Brown",
  "age": "16"
```


Document 2

```json
  "firstname": "John",
  "lastname": "Brown",
  "age": "21"
```

Document 3

```json
  "firstname": "Greg",
  "lastname": "Greene",
  "age": "35"
```

Document 4

```json
  "firstname": "Amanda",
  "lastname": "Greene",
  "age": "44"
```

The `rolodex` database now contains ten JSON documents. 


##Creating a design document

You configure a Search Index or a [MapReduce view](creating_views.html#views-mapreduce-) by adding 
[design documents](design_documents.html#design-documents) 
to the database. Design documents contain instructions about how the view 
or index must be built. When you change the design documents, the index is overwritten and recreated from scratch.

1.  From the Dashboard, open the `rolodex` database.
2.  On the Design Documents tab, click **+** and select **New Doc**. 
3.  Replace the `_id` with `rolodex-index-design-doc` and click **Create Document**. 
    The design document is added to the list of documents in the database. 

The index information for this tutorial will be stored in the `rolodex-index-design-doc` design document. 


## Creating an index 

With Cloudant Query, you can build [indexes](cloudant_query.html#creating-an-index) using MapReduce 
Views (type=json) and Search Indexes (type=text). If you know exactly what data 
you want to find, you can specify how to create the index by making it of type 
JSON. This type of index reduces storage and processing to a minimum. For this 
exercise, the `rolodex` database columns include the following fields:

*   Firstname
*   Lastname
*   Sex
*   Address
*   City
*   State
*   Zipcode
*   Areacode
*   Phone number



###Creating a "type=json" index

Creating an index can reduce the load on your environment as well as the size of your data set. You
select a subset of the columns listed in the table in the database to do this. To specify the columns, 
add them to the `fields` parameter as demonstrated in the example. 

To create a new search index in the Cloudant Dashboard: 

1.  On the Design Documents tab, click **+** and select **New Search Index**. 
2.  Ensure the Save to design document drop-down says New document. 
3.  Type `rolodex-index-design-doc` for the name in the field next to `_design/`. 
4.  In the Index name field, type `JSONindex`.
5.  Accept the defaults for the rest of the fields and click **Create Document and Build Index**.
    The new index opens under the Design Documents tab.

  
To create a new search index from the command line: 

1.  Create an index of type JSON by making the following `POST` request to the `_index` endpoint.
2.  In the request body for the JSON object, specify the `state` and `area code` fields.   
3.  Set the `type` field equal to `json`. 


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
```


###Creating a "type=text" index

A "type=text" index automatically indexes all the documents and fields in your database. As such, you can 
search and retrieve information from any field in the database.  

You select a subset of the columns listed in the database table to do this. To specify the columns, 
add them to the `fields` parameter as shown in the example. 

1.  Create a text type index by making a `POST` request to the `_index` endpoint.
2.  In the request body for the JSON object, specify the `sex`, `lastname`, and `areacode` fields.   
3.  Set the `type` equal to `text` to specify a text type index. 


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


### Listing Cloudant Query indexes 

Now, list all the indexes in the `rolodex` database by using the GET command. 

```json
    GET /rolodex/_index
```

Return JSON lists the indexes in the database.

```
{"total_rows":2,"indexes":[{"ddoc":null,"name":"_all_docs","type":"special","def":{"fields":[{"_id":"asc"}]}},{"ddoc":"_design/a7ee061f1a2c0c6882258b2f1e148b714e79ccea","name":"a7ee061f1a2c0c6882258b2f1e148b714e79ccea","type":"json","def":{"fields":[{"foo":"asc"}]}}]}
```



## Creating a query 

When you write your query statement, you can narrow the data you search by using [selector syntax](cloudant_query.html#selector-syntax) and 
[implicit](cloudant_query.html#implicit-operators) or [explicit](cloudant_query.html#explicit-operators) operators.




### Searching the database using a JSON index

When you use [selector syntax](cloudant_query.html#selector-syntax), you must specify at least one field and 
its corresponding value. When the query runs, it uses these values to search for matches in the database. The 
selector is a JSON object

In this example, the query finds documents whose last name field equals`Greene`. The result set only contains 
`firstname` and `lastname` fields. The `sort` field specifies the field to sort by, `firstname` and the sequence
of the results, in this case, ascending. The result set in this example displays by first name in ascending order. 

1.  From the Databases tab in the Cloudant Dashbaord, click `rolodex` to open the database.
2.  Click on the index created earlier, `JSONindex`.
3.  Enter the selector statement below into the Query field and click **Query**.
    The search results display.   


```json
{
  "selector": {
      "lastname": "Greene"
    }
  },
  "fields": ["firstname","lastname", 
    "_id",
    "_rev"
  ],
  "sort": [
    {
      "firstname": "asc"
    }
  ]
}
```


Results from the search.


```json
{
  "docs": [
    {     
        "firstname": "Amanda", 
        "lastname": "Greene"   
        }
   {
        "firstname": "Greg",   
        "lastname": "Greene"
        }
     ]
}
```

### Querying the database using a text index

[Search for people who live in California and have a 650 area code.]
Using operators in your query allows you to create a more granular search. Operators are described 
[here](cloudant_query.html#query) under Query Parameters. In this example, the operators `$and`, `$text`, 
and `$gt` define the search parameters. 

    *   $and    Finds a match when all the selectors in the array match. 
    *   $text   Matches any word or string in the document. It is not case sensitive. The $text operator is only available with the index "type=text". However, searching for field names is an invalid use of the $text operator. 
    *   $gt     Finds matches greater than the specified value.  


In this example, the query searches for documents whose last name field equals `Brown` and age value is greater than `20`. 
The results will contain the `firstname`, `lastname`, and `age` fields sorted in ascending order by `firstname`. 


1.  From the Databases tab in the Cloudant Dashbaord, click `rolodex` to open the database.
2.  Click on the index created earlier, `JSONindex`.
3.  Enter the selector statement below into the Query field and click **Query**.
    The search results display.    

            
```json
POST /rolodex/_find
{
    "selector": {
        "$and": [
             {
                "$text": "Brown"
            },
            {
                "$gt": 20
                }
            }
    ]
   },
        "fields": [
            "firstname", "lastname", "age"],
  "sort": [
    {
      "firstname": "asc"
    }
  ]            
 }        
```


Results from the search. 

```json
{
  "docs": [
 {     
    "firstname": "John",
    "lastname": "Brown",
    "age": "21"
       },
{
    "firstname": "Sally",
    "lastname": "Brown",
    "age": "16"
       }
  ]
}
```



