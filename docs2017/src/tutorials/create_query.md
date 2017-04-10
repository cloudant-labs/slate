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

## Creating a database using the Cloudant Dashboard

This tutorial is based on the `rolodex` database that you are going to create. 

1.  Create a Cloudant account [here](https://cloudant.com/sign-in/) if you do not already have one.
2.  Log in to the Cloudant Dashboard. 
3.  Verify that the Databases tab is selected in the left navigation. 
4.  Click **Create Database**. 
5.  Enter `rolodex` as the name for the database and click **Create**. 
    The `rolodex` database automatically opens. 
6.  Click **+** next to All Documents and select **New Doc**.
    The New Document window displays. 
7.  Create a new document by inserting the following text after the "_id" line and inside the brackets.   


```json
  ,
  "firstname": "Sally",
  "lastname": "Brown",
  "sex": "female",
  "address": "122 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-9354"
```


8. Repeat the steps 6 and 7 to create nine new documents using the text below. 


Document 1

```json
   ,
  "firstname": "John",
  "lastname": "Smith",
  "sex": "male",
  "address": "123 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4614"
```

Document 2

```json
   ,
  "firstname": "Greg",
  "lastname": "Greene",
  "sex": "male",
  "address": "124 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4445"
```

Document 3
```json
   ,
  "firstname": "Dan",
  "lastname": "Brown",
  "sex": "male",
  "address": "125 Main Street",
  "city": "Peoria",
  "state": "IL",
  "zipcode": 61602,
  "areacode": 309,
  "phonenumber": "334-4275"
```

Document 4

```json
   ,
    "firstname": "Janine",
    "lastname": "Lee",
    "sex": "female",
    "address": "126 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "726-9938"
```

Document 5

```json
   ,
  "firstname": "Sam",
  "lastname": "Harris",
  "sex": "male",
  "address": "125 Second Street",
  "city": "San Mateo",
  "state": "CA",
  "zipcode": 94401,
  "areacode": 650,
  "phonenumber": "225-4444"
```

Document 6

```json
   ,
  "firstname": "Amanda",
  "lastname": "Greene",
  "sex": "female",
  "address": "124 Second Street",
  "city": "San Mateo",
  "state": "CA",
  "zipcode": 94401,
  "areacode": 650,
  "phonenumber": "613-8462"
```

Document 7

```json
    ,
    "firstname": "Tammy",
    "lastname": "Smith",
    "sex": "female",
    "address": "122 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "333-7310"
```

Document 8

```json
    ,
    "firstname": "Patricia",
    "lastname": "Jones",
    "sex": "female",
    "address": "125 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "336-4003"  
```

Document 9

```json
    ,
    "firstname": "Nick",
    "lastname": "Brown",
    "sex": "male",
    "address": "126 Second Street", 
    "city": "San Mateo", 
    "state": "CA",
    "zipcode": 94401,
    "areacode": 650,
    "phonenumber": "334-4841"
```

The `rolodex` database now contains ten JSON documents. 


##Creating a design document

You configure a search index or a MapReduce view by adding Design Documents 
to the database. Design Documents contain instructions about how the view or index must be 
built. When you change the Design Document, the index is overwritten and recreated from scratch.

1.  From the Dashboard, open the `rolodex` database.
2.  On the Design Doc tab, click **+** and select **New Doc**. 
3.  Replace the `_id` with `rolodex-index-design-doc` and click **Create Document**.
The Design Document is added to the list of documents in the database. 

The index and view information for this tutorial will be stored in this Design Document. 


## Creating an index 

With Cloudant Query, you can build indexes using MapReduce 
Views (type=json) and Search Indexes (type=text). The `rolodex` database contains the 
following columns:

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
select a subset of the columns listed in the table in the database to do this. You select the columns
by specifying them in the `fields` parameter as shown in the request below. 
  
1.  Create an index with `type=JSON` specified by making a `POST` request to the `_index` endpoint.
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

If you want to search all your data, you can create a "type=text" index. 
A "type=text" index automatically indexes all the documents and fields in your database which
allows you to query and retrieve information from all the data in your database.  

1.  Create a text type index by making a `POST` request to the `_index` enpoint.
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

```
    GET /rolodex/_index
```

Return JSON lists the indexes in the database.

```
{"total_rows":2,"indexes":[{"ddoc":null,"name":"_all_docs","type":"special","def":{"fields":[{"_id":"asc"}]}},{"ddoc":"_design/a7ee061f1a2c0c6882258b2f1e148b714e79ccea","name":"a7ee061f1a2c0c6882258b2f1e148b714e79ccea","type":"json","def":{"fields":[{"foo":"asc"}]}}]}
```



## Creating a query 

You can narrow the data you search by using [selector syntax](cloudant_query.html#selector-syntax) or 
operators, ([implicit](cloudant_query.html#implicit-operators) or [explicit](cloudant_query.html#explicit-operators))
 when you write your query statement. 


### Querying the database using selector syntax

The following request uses selector syntax to search the `rolodex` database. This query will find 
documents with the last name is `Greene`. 

In this example, you must type in the name of the field to search after the `selector` field. 
In this case, type in the lastname field and tthe selector syntax uses the field to search, 

1.  After `selector`, type in `"lastname": "Greene"` to find all the documents with the last name Greene.
2.  Type in `firstname` and `lastname`. 
    These are the fields that display with the results. 
3.  Type in `lastname` to sort the results' list by the last name.


```
POST /rolodex/_find
{
    "selector": {
        "lastname": "Greene"
        }
         "fields": ["firstname", "lastname"],
         "sort": ["firstname"]
    }        
```


Results from the search.


```
{
  "docs": [
    {     
        "firstname": "Amanda",
        "lastname": "Greene",
        "city": "San Mateo",        
        "state": "CA"
        }
   {
        "firstname": "Greg",
        "lastname": "Greene",
        "city": "Peoria",
        "state": "IL",
        }
     ]
}
```

### Querying the database using the `$and` operator

[Search for people who live in California and have a 650 area code.]
The following request uses selector syntax and the explicit operator `$and`. In this case, the query will find
the documents in the database with a female who has a 650 area code. 

1.  After `selector`, type in `"lastname": "Greene"` to find all the documents with the last name Greene.
2.  Type in `firstname` and `lastname`. 
    These are the fields that display with the results. 
3.  Type in `lastname` to sort the results' list by the last name.


```
POST /rolodex/_find
{
    "selector": {
        "$and": [
             {
                "$text": "female"
            },
            {
                "areacode": 650
                }
            }
    ]
   },
        "fields": [
            "firstname", "lastname", "areacode"]  
    }        
```


Results from the search. 

```
{
  "docs": [
 {     
    "firstname": "Janine",
    "lastname": "Lee",
    "areacode": 650
       }
 {
    "firstname": "Amanda",
    "lastname": "Greene",
    "areacode": 650        
       }
    
 {  
     "firstname": "Tammy",
     "lastname": "Smith",
     "areacode": 650 
       }
 {
    "firstname": "Patricia",
    "lastname": "Jones",
       "areacode": 650 
       }
     ]
}
```




