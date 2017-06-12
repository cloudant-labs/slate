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

To begin, you create the `query-demo` database, some JSON documents that contain the data for these exercises, and a design document that contains information about how to build your index. Next, you create an index and run queries against it. 

In this tutorial, you can use either Cloudant
Dashboard or the command line. Instructions for both methods are provided. Follow the links that are provided throughout 
this tutorial for more information.

You complete the following tasks during this tutorial:

1.  [Create a database.](create_query.html#creating-a-database)
2.  [Create a design document and index.](create_query.html#creating-a-design-document)
3.  [Query the database.](create_query.html#creating-a-query)


## Assumptions

Before you begin, follow these steps to prepare for the tutorial. 

1.  [Create a Bluemix account.](https://console.ng.bluemix.net/registration/)
2.  Log in to the [Cloudant Dashboard](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db).  
3.  [Create a Cloudant instance on Bluemix.](https://console.ng.bluemix.net/docs/services/Cloudant/tutorials/create_service.html#creating-a-cloudant-instance-on-bluemix)
4.  (Optional) [Create an acurl alias](https://console.ng.bluemix.net/docs/services/Cloudant/guides/acurl.html#authorized-curl-acurl-) 
    to make it easier and faster to run commands from the command line.
5.  Replace the `$ACCOUNT` variable in the following commands with the name you use to 
    log in to Cloudant Dashboard. If you decide not to set up `acurl`, use this
    URL instead of the one provided in the exercises. 
    
    <code>curl https://$ACCOUNT:$PASSWORD@$ACCOUNT.cloudant.com/foo -X PUT</code>

 

## Creating a database

In this section, you create the `query-demo` [database](../api/database.html#create) which is the database that we use in this tutorial.

From the command line:

1.  Create a database by running this command.<br>

    <code>acurl https://$ACCOUNT.cloudant.com/query-demo -X PUT</code>

2.  Verify that the database was created successfully in the results. 
    
    *Results:*
    ```json
    {"ok":true}
    ```

From the Cloudant Dashboard:

<ol><li>Open the Cloudant service instance that you created. </li>
<li>Select the Databases tab. 
<p><img src="../images/tabs.png" alt="Databases tab"></p></li>
<li>Click <b>Create Database</b>. </li>
<li>Enter <code>query-demo</code> and click <b>Create</b>.
<p>The <code>query-demo</code> database automatically opens.</p>
</li>
</ol>

### Listing databases

Verify that the `query-demo` database was created correctly. 

From the command line:


1.  See the database by running this command.

    <code>acurl https://$ACCOUNT.cloudant.com/_all_dbs</code>

2.  See the `query-demo` database and any other databases that are associated with your account.   

    *Results:*
    ```json
    ["query-demo"]
    ```

From the Cloudant Dashboard:

1.  Click the **Databases** tab.
2.  See the `query-demo` database in the list on the **Your Databases** tab.



### Deleting a database

If you decide to delete the database, for example, if you made a mistake, you can delete the database and start again. 

From the command line:

1.  Delete the database by running this command.

    <code>acurl https://$ACCOUNT.cloudant.com/query-demo -X DELETE</code>

2.  See the results to verify the `query-demo` database was deleted. 

    *Results:*
    ```json
    {"ok":true}
    ```


From the Cloudant Dashboard:

<ol>
<li>Select the <b>Your Databases</b> tab.</li>
<li>Click <b>Delete</b> next to the database you want to delete.</li> 
<li>Enter the name of the database and click <b>Delete Database</b>.</li>
</ol>

## Creating documents in the database

The JSON documents that you create here contain the data you use to query the `query-demo` database in later exercises. 

From the command line:

<ol><li>Copy the sample JSON to a data file named <code>bulkcreate.dat</code> to create all five documents.
<p><pre>{
	"docs": 
       [
	{ 
		"_id": "doc1",
		"firstname": "Sally",
		"lastname": "Brown",
		"age": 16,
		"location": "New York City, NY"
    },
  { 
		"_id": "doc2",
        "firstname": "John",
	    "lastname": "Brown",
	    "age": 21,
        "location": "New York City, NY"
  },
   {
		"_id": "doc3",
		"firstname": "Greg",
		"lastname": "Greene",
		"age": 35,
		"location": "San Diego, CA"
   },
  {
		"_id": "doc4",
		"firstname": "Amanda",
		"lastname": "Greene",
		"age": 44,
		"location": "Baton Rouge, LA"
  },
   {
		"_id": "doc5",
		"firstname": "Lois",
		"lastname": "Brown",
		"age": 33,
		"location": "Syracuse, NY"
   }
  ]
}</pre></p></li>
<li>Run this command to create the documents. 
<p>The following POST command creates five individual documents at the same time. </p>
<p><code>acurl https://$ACCOUNT.cloudant.com/query-demo/_bulk_docs -X POST -H "Content-Type: application/json" -d \@bulkcreate.dat</code></p>
<p><i>Results:</i></p> 
<p><pre>[{"ok":true,
"id":"doc1","rev":"1-57a08e644ca8c1bb8d8931240427162e"},
{"ok":true,"id":"doc2","rev":"1-bf51eef712165a9999a52a97e2209ac0"},
{"ok":true,"id":"doc3","rev":"1-9c9f9b893fcdd1cbe09420bc4e62cc71"},
{"ok":true,"id":"doc4","rev":"1-6aa4873443ddce569b27ab35d7bf78a2"},
{"ok":true,"id":"doc5","rev":"1-d881d863052cd9681650773206c0d65a"}]</pre></p>
<p><b>Note:</b> Notice that the '@' symbol, used to indicate that the data 
is included in a file, is identified by the supplied name.</p></li></ol>

From the Cloudant Dashboard:

<ol>
<li>Select the <b>All Documents</b> tab. </li>
<li>Click <b>+</b> and select <b>New Doc</b>.
<p>The New Document window opens. </p></li>
<li>To create a JSON document, copy the following sample text and replace the existing text in the new document.
<p><i>First sample document</i>:<br>
<pre>{ 
        "firstname": "Sally",
        "lastname": "Brown",
        "age": 16,
        "location": "New York City, NY",
        "_id": "doc1"
     }</pre></p>

</li>
<li>Repeat the previous step and add the remaining documents to the database.
<p><i>Second sample document</i>:<br>
<pre>{ 
        "firstname": "John",
        "lastname": "Brown",
        "age": 21,
        "location": "New York City, NY",
        "_id": "doc2"
   }</pre></p>
<p><i>Third sample document:</i><br>
<pre> {
        "firstname": "Greg",
        "lastname": "Greene",
        "age": 35,
		"location": "San Diego, CA",
        "_id": "doc3"
     }
</pre>
</p>
<p><i>Fourth sample document:</i><br>
<pre>{
        "firstname": "Amanda",
        "lastname": "Greene",
        "age": 44,
		"location": "Baton Rouge, LA",
        "_id": "doc4"
      }</pre>
</p>
<p><i>Fifth sample document:</i><br>
<pre>{
        "firstname": "Lois",
        "lastname": "Brown",
        "age": 33,
        "location": "New York City, NY",
        "_id": "doc5"
     }
</pre>
</li>
<p>The `query-demo` database was created and populated with five JSON documents. </p></li></ol>

### Listing the documents in the database

Check the database to verify that all the documents in the previous exercise were created successfully. 

From the command line:

<ol><li>List all the documents in the database.
<p><code>acurl https://$ACCOUNT.cloudant.com/query-demo/_all_docs</code></p>
</li>
<li>Verify that the results include the newly created documents. 
<p><i>Results:</i></p>
<p><pre>{"total_rows":5,"offset":0,"rows":[
    {"id":"doc1","key":"doc1","value":{"rev":"1-bf51eef712165a9999a52a97e2209ac0"}},
    {"id":"doc2","key":"doc2","value":{"rev":"1-57a08e644ca8c1bb8d8931240427162e"}},
    {"id":"doc3","key":"doc3","value":{"rev":"1-9c9f9b893fcdd1cbe09420bc4e62cc71"}},
    {"id":"doc4","key":"doc4","value":{"rev":"1-6aa4873443ddce569b27ab35d7bf78a2"}},
    {"id":"doc5","key":"doc5","value":{"rev":"1-d881d863052cd9681650773206c0d65a"}},
  ] 
}
</pre></p></li></ol>


From the Cloudant Dashboard:

<ol><li>Select <b>Databases</b> > `query-demo` database > <b>All Documents</b>.</li>
<li>Verify that all the documents are listed. </li>
</ol>

## Creating an index

In Cloudant, you use [search indexes](../api/search.html#search). You can specify a json or text type index. 
Creating a ["type=json"](../api/cloudant_query.html#creating-a-type-json-index) index reduces the load on
your environment and the size of your data set. You use this type of index if you are familar with your data and have a good idea  
what you want to find. 

If you choose a "type=text" index, 
all the documents and fields in your database are automatically indexed. As such, you can
search and retrieve information from any field. The time this takes varies based on the size of your data set. 

For this tutorial, we create a "type=json" index. If you want to create a ["type=text"](../api/cloudant_query.html#creating-a-type-text-index) index, 
change the value in the `type` field to `text`. 

To create an index:

<ol><li>From the command line, run this command to create an index.
<p><code>curl https://$ACCOUNT.cloudant.com/query-demo/_index -X POST -H "Content-Type: application/json" -d \@index.dat</p></code>
<p><i>Results:</i></p>
</p><pre>{"result":"created",
"id":"_design/752c7031f3eaee0f907d18e1424ad387459bfc1d",
"name":"query-index"}</pre></p>
</li>
<li>From the Cloudant Dashboard, create an index by following these steps:
<ol type=a><li>Click <b>+</b> > <b>Query Indexes</b>.</li>
<li>Paste the following sample JSON into the Index field.
<p><pre>
{
  "index": {
    "fields": [
         "firstname", 
         "lastname", 
         "location", 
         "age"
    ]
  },
  "name": "query-index",
  "type": "json"
}</pre></p></li>
<p>The index was created and is ready to query. </p>
</li></ol>


## Creating a query

When you create your [query](../api/cloudant_query.html#query) statement, you can narrow the data that you search for with [selector syntax](../api/cloudant_query.html#selector-syntax) and
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.

In a [selector expression](../api/cloudant_query.html#creating-selector-expressions), you specify at least one field and
its corresponding value. When the query runs, it uses these values to search the database for matches. The
selector is a JSON object. For this exercise, you use the selector expression that is described here.

For anything but the most simple query, add the JSON to a data file and run it from the command line.

### Running a query with a simple selector statement

To find a single document in the database, specify one piece of information, for example, a first name. 

From the command line:

1.  Copy the sample JSON into a data file named `query1.dat`.
```json
{
  "selector": {
        "firstname" : "Sally"            
        },
          "fields": ["firstname","lastname" ]        
}        
```    
{:codeblock}
2.  Run this command to query the database.

    <code>acurl https://$ACCOUNT.cloudant.com/query-demo/_find -X POST -H "Content-Type: application/json" -d \@query1.dat</code>

3.  See the query results.

    _Results:_
    ```json
    {
    "docs":
       [ {"firstname":"Sally","lastname":"Brown"} ]
     }
    ```


From the Cloudant Dashboard:

<ol><li>Click the <b>Query</b> tab..</li>
<li>Copy and paste the following selector statement into the Cloudant Query window and click <b>Run Query</b>.  
<p><pre>
{
  "selector": {
        "firstname" : "Sally"            
        }    
}   
</pre></p>
<p>The document with Sally Brown's information appears in the right pane. </p>
</li></ol>

### Running a query with two fields

Specify the documents that you want to find in the database by using the `selector` parameter. For example, everyone who lives in New York City, NY.

```json
{
    "selector": {
        "name": { "Brown" },
                { "location": "New York City, NY" }
        }                
    }        
```    
{:codeblock}

Specify the information that you want from each document that is a match. The values that are specified in 
the `fields` parameter determine what is returned. In this case, the results include the first 
and last name of everyone who meets the search criteria. The results are sorted by first name 
in ascending order based on the `sort` parameters values.

```json
    {
    "fields": ["firstname","lastname", "location"   ],
    "sort": [ { "firstname": "asc" }  ]
   }      
```  
{:codeblock}
  

From the command line:

1.  Copy the sample JSON into a data file named `query1.dat`.
```json
{
    "selector": {
        "name": { "Brown" },
                { "location": "New York City, NY" }
        }                
    },
  "fields": ["firstname", "lastname", "city" ],
  "sort": [ { "lastname": "asc" } ]  
}
```
2.  Run this command to query the database.

    <code>acurl https://$ACCOUNT.cloudant.com/query-demo/_find -X POST -H "Content-Type: application/json" -d \@query1.dat</code>

3.  See the query results.

    _Results:_
    ```json
    {"docs":[
    {"_id":"doc2","_rev":"1-2c5ee70689bb75af6f65b0335d1c92f4","firstname":"John","lastname":"Brown","age":21,"location":"New York City, NY"},
    {"_id":"doc3","_rev":"1-f6055e3e09f215c522d45189208a1bdf","firstname":"Greg","lastname":"Greene","age":35,"location":"San Diego, CA"},
    {"_id":"doc4","_rev":"1-9c7b5fdee4c69148cba291fa7ecbbed4","firstname":"Amanda","lastname":"Greene","age":44,"location":"Baton Rouge, LA"},
    {"_id":"doc5","_rev":"1-19f7ecbc68090bc7b3aa4e289e363576","firstname":"Lois","lastname":"Brown","age":33,"location":"Syracuse, NY"}
    ]}
        ```


From the Cloudant Dashboard:

<ol><li>Click the <b>Query</b> tab.</li>
<li>Copy and paste the following selector statement into the Cloudant Query window and click <b>Run Query</b>.  
<p><pre>
{
    "selector": {
        "name": { "Brown" },
                { "location": "New York City, NY" }
        }                
    },
  "fields": ["firstname", "lastname", "city" ],
  "sort": [ { "lastname": "asc" } ]  
}
</pre></p>
<p>The documents with John and Sally Brown's information appears in the right pane. </p>
</li></ol>

### Running a query with multiple operators

In this example, the $and, $text, and $gt are used to search for people with the last name Brown who are older than 20 years.
The combination of operators 

```json
{ "selector": {
    "$and": [   { "$eq": "Brown"  },
                { "$gt": 20 }   ]
   }, 
```   
{:codeblock}

Based on the values that are specified in the `field` parameter, the results include the first name, last name, and age sorted by first name in ascending order.

```json
  "fields": [ "firstname", "lastname", "age"],
  "sort": [  { "firstname": "asc" } ]           
```
{:codeblock}

From the command line:

1.  Copy this sample JSON to a file named `query1.dat`.
```json
{ "selector": {
    "$and": [   { "$eq": "Brown"  },
                { "$gt": 20 }   ]
     },
   "fields" : [ "firstname","lastname", "age" ],
   "sort" : [ { "firstname": "asc" } ]	
}
```
2. Run this query:

    <code>acurl https://$ACCOUNT.cloudant.com/query-demo/_find -X POST -H "Content-Type: application/json" -d \@query1.dat</code>

3.  See the query results.

    _Results:_
    ```{ "docs":[
    {"_id":"doc4","_rev":"1-9c7b5fdee4c69148cba291fa7ecbbed4","firstname":"Amanda","lastname":"Greene","age":44,"location":"Baton Rouge, LA"}
    ]}
    ```
    {:codeblock}

From the Cloudant Dashboard:

1.  Click the **Query** tab. 
2.  Copy and paste the JSON into the Cloudant Query window and click **Run Query**.  
```json
{ "selector": {
    "$and": [   { "$eq": "Brown"  },
                { "$gt": 20 }   ]
     },
   "fields" : [ "firstname","lastname", "age" ],
   "sort" : [ { "firstname": "asc" } ]	
}
```
The following documents match the query criteria. 
_Results:_
```json
Amanda Greene, 44
Greg Greene, 35
John Brown 21
Lois Brown, 33
```
{:codeblock}







