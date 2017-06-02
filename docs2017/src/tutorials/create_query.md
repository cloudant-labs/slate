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

To begin, you create the `rolodex` database and some JSON documents that contain the data for these exercises. Next, you create
a design document that  
contains information about how to build your indexes. You create two different types of indexes to demonstrate how an index  
can make it easier and faster to find data. Finally, you create and run queries against the database. 

While this tutorial focuses on creating a query with Cloudant Dashboard, you can use either Cloudant
Dashboard or the command line. Follow the links that are provided throughout this tutorial for information about using the command line.

You complete the following tasks during this tutorial:

1.  [Creating a database](create_query.html#creating-a-database-using-the-cloudant-dashboard)
2.  [Creating a design document](create_query.html#creating-a-design-document)
3.  [Creating an index](create_query.html#creating-an-index)
4.  [Creating a query](create_query.html#creating-a-query)


## Creating a database

You create the `rolodex` [database](../api/database.html#create). The database that the tutorial uses throughout this tutorial.

<ol><li>If you do not already have one, create an IBM Bluemix Cloudant account [here](https://console.ng.bluemix.net/registration/?target=%2Fcatalog%2Fservices%2Fcloudant-nosql-db%2F) and log in to it.</li>
<li>Log in to the Cloudant Dashboard.</li>
<li>Select the Databases tab.
<p>![Databases tab](../images/tabs.png)</p></li>
<li>Click <b>Create Database</b>. </li>
<li>Type <code>rolodex</code> and click <b>Create</b>.
<p>The <code>rolodex</code> database automatically opens.</p>
</li>
<li>(Optional) To create a database from the command line, run this command.
<p><code>curl https://$ACCOUNT.bluemix.cloudant.com/rolodex -X PUT</code></p>
<p>Results:
<code>{"ok":true}</code></p></li></ol>

### Listing all databases

To list all the databases for your account, run the following command.
```json
curl https://$ACCOUNT.cloudant.com/_all_dbs
```

Results: ```["rolodex"]```


### Deleting a database

To delete a database, run the following command:
```json
curl https://$ACCOUNT.cloudant.com/rolodex -X DELETE
```

Results: ```{"ok":true}```

## Creating documents in the database

The JSON documents contain the data that the queries we create use to extract information from the database.
<ol>
<li>From the <b>All Documents</b> tab, click <b>+</b> and select <b>New Doc</b>.
<p>The New Document window opens. </p></li>
<li>To create a JSON document, copy and paste the following sample text the new document.
<p><b>First sample document</b>:<br>
<code>{ "_id": "doc1",<br>
"firstname": "Sally",<br>
"lastname": "Brown",<br>
"age": 16,<br>
"city": "New York City",<br>
"state": "New York" <br>
}</code></p>
</li>
<li>Repeat the previous step and add the remaining documents to the database.
<p><b>Second sample document</b>:<br>
<code>{ "_id": "doc2",<br>
  "firstname": "John",<br>
  "lastname": "Brown",<br>
  "age": 21,<br>
  "city": "New York City",<br>
  "state": "New York"<br>
}</code><br></p>
<p><b>Third sample document:</b><br>
<code>{"_id": "doc3",<br>
"firstname": "Greg",<br>
"lastname": "Greene",<br>
"age": 35,<br>
"city": "San Diego",<br>
"state": "California"<br>
}
</code>
</p>
<p><b>Fourth sample document:</b><br>
<code>{"_id": "doc4",<br>
"firstname": "Amanda",<br>
"lastname": "Greene",<br>
"age": 44,<br>
"city": "Syracuse",<br>
"state": "New York"<br>
}</code>
</p>
<p><b>Fifth sample document:</b><br>
<code>{"_id": "doc5",<br>
"firstname": "Lois",<br>
"lastname": "Brown",<br>
"age": 33,<br>
"city": "Baton Rouge",<br>
"state": "Louisiana"<br>
}
</code>
</li>
<li>(Optional) To create documents from the command line, follow these steps.
<ol type=a><li>Create a data file called, <code>bulkcreate.dat</code>, by using the sample data that follows.
<p><code>
{
	"docs": [
{ 
"firstname": "Sally",
"lastname": "Brown",
"age": 16,
"city": "New York City",
"state": "New York", 
"_id": "doc1"
},
{ 
  "firstname": "John",
  "lastname": "Brown",
  "age": 21,
  "city": "New York City",
  "state": "New York",
  "_id": "doc2"
},
{
"firstname": "Greg",
"lastname": "Greene",
"age": 35,
"city": "San Diego",
"state": "California",
"_id": "doc3"
},
{
"firstname": "Amanda",
"lastname": "Greene",
"age": 44,
"city": "Syracuse",
"state": "New York",
"_id": "doc4"
},
{
"firstname": "Lois",
"lastname": "Brown",
"age": 33,
"city": "Baton Rouge",
"state": "Louisiana",
"_id": "doc5"
    }
 ]
}
</code></p></li>
<li>Run the following command for each data file.  
<code>curl https://$ACCOUNT.cloudant.com/rolodex-test -X POST -H "Content-Type: application/json" -d \@bulkcreate.dat</code>
<p>{"ok":true,"id":"51b07e035a22a5d420bf12cafa501627","rev":"1-876f5eb48824b9c4c94f7c834e62bd34"}</p>
<p><b>Note:</b> Notice that the '@' symbol, used to indicate that the data is included in a file, is identified by the supplied name.</p></li>
</ol></li></ol>
<p>The `rolodex` database was created and populated with five JSON documents. </p>

### Listing all the documents in the database

Check the database and verify that all the documents in the previous exercise were created successfully. 

To list all the documents in the database, run the following command:

curl https://$ACCOUNT.cloudant.com/rolodex/_all_docs

**Results:**
```
{"total_rows":5,"offset":0,"rows":[
{"id":"doc1","key":"doc1","value":{"rev":"1-bf51eef712165a9999a52a97e2209ac0"}},
{"id":"doc2","key":"doc2","value":{"rev":"1-57a08e644ca8c1bb8d8931240427162e"}},
{"id":"doc3","key":"doc3","value":{"rev":"1-9c9f9b893fcdd1cbe09420bc4e62cc71"}},
{"id":"doc4","key":"doc4","value":{"rev":"1-6aa4873443ddce569b27ab35d7bf78a2"}},
{"id":"doc5","key":"doc5","value":{"rev":"1-d881d863052cd9681650773206c0d65a"}},
]}
```


## Creating a design document

[Design documents](../api/design_documents.html#design-documents) contain instructions about how views
and indexes must be built. When you change a design document, the index is overwritten and
re-created from scratch.

Indexes and views have the same purpose—to improve processing and return time for database queries. However, the mechanics are different.
A view selectively filters documents. In Cloudant, views are written using Javascript functions.
You define a view in the `view` field inside a design
document. When you run a query using your view, Cloudant applies the Javascript function to all the documents in the database.

Cloudant search indexes are also defined in design documents. Each index is defined by an index function that determines the data to index
and store. These indexes use [Lucene Query
Parser Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview)
to query databases.

To create a design document:

<ol><li>From the <b>Design Documents</b> tab, click <b>Create</b> > <b>New Doc</b>.</li>
<li>Replace the <code>_id</code> value with <code>rolodex-index-design-doc</code> as seen in the example.
<code>
{
  "_id": "rolodex-index-design-doc"
}
</code>
<li>Click <b>Create Document</b>.
<p>The <code>rolodex-index-design-doc</code> design document is created.</p></li>
<li>(Optional) Create a design document from the command line.
<p><code>curl https://$ACCOUNT.cloudant.com/rolodex -X POST -H "Content-Type: application/json" -d "{ \"_id\": \"doc1410\", \"_id\": \" rolodex-index-design-doc\" }"</code></p>
<p><b>Results:</b></p>
<p><code>{"ok":true,"id":" rolodex-index-design-doc","rev":"1-967a00dff5e02add41819138abb3284d"}</code><p>
</li></ol>

## Creating an index

In Cloudant, you build [indexes](../api/using_views.html#indexes) by using
[view (MapReduce)](../api/creating_views.html#views-mapreduce-) and [search indexes](../api/search.html#search).

### Creating a "type=json" index

Creating a ["type=json"](../api/cloudant_query.html#creating-a-type-json-index) index reduces the load on
your environment and the size of your data set.

To create a "type=json" index:

<ol><li>Select <b>Design Documents</b> tab.</li>
<li>Click <b>+</b> > <b>New Search Index</b>.</li>
<li>Select <b>New document</b> from the Save to design document drop-down menu.</li>
<li>Type <code>rolodex-index-design-doc</code> in the <code>_design</code> field.</li>
<li>Type <code>JSONsearch</code> in the Index name field.</li>
<li>Replace the text in the Search index function field with the text in the sample.
<p><code>
{    
	 "index": {       
            "fields": ["firstname", "lastname", "city", "age"]  
                    },
	 "name": "JSONindex",
	 "type": "json"            
    } 
</code></p>
</li>
<li>Accept the remaining default options.</li>
<li>Click <b>Create Document and Build Index</b>.</li>
<li>(Optional) Create an index from the command line.
<code>
<p>curl https://$ACCOUNT.cloudant.com/rolodex-test/_index -X POST -H "Content-Type: application/json" -d \@JSONsearch.dat</p></code>
<p><code>{"result":"created","id":"_design/d3fd6f7b1fa434cbbb058a7e377d51ec0d26cee9","name":"d3fd6f7b1fa434cbbb058a7e377d51ec0d26cee9"}</code></p>
</li></ol>

The `JSONsearch` was created. See the index by expanding `rolodex=index-design-doc` > **Search Indexes** or run `curl https://$ACCOUNT.cloudant.com/rolodex/_index`
from the command line.

### Creating a "type=text" index

When you create a ["type=text"](../api/cloudant_query.html#creating-a-type-text-index) index, all the documents and fields in your database
are automatically indexed. As such, you can
search and retrieve information from any field.  

To create the index:

<ol><li>Select <b>Design Documents</b> tab.</li>
<li>Click <b>+</b> and click <b>New Search Index</b>.</li>
<li>Select <b>New document</b> from the Save to design document drop-down menu.</li>
<li>Replace <code>newDesignDoc</code> with <code>rolodex-index-design-doc</code>.</li>
<li>Type <code>TEXTsearch</code> in the Index name field.</li>
<li>Replace the text in the Search index function field with the text below.
<p><code>
{
        "index": {
        "fields": [ "firstname", "lastname", "age" ]
        }
   }</code></p>
</li>
<li>Accept the remaining options.</li>
<li>Click <b>Create Document and Build Index</b>.</li>
<li>(Optional) Create an index from the command line.
<p><code>curl https://dbsgrl.cloudant.com/rolodex-test/_index -X POST -H "Content-Type: application/json" -d \@TEXTsearch.dat</code></p>
<p>Results:</p>
<code>{"result":"created","id":"_design/d3fd6f7b1fa434cbbb058a7e377d51ec0d26cee9","name":"d3fd6f7b1fa434cbbb058a7e377d51ec0d26cee9"}</code>
</li></ol>

The `TEXTsearch` was created. See the index by expanding `rolodex=index-design-doc` > **Search Indexes** or run `curl https://$ACCOUNT.cloudant.com/rolodex/_index`
from the command line.

### Listing Cloudant Query indexes

You can see all the indexes in the `rolodex` database from the Cloudant Dashboard or
[list](../api/cloudant_query.html#list-all-cloudant-query-indexes) them from the command line.

1.  Expand `rolodex-index-design-doc` under Design Documents tab.
2.  Expand **Search Indexes**.
3.	(Optional) Search for an index from the command line.
```json
curl https://$ACCOUNT.cloudant.com/rolodex/_index
```
**Results:**
```json


```

The two indexes you created appear. You can edit, clone, or delete indexes here. When you select an index, you can use it to query the database.


## Creating a query

When you create your [query](../api/cloudant_query.html#query) statement, you can narrow the data that you search with [selector syntax](../api/cloudant_query.html#selector-syntax) and
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.


### Querying the database with `selector` syntax

In a [selector expression](../api/cloudant_query.html#creating-selector-expressions), you specify at least one field and
its corresponding value. When the query runs, it uses these values to search the database for matches. The
selector is a JSON object. For this exercise, you use the selector expression that is described here.

Specify the documents that you want to find in the database in the `selector` parameter. For example, everyone who lives in New York City, New York.

```json
{
  "selector": {
        "city" : "New York City",  
        "state": "New York"
    }
```    
{:codeblock}

Specify how you want the information that is returned in the `fields` parameter. In this case, the first and last
name of everyone in who meets the search criteria. The results are sorted by first name in ascending order based on the `sort` parameters values.

```json
{
"fields": ["firstname","lastname"  
    ],
  "sort": [
    {
      "firstname": "asc"
    }  
```  
{:codeblock}

To run the query:

<ol><li>Click the <code>JSONsearch</code> index that you created earlier by expanding <code>rolodex-index-design-doc</code> > <b>Search Indexes</b> > <b>JSONsearch</b>.</li>
<li>Copy and paste the following selector statement to the Query field and click <b>Query</b>.  
<p><code>
{
  "selector": {
        "city" : "New York City",    
       "state": "New York",      
       "firstname": {"$gt": null}
      },    
   "fields": ["firstname","lastname", "city"
      ],
   "sort": [ { "firstname": "asc" } ],
   “use_index”: [ “JSONsearch”]		
}
</code></p>
<p><b>Example results returned from search:</b></p>
<p><code>{
"docs":
   [
    {"firstname":"John","lastname":"Brown","city":"New York City"},
    {"firstname":"Sally","lastname":"Brown","city":"New York City"}
   ]
 }
</code></p></li>

<li>(Optional) Run a query from the command line.
<p><code>curl https://dbsgrl.cloudant.com/rolodex-test/_find -X POST -H "Content-Type: application/json" -d \@query1.dat</code></p>
</li>

### Querying the database with operators

Using operators in your query provides a more granular search. Operators are described
[here](../api/cloudant_query.html#query-parameters). In this example, the operators `$and`, `$text`,
and `$gt` define the search parameters. These operators perform the following functions:

    *   $and    Finds a match when all the selectors in the array match.
    *   $text   Matches any word or string in the document. It is not case-sensitive. The $text operator is only available with the index "type=text". However, searching for field names is an invalid use of the $text operator.
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
  }
```   
{:codeblock}

Based on the values in the `field` parameter, the results include the first name, last name, and age sorted by first name in ascending order.

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
{:codeblock}

To run the query:

1.  Click the `TEXTsearch` index that you created earlier by expanding `rolodex-index-design-doc` > **Search Indexes** > **TEXTsearch**.
2.  Copy and paste the example selector statement into the Query field and click **Query**.  
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
{:codeblock}

_Example results returned from search:_

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
{:codeblock}
