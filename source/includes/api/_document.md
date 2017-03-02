## Documents

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Documents topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/document.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Documents are [JSON objects](http://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example).
Documents are containers for your data, and are the basis of the Cloudant database.

All documents must have two fields:
a unique `_id` field, and a `_rev` field.
The `_id` field is either created by you,
or generated automatically as a [UUID](http://en.wikipedia.org/wiki/Universally_unique_identifier) by Cloudant.
The `_rev` field is a revision number,
and is [essential to Cloudant's replication protocol](mvcc.html).
In addition to these two mandatory fields,
documents can generally contain any other content that can be described using JSON.

<div></div>

> Example of JSON document attempting to create a topmost field with an underscore prefix:

```json
{
	"_top_level_field_name": "some data"
}
```

> Error message returned when attempting to create a topmost field with an underscore prefix:

```json
{
	"error": "doc_validation",
	"reason": "Bad special document member: _top_level_field_name"
}
```

Field names beginning with the underscore character (`_`) are reserved in Cloudant.
This means you cannot normally have your own field names that begin with an underscore.
For example,
the field `example` would be permitted,
but the field `_example` would result in a `doc_validation` error message.

<div></div>

> Example of JSON document attempting to create a field with an underscore prefix, nested within an object:

```json
{
	"another_top_level_field_name": "some data",
	"another_field": {
		"_lower_level_field_name": "some more data"
	}
}
```

> Example success message returned when creating a nested field with an underscore prefix:

```json
{
	"ok": true,
	"id": "2",
	"rev": "1-9ce0b1caa2d37165b135ab585275d8d4"
}
```

However,
if the field name is for an object nested _within_ the document,
it is possible to use an underscore prefix for the field name.

<div></div>

Cloudant uses an [eventually consistent](cap_theorem.html#consistency) model for data.
This means that under some conditions,
it is possible that if your application performs a document write or update,
followed immediately by a read of the same document,
older document content is retrieved.
In other words,
your application would see the document content as it was *before* the write or update occurred.
For more information about this,
see the topic on [Consistency](cap_theorem.html#consistency).

<h3 id="documentCreate">Create</h3>

> Creating a document:

```http
POST /$DATABASE HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE \
     -X POST \
     -H "Content-Type: application/json" \
     -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
var db = account.use($DATABASE);

db.insert($JSON, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

```json
{
  "_id": "apple",
  "item": "Malus domestica",
  "prices": {
    "Fresh Mart": 1.59,
    "Price Max": 5.99,
    "Apples Express": 0.79
  }
}
```

To create a document, make a POST request with the document's JSON content to `https://$USERNAME.cloudant.com/$DATABASE`.

<div></div>

> Example response:

```json
{
  "ok":true,
  "id":"apple",
  "rev":"1-2902191555"
}
```

The response is a JSON document containing the ID of the created document, the revision string, and `"ok": true`. If you did not provide an `_id` field, Cloudant generates one automatically as a [UUID](http://en.wikipedia.org/wiki/Universally_unique_identifier). If creation of the document failed, the response contains a description of the error.

<aside class="warning" role="complementary" aria-label="cannotmeetquorum">If the write quorum cannot be met, a [`202` response](http.html#202) is returned.</aside>

### Read

> Reading a document:

```http
GET /$DATABASE/$DOCUMENT_ID HTTP/1.1
```

```shell
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
var db = account.use($DATABASE);

db.get($JSON._id, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

To retrieve a document, make a GET request to `https://$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID`.
If you do not know the `_id` for a particular document,
you can [query the database](database.html#get-documents) for all documents.

<div></div>

> Example response:

```json
{
  "_id": "apple",
  "_rev": "1-2902191555",
  "item": "Malus domestica",
  "prices": {
    "Fresh Mart": 1.59,
    "Price Max": 5.99,
    "Apples Express": 0.79
  }
}
```

The response contains the document you requested or a description of the error, if the document could not be retrieved.

#### Query Parameters

This is a list of parameters you can add to the URL in the usual way, e.g. `/db/doc?attachments=true&conflicts=true`. All parameters are *optional*.

| Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Type | Description | Default |
|------|------|-------------|---------|
| `attachments` | boolean | Includes attachments bodies in response. | false |
| `att_encoding_info` | boolean | Includes encoding information in attachment stubs if the particular attachment is compressed. | false |
| `atts_since` | array of revision strings | Includes attachments only since specified revisions. Doesn’t includes attachments for specified revisions. | [] |
| `conflicts` | boolean | Includes information about conflicts in document. | false |
| `deleted_conflicts` | boolean | Includes information about deleted conflicted revisions. | false |
| `latest` | boolean | Forces retrieving latest “leaf” revision, no matter what rev was requested. | false |
| `local_seq` | boolean | Includes last update sequence number for the document. | false |
| `meta` | boolean | Acts same as specifying all conflicts, deleted_conflicts and open_revs query parameters. | false |
| `open_revs` | array or `all` | Retrieves documents of specified leaf revisions. Additionally, it accepts value as all to return all leaf revisions. | [] |
| `rev` | string | Retrieves document of specified revision. | - |
| `revs` | boolean | Includes list of all known document revisions. | false |
| `revs_info` | boolean | Includes detailed information for all known document revisions. | false |

<aside class="warning" role="complementary" aria-label="readsmightbestale">Due to the distributed, eventually consistent nature of Cloudant, reads might return stale data. In particular, data that has just been written, even by the same client, might not be returned from a read request immediately following the write request. To work around this behavior, a client can cache state locally. Caching also helps to keep request counts down and thus increase application performance and decrease load on the database cluster. This also applies to requests to map-reduce and search indexes.
</aside>

### Read Many

To fetch many documents at once, [query the database](database.html#get-documents).

### Update

> Updating a document

```http
PUT /$DATABASE/$DOCUMENT_ID HTTP/1.1
```

```shell
// make sure $JSON contains the correct `_rev` value!
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID \
     -X PUT \
     -H "Content-Type: application/json" \
     -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
var db = account.use($DATABASE);

// make sure $JSON contains the correct `_rev` value!
$JSON._rev = $REV;

db.insert($JSON, $JSON._id, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

```json
{
  "_id": "apple",
  "_rev": "1-2902191555",
  "item": "Malus domestica",
  "prices": {
    "Fresh Mart": 1.59,
    "Price Max": 5.99,
    "Apples Express": 0.79,
    "Gentlefop's Shackmart": 0.49
  }
}
```

To update (or create) a document, make a PUT request with the updated JSON content *and* the latest `_rev` value (not needed for creating new documents) to `https://$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID`.

<aside class="warning" role="complementary" aria-label="uselatestrev1">If you fail to provide the latest `_rev`, Cloudant responds with a [409 error](http.html#409).
This error prevents you overwriting data changed by other processes. If the write quorum cannot be met, a [`202` response](http.html#202) is returned.</aside>

<aside class="warning" role="complementary" aria-label="updateconflicts">
Any document update can lead to a conflict - especially if you replicate updated documents. To learn more about avoiding and resolving conflicts, check out our [Document Versioning and MVCC guide](mvcc.html).
</aside>

<div></div>

> Example response:

```json
{
  "ok":true,
  "id":"apple",
  "rev":"2-9176459034"
}
```

The response contains the ID and the new revision of the document or an error message in case the update failed.

<div id="document-delete"></div>

### Delete

> Delete request

```http
DELETE /$DATABASE/$DOCUMENT_ID?rev=$REV HTTP/1.1
```

```shell
// make sure $JSON contains the correct `_rev` value!
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID?rev=$REV -X DELETE
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
var db = account.use($DATABASE);

// make sure $JSON contains the correct `_rev` value!
db.destroy($JSON._id, $REV, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

> Deletion response:

```json
{
  "id" : "apple",
  "ok" : true,
  "rev" : "3-2719fd4118"
}
```

To delete a document, make a DELETE request with the document's latest `_rev` in the query string, to `https://$USERNAME.cloudant.com/$DATABASE/$DOCUMENT_ID`.

The response contains the ID and the new revision of the document or an error message in case the update failed.

<aside class="warning" role="complementary" aria-label="uselatestrev2">If you fail to provide the latest `_rev`, Cloudant responds with a [409 error](http.html#409).
This error prevents you overwriting data changed by other clients. If the write quorum cannot be met, a [`202` response](http.html#202) is returned.</aside>

<aside class="warning" role="complementary" aria-label="notcompletedelete">CouchDB doesn’t completely delete the specified document. Instead, it leaves a tombstone with very basic information about the document. The tombstone is required so that the delete action can be replicated. Since the tombstones stay in the database indefinitely, creating new documents and deleting them increases the disk space usage of a database and the query time for the primary index, which is used to look up documents by their ID.
</aside>

### 'Tombstone' documents

Tombstone documents are small documents retained in place within a database when the original document is deleted.
Their purpose is to allow the deletion to be replicated.

When the replication has completed,
the tombstones are no longer required.
Normally,
this is not a problem,
as automatic compaction helps ensure that only the minimal amount of data is retained and transferred during replication.
Nevertheless,
tombstone documents are not automatically removed,
or 'purged'.

Over time,
as documents are created and deleted,
the number of tombstone documents increases.
Each tombstone is small,
but gradually they add to database disk space usage,
and to the query time for the primary index.
To reduce these effects,
you might want to remove the tombstones.

<div></div>

#### Simple removal of 'tombstone' documents

> Example filter to exclude deleted documents during a replication

```json
{
  "_id": "_design/filters",
  "filters": {
      "deleted_filter": "function(doc, req) { return !doc._deleted; };"
  }
}
```

To remove tombstones manually,
perform the following steps:

1.	Create a new database to hold the required documents. The new database is intended to hold all documents _except_ the tombstone documents.
2.	Set up a [filtered replication](advanced_replication.html#filtered-replication) to replicate documents from the original database to the new database.  Configure the filter so that documents with the '`_deleted`' attribute are not replicated.
3.	When replication is complete, switch your application logic to use the new database.
4.	Verify that your applications work correctly with the new database. When you are satisfied that everything is working correctly, you might wish to delete the old database.

<aside class="warning" role="complementary" aria-label="avoiddeletinglots">In general,
you should try to design and implement your applications to perform the minimum necessary amount of deletion.</aside>

#### Advanced removal of 'tombstone' documents

The simple removal technique described previously works well,
so long as documents are not being updated in the source database while the replication takes place.

If updates _are_ made during replication,
it is possible that a complete document is replicated to the target database as normal,
but is also deleted from the source database,
leaving a tombstone.
The problem is that the tombstone is not replicated across to the target database,
because it is excluded by the filter.
As a result,
the document that was deleted from the source database is not deleted from the target database,
causing an inconsistency.

A solution is to perform more advanced removal of tombstones using
a [`validate_doc_update` function](http://docs.couchdb.org/en/1.6.1/couchapp/ddocs.html#validate-document-update-functions).

A `validate_doc_update` function is stored in a design document.
The function is executed every time a document is updated in the database.
The function can be used to prevent invalid or unauthorized document updates from being performed.

The function works using the following parameters:

-	The new version of the document.
-	The current version of the document in the database.
-	A user context, which provides details about the user supplying the updated document.

The function inspects the request to determine if the update should proceed.
If the update is permitted,
the function simply returns.
If the update is not permitted,
a suitable error object is returned.
In particular,
if the user is not authorized to make the update,
an `unauthorized` error object is returned,
along with an explanatory error message.
Similarly,
if the requested update is not allowed for some reason (such as some mandatory fields being absent from the new document),
then a `forbidden` error object is returned,
again with an explanatory error message.

<div></div>

> Example `validate_doc_update` function to reject deleted documents not already present in the target database

```
function(newDoc, oldDoc, userCtx) {
	// any update to an existing doc is OK
	if(oldDoc) {
		return;
	}

	// reject tombstones for docs we don’t know about
	if(newDoc["_deleted"]) {
		throw({forbidden : "Deleted document rejected"});
	}

	return; // Not strictly necessary, but clearer.
}
```

For tombstone removal,
a suitable `validate_doc_update` function would work as follows:

1.	If the update is to apply a change to an existing document (`oldDoc`) within the target database, the function allows this by simply returning.  The reason is that the update is to a document that was copied to the target database during the replication, but has subsequently changed in the source database during the replication. It is possible that the change is a 'Delete', which results in a tombstone record in the target database.  The tombstone record is removed by a subsequent replication process at some point in the future.
2.	If the target database does _not_ have a copy of the current document, _and_ the update document has the `_deleted` property (indicating that it is a tombstone), then the update must be a tombstone _and_ it has been encountered before, so the update should be rejected.
3.	Finally, if the function has not yet returned or thrown an error, allow the update to replicate to the target database, as some other condition applies.

To use a `validate_doc_update` function to remove tombstone documents:

1.	Stop replication from the source to the target database.
2.	If appropriate, delete the target database, then create a new target database.
3.	Add a suitable `validate_doc_update` function, similar to the example provided. Add it to a design document in the target database.
4.	Restart replication between the source and the (new) target database.
5.	When replication is complete, switch your application logic to use the new database.
6.	Verify that your applications work correctly with the new database. When you are satisfied that everything is working correctly, you might wish to delete the old database.

A variation for using the `validate_doc_update` function to remove tombstone documents is possible.
You might add some metadata to the tombstone documents,
using it to record the deletion date.
The function could then inspect the metadata and permit deletion documents through,
in order to replicate the deletion correctly.

#### Performance implications of tombstone removal

Remember that tombstones are used for more consistent deletion of documents from databases.
This is especially important for mobile devices:
without tombstone documents,
a deletion might not replicate correctly to a mobile device,
with the result that documents might never be deleted from the device.

If you recreate a database,
for example to be a new target for a replication,
any clients that use the target database as a server _must_ work through _all_ the changes again,
because the database sequence numbers are likely to have changed.

<aside class="warning" role="complementary" aria-label="avoidclientvdu">If you are using a `validate_doc_update` function,
you should avoid replicating that function to clients.
This is to prevent the possibility of unwanted side effects as a result of having the function present on the client.

Cloudant Sync does not replicate design documents,
so this should not normally be a problem for Cloudant.
However,
other clients might replicate design documents or `validate_doc_update` functions,
potentially resulting in unwanted side effects.</aside>

### Bulk Operations

The bulk document API allows you to create and update multiple documents at the same time within a single request. The basic operation is similar to creating or updating a single document, except that you batch the document structure and information. When creating new documents the document ID is optional. For updating existing documents, you must provide the document ID, revision information, and new document values.

<div></div>

#### Request Body

> Request to update/create/delete multiple documents:

```http
POST /$DATABASE/_bulk_docs HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/_bulk_docs -X POST -H "Content-Type: application/json" -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano("https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com");
var db = account.use($DATABASE);

db.bulk($JSON, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

```json
{
  "docs": [
    {
      "name": "Nicholas",
      "age": 45,
      "gender": "female",
      "_id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
      "_rev": "1-54dd23d6a630d0d75c2c5d4ef894454e"
    },
    {
      "name": "Taylor",
      "age": 50,
      "gender": "female"
    },
    {
      "_id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
      "_rev": "1-a2b6e5dac4e0447e7049c8c540b309d6",
      "_deleted": true
    }
  ]
}
```

For both inserts and updates the basic structure of the JSON document in the request is the same:

<table>
<colgroup>
<col width="15%" />
<col width="36%" />
<col width="26%" />
<col width="15%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Field</th>
<th align="left">Description</th>
<th align="left">Type</th>
<th align="left">Optional</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><code>docs</code></td>
<td align="left">Bulk Documents Document</td>
<td align="left">array of objects</td>
<td align="left">no</td>
</tr>
</tbody>
</table>

#### Object in `docs` array

<table>
<colgroup>
<col width="15%" />
<col width="41%" />
<col width="10%" />
<col width="33%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Field</th>
<th align="left">Description</th>
<th align="left">Type</th>
<th align="left">Optional</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><code>_id</code></td>
<td align="left">Document ID</td>
<td align="left">string</td>
<td align="left">optional only for new documents</td>
</tr>
<tr class="even">
<td align="left"><code>_rev</code></td>
<td align="left">Document revision</td>
<td align="left">string</td>
<td align="left">mandatory for updates and deletes, not used for new documents</td>
</tr>
<tr class="odd">
<td align="left"><code>_deleted</code></td>
<td align="left">Whether the document should be deleted</td>
<td align="left">boolean</td>
<td align="left">yes</td>
</tr>
</tbody>
</table>

#### Response

> Example response:

```json
[{
  "id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
  "rev": "2-ff7b85665c4c297838963c80ecf481a3"
}, {
  "id": "5a049246-179f-42ad-87ac-8f080426c17c",
  "rev": "2-9d5401898196997853b5ac4163857a29"
}, {
  "id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
  "rev": "2-cbdef49ef3ddc127eff86350844a6108"
}]
```

The HTTP status code tells you whether the request was fully or partially successful. In the response body, you get an array with detailed information for each document in the request.

<table>
<colgroup>
<col width="7%" />
<col width="92%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Code</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">201</td>
<td align="left">The request succeeded, but this does not imply all documents were updated. Inspect the response body to determine the status of each requested change, and <a href="document.html#bulk-document-validation-and-conflict-errors">address any problems</a>.</td>
</tr>
<tr class="even">
<td align="left">202</td>
<td align="left">For at least one document, the write quorum has not been met.</td>
</tr>
</tbody>
</table>

#### Inserting Documents in Bulk

> Example bulk insert of three documents:

```
{
  "docs": [{
    "name": "Nicholas",
    "age": 45,
    "gender": "male",
    "_id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
    "_attachments": {

    }
  }, {
    "name": "Taylor",
    "age": 50,
    "gender": "male",
    "_id": "5a049246-179f-42ad-87ac-8f080426c17c",
    "_attachments": {

    }
  }, {
    "name": "Owen",
    "age": 51,
    "gender": "male",
    "_id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
    "_attachments": {

    }
  }]
}
```

To insert documents in bulk into a database you need to supply a JSON structure with the array of documents that you want to add to the database. You can either include a document ID for each document, or allow the document ID to be automatically generated.

<div></div>

> Example response header after bulk insert of three documents:

```
201 Created
Cache-Control: must-revalidate
Content-Length: 269
Content-Type: application/json
Date: Mon, 04 Mar 2013 14:06:20 GMT
server: CouchDB/1.0.2 (Erlang OTP/R14B)
x-couch-request-id: e8ff64d5
```

> Example response content after bulk insert of three documents:

```
    [{
      "id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
      "rev": "1-54dd23d6a630d0d75c2c5d4ef894454e"
    }, {
      "id": "5a049246-179f-42ad-87ac-8f080426c17c",
      "rev": "1-0cde94a828df5cdc0943a10f3f36e7e5"
    }, {
      "id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
      "rev": "1-a2b6e5dac4e0447e7049c8c540b309d6"
    }]
```

The return code from a successful bulk insertion is [`201`](http.html#201),
with the content of the returned structure indicating specific success or otherwise messages on a per-document basis.

The return structure from the example contains a list of the documents created, including their revision and ID values.

The content and structure of the returned JSON depends on the transaction semantics being used for the bulk update; see [Bulk Documents Transaction Semantics](#bulk-documents-transaction-semantics) for more information. Conflicts and validation errors when updating documents in bulk must be handled separately; see [Bulk Document Validation and Conflict Errors](#bulk-document-validation-and-conflict-errors).

<div></div>

#### Updating Documents in Bulk

> Example request to perform bulk update:

``` http
POST /test/_bulk_docs HTTP/1.1
Accept: application/json
```

``` shell
curl -X POST "https://$USERNAME.cloudant.com/$DATABASE/_bulk_docs" -d @request.json
```

> Example JSON to bulk update documents:

```
{
  "docs": [{
    "name": "Nicholas",
    "age": 45,
    "gender": "female",
    "_id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
    "_attachments": {

    },
    "_rev": "1-54dd23d6a630d0d75c2c5d4ef894454e"
  }, {
    "name": "Taylor",
    "age": 50,
    "gender": "female",
    "_id": "5a049246-179f-42ad-87ac-8f080426c17c",
    "_attachments": {

    },
    "_rev": "1-0cde94a828df5cdc0943a10f3f36e7e5"
  }, {
    "name": "Owen",
    "age": 51,
    "gender": "female",
    "_id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
    "_attachments": {

    },
    "_rev": "1-a2b6e5dac4e0447e7049c8c540b309d6"
  }]
}
```

The bulk document update procedure is similar to the insertion procedure, except that you must specify the document ID and current revision for every document in the bulk update JSON string.

<div></div>

> Example JSON structure returned after bulk update:

```
[{
  "id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
  "rev": "2-ff7b85665c4c297838963c80ecf481a3"
}, {
  "id": "5a049246-179f-42ad-87ac-8f080426c17c",
  "rev": "2-9d5401898196997853b5ac4163857a29"
}, {
  "id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
  "rev": "2-cbdef49ef3ddc127eff86350844a6108"
}]
```

The return structure is the JSON of the updated documents, with the new revision and ID information.

<div></div>

You can optionally delete documents during a bulk update by adding the `_deleted` field with a value of `true` to each document ID/revision combination within the submitted JSON structure.

The return code from a successful bulk update is [`201`](http.html#201),
with the content of the returned structure indicating specific success or otherwise messages on a per-document basis.

The content and structure of the returned JSON depends on the transaction semantics being used for the bulk update; see [Bulk Documents Transaction Semantics](#bulk-documents-transaction-semantics) for more information. Conflicts and validation errors when updating documents in bulk must be handled separately; see [Bulk Document Validation and Conflict Errors](#bulk-document-validation-and-conflict-errors).

#### Bulk Documents Transaction Semantics

> Response with errors

```json
[
   {
      "id" : "FishStew",
      "error" : "conflict",
      "reason" : "Document update conflict."
   },
   {
      "id" : "LambStew",
      "error" : "conflict",
      "reason" : "Document update conflict."
   },
   {
      "id" : "7f7638c86173eb440b8890839ff35433",
      "error" : "conflict",
      "reason" : "Document update conflict."
   }
]
```

Cloudant only guarantees that some of the documents are saved if your request yields a [`202` response](http.html#202).
The response contains the list of documents successfully inserted or updated during the process.

The response structure indicates whether the document was updated successfully.
It does this by supplying the new `_rev` parameter,
indicating that a new document revision was successfully created.

If the update failed, then you get an `error` of type `conflict`.
In this case,
no new revision has been created.
You must submit the document update with the correct revision tag, to update the document.

<div></div>

#### Bulk Document Validation and Conflict Errors

The JSON returned by the `_bulk_docs` operation consists of an array of JSON structures,
one for each document in the original submission.
The returned JSON structure should be examined to ensure that all of the documents submitted in the original request were successfully added to the database.

The structure of the returned information is:

<table>
<colgroup>
<col width="20%" />
<col width="36%" />
<col width="26%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Field</th>
<th align="left">Description</th>
<th align="left">Type</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">docs [array]</td>
<td align="left">Bulk Documents Document</td>
<td align="left">array of objects</td>
</tr>
</tbody>
</table>

#### Fields of objects in docs array

<table>
<colgroup>
<col width="12%" />
<col width="50%" />
<col width="12%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Field</th>
<th align="left">Description</th>
<th align="left">Type</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">id</td>
<td align="left">Document ID</td>
<td align="left">string</td>
</tr>
<tr class="even">
<td align="left">error</td>
<td align="left">Error type</td>
<td align="left">string</td>
</tr>
<tr class="odd">
<td align="left">reason</td>
<td align="left">Error string with extended reason</td>
<td align="left">string</td>
</tr>
</tbody>
</table>

When a document (or document revision) is not correctly committed to the database because of an error, you should check the `error` field to determine error type and course of action.
The error is one of `conflict` or `forbidden`.

#### `conflict`

The document as submitted is in conflict.
If you used the default bulk transaction mode,
then the new revision was not created.
You must re-submit the document to the database.

Conflict resolution of documents added using the bulk docs interface is identical to the resolution procedures used when resolving conflict errors during replication.

#### `forbidden`

> Example javascript to produce `forbidden` error as part of a validation function:

```
throw({forbidden: 'invalid recipe ingredient'});
```

> Resulting error message from the validation function:

```json
{
   "id" : "7f7638c86173eb440b8890839ff35433",
   "error" : "forbidden",
   "reason" : "invalid recipe ingredient"
}
```

Entries with this error type indicate that the validation routine applied to the document during submission has returned an error.

<div id="quorum"></div>

### Quorum - writing and reading data

In a distributed system,
it is possible that a request might take some time to complete.
A 'quorum' mechanism is used to help determine when a given request,
such as a write or read,
has completed successfully.

For help understanding quorum settings and their implications on dedicated Cloudant systems,
contact Cloudant support.

### TTL - Time to Live

[Time to Live](https://en.wikipedia.org/wiki/Time_to_live) (TTL) is a property of data,
where after a relative amount of time,
or at an absolute time,
the data is deemed to have expired.
The data itself might be deleted or moved to an alternative (archive) location.

Cloudant does not support Time to Live functionality.

The reason is that Cloudant documents are only soft-deleted,
not completely deleted.
The soft deletion involves replacing the original document with a smaller record.
This small record is required for replication purposes; it helps ensure that the correct revision to use can be identified during replication.

If TTL were available in Cloudant,
the resulting potential increase in short-lived documents and soft deletion records would mean that the database size could grow in an unbounded fashion.
