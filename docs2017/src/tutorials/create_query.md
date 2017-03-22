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
    Each database automatically includes a design document. Indexes are created in the design document. When you change the design document, the index is overwritten. To create an index of type JSON, make a POST request to the database. 
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


Example document 1
```json
{
    "first name": "Sally",
    "last name": "Brown",
    “sex”: “female”
    "address": "122 Main Street”, 
    “city”: “Peoria”, 
    “state”: “IL”,
    “zip code: 61602,
    “area code”: 309,
    "phone": “334-9354”
}    
```


8. Create nine more documents using the following text by inserting the text after the "_id" line and inside the brackets. 


Example document 2
```json
{
    "first name": "John",
    "last name": "Smith",
    “sex”: “male”
    "address": "123 Main Street”, 
    “city”: “Peoria”, 
    “state”: “IL”,
    “zip code: 61602, 
    “area code”: 309,
    "phone": “334-4614"
}
```

Example document 3
```json
{
    "first name": "Greg",
    "last name": "Mason",
    “sex”: “male”
    "address": "124 Main Street”, 
    “city”: “Peoria”, 
    “state”: “IL”,
    “zip code: 61602,
    “area code”: 309,
    "phone": “334-4445”
}
```

Example document 4
```json
{
    "first name": “Dan”,
    "last name": “Brown”,
    “sex”: “male”
    "address": "125 Main Street”, 
    “city”: “Peoria”, 
    “state”: “IL”,
    “zip code: 61602,
    “area code”: 309,
    "phone": “334-4275”
}
```

Example document 5
```json
{
    "first name": "Janine",
    "last name": "Lee",
    “sex”: “female”
    "address": "126 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": “726-9938”
}
```

Example document 6
```json
{
    "first name": "Sam",
    "last name": "Harris",
    “sex”: “male”
    "address": "125 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": "225-4444"
}
```

Example document 7
```json
{
    "first name": “Amanda”,
    "last name": “Green”,
    “sex”: “female”
    "address": "124 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": “613-8462”
}
```

Example document 8
```json
{
    "first name": “Tammy”,
    "last name": “Smith”,
    “sex”: “female”
    "address": "122 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": "333-7310”
}
```

Example document 9
```json
{
    "first name": “Patricia”,
    "last name": “Jones”,
    “sex”: “female”
    "address": "125 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": "336-4003”
}
```

Example document 10
```json
{
    "first name": “Nick”,
    "last name": “Brown”,
    “sex”: “male”
    "address": "126 Second Street”, 
    “city”: “San Mateo”, 
    “state”: “CA”,
    “zip code: 94401,
    “area code”: 650,
    "phone": "334-4841”
}
```

The `rolodex` database now contains ten JSON documents. 

## Creating an index 
With Cloudant Query, you can use the Primary Index out-of-the-box. You can also build indexes using MapReduce 
Views (type=json) and Search Indexes (type=text). When you create an index, you must select the columns 
from the database table that you want to search. For example, the `rolodex` database contains the following 
columns:

*   First name
*   Last name
*   Sex
*   Address
*   City
*   State
*   Zip code
*   Area code
*   Phone number

When you create an index, it is important to select the columns that will improve your searches. The following
examples show how to create an index to reduce your data set and the load on your environment. 



###Creating a "type=JSON" index
Use a "type=JSON" index to maximize flexiblity when you query the database. 

1.  Set the type field to JSON.   
2.  Create a `POST` request using the following fields.   

POST request

```json  
    {
        "index": {
            "fields": {"name","address","phone number"} 
        }
        "name" : "rolodex-index",
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
Use a "type=text" index to maximize flexiblity when you query the database. 



### Listing Cloudant Query indexes 

You can list all the indexes in a database using the GET endpoint. 

```
    GET /rolodex/_index
```

Return JSON lists the index in the database in the following manner.

```
    [INSERT RETURN JSON]
```


### Deleting an index

Indexes are saved to the design document. Therefore, the index must be deleted from the design document. You delete the index from the design document using the DELETE endpoint.

To delete the index we created, use the following DELETE string [?].

```
    DELETE /rolodex/_index/$DDOC/JSON/$NAME
```    

Return JSON [shows the index was deleted].

```
     [INSERT RETURN JSON]
``` 




## Creating a query 
[Search for one document.]

1.  Search for a specific document.
    ```

POST /rolodex/_find
{
    "selector": {
        "area code": 650
        "last name": Brown
        }
         "fields": ["first name", "last name", "address", "area code", "phone number"],
         "sort": ["last name"],
         "limit": 10
         "skip": 0
    }        



### Querying the rolodex database using selector syntax
[Using selector syntax and two operators. Search for people who live in Indiana.]

### Querying the rolodex database using operators
[Search for people who live in California and have a 650 area code.]

    

