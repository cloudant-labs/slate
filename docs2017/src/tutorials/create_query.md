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

To begin, you create the `rolodex` database, some JSON documents that contain the data for these exercises, and a design document that contains information about how to build your index. Next, you create an index and run queries against it. 

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

In this section, you create the `rolodex` [database](../api/database.html#create) which is the database that we use in this tutorial.

From the command line:

1.  Create a database by running this command.<br>

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex -X PUT</code>

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
<li>Enter <code>rolodex</code> and click <b>Create</b>.
<p>The <code>rolodex</code> database automatically opens.</p>
</li>
</ol>

### Listing databases

Verify that the `rolodex` database was created correctly. 

From the command line:


1.  Show the databases by running this command.

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/_all_dbs</code>

2.  See the `rolodex` database and any other databases that are associated with your account.   

    *Results:*
    ```json
    ["rolodex"]
    ```

From the Cloudant Dashboard:

1.  Click the **Databases** tab.
2.  See the `rolodex` database in the list on **Your Databases** tab.



### Deleting a database

If you decide to delete the database, for example, if you made a mistake, you can delete the database and start again. 

From the command line:

1.  Delete the database by running this command.

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex -X DELETE</code>

2.  See the results to verify the `rolodex` database was deleted. 

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

The JSON documents that you create here contains the data you use to query the `rolodex` database in later exercises. 

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
		"city": "New York City",
		"state": "New York"	
    },
  { 
		"_id": "doc2",
	  	"firstname": "John",
	    "lastname": "Brown",
	    "age": 21,
        "city": "New York City",
        "state": "New York"
  },
   {
		"_id": "doc3",
		"firstname": "Greg",
		"lastname": "Greene",
		"age": 35,
		"city": "San Diego",
		"state": "California"

   },
  {
		"_id": "doc4",
		"firstname": "Amanda",
		"lastname": "Greene",
		"age": 44,
		"city": "Syracuse",
		"state": "New York"
  },
   {
		"_id": "doc5",
		"firstname": "Lois",
		"lastname": "Brown",
		"age": 33,
		"city": "Baton Rouge",
		"state": "Louisiana"
   }
  ]
}</pre></p></li>
<li>Run this command to create the documents. 
<p>The following POST command creates five individual documents at the same time. </p>
<p><code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_bulk_docs -X POST -H "Content-Type: application/json" -d \@bulkcreate.dat</code></p>
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
        "city": "New York City",
        "state": "New York", 
        "_id": "doc1"
     }</pre></p>

</li>
<li>Repeat the previous step and add the remaining documents to the database.
<p><i>Second sample document</i>:<br>
<pre>{ 
        "firstname": "John",
        "lastname": "Brown",
        "age": 21,
        "city": "New York City",
        "state": "New York",
        "_id": "doc2"
   }</pre></p>
<p><i>Third sample document:</i><br>
<pre> {
        "firstname": "Greg",
        "lastname": "Greene",
        "age": 35,
        "city": "San Diego",
        "state": "California",
        "_id": "doc3"
     }
</pre>
</p>
<p><i>Fourth sample document:</i><br>
<pre>{
        "firstname": "Amanda",
        "lastname": "Greene",
        "age": 44,
        "city": "Syracuse",
        "state": "New York",
        "_id": "doc4"
      }</pre>
</p>
<p><i>Fifth sample document:</i><br>
<pre>{
        "firstname": "Lois",
        "lastname": "Brown",
        "age": 33,
        "city": "Baton Rouge",
        "state": "Louisiana",
        "_id": "doc5"
     }
</pre>
</li>
<p>The `rolodex` database was created and populated with five JSON documents. </p></li></ol>

### Listing the documents in the database

Check the database to verify that all the documents in the previous exercise were created successfully. 

From the command line:

<ol><li>List all the documents in the database.
<p><code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_all_docs</code></p>
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

<ol><li>Select <b>Databases</b> > `rolodex` database > <b>All Documents</b>.</li>
<li>Verify that all the documents are listed. </li>
</ol>


## Creating a design document

A [design document](../api/design_documents.html#design-documents) enables you to 
create a JavaScript formula to speed up an index. It also contains instructions about how views
and indexes must be built. When you change a design document, the index is overwritten and
re-created from scratch.

Indexes and views have the same purpose—to improve processing and return time for database queries. However, the mechanics are different.
A view selectively filters documents. In Cloudant, views are written that use JavaScript functions.
You define a view in the `view` field inside a design
document. When you run a query that uses your view, Cloudant applies the JavaScript function to all the documents in the database.

Cloudant search indexes are also defined in design documents. Each index is defined by an index function that determines the data to index
and store. These indexes use [Lucene Query
Parser Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview)
to query databases.

From the command line:

Before you start this exercise, you must <a href="#Create a design document">create a design document in Cloudant Dashboard</a>.

1.  From Cloudant Dashboard, click the **All Documents** tab and edit `_design/rolodex-design-doc` design document.
2.  Copy the JSON and use it to create a data file named `designdoc.dat`.
3.  To create the design document and index, run this command.

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_index -X POST -H "Content-Type: application/json" -d \@designdoc.dat</code>

    *Results:*
    ```json
    {"ok":true,"id":" rolodex-index-design-doc","rev":"1-967a00dff5e02add41819138abb3284d"}
    ```

<a name="Create a design document">From the Cloudant Dashboard</a>:

<ol>
<li>Select <b>Design Documents</b> and click <b>Create</b> > <b>New Search Index</b>.</li>
<li>Enter <code>rolodex-design-doc</code> in the <code>_design</code> field.</li>
<li>Enter <code>rolodex-index</code> in the Index name field.</li>
<li>Accept the default selections on the rest of the page. </li>
<li>Click <b>Create Document and Build Index</b>.
<p>The <code>rolodex-design-doc</code> design document and the `rolodex-index` index appear under the Design Documents tab.</p></li>
<li>Click the **All Documents** tab and edit the <code>_design/rolodex-design-doc</code> design document.</li>
<li>Copy the following sample `rolodexindex` JSON and replace the text in the Search index function window. 
<p><i>Sample `rolodexindex` JSON</i></p>
<p><pre>
    {
        "index": {       
           "fields": ["firstname", "lastname", "city", "age"]  
             },
	    "name": "rolodexindex"            
 } 
</pre></p></li>
<li>Accept the default selections for the rest of the page. </li>
<li>Click <b>Save Document and Build Index</b>.
<p>You created a design document and added the index information to it. </p></li>
</ol>



### Listing a Cloudant Query index

Verify that the `rolodex-index` is [listed](../api/cloudant_query.html#list-all-cloudant-query-indexes) in the `rolodex` database.

From the command line:

1.  Search for an index by running this command.  

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_index</code>

2.  See the results to verify that the index was created. 

    <pre>
    <i>Results:</i>
    
    {
        "total_rows":1,
            "indexes":
                [{"ddoc":null,
                "name":"_all_docs",
                "type":"special",
                "def":{"fields":[{"_id":"asc"}]
          }
        }
      ]
    }
    </pre>

From the Cloudant Dashboard:

<ol><li>Select <b>Databases</b> > <b>Design Documents</b> to expand <code>rolodex-index-design-doc</code>.</li>
<li>Expand <b>Search Indexes</b>.
<p>You can see the JSONindex you created. You can edit, clone, or delete indexes here. When you select an index, you can use it to query the database.</p></li>
</ol>




## Creating a query

When you create your [query](../api/cloudant_query.html#query) statement, you can narrow the data that you search with [selector syntax](../api/cloudant_query.html#selector-syntax) and
[implicit](../api/cloudant_query.html#implicit-operators) or [explicit](../api/cloudant_query.html#explicit-operators) operators.

In a [selector expression](../api/cloudant_query.html#creating-selector-expressions), you specify at least one field and
its corresponding value. When the query runs, it uses these values to search the database for matches. The
selector is a JSON object. For this exercise, you use the selector expression that is described here.

For anything but the most simple query, add the JSON to a data file and run it from the command line.

### Querying the `rolodex` database by using a selector statement

Specify the documents that you want to find in the database by using the `selector` parameter. For example, everyone who lives in New York City, New York.

```json
{
  "selector": {
        "city" : "New York City",  
        "state": "New York",
        "firstname": {"$gt": null}        
    }
```    
{:codeblock}

Specify the information that you want from each document that is a match. The values that are specified in 
the `fields` parameter determine what is returned. In this case, the results include the first 
and last name of everyone who meets the search criteria. The results are sorted by first name 
in ascending order based on the `sort` parameters values.

```json
    {
    "fields": ["firstname","lastname"   ],
    "sort": [ { "firstname": "asc" }  ]
   }      
```  
{:codeblock}
  

From the command line:

1.  Copy the sample JSON into a data file named `query1.dat`. 
2.  Run this command to query the database.

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_find -X POST -H "Content-Type: application/json" -d \@query1.dat</code>

3.  See the query results.

    _Results:_
    ```json
    {
    "docs":
       [
        {"firstname":"John","lastname":"Brown","city":"New York City"},
        {"firstname":"Sally","lastname":"Brown","city":"New York City"}
       ]
     }
    ```


From the Cloudant Dashboard:

<ol><li>Click the <code>JSONindex</code> index that you created earlier by expanding <code>rolodex-index-design-doc</code> > <b>Search Indexes</b> > <b>JSONindex</b>.</li>
<li>Copy and paste the following selector statement to the Query field and click <b>Query</b>.  
<p><pre>
{
  "selector": {
        "city": "New York City",    
       "state": "New York",      
       "firstname": {"$gt": null}
     },    
        "fields": ["firstname","lastname", "city" ],
        "sort": [ { "firstname": "asc" } ],
        “use_index”: [ “JSONindex”]		
}
</pre></p>
<p><i>Results:</i></p>
<p><pre>{
"docs":
   [
    {"firstname":"John","lastname":"Brown","city":"New York City"},
    {"firstname":"Sally","lastname":"Brown","city":"New York City"}
   ]
 }
</pre></p></li></ol>



### Querying the `rolodex` database by using operators

This example searches the database for people with the last name Brown who are older than 20 years.

```json
    {"selector": {
        "$and": [   { "$text": "Brown"  },
                    { "$gt": 20 }   ]
        }
```   
{:codeblock}

Based on the values that are specified in the `field` parameter, the results include the first name, last name, and age sorted by first name in ascending order.

```json
  "fields": [ "firstname", "lastname", "age"],
  "sort": [  { "age": "asc" } ]           
```
{:codeblock}

From the command line:

1. Run this query:

    <code>acurl https://$ACCOUNT.bluemix.cloudant.com/rolodex/_find -X POST -H "Content-Type: application/json" -d \@query2.dat</code>

2.  See the query results.

    _Results:_
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

From the Cloudant Dashboard:

1.  Click the `JSONindex` index that you created earlier by expanding `rolodex-index-design-doc` > **Search Indexes** > **JSONindex**.
2.  Copy and paste the JSON into the Query field and click **Query**.  
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
_Results:_
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
