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

This tutorial demonstrates how to create a design document and an index, and how to use Cloudant Query to extract specific data 
from the database.

To start the tutorial, you create a database and JSON documents that contain data. Next, you create a design document
which contains information about how to build your index. You create two different types of indexes to demonstrate how
they make it easier and faster to find data. Lastly, you write and run queries.  

Here are the high-level tasks you will complete for this tutorial:

1.  [Creating a database using the Cloudant Dashboard](create_query.html#creating-a-database-using-the-cloudant-dashboard)
2.  [Creating a design document](create_query.html#creating-a-design-document)
3.  [Creating an index](create_query.html#creating-an-index)
4.  [Creating a query](create_query.html#creating-a-query)


## Creating a database using the Cloudant Dashboard

This tutorial is based on the `rolodex` database that you create using these steps. 

When you create a query using Cloudant, you create it using the Cloudant Dashboard or the command line. This tutorial
focuses on creating a query with the Cloudant Dashboard. However, the documentation links provided throughout give
examples for both the command line and Cloudant Dashboard. 

When you create the [database](../api/database.html#create) in this exercise, you also create four JSON documents.  

To create a database and JSON documents:
1.  Create a Cloudant account [here](https://cloudant.com/sign-in/) if you do not already have one.
2.  Log in to the Cloudant Dashboard.
3.  Verify that the Databases tab is selected in the left navigation. 
4.  Click **Create Database**. 
5.  Type `rolodex` as the name for the database and click **Create**.
    The `rolodex` database automatically opens.
6.  From the All Documents tab, click **+** and select **New Doc**.
    The new document opens. 
7.  Add the text for each document as shown in the examples below.

_First sample document:_
```json
    {
      "_id": "xxxxxxxxxxxxxxxxx"
                "firstname": "Sally",
                "lastname": "Brown",
                "age": 16,
                "city": "New York City",
                "state": "New York"                
        }
```
_Second sample document:_
```json
{
     "_id": "xxxxxxxxxxxxxxxxx"
            "firstname": "John",
            "lastname": "Brown",
            "age": 21,
            "city": "San Francisco",
            "state": "California"   
}  
```

_Third sample document:_
```json
{
    "_id": "xxxxxxxxxxxxxxxxx"
        "firstname": "Greg",
        "lastname": "Greene",
        "age": 35,
        "city": "Princeton",
        "state": "New Jersey"   
}  
```

_Fourth sample document:_
```json
{
  "_id": "xxxxxxxxxxxxxxxxx"
    "firstname": "Amanda",
    "lastname": "Greene",
    "age": 44,
    "city": "New York City",
    "state": "New York"     
}
```

_Fifth sample document:_
```json
{
      "_id": "xxxxxxxxxxxxxxxxx"
        "firstname": "Lois",
        "lastname": "Brown",
        "age": 33,
        "city": "Baton Rouge",
        "state": "Louisiana"     
}
```


The `rolodex` database and five JSON documents were created. 


## Creating a design document

Design documents contain instructions about how views 
and indexes must be built. When you change the design documents, the index is overwritten and 
recreated from scratch.

Indexes and views have the same purpose, to improve processing and return time for database queries.  
However, the mechanics are different. A view selectively filters documents. You define 
a view in the `view` field inside a design 
document. In Cloudant, views are written using Javascript functions. When you run a query using 
your view, Cloudant applies the Javascript function to 
all the document in the database. 

Cloudant search indexes are also defined in design documents. These indexes use [Lucene Query 
Parsar Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview) 
to query databases. Each index is defined by an index function that determines 
the data to index and store in the index. 

You configure a [search index](../api/search.html#search) or a 
[MapReduce view](../api/creating_views.html#views-mapreduce-) by adding 
[design documents](../api/design_documents.html#design-documents) 
to the database. 

1.  From the Dashboard, open the `rolodex` database.
2.  From the Design Documents tab, click **+** and select **New Doc**. 
3.  Replace `_id` with `rolodex-index-design-doc` and click **Create Document**. 
    The design document is added to the list of documents in the database. 

The index information for this tutorial is stored in the `rolodex-index-design-doc` design document. 


## Creating an index 

With Cloudant Query, you build [indexes](../api/using_views.html#indexes) using MapReduce 
Views (type=json) and Search Indexes (type=text). If you know exactly what data 
you want to find, you specify how to create the index by making it of type 
JSON. This type of index keeps storage and processing to a minimum. The `rolodex` 
database columns include the following fields:

*   First name
*   Last name
*   Age
*   City
*   State


### Creating a "type=json" index

Creating a ["type=json"](../api/cloudant_query.html#creating-a-type-json-index) index reduces the load on 
your environment as well as the size of your data set. You
select a subset of the columns listed in the table in the database to do this. To specify the columns, 
add them to the `fields` parameter as demonstrated in this exercise. 

To create a new search index in the Cloudant Dashboard: 

1.  In the `rolodex` database, from the Design Documents tab, click **+** and select **New Search Index**. 
2.  Verify New document is selected in the **Save to design document** field.
3.  Type `rolodex-index-design-doc` in the `_design/` field. 
4.  In the Index name field, type `JSONindex`.
5.  From the Search index function window, replace the text with the text below. 

_Sample JSON search index:_
```json
    function (doc) [
    {
        "index": {
            "fields": [
                {
                   "firstname" : "string",
                   "lastname" : "string",
                   "city" : "string"                   
                    }
                ]                    
        },
    }
]   
```
<ol><li value="6">Accept the defaults for the remainder of the fields and click **Create Document and Build Index**.
    <p>The new index opens under the Design Documents tab.</p></li></ol>

### Creating a "type=text" index

When you create a ["type=text"](../api/cloudant_query.html#creating-a-type-text-index) index, it 
automatically indexes all the documents and fields in your database. As such, you can 
search and retrieve information from any field.  

To create an index, you select a subset of the columns listed in the database table. 
To specify the columns, add them to the `fields` parameter as shown in the example. 

1.  In the `rolodex` dataabase, from the Design Documents tab, click **+** and select **New Search Index**. 
2.  Verify New document is selected in the **Save to design document** field.
3.  Type `rolodex-index-design-doc` for the name in the field next to `_design/`. 
4.  In the Index name field, type `TEXTindex`.
5.  Accept the defaults for the remainder of the fields and click **Create Document and Build Index**.
6.  From the Search index function window, replace the text with the text below

_Search text search index:_
  function (doc) [
    {
        "index": {
            "fields": [
           {
               "name": "firstname",
               "type": "string"
            },
               {
                "name": "lastname",
                "type": "string"
            },
               {
                "name": "age",
                "type": "number"
            },
               {
                "name": "city",
                "type": "string"
            },   
               {
                "name": "state",
                "type": "string"
            }             
        ]
    },
}
]


The new index displays with `rolodex-index-design-doc`.

### Listing Cloudant Query indexes 

You can see all the indexes in the `rolodex` database from the Cloudant Dashboard or [list](../api/cloudant_query.html#list-all-cloudant-query-indexes) them from the command line. 

1.  From the Databases tab, click `rolodex-index-design-doc`. 
2.  Click Search Indexes.
    The indexes for the database display. You can edit, clone, or delete an index here or query the database. 

## Creating a query 

When you create your [query](../api/cloudant_query.html#query) statement, you can narrow the data you search by using [selector syntax](../api/cloudant_query.html#selector-syntax) and 
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.


### Searching the database using selector syntax

In a [selector expressions](../api/cloudant_query.html#creating-selector-expressions), you must specify at least one field and 
its corresponding value. When the query runs, it uses these values to search for matches in the database. The 
selector is a JSON object.

Using the `selector` expression you specify the search results you want. In this case, search the `rolodex` database and find the
documents with `lastname=Brown` and `city=New York City`.
_Example selector expression:_
```json
{
  "selector": {
      "lastname": "Brown",
      "city" : "New York City"  
    }
```    

The `"fields"` parameter indicates that the search results include the first and last name.
_Example `"fields"` parameter:_
```json
  "fields": ["firstname","lastname"
  ],
```

The `"sort"` parameter indicates that the search results sort in ascending order by first name.
_Example `"sort"` parameter:_
```json
  "sort": [
    {
      "firstname": "asc"
    }
```    
To run the query:
1.  From the Databases tab, click `rolodex` to open the database.
2.  Click on the `JSONindex` index that you created earlier.
3.  Add the following selector statement into the Query field and click **Query**.  

_Example query to find last name and city:_
```json
{
  "selector": {
      "lastname": "Greene",
      "city" : "Syracuse"      
    },
  "fields": ["firstname","lastname"
  ],
  "sort": [
    {
      "firstname": "asc"
    }
  ]
}
```

_Example results from the search:_


```json
{
  "docs": [
    {     
        "firstname": "Amanda", 
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

In this example, the search looks for documents whose last name field equals `Brown` and age value is greater than `20`. 
The results contain the `firstname`, `lastname`, and `age` fields sorted in ascending order by `firstname`. 

The expression used in this exercise demonstrates how operators can be used in combination. Together the operators create 
a search that finds the Browns in the database who are older than 20.

1.  In the Cloudant Dashboard on the Databases tab, click `rolodex` to open the database.
2.  Click on `TEXTindex` created in a previous exercise.
3.  Paste the example selector statement below into the Query field and click **Query**.
    The search results display.    


_Example query to find documents where last name=`Brown` and age is greater than 20:_
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

_Example results from the search:_

```json
{
  "docs": [
 {     
    "firstname": "John",
    "lastname": "Brown",
    "age": "21"
       },
 {     
    "firstname": "Lois",
    "lastname": "Brown",
    "age": "33"
       }       
  ]
}
```



