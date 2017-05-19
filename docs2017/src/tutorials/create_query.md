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

# Creating a Cloudant Query

This tutorial demonstrates how to create a design document and an index, and use Cloudant Query to extract specific data 
from the database.

To write a query, you must first create a database and JSON documents that contain data. Next, you create a design document
that contains information about how to build your index. You create an index. This tutorial shows how to build two different types of indexes. 
When you run the query, the index you create makes it easier and faster to find data within the data set.

<ol>
<li>[Creating a database using the Cloudant Dashboard](create_query.html#creating-a-database-using-the-cloudant-dashboard)</li>
<li>[Creating a design document](create_query.html#creating-a-design-document)</li>
<li>[Creating an index](create_query.html#creating-an-index)</li>
<li>[Writing a query](create_query.html#creating-a-query)
</li>
</ol>

## Creating a database using the Cloudant Dashboard

This tutorial is based on the `rolodex` [database](../api/database.html#create) that you create using these steps. 

When you create a query using Cloudant, you create it using the Cloudant Dashboard or the command line. This tutorial
focuses on creating a query with the Cloudant Dashboard. However, the documentation links provided throughout give
examples for the command line and Cloudant Dashboard. 

When you create the database in this exercise, you also create four JSON documents. The sample documents
contain three fields: first name, last name, and age. 

<ol><li>Create a Cloudant account [here](https://cloudant.com/sign-in/) if you do not already have one.</li>
<li>Log in to the Cloudant Dashboard.</li>
<li>Verify that the Databases tab is selected in the left navigation. </li>
<li>Click **Create Database**. </li>
<li>Type `rolodex` as the name for the database and click **Create**.<br>
    The `rolodex` database automatically opens.</li>
<li>From the All Documents tab, click **+** and select **New Doc**.<br>
    The new document opens. </li>
<li>Add the text for the first document after the `_id` line and inside the brackets.</li></ol>

_Details for the first document:_
```json
    {
      "_id": "xxxxxxxxxxxxxxxxx"
                "firstname": "Sally",
                "lastname": "Brown",
                "age": "16",
                "city": "New York City",
                "state": "New York"                
        }
```

<oL><li value="8">Repeat steps 6 and 7 for the remainder of the documents. 
<p>Use the following information for the content of each document. 

_Details for the second document:_
```json
  "firstname": "John",
  "lastname": "Brown",
  "age": "21",
  "city": "San Francisco",
  "state": "California"     
```

_Details for the third document:_
```json
  "firstname": "Greg",
  "lastname": "Greene",
  "age": "35",
  "city": "Princeton",
  "state": "New Jersey"     
```

_Details for the fourth document:_
```json
  "firstname": "Amanda",
  "lastname": "Greene",
  "age": "44",
  "city": "New York City",
  "state": "New York"     
```

_Details for the fifth document:_
```json
  "firstname": "Lois",
  "lastname": "Smythe",
  "age": "32",
  "city": "Baton Rouge",
  "state": "Louisiana"     
```
</p></li>
</ol>

The `rolodex` database now contains five JSON documents. 


##Creating a design document

You configure a [Search Index](../api/search.html#search) or a [MapReduce view](../api/creating_views.html#views-mapreduce-) by adding 
[design documents](../api/design_documents.html#design-documents) 
to the database. An index contains pointers to the exact location of information in the database table based on one or more columns. 

Design documents contain instructions about how the view 
or index must be built. When you change the design documents, the index is overwritten and recreated from scratch.

1.  From the Dashboard, open the `rolodex` database.
2.  From the Design Documents tab, click **+** and select **New Doc**. 
3.  Replace `_id` with `rolodex-index-design-doc` and click **Create Document**. <br>
    The design document is added to the list of documents in the database. 

The index information for this tutorial is stored in the `rolodex-index-design-doc` design document. 


## Creating an index 

With Cloudant Query, you build [indexes](../api/using_views.html#indexes) using MapReduce 
Views (type=json) and Search Indexes (type=text). If you know exactly what data 
you want to find, you specify how to create the index by making it of type 
JSON. This type of index keeps storage and processing to a minimum. For this 
exercise, the `rolodex` database columns include the following fields:

*   First name
*   Last name
*   Age
*   City
*   State


###Creating a "type=json" index

Creating a ["type=json"](../api/cloudant_query.html#creating-a-type-json-index) index reduces the load on 
your environment as well as the size of your data set. You
select a subset of the columns listed in the table in the database to do this. To specify the columns, 
add them to the `fields` parameter as demonstrated in the example. 

To create a new search index in the Cloudant Dashboard: 

1.  In the `rolodex` database, from the Design Documents tab, click **+** and select **New Search Index**. 
2.  Verify New document is selected in the **Save to design document** field.
3.  Type `rolodex-index-design-doc` in the `_design/` field. 
4.  In the Index name field, type `JSONindex`.
5.  From the Search index function window, replace the text with the text below. 

_Search index function text:_
```json
    function (doc) {
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
<ol><li value="6">Accept the defaults for the remainder of the fields and click **Create Document and Build Index**.
    <p>The new index opens under the Design Documents tab.</p></li></ol>

###Creating a "type=text" index

When you create a ["type=text"](../api/cloudant_query.html#creating-a-type-text-index) index, it automatically indexes all the documents and fields in your database. As such, you can 
search and retrieve information from any field.  

To create an index, you select a subset of the columns listed in the database table. 
To specify the columns, add them to the `fields` parameter as shown in the example. 

1.  In the `rolodex` dataabase, from the Design Documents tab, click **+** and select **New Search Index**. 
2.  Verify New document is selected in the **Save to design document** field.
3.  Type `rolodex-index-design-doc` for the name in the field next to `_design/`. 
4.  In the Index name field, type `TEXTindex`.
5.  Accept the defaults for the remainder of the fields and click **Create Document and Build Index**.<br>
6.  From the Search index function window, replace the text with the text below

_Search index function text:_
```json
 function (doc) 
 {           
    "index": {
       "default_field": {
            "enabled": true,
            "analyzer": "standard"
            },           
        "selector": {},
                "fields": [
                    {"name": "firstname", "type": "string"},
                    {"name": "lastname", "type": "string"},
                    {"name": "age", "type": "number"}
               ]
        }   
    }
```
    The new index opens under the Design Documents tab.

### Listing Cloudant Query indexes 

You can [list](../api/cloudant_query.html#list-all-cloudant-query-indexes) all the indexes in the `rolodex` database by using the GET command. 

```json
    GET /rolodex/_index
```

Return JSON lists the indexes in the database.

```
{
    "total_rows":2,
      "indexes": [
         {
            "ddoc":null,
            "name":"_all_docs",
            "type":"special",
            "def":{
                "fields":[
                    {"_id":"asc"}
            ]
          }
       },
       {    
           "ddoc":"_design/a7ee061f1a2c0c6882258b2f1e148b714e79ccea",
           "name":"a7ee061f1a2c0c6882258b2f1e148b714e79ccea",
           "type":"json",
           "def": {
               "fields": [
                   {"foo":"asc"}
               ]
            }
         }
     ]
}
```



## Writing a query 

When you write your [query](../api/cloudant_query.html#query) statement, you can narrow the data you search by using [selector syntax](../api/cloudant_query.html#selector-syntax) and 
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.


### Searching the database using selector syntax

In a [selector expressions](../api/cloudant_query.html#creating-selector-expressions), you must specify at least one field and 
its corresponding value. When the query runs, it uses these values to search for matches in the database. The 
selector is a JSON object

In this example, the query finds documents whose last name field equals `Greene`. The results only contain the 
`firstname` and `lastname` fields. The value specified in the `sort` field determines the order and the sequence 
of the results. The results in this example display by first name in ascending order. 

1.  From the Databases tab in the Cloudant Dashbaord, click `rolodex` to open the database.
2.  Click on the index created earlier, `JSONindex`.
3.  Add the following selector statement into the Query field and click **Query**.<br>
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

### Querying the database using operators

Using operators in your query allows you to create a more granular search. Operators are described 
[here](../api/cloudant_query.html#query-parameters). In this example, the operators `$and`, `$text`, 
and `$gt` define the search parameters. These operators perform the following functions:

    *   $and    Finds a match when all the selectors in the array match. 
    *   $text   Matches any word or string in the document. It is not case sensitive. The $text operator is only available with the index "type=text". However, searching for field names is an invalid use of the $text operator. 
    *   $gt     Finds matches greater than the specified value.  


```json
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

In this example, the search looks for documents whose last name field equals `Brown` and age value is greater than `20`. 
The results contain the `firstname`, `lastname`, and `age` fields sorted in ascending order by `firstname`. 

1.  In the Cloudant Dashboard on the Databases tab, click `rolodex` to open the database.
2.  Click on `JSONindex` created in a previous exercise.
3.  Paste the example selector statement into the Query field and click **Query**.<br>
    The search results display.    
 

            
```json
POST /rolodex/_find HTTP/1.1
Content-Type: application/json
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



