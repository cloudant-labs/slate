## Design Documents

Instead of storing data in a document,
you might also have special documents that store other content, such as functions.
The special documents are called "design documents".

Design documents are [documents](document.html) that have an `_id` beginning with `_design/`. They can be read and updated in the same way as any other document in the database.
Cloudant reads specific fields and values of design documents as functions.
Design documents are used to [build indexes](#indexes), [validate updates](#update-validators), and [format query results](#list-functions).

### Creating or updating a design document

-   **Method**: `PUT /$DATABASE/_design/DESIGN_DOC`
-   **Request**: JSON of the design document information
-   **Response**: JSON status
-   **Roles permitted**: \_admin

To create a design document, upload it to the specified database.

In these examples,
`$VARIABLES` might refer to standard and design documents.
To distinguish between them,
standard documents have an `_id` indicated by `$DOCUMENT_ID`,
while design documents have an `_id` indicated by `$DESIGN_ID`.

<aside class="warning" role="complementary" aria-label="designupdateaffectsindexes">If a design document is updated,
Cloudant deletes the indexes from the previous version,
and recreates the index from scratch.
If you need to make changes to a design document for a larger database,
have a look at the [Design Document Management Guide](design_document_management.html#managing-changes-to-a-design-document).</aside>

The structure of design document is as follows:

-   **\_id**: Design Document ID
-   **\_rev**: Design Document Revision
-   **views (optional)**: an object describing MapReduce views
    -   **viewname** (one for each view): View Definition
        -   **map**: Map Function for the view
        -   **reduce (optional)**: Reduce Function for the view
        -   **dbcopy (optional)**: Database name to store view results in
-   **indexes (optional)**: an object describing search indexes
    -   **index name** (one for each index): Index definition
        -   **analyzer**: Object describing the analyzer to be used or an object with the following fields:
            -   **name**: Name of the analyzer. Valid values are `standard`, `email`, `keyword`, `simple`, `whitespace`, `classic`, `perfield`.
            -   **stopwords (optional)**: An array of stop words. Stop words are words that should not be indexed. If this array is specified, it overrides the default list of stop words. The default list of stop words depends on the analyzer. The list of stop words for the standard analyzer is: "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with".
            -   **default (for the per field analyzer)**: default language to use if there is no language specified for the field
            -   **fields (for the per field analyzer)**: An object specifying which language to use to analyze each field of the index. Field names in the object correspond to field names in the index (i.e. the first parameter of the index function). The values of the fields are the languages to be used, e.g. "english".
        -   **index**: Function that handles the indexing
-   **shows (optional)**: Show functions
    -   **function name** (one for each function): Function definition
-   **lists (optional)**: List functions
    -   **function name** (one for each function): Function definition

### Copying a Design Document

You can copy the latest version of a design document to a new document
by specifying the base document and target document.
The copy is requested using the `COPY` HTTP request.

<aside class="warning" role="complementary" aria-label="copynonstandard">`COPY` is a non-standard HTTP command.</aside>

<div></div>

>  Example command to copy a design document:

```http
COPY /recipes/_design/recipes HTTP/1.1
Content-Type: application/json
Destination: /recipes/_design/recipelist
```

```shell
curl "https://$ACCOUNT.cloudant.com/recipes/_design/recipes" \
     -X COPY \
     -H 'Content-Type: application/json' \
     -H 'Destination: /recipes/_design/recipelist'
```

> Example response to copy command:

```json
{
  "id": "recipes/_design/recipelist",
  "rev": "1-9c65296036141e575d32ba9c034dd3ee"
}
```

An example request to copy the design document `recipes` to the new
design document `recipelist` produces a response containing the ID and revision of
the new document.

<aside class="notice" role="complementary" aria-label="noautoreconstruct">Copying a design document does not automatically reconstruct the view
indexes. Like other views, these are recreated the first
time the new view is accessed.</aside>

<div></div>

#### The structure of the copy command

-	 **Method**: `COPY /$DATABASE/_design/design-doc`
-	 **Request**: None
-	 **Response**: JSON describing the new document and revision
-	 **Roles permitted**: \_writer
-	 **Query Arguments**:
    -	**Argument**: `rev`
        -	**Description**:  Revision to copy from
        -	**Optional**: yes
        -	**Type**: string
-	**HTTP Headers**
    -	**Header**: `Destination`
        -	**Description**: Destination document (and optional revision)
        -	**Optional**: no

The source design document is specified on the request line, with the
`Destination` HTTP Header of the request specifying the target
document.

<div></div>

#### Copying from a specific revision

>  Example command to copy a specific revision of the design document:

```http
COPY /recipes/_design/recipes?rev=1-e23b9e942c19e9fb10ff1fde2e50e0f5 HTTP/1.1
Content-Type: application/json
Destination: recipes/_design/recipelist
```

```shell
curl "https://$ACCOUNT.cloudant.com/recipes/_design/recipes?rev=1-e23b9e942c19e9fb10ff1fde2e50e0f5" \
     -X COPY \
     -H 'Content-Type: application/json' \
     -H 'Destination: /recipes/_design/recipelist'
```

To copy *from* a specific version, add the `rev` argument to the query
string.

The new design document is created using the specified revision of
the source document.

<div></div>

#### Copying to an existing design document

>  Example command to overwrite an existing copy of the design document:

```http
COPY /recipes/_design/recipes
Content-Type: application/json
Destination: recipes/_design/recipelist?rev=1-9c65296036141e575d32ba9c034dd3ee
```

```shell
curl "https://$ACCOUNT.cloudant.com/recipes/_design/recipes" \
     -X COPY \
     -H 'Content-Type: application/json' \
     -H 'Destination: /recipes/_design/recipelist?rev=1-9c65296036141e575d32ba9c034dd3ee'
```

> Example response to overwriting successfully an existing design document:

```json
{
    "id" : "recipes/_design/recipes"
    "rev" : "2-55b6a1b251902a2c249b667dab1c6692",
}
```

To copy to an existing document, specify the current revision
string for the target document, using the `rev` parameter to the
``Destination`` HTTP Header string.

The return value is the new revision of the copied document.

### Deleting a design document

> Example command to delete a design document:

```http
DELETE /recipes/_design/recipes?rev=2-ac58d589b37d01c00f45a4418c5a15a8 HTTP/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/recipes/_design/recipes?rev=2-ac58d589b37d01c00f45a4418c5a15a8" \
     -X DELETE
```

> Example response, containing the delete document ID and revision:

```json
{
  "id": "recipe/_design/recipes",
  "ok": true,
  "rev": "3-7a05370bff53186cb5d403f861aca154"
}
```

You can delete an existing design document. Deleting a design document also
deletes all of the associated view indexes, and recovers the
corresponding space on disk for the indexes in question.

To delete successfully, you must specify the current revision of the design document
using the `rev` query argument.

<div></div>

#### The structure of the delete command

-	 **Method**: `DELETE /db/_design/design-doc`
-	 **Request**:  None
-	 **Response**:  JSON of deleted design document
-	 **Roles permitted**: _writer
-	 **Query Arguments**:
    -	**Argument**: `rev`
        -	**Description**: Current revision of the document for validation
        -	**Optional**: yes
        -	**Type**: string
-	**HTTP Headers**
    -	**Header**: `If-Match`
        -	**Description**: Current revision of the document for validation
        -	**Optional**: yes

### Views

An important use of design documents is for creating views. These are discussed in more detail [here](creating_views.html).

### Rewrite rules

> Example rewrite rules:

```json
"rewrites": [
  {
    "from": "/",
    "to": "index.html",
    "method": "GET",
    "query": {}
  },
  {
    "from": "/foo/:var",
    "to": "/foo",
    "method": "GET",
    "query": {"v": "var"}
  }
]
```

A design document can contain rules for URL rewriting, by using an array in the `rewrites` field.
Requests that match the rewrite rules must have a URL path that starts with `/$DATABASE/_design/doc/_rewrite`.

Each rule is a JSON object with 4 fields:

<table>
<colgroup>
<col width="20%" />
<col width="80%" />
</colgroup>
<thead>
<tr>
<th>Field</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>from</code></td>
<td>A path relative to <code>/$DATABASE/_design/doc/_rewrite</code>, used to match URLs to rewrite rules. Path elements that start with a <code>:</code> are treated as variables and match any string that does not contain a <code>/</code>. A <code>*</code> can only appear at the end of the string, and matches any string - including slashes.</td>
</tr>
<tr>
<td><code>to</code></td>
<td>The path (relative to <code>/$DATABASE/_design/doc/</code> and not including the query part of the URL) that is the result of the rewriting step. Variables captured in <code>from</code> can be used in <code>to</code>. <code>*</code> can also be used and contains everything captured by the pattern in <code>from</code>.</td>
</tr>
<tr>
<td><code>method</code></td>
<td>The HTTP method that should be matched on.</td>
</tr>
<tr>
<td><code>query</code></td>
<td>The query part of the resulting URL. This is a JSON object containing the key/value pairs of the query.</td>
</tr>
</tbody>
</table>

#### Example rewrite rules

<table>
<colgroup>
<col width="30%" />
<col width="30%" />
<col width="30%" />
<col width="10%" />
</colgroup>
<thead>
<tr>
<th>Rule</th>
<th>URL</th>
<th>Rewrite to</th>
<th>Tokens</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>{"from": "/a/b", "to": "/some/"}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a/b?k=v</code></td>
<td><code>/$DATABASE/_design/doc/some?k=v</code></td>
<td>k = v</td>
</tr>
<tr>
<td><code>{"from": "/a/b", "to": "/some/:var"}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a/b</code></td>
<td><code>/$DATABASE/_design/doc/some/b?var=b</code></td>
<td>var = b</td>
</tr>
<tr>
<td><code>{"from": "/a", "to": "/some/*"}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a</code></td>
<td><code>/$DATABASE/_design/doc/some</code></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><code>{"from": "/a/*", "to": "/some/*}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a/b/c</code></td>
<td><code>/$DATABASE/_design/doc/some/b/c</code></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><code>{"from": "/a", "to": "/some/*"}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a</code></td>
<td><code>/$DATABASE/_design/doc/some</code></td>
<td>&nbsp;</td>
</tr>
<tr>
<td><code>{"from": "/a/:foo/*","to": "/some/:foo/*"}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a/b/c</code></td>
<td><code>/$DATABASE/_design/doc/some/b/c?foo=b</code></td>
<td>foo = b</td>
</tr>
<tr>
<td><code>{"from": "/a/:foo", "to": "/some", "query": { "k": ":foo" }}</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a/b</code></td>
<td><code>/$DATABASE/_design/doc/some/?k=b&foo=b</code></td>
<td>foo =:= b</td>
</tr>
<tr>
<td><code>{"from": "/a", "to": "/some/:foo" }</code></td>
<td><code>/$DATABASE/_design/doc/_rewrite/a?foo=b</code></td>
<td><code>/$DATABASE/_design/doc/some/b&foo=b</code></td>
<td>foo = b</td>
</tr>
</tbody>
</table>

### Indexes

All queries operate on pre-defined indexes defined in design documents.
These indexes are:

* [Search](search.html)
* [MapReduce](creating_views.html)

<!-- * [Geo](#geo) -->

For example,
to create a design document used for searching,
you must ensure that two conditions are true:

1. You have identified the document as a design document by having an `_id` starting with `_design/`.
2. A [search index](search.html) has been created within the document by [updating](document.html#update) the document with the appropriate field or by [creating](document.html#create) a new document containing the search index.

As soon as the search index design document exists and the index has been built, you can make queries using it.

For more information about search indexing,
refer to the [search](search.html) section of this documentation.

#### General notes on functions in design documents

Functions in design documents are run on multiple nodes for each document and might be run several times. To avoid inconsistencies, they need to be idempotent, meaning they need to behave identically when run multiple times and/or on different nodes. In particular, you should avoid using functions that generate random numbers or return the current time.


### List Functions

> Example design document referencing a list function:

```json
{
  "_id": "_design/list_example",
  "lists": {
    "FUNCTION_NAME": "function (head, req) { ... }"
  }
}
```

> Example list function:

```
function (head, req) {
  // specify our headers
  start({
    headers: {
      "Content-Type": 'text/html'
    }
  });
  // send the respond, line by line
  send('<html><body><table>');
  send('<tr><th>ID</th><th>Key</th><th>Value</th></tr>')
  while(row = getRow()){
    send(''.concat(
      '<tr>',
      '<td>' + toJSON(row.id) + '</td>',
      '<td>' + toJSON(row.key) + '</td>',
      '<td>' + toJSON(row.value) + '</td>',
      '</tr>'
    ));
  }
  send('</table></body></html>');
}
```

> Example query:

```http
GET /$DATABASE/$DESIGN_ID/_list/$LIST_FUNCTION/$MAPREDUCE_INDEX HTTP/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_list/$LIST_FUNCTION/$MAPREDUCE_INDEX" \
```

```javascript
var nano = require('nano');
var db = account.use($DATABASE);

db.view_with_list($DESIGN_ID, $MAPREDUCE_INDEX, $LIST_FUNCTION, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Use list functions to customize the format of [MapReduce](creating_views.html#using-views) query results.
They are used when you want to access Cloudant directly from a browser, and need data to be returned in a different format, such as HTML.
You can add any query parameters to the request that would normally be used for a view request. Instead of using a MapReduce index, you can also use `_all_docs`.

<aside class="warning" role="complementary" aria-label="listresultnotstored">The result of a list function is not stored. This means that the function is executed every time a request is made.
As a consequence, using map-reduce functions might be more efficient.
For web and mobile applications, consider whether any computations done in a list function would be better placed in the application tier.</aside>

List functions require two arguments: `head` and `req`.

When you define a list function,
you use it by making a `GET` request to `https://<account>.cloudant.com/<databases>/<design_id>/_list/<list_function>/<mapreduce_index>`.
In this request:

* `<list_function>` is the name of list function you defined.
* `<mapreduce_index>` is the name of the index providing the query results you want to format.

The other parameters are the same query parameters described [here](cloudant_query.html#query-parameters).

#### head

Field | Description
------|-------------
total_rows | Number of documents in the view
offset | Offset where the document list started

#### req

Field | Description
------|-------------
body | Request body data as string. If the request method is `GET` this field contains the value "undefined". If the method is `DELETE` or `HEAD` the value is "" (empty string).
cookie | Cookies object.
form | Form data object. Contains the decoded body as key-value pairs if the Content-Type header was `application/x-www-form-urlencoded`.
headers | Request headers object.
id | Requested document id string if it was specified or null otherwise.
info | Database information
method | Request method as string or array. String value is a method as one of: `HEAD`, `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`, and `TRACE`. Otherwise it will be represented as an array of char codes.
path | List of requested path sections.
peer | Request source IP address.
query | URL query parameters object. Note that multiple keys are not supported and the last key value suppresses others.
requested_path | List of actual requested path section.
raw_path | Raw requested path string.
secObj | The database's [security object](authorization.html#viewing-permissions)
userCtx | Context about the currently authenticated user, specifically their `name` and `roles` within the current database.
uuid | A generated UUID

### Show Functions

> Design doc with a show function:

```json
{
  "_id": "_design/show_example",
  "shows": {
    "FUNCTION_NAME": "function (doc, req) { ... }"
  }
}
```

> Example show function:

```
function (doc, req) {
  if (doc) {
    return "Hello from " + doc._id + "!";
  } else {
    return "Hello, world!";
  }
}
```

> Example query:

```http
GET /<database>/<design_id>/_show/<show_function>/<document_id http>/1.1
Host: <account>.cloudant.com
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_show/$SHOW_FUNCTION/$DOCUMENT_ID \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.show($DESIGN_ID, $SHOW_FUNCTION, $DOCUMENT_ID, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

Show functions are similar to [list functions](#list-functions) but are used to format individual documents.
They are used when you want to access Cloudant directly from a browser, and need data to be returned in a different format, such as HTML.

<aside class="warning" role="complementary" aria-label="showresultnotstored">The result of a show function is not stored. This means that the function is executed every time a request is made.
As a consequence, using map functions might be more efficient.
For web and mobile applications, consider whether any computations done in a show function would be better placed in the application tier.</aside>

Show functions receive two arguments: `doc`, and [req](#req). `doc` is the document requested by the show function.

When you have defined a show function, you query it with a `GET` request to `https://<account>.cloudant.com/<database>/<design_id>/_show/<show_function>/<document_id>`,
where `<show_function>` is the name of the function that is applied to the document that has `<design_id>` as its `_id`.

### Update Handlers

> Example design doc:

```json
{
  "_id": "_design/update_example",
  "updates": {
    "UPDATE_HANDLER_NAME": "function (doc, req) { ... }"
  }
}
```

> Example update handler:

```
function(doc, req){
  if (!doc){
    if ('id' in req && req.id){
      // create new document
      return [{_id: req.id}, 'New World']
    }
    // change nothing in database
    return [null, 'Empty World']
  }
  doc.world = 'hello';
  doc.edited_by = req.userCtx.name
  return [doc, 'Edited World!']
}
```

> Example query:

```http
POST /<database>/<design_id>/_update/<update_handler http>/1.1
Content-Type: application/json
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_update/$UPDATE_HANDLER" \
     -X POST \
     -H 'Content-Type: application/json' \
     -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.atomic($DESIGN_ID, $UPDATE_HANDLER, $DOCUMENT_ID, $JSON, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

Update handlers are custom functions that live on Cloudant's server that will create or update a document.
This can, for example, provide server-side modification timestamps, and document updates to individual fields without the latest revision.

Update handlers receive two arguments: `doc` and [req](#req).
If a document ID is provided in the request to the update handler, then `doc` will be the document corresponding with that ID. If no ID was provided, `doc` will be `null`.

Update handler functions must return an array of two elements, the first being the document to save (or null, if you don't want to save anything), and the second being the response body.

Here's how to query update handlers:

Method | URL
-------|------
POST | `https://<account>.cloudant.com/<database>/<design_id>/_update>/<update_handler>`
PUT | `https://<account>.cloudant.com/<database>/<design_id>/_update>/<update_handler>/<document_id>`

Where `<design_id>` is the `_id` of the document defining the update handler, `$UPDATE_HANDLER` is the name of the update handler, and `<document_id>` is the `_id` of the document you want the handler to, well, handle.

### Filter Functions

> Example design document containing a filter function:

```json
{
  "_id":"_design/FILTER_EXAMPLE",
  "filters": {
    "FILTER_EXAMPLE": "function (doc, req) { ... }"
  }
}
```

Filter functions are design documents that enable you to filter the [changes feed](database.html#get-changes).
They work by applying tests to each of the objects included in the changes feed.
If any of the function tests fail,
the object is 'removed' or 'filtered' from the feed.
If the function returns a `true` result when applied to a change,
the change remains in the feed.
Therefore,
filter functions let you 'remove' or 'ignore' changes you don't want to monitor.

<aside class="information" role="complementary" aria-label="modifyreplicationtask">Filter functions can also be used to modify a [replication task](advanced_replication.html#filtered-replication).</aside>

<div></div>

> Example filter function:

```
function(doc, req){
  // we need only `mail` documents
  if (doc.type != 'mail'){
    return false;
  }
  // we're interested only in `new` ones
  if (doc.status != 'new'){
    return false;
  }
  return true; // passed!
}
```

Filter functions require two arguments: `doc` and [`req`](#req).

The `doc` argument represents the document being tested for filtering.

The `req` argument contains additional information about the HTTP request.
It enables you to create filter functions that are more dynamic,
because they are based on additional factors such as query parameters or the user context.

For example,
you could control aspects of the filter function tests by using dynamic values provided as part of the HTTP request.
In many filter function use cases,
however,
only the `doc` parameter is used.

More details about the `req` parameter are available [here](#req).

<div></div>

> Example query:

```http
GET /<database>/_changes?filter=<design_id>/<filter_function http>/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/_changes?filter=$DESIGN_ID/$FILTER_FUNCTION" \
```

To apply a filter function to the changes feed,
include the `filter` parameter in the `_changes` query,
providing the name of the filter to use.

<div></div>

> Using the `req` argument:

```http
GET /<database>/_changes?filter=<design_id>/<filter_function&status=new http>/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/_changes?filter=$DESIGN_ID/$FILTER_FUNCTION&status=new" \
```

> Example filter function that uses the `req` argument:

```
function(doc, req){
  // we need only `mail` documents
  if (doc.type != 'mail'){
    return false;
  }
  // we're interested only in `new` ones
  if (doc.status != req.query.status){
    return false;
  }
  return true; // passed!
}
```

The `req` argument gives you access to aspects of the HTTP request using the `query` property.

### Update Validators

> Example design document:

```json
{
  "_id": "_design/validator_example",
  "validate_doc_update": "function(newDoc, oldDoc, userCtx, secObj) { ... }"
}
```

> Example update validator:

```
function(newDoc, oldDoc, userCtx, secObj) {
  if (newDoc.address === undefined) {
     throw({forbidden: 'Document must have an address.'});
  }
}
```

> Example response:

```json
{
  "error": "forbidden",
  "reason": "Document must have an address."
}
```

Update validators evaluate whether a document should be written to disk when insertions and updates are attempted.
They do not require a query because they implicitly run during this process. If a change is rejected, the update validator responds with a custom error.

Update validators get four arguments:

* `newDoc`: the version of the document passed in the request.
* `oldDoc`: the version of the document currently in the database, or `null` if there is none.
* `userCtx`: context about the currently authenticated user, such as `name` and `roles`..
* `secObj`: the database's [security object](authorization.html#viewing-permissions)

Update validators do not apply when a design document is updated by an admin user, so that admins can never accidentally lock themselves out.

### Retrieving information about a design document

There are two endpoints available that provide you with more information: `_info` and `_search_info`.

> Example to get the information for the `recipesdd` design document in the `recipes` database:

```http
GET /recipes/_design/recipesdd/_info HTTP/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/recipes/_design/recipesdd/_info" \
```

> Example JSON structure response:

```json
{
   "name" : "recipesdd",
   "view_index": {
      "compact_running": false,
      "updater_running": false,
      "language": "javascript",
      "purge_seq": 10,
      "waiting_commit": false,
      "waiting_clients": 0,
      "signature": "fc65594ee76087a3b8c726caf5b40687",
      "update_seq": 375031,
      "disk_size": 16491
   },
}
```

-   **Method**: `GET /db/_design/design-doc/_info`
-   **Request**: None
-   **Response**: JSON of the design document information
-   **Roles permitted**: \_reader

Obtains information about a given design document, including the index, index size and current status of the design document and associated index information.

The individual fields in the returned JSON structure are as follows:

-   **name**: Name/ID of Design Document
-   **view\_index**: View Index
    -   **compact\_running**: Indicates whether a compaction routine is currently running on the view
    -   **disk\_size**: Size in bytes of the view as stored on disk
    -   **language**: Language for the defined views
    -   **purge\_seq**: The purge sequence that has been processed
    -   **signature**: MD5 signature of the views for the design document
    -   **update\_seq**: The update sequence of the corresponding database that has been indexed
    -   **updater\_running**: Indicates if the view is currently being updated
    -   **waiting\_clients**: Number of clients waiting on views from this design document
    -   **waiting\_commit**: Indicates if there are outstanding commits to the underlying database that need to processed

> Example to get information about the `description` search within the `app` design document in the `foundbite` database:

```http
GET /foundbite/_design/app/_search_info/description HTTP/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/foundbite/_design/app/_search_info/description" \
```

> Example JSON structure response:

```json
{
	"name": "_design/app/description",
	"search_index": {
		"pending_seq": 63,
		"doc_del_count": 3,
		"doc_count": 10,
		"disk_size": 9244,
		"committed_seq": 63
	}
}
```

-   **Method**: `GET /db/_design/design-doc/_search_info/yourSearch`
-   **Request**: None
-   **Response**: JSON information about the specified search
-   **Roles permitted**: \_reader

Obtains information about a search specified within a given design document.

The individual fields in the returned JSON structure are as follows:

-   **name**: Name/ID of the Search within the Design Document
-   **search\_index**: The Search Index
    -   **pending\_seq**: The sequence number of changes in the database that have reached Lucene, both in memory and on disk.
    -   **doc\_del\_count**: Number of deleted documents in the index.
    -   **doc\_count**: Number of documents in the index.
    -   **disk\_size**: The size of the index on disk, in bytes.
    -   **committed\_seq**: The sequence number of changes in the database that have been committed to the Lucene index on disk.
