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

To begin, you create the `rolodex` database, similar to an address book, and JSON documents that contain the data for the database, including 
the name, age, city, and state for each document. Next, you create a design document that  
contains information about how to build your indexes. You create two different types of indexes to demonstrate how an index  
can make it easier and faster to find data. Finally, you create and run queries against the database. 

While this tutorial focuses on creating a query with Cloudant Dashboard, you can use either Cloudant 
Dashboard or the command line. Follow the links provided throughout this tutorial for information about using the command line. 

Here are the tasks you complete during this tutorial:

1.  [Creating a database using the Cloudant Dashboard](create_query.html#creating-a-database-using-the-cloudant-dashboard)
2.  [Creating a design document](create_query.html#creating-a-design-document)
3.  [Creating an index](create_query.html#creating-an-index)
4.  [Creating a query](create_query.html#creating-a-query)


## Creating a database using the Cloudant Dashboard

Now, you create the `rolodex` database using these steps. When you create the [database](../api/database.html#create) in this exercise, you also 
create the JSON documents used throughout this tutorial.  

To create a database and JSON documents:

1.  If you do not already have one, create a Cloudant account [here](https://cloudant.com/sign-in/).
2.  Log in to the Cloudant Dashboard.
3.  Select **Databases** from the left menu. 
4.  Click **Create Database**. 
5.  Type `rolodex` for the name of the database and click **Create**.<br>
    The `rolodex` database automatically opens.
6.  Select **All Documents** in the left menu.
7.  Click **+** > **New Doc**.<br>
    The new document window opens. 
8.  Copy and paste the sample text below to create a JSON document for the database.

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

<ol><li value="9">Repeat step 8 to add the remaining documents to the database.</li></ol>

_Second sample document:_
```json
{
     "_id": "xxxxxxxxxxxxxxxxx"
            "firstname": "John",
            "lastname": "Brown",
            "age": 21,
            "city": "New York City",
            "state": "New York"   
}  
```

_Third sample document:_
```json
{
    "_id": "xxxxxxxxxxxxxxxxx"
        "firstname": "Greg",
        "lastname": "Greene",
        "age": 35,
        "city": "San Diego",
        "state": "California"   
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


The `rolodex` database has been created and populated with five JSON documents. 


## Creating a design document

[Design documents](../api/design_documents.html#design-documents) contain instructions about how views 
and indexes must be built. When you change a design document, the index is overwritten and 
recreated from scratch. 

Indexes and views have the same purpose, to improve processing and return time for database queries. However, the mechanics are different. 

A view selectively filters documents. You define 
a view in the `view` field inside a design 
document. In Cloudant, views are written using Javascript functions. When you run a query using 
your view, Cloudant applies the Javascript function to 
all the documents in the database. 

Cloudant search indexes are also defined in design documents. Each index is defined by an index function that determines 
what data to index and then store in the index. These indexes use [Lucene Query 
Parsar Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview) 
to query databases.  

To create a design document: 

1.  Select **Design Documents**.
2.  Click **+** > **New Doc**. 
3.  Replace `_id` with `rolodex-index-design-doc`.
4.  Click **Create Document**. <br>
    The `rolodex-index-design-doc` design document is created and holds the index information for the `rolodex` database. 


## Creating an index 

With Cloudant Query, you build [indexes](../api/using_views.html#indexes) using 
[view (MapReduce)](../api/creating_views.html#views-mapreduce-) and [search indexes](../api/search.html#search). T

### Creating a "type=json" index

Creating a ["type=json"](../api/cloudant_query.html#creating-a-type-json-index) index reduces the load on 
your environment and the size of your data set. 

To create a "type=json" index: 

1.  Select **Design Documents**.
2.  Click **+** > **New Search Index**. 
3.  Select `_design/rolodex-index-design-doc` from the **Save to design document** drop-down menu, 
4.  Type `JSONindex` in the Index name field.
5.  Replace the text in the Search index function field with the text below.

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

<ol><li value="6">Accept the remaining options and click **Create Document and Build Index**.</li></ol>
The `JSONindex` was created. You can see your index expanding `rolodex=index-design-doc` and Search Indexes to see the `JSONindex` index.

### Creating a "type=text" index

When you create a ["type=text"](../api/cloudant_query.html#creating-a-type-text-index) index, it 
automatically indexes all the documents and fields in your database. As such, you can 
search and retrieve information from any field.  

To create the index:

1.  Select Design Documents.
2.  Click **+** > **New Search Index**. 
3.  Select `_design/rolodex-index-design-doc` from the **Save to design document** drop-down menu.
4.  Type `TEXTindex` in the Index name field. 
5.  Replace the text in the Search index function field with the text below.

_Search text search index:_

```json
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
```

<ol><li value="6">Accept the remaining options and click **Create Document and Build Index**.</li></ol>
The `TEXTindex` was created. You can see your index expanding `rolodex=index-design-doc` and Search Indexes to see the `TEXTindex` index.

### Listing Cloudant Query indexes 

You can see all the indexes in the `rolodex` database from the Cloudant Dashboard or 
[list](../api/cloudant_query.html#list-all-cloudant-query-indexes) them from the command line. 

1.  Expand `rolodex-index-design-doc` under Design Documents. 
2.  Click Search Indexes.<br>
    The two indexes you created appear. You can edit, clone, or delete an index here. When you select an index, you can use it to query the database. 

## Creating a query 

When you create your [query](../api/cloudant_query.html#query) statement, you can narrow the data you search by using [selector syntax](../api/cloudant_query.html#selector-syntax) and 
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.


### Querying the database using selector syntax

In a [selector expression](../api/cloudant_query.html#creating-selector-expressions), you specify at least one field and 
its corresponding value. When the query runs, it uses these values to search the database for matches. The 
selector is a JSON object. For this exercise, you use the selector expression that is described here. 

This expression finds information from the database about people who live in New York, specifically New York City.   

```json
{
  "selector": {
        "city" : "New York City",  
        "state": "New York"
    }
```    

What you specify in the `fields` parameter determines the information that is returned. In this case, the first and last 
name of everyone in the database who lives in New York City, New York. The results are sorted by first name in ascending order. 

```json
  "fields": ["firstname","lastname"  
  ],
  "sort": [
    {
      "firstname": "asc"
    }  
```  

To run the query:

1.  Click on the `JSONindex` index that you created earlier by expanding `rolodex-index-design-doc` > Search Indexes > JSONindex.
2.  Copy and paste the following selector statement to the Query field and click **Query**.  

_Example query to find people who live in New York City, NY:_

```json
{
  "selector": {
        "city" : "New York City",  
        "state": "New York"      
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

_Example results returned from search:_

```json
{
  "docs": [
    {     
        "firstname": "Amanda", 
        "lastname": "Greene"   
        }
    {     
        "firstname": "John", 
        "lastname": "Brown"   
        }
    {     
        "firstname": "Sally", 
        "lastname": "Brown"   
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

This example searches the database for people with the last name Brown and an age greater than 20.

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
```   

The results returned contain the first name, last name, and age sorted by first name in ascending order. 

```json
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
To run the query:

1.  Click on the `TEXTindex` index that you created earlier by expanding `rolodex-index-design-doc` > Search Indexes > JSONindex.
2.  Copy and paste the example selector statement below into the Query field and click **Query**.  

_Example query to find documents where last name equals Brown and age is greater than 20:_

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



