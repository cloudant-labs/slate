---

copyright:
  years: 2015, 2017
lastupdated: "2017-04-27"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-04-27 -->

# Documents

Documents are
[JSON objects ![External link icon](../images/launch-glyph.svg "External link icon")](http://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example){:new_window}.
Documents are containers for your data,
and are the basis of the Cloudant database.
{:shortdesc}

Documents are limited to a maximum size of 64 MB.

>   **Note**: If you are using a [Cloudant service on IBM Bluemix](../offerings/bluemix.html),
    documents are limited to a maximum size of 1 MB.
    Exceeding this limit causes a [`413` error](http.html#413).

All documents must have two fields:
a unique `_id` field, and a `_rev` field.

The `_id` field is either created by you,
or generated automatically as a
[UUID ![External link icon](../images/launch-glyph.svg "External link icon")](http://en.wikipedia.org/wiki/Universally_unique_identifier){:new_window} by Cloudant.

The `_rev` field is a revision number,
and is [essential to the Cloudant replication protocol](../guides/mvcc.html).
In addition to these two mandatory fields,
documents can generally contain any other content that can be described by using JSON.

Field names that begin with the underscore character (`_`) are reserved in Cloudant.
This rule means that you cannot normally have your own field names that begin with an underscore.
For example,
the field `example` would be accepted,
but the field `_example` would result in a `doc_validation` error message.

_Example of JSON document that attempts to create a topmost field with an underscore prefix:_

```json
{
	"_top_level_field_name": "some data"
}
```
{:codeblock}

_Error message that is returned when you attempt to create a topmost field with an underscore prefix:_

```json
{
	"error": "doc_validation",
	"reason": "Bad special document member: _top_level_field_name"
}
```
{:codeblock}

However,
if the field name is for an object _nested within_ the document,
it is possible to use an underscore prefix for the field name.

_Example of JSON document that attempts to create a field with an underscore prefix, nested within an object:_

```json
{
	"another_top_level_field_name": "some data",
	"another_field": {
		"_lower_level_field_name": "some more data"
	}
}
```
{:codeblock}

_Example success message (abbreviated) returned when a nested field with an underscore prefix is created:_

```json
{
	"ok": true,
	"id": "2",
	"rev": "1-9ce...8d4"
}
```
{:codeblock}

Cloudant uses an [eventually consistent](../guides/cap_theorem.html#consistency) model for data.
This model means that under some conditions,
it is possible that if your application writes or updates a document,
followed immediately by a read of the same document,
older document content is retrieved.
In other words,
your application would see the document content as it was *before* the write or update occurred.
For more information about this model,
see the topic on [Consistency](../guides/cap_theorem.html#consistency).

<div id="documentCreate"></div>

## Create

To create a document,
send a `POST` request with the document's JSON content to `https://$ACCOUNT.cloudant.com/$DATABASE`.

_Creating a document by using HTTP:_

```http
POST /$DATABASE HTTP/1.1
Content-Type: application/json
```
{:codeblock}

_Creating a document by using the command line:_

```sh
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE \
	-X POST \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

<!--

_Creating a document, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.insert($JSON, function (err, body, headers) {
	if (!err) {
		console.log(body);
	}
});
```
{:codeblock}

-->

_Example JSON document:_

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
{:codeblock}

The response is a JSON document that contains the ID of the created document,
the revision string,
and `"ok": true`.

If you did not provide an `_id` field,
Cloudant generates one automatically as a
[UUID ![External link icon](../images/launch-glyph.svg "External link icon")](http://en.wikipedia.org/wiki/Universally_unique_identifier){:new_window}.

A failure to create the document results in a
response that contains a description of the error.

_Example response after successfully creating a document:_

```json
{
	"ok":true,
	"id":"apple",
	"rev":"1-2902191555"
}
```
{:codeblock}

>	**Note**: If the write [quorum](#quorum) cannot be met during an attempt to create a document,
a [`202` response](http.html#202) is returned.

## Read

To retrieve a document,
send a GET request to `https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID`.

If you do not know the `_id` for a particular document,
you can [query the database](database.html#get-documents) for all documents.

>	**Note**: Due to the distributed,
eventually consistent nature of Cloudant,
reads might return stale data.
In particular,
data that were written recently,
even by the same client,
might not be returned from a read request immediately following the write request.
To work around this behavior,
a client can cache the state of data locally.
Caching also helps to keep request counts down,
increase application performance,
and decrease load on the database cluster.
This behavior also applies to other read requests such as to map-reduce and search indexes.

_Example of retrieving a document by using HTTP:_

```http
GET /$DATABASE/$DOCUMENT_ID HTTP/1.1
```
{:codeblock}

_Example of retrieving a document by using the command line:_

```sh
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID
```
{:codeblock}

<!--

_Example of retrieving a document, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.get($JSON._id, function (err, body, headers) {
	if (!err) {
		console.log(body);
	}
});
```
{:codeblock}

-->

The response contains the document that you requested,
or a description of the error if the document cannot be retrieved.

_Example response:_

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
{:codeblock}

### Query Parameters

You can add some query parameters to the URL,
for example `/mydatabase/doc?attachments=true&conflicts=true`.

All parameters are *optional*.

Name                | Type | Description | Default
--------------------|------|-------------|--------
`attachments`       | Boolean | Includes attachments bodies in response. | False
`att_encoding_info` | Boolean | Includes encoding information in attachment stubs if the particular attachment is compressed. | False
`atts_since`        | Array of revision strings | Includes attachments only since specified revisions. Does not include attachments for specified revisions. | []
`conflicts`         | Boolean | Includes information about conflicts in document. | False
`deleted_conflicts` | Boolean | Includes information about deleted conflicted revisions. | False
`latest`            | Boolean | Forces retrieval of the most recent 'leaf' revision, no matter what revision was requested. | False
`local_seq`         | Boolean | Includes last update sequence number for the document. | False
`meta`              | Boolean | Acts same as specifying the `conflicts`, `deleted_conflicts`, and `open_revs` query parameters. | False
`open_revs`         | Array or `all` | Retrieves documents of specified leaf revisions. Additionally, it accepts the value `all` to return all leaf revisions. | []
`rev`               | String | Retrieves document of specified revision. | -
`revs`              | Boolean | Includes list of all known document revisions. | False
`revs_info`         | Boolean | Includes detailed information for all known document revisions. | False

## Read Many

To fetch more than one document at a time,
[query the database](database.html#get-documents)
by using the `include_docs` option.

## Update

To update a document,
send a `PUT` request with the updated JSON content *and* the most recent `_rev` value
to `https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID`.
You can also use this `PUT` method to create a document,
in which case you do not need to supply the most recent `_rev` value.

>   **Note**: If you fail to provide the most recent `_rev` when you attempt to update an existing document,
    Cloudant responds with a [409 error](http.html#409).
    This error prevents you overwriting data that were changed by other processes.
    If the write [quorum](#quorum) cannot be met, a [`202` response](http.html#202) is returned.

>   **Note**: Any document update can lead to a conflict,
    especially when you replicate updated documents.
    More information about avoiding and resolving conflicts is in
    the [Document Versioning and MVCC guide](../guides/mvcc.html).

_Example of using HTTP to update a document:_

```http
PUT /$DATABASE/$DOCUMENT_ID HTTP/1.1
```
{:codeblock}

_Example of using the command line to update a document:_

```sh
# make sure $JSON contains the correct `_rev` value!
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID \
	-X PUT \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

<!--

_Example of updating a document, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

// make sure $JSON contains the correct `_rev` value!
$JSON._rev = $REV;

db.insert($JSON, $JSON._id, function (err, body, headers) {
	if (!err) {
		console.log(body);
	}
});
```
{:codeblock}

-->

_Example of JSON data that contains an updated document:_

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
{:codeblock}

The response contains the ID and the new revision of the document,
or an error message if the update failed.

_Example response after a successful update:_

```json
{
	"ok":true,
	"id":"apple",
	"rev":"2-9176459034"
}
```
{:codeblock}

<div id="document-delete"></div>

## Delete

To delete a document,
send a `DELETE` request with the document's most recent `_rev` in the query string
to `https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID`.

The response contains the ID and the new revision of the document,
or an error message if the delete failed.

>	**Note**: If you fail to provide the most recent `_rev`,
Cloudant responds with a [409 error](http.html#409).
This error prevents you overwriting data that were changed by other clients.
If the write [quorum](#quorum) cannot be met,
a [`202` response](http.html#202) is returned.

Deleting a document does not _remove_ the document from the database.
Deletion marks a document with status `_deleted=true`,
and gives it a new revision value.
The deleted document is still listed within the [`_changes` feed](database.html#get-changes).

Deleting a document leaves a [tombstone](#-tombstone-documents) with basic information about the document.
The tombstone is needed so that the delete action can be replicated to other copies of the database.
Since the tombstones stay in the database indefinitely,
creating new documents and deleting them increases the disk space usage of a database.
They might also increase the query time for the primary index,
which is used to look up documents by their ID.

>   **Note**: To remove a document fully, use a [`_purge` command](#purge).

_Example of using HTTP to delete a document:_

```http
DELETE /$DATABASE/$DOCUMENT_ID?rev=$REV HTTP/1.1
```
{:codeblock}

_Example of using the command line to delete a document:_

```sh
# make sure $JSON contains the correct `_rev` value!
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID?rev=$REV -X DELETE
```
{:codeblock}

<!--

_Example of a delete request, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

// make sure $JSON contains the correct `_rev` value!
db.destroy($JSON._id, $REV, function (err, body, headers) {
	if (!err) {
		console.log(body);
	}
});
```
{:codeblock}

-->

_Example response after a successful deletion request:_

```json
{
	"id" : "apple",
	"ok" : true,
	"rev" : "3-2719fd4118"
}
```
{:codeblock}

## 'Tombstone' documents

Tombstone documents are small documents that are retained in place within a database when the original document is deleted.
Their purpose is to allow the deletion to be replicated.

When the replication completes,
the tombstones are no longer needed.
Automatic compaction helps ensure that only the minimal amount of data is retained and transferred during replication.
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

### Simple removal of 'tombstone' documents

To remove tombstones manually,
do the following steps:

1.	Create a database to hold the database documents.
	The new database is intended to hold all documents _except_ the tombstone documents.
2.	Set up a [filtered replication](advanced_replication.html#filtered-replication) to
	replicate documents from the original database to the new database.
	Configure the filter so that documents with the '`_deleted`' attribute are not replicated.
3.	When replication is complete,
	switch your application logic to use the new database.
4.	Verify that your applications work correctly with the new database.
	When you are satisfied that everything is working correctly,
	you might want to delete the old database.

>	**Note**: In general,
try to design and implement your applications to do the minimum necessary amount of deletion.

_Example filter to exclude deleted documents during a replication:_

```json
{
	"_id": "_design/filters",
	"filters": {
		"deleted_filter": "function(doc, req) { return !doc._deleted; };"
	}
}
```
{:codeblock}

### Advanced removal of tombstone documents

The [simple removal technique](#simple-removal-of-tombstone-documents) works well,
if documents are not being updated in the source database while the replication takes place.

If updates _are_ made during replication,
it is possible that a complete document is replicated to the target database as normal,
but is also deleted from the source database,
leaving a tombstone.
The problem is that the tombstone is not replicated across to the target database
because it is excluded by the filter.
As a result,
the document that was deleted from the source database is not deleted from the target database,
causing an inconsistency.

A solution is to do more advanced removal of tombstones by using
a [`validate_doc_update` function ![External link icon](../images/launch-glyph.svg "External link icon")](http://docs.couchdb.org/en/1.6.1/couchapp/ddocs.html#validate-document-update-functions){:new_window}.

A `validate_doc_update` function is stored in a design document.
The function is run every time that a document is updated in the database.
The function can be used to prevent invalid or unauthorized document updates.

The function works by using the following parameters:

-	The new version of the document.
-	The current version of the document in the database.
-	A user context,
	which provides details about the user that supplied the updated document.

The function inspects the request to determine whether the update is allowed to proceed.
If the update is acceptable,
the function returns.
If the update is not acceptable,
a suitable error object is returned.
In particular,
if the user is not authorized to make the update,
an `unauthorized` error object is returned,
along with an explanatory error message.
Similarly,
if the requested update is not allowed for some reason (such as when some mandatory fields are absent from the new document),
then a `forbidden` error object is returned,
again with an explanatory error message.

For tombstone removal,
a suitable `validate_doc_update` function would work as follows:

1.	If the update is to apply a change to an existing document (`oldDoc`) within the target database,
	the function allows the change by returning.
	The reason is that the update affected a document that was copied to the target database during the replication,
	but then changed in the source database during the replication.
	It is possible that the change was a `DELETE`,
	resulting in a tombstone record in the target database.
	The tombstone record is removed by a subsequent replication process at some point in the future.
2.	If the target database does _not_ have a copy of the current document,
	_and_ the update document has the `_deleted` property (indicating that it is a tombstone),
	then the update must be a tombstone _and_ it was encountered before,
	so the update must be rejected.
3.	Finally,
	if the function did not return or 'throw' an error,
	allow the update to replicate to the target database,
	as some other condition applies.

_Example JavaScript `validate_doc_update` function to reject deleted documents not already present in the target database:_

```javascript
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
{:codeblock}

To use a `validate_doc_update` function to remove tombstone documents:

1.	Stop replication from the source to the target database.
2.	If appropriate,
	delete the target database,
	then create a new target database.
3.	Add a suitable `validate_doc_update` function,
	similar to the example provided.
	Add it to a design document in the target database.
4.	Restart replication between the source and the (new) target database.
5.	When replication is complete,
	switch your application logic to use the new database.
6.	Verify that your applications work correctly with the new database.
	When you are satisfied that everything is working correctly,
	you might want to delete the old database.

A variation for using the `validate_doc_update` function to remove tombstone documents if possible.
You might add some metadata to the tombstone documents,
for example to record the deletion date.
The function might then inspect the metadata and allow deletion documents through
if they must be applied to the target database.
This check helps ensure correct replication of the deletion.

### Performance implications of tombstone removal

Tombstones are used for more consistent deletion of documents from databases.
This purpose is especially important for mobile devices:
without tombstone documents,
a deletion might not replicate correctly to a mobile device,
with the result that documents might never be deleted from the device.

If you re-create a database,
for example to be a new target for a replication,
any clients that use the target database as a server _must_ work through _all_ the changes again
because the database sequence numbers are likely to be different.

>	**Note**: If you are using a `validate_doc_update` function,
avoid replicating that function to clients.
This rule is to prevent the possibility of unwanted side effects as a result of having the function present on the client.

>	**Note**: [Cloudant Sync](../libraries/supported.html#mobile) libraries do not replicate design documents,
so replication of `validate_doc_update` functions is not normally a problem for Cloudant.
However,
other clients might replicate the design documents or `validate_doc_update` functions,
potentially resulting in unwanted side effects.

## Purge

Unlike [deleting a document](#delete),
purging a document removes all references to that document from the database.
Following a purge,
the affected documents are no longer available and cannot be listed by using the [`_all_docs`](database.html#get-documents)
or [`_changes`](database.html#get-changes) commands.
When you request a purge of a document,
it does not matter whether a document still exists,
or was [deleted](#delete) previously.

A purge request must identify the `leaf` version of a document.
In other words,
you must specify the _last_ revision of a document.
You cannot request a purge of an earlier revision of a document.

When a purge is requested,
it affects the specified ('leaf') version of a document,
_and_ all its predecessor versions.
This effect is necessary to ensure that all references to the document can be removed from the database.
However,
if a document version is _also_ present within another revision branch,
then the purging process halts before it removes the version that would 'orphan' the revision branch.

<div id="sampleDocumentStructure"></div>

For example,
in the following diagram,
an original document with revision value `1-7a7e4b29f3af401e69b6f86e4c26b727`
was modified by two separate applications.
These modifications resulted in two separate revision branches.

![Document with two revision branches](../images/fb86021a.png)

Suppose that a decision is taken to purge the document branch
that ends in revision value `4-53b84f8bf5539a7fb7f8074d1f685e5e`.

Beginning with the specified revision,
all references to each 'ancestor' version of the document are removed from the database.
However,
the document with revision value `1-7a7e4b29f3af401e69b6f86e4c26b727` is
an ancestor of revision `4-53b84f8bf5539a7fb7f8074d1f685e5e`
_and_ revision `2-98e2b4ecd9a0da76fe8b83a83234ee71`.
Therefore,
document `1-7a7e4b29f3af401e69b6f86e4c26b727` is _not_ removed from the database.
The resulting document structure looks like the following diagram.

![Purged document with one remaining revision branches](../images/fb86021b.png)

A subsequent request to purge the document with revision `2-98e2b4ecd9a0da76fe8b83a83234ee71`
results in the removal of _all_ the revisions
because no revision branches are left in an orphan state by the purge.

### Deciding between purge or delete

You might want to purge rather than delete a document for two reasons.

1.  You want to remove a document that is not needed anymore.
    Purging all leaf revisions of a document causes the complete purging of the document.
    Purging enables the database to reclaim the disk space that is used by a document.
    The disk space is reclaimed after the database runs an internal compaction task.
2.  You want to get rid of conflicts.
    If a document has several revision branches,
    for example after two separate applications updated the document independently,
    purging all but one of these branches leads to the partial purging of the document.
    The document remains available in the database,
    but in a new form without the purged branches and revisions.
    A new record is created in the [`_changes`](database.html#get-changes) for this document.

### Purging and replication

A document purge must be replicated to other databases.

This replication is made possible by an internal database purge record.
The number of records that are stored is defined by a `purged_docs_limit` parameter.
When a document purge is requested,
the details of that request and its outcome are stored in the purge record.

During a replication between two databases,
the database purge records are reconciled to ensure that
the details of which documents were purged are replicated correctly and automatically.

### Purging and indexes

When a document is purged,
the change might require an update to indexes within the database.

If a document is not changed as a result of a purge request,
no index change is needed.

If a document is removed as a result of a purge request,
then any index that originally included the document as part of the index scope is updated.

If a purge request applies to a document that has more than one revision branch,
and after the purge a different document revision applies rather than the one originally used in an index,
then the index is updated.

For example,
looking at the [earlier revision branch structure](#sampleDocumentStructure),
an index might include document revision `4-53b84f8bf5539a7fb7f8074d1f685e5e`.
After the purge,
revision `2-98e2b4ecd9a0da76fe8b83a83234ee71` remains.
Therefore,
the index is updated by using revision `2-98e2b4ecd9a0da76fe8b83a83234ee71`.

### The `purged_docs_limit` parameter

The `purged_docs_limit` parameter defines the number of purge request records that can be stored in a database.

The default value is 1000.
The default value means that at least the most recent 1000 purge requests are stored.
The database might store older purge requests if other indexing or replication tasks are still processing
these other purge requests.

To find the current value of the `purged_docs_limit` parameter,
send a `GET` request to the `_purged_docs_limit` endpoint of the database.

_Example of using HTTP to find the value of the `purged_docs_limit` parameter:_

```http
GET /$DATABASE/_purged_docs_limit
```
{:codeblock}

_Example of using the command line to find the value of the `purged_docs_limit` parameter:_

```sh
curl -X GET https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/_purged_docs_limit
```
{:codeblock}

_Example response after a successful request to get the value of the `purged_docs_limit` parameter:_

```json
{
	"????": "????"
}
```
{:codeblock}

To set the value of the `purged_docs_limit` parameter,
send a `PUT` request to the `_purged_docs_limit` endpoint of the database,
with a JSON document that includes the wanted value.

_Example of using HTTP to set the value of the `purged_docs_limit` parameter:_

```http
PUT /$DATABASE/_purged_docs_limit
```
{:codeblock}

_Example of using the command line to set the value of the `purged_docs_limit` parameter:_

```sh
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/_purged_docs_limit \
	-X PUT \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

_Example of JSON data that contains the wanted value of the `purged_docs_limit` parameter:_

```json
{
	"????": "????"
}
```
{:codeblock}

_Example response after a successful change to the value of the `purged_docs_limit` parameter:_

```json
{
	"ok":true
}
```
{:codeblock}

### Purging documents

Using the [previous example](#sampleDocumentStructure) document structure,
suppose that an application needs to purge the document with revision value `4-53b84f8bf5539a7fb7f8074d1f685e5e`.

To request a document purge,
send a description of the purge to the database `_purge` endpoint.

_Example of using HTTP to request the purge of a document:_

```http
POST /$DATABASE/_purge HTTP/1.1
```
{:codeblock}

_Example of using the command line to request the purge of a document:_

```sh
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/_purge \
	-X PUT \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

Provide the description of which document revisions to purge by using a JSON format document.
For example,
to purge the document with revision value `4-53b84f8bf5539a7fb7f8074d1f685e5e`,
you might use a JSON document similar to the following example.

_Example of JSON request to purge a document:_

```json
{
  "doc1":[
    "4-53b84f8bf5539a7fb7f8074d1f685e5e"
  ]
}
```
{:codeblock}

The response contains the ID and the new revision of the document,
or an error message if the update failed.

If the purge request succeeds,
the HTTP response code is [`201`](http.html#201) or [`202`](http.html#202).
The difference is that a `202` response indicates that the request was accepted,
but that the [quorum](#quorum) for the operation was not met.

If the purge request does not succeed,
the HTTP response code is [`500`](http.html#500).

_Example `201` response after a successful request and quorum was reached:_

```json
{
  "purged": {
    "doc1": {
      "ok": true,
      "purged": [
        "4-53b84f8bf5539a7fb7f8074d1f685e5e"
      ]
    }
  }
}
```
{:codeblock}

_Example `202` response after a successful request, but quorum was not reached:_

```json
{
  "purged": {
    "doc1": {
      "accepted": true,
      "purged": [
        "4-53b84f8bf5539a7fb7f8074d1f685e5e"
      ]
    }
  }
}
```
{:codeblock}

_Example response after a successful request, but no documents were purged:_

```json
{
  "purged": {
    "doc1": {
      "ok": true,
      "purged": [ ]
    }
  }
}
```
{:codeblock}

<div><!-- Reset markdown --></div>

<blockquote>
<p><strong>Note</strong>: The last example does not list any documents in the <code>purged</code> array object.
The empty array indicates that the purge request was describing documents that were:
<ul>
<li>Not leaf revision documents.</li>
<li>Already purged.</li>
</ul>
</p>
</blockquote>

<div><!-- Reset markdown --></div>

_Example `500` response after a failed request to purge documents:_

```json
{
  "error": "error",
  "reason": "internal_server_error"
}
```
{:codeblock}

### Purging multiple documents

You can request that multiple documents are purged at the same time.
Each of the listed documents must be a leaf document.
In other words,
you must specify the most recent revision of each document,
not an earlier revision.

_Example of JSON request to purge two 'leaf' documents:_

```json
{
  "doc1":[
    "4-53b84f8bf5539a7fb7f8074d1f685e5e",
    "2-98e2b4ecd9a0da76fe8b83a83234ee71"
  ]
}
```
{:codeblock}

_Example response after a successful request to purge multiple documents:_

```json
{
  "purged": {
    "doc1": {
      "ok": true,
      "purged": [
        "4-53b84f8bf5539a7fb7f8074d1f685e5e",
        "2-98e2b4ecd9a0da76fe8b83a83234ee71"
      ]
    }
  }
}
```
{:codeblock}

### Database compaction after a purge

Storage space that was used by purged documents is reclaimed automatically when a database compaction runs.

## Bulk Operations

Use the bulk document API to create and update multiple documents at the same time within a single request.
The basic operation is similar to creating or updating a single document,
except that you batch the document structure and information.

When you create new documents, the document ID is optional.
For updating existing documents,
you must provide the document ID,
revision information,
and new document values.

>	**Note:** A special case of bulk operations is the [`_bulk_get`](#the-_bulk_get-endpoint) endpoint.

<div id="request-body"></div>

### Bulk request structure

For both inserts and updates the basic structure of the JSON document in the request is the same:

Field  | Description             | Type             | Optional
-------|-------------------------|------------------|---------
`docs` | Bulk Documents Document | Array of objects | no

<div id="object-in-docs-array"></div>

Each `docs` array object has the following structure:

Field      | Description                           | Type    | Optional
-----------|---------------------------------------|---------|---------
`_id`      | Document ID                           | String  | Optional only for new documents.
`_rev`     | Document revision                     | String  | Mandatory for updates and deletes, not used for new documents.
`_deleted` | Whether the document must be deleted. | Boolean | Yes

_Example of using HTTP to create, update, or delete multiple documents:_

```http
POST /$DATABASE/_bulk_docs HTTP/1.1
Content-Type: application/json
```
{:codeblock}

_Example of using the command line to create, update, or delete multiple documents:_

```sh
curl https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com/$DATABASE/_bulk_docs \
	-X POST \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

<!--

_Example request to create, update, or delete multiple documents, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://$USERNAME:$PASSWORD@$ACCOUNT.cloudant.com");
var db = account.use($DATABASE);

db.bulk($JSON, function (err, body) {
	if (!err) {
		console.log(body);
	}
});
```
{:codeblock}

-->

_Example JSON describing the update, creation, and deletion of three documents in one bulk request:_

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
{:codeblock}

<div id="response"></div>

### Bulk request responses

The HTTP status code that is received in response indicates whether the request was fully or partially successful.
In the response body itself,
you get an array with detailed information for each document in the request.

Code | Description
-|-
`201` | The request did succeed, but this success does not imply all documents were updated. Inspect the response body to determine the status of each requested change, and [address any problems](#bulk-document-validation-and-conflict-errors).
`202` | For at least one document, the write [quorum](#quorum) was not met.

_Example response from a bulk request:_

```json
[
	{
		"id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
		"rev": "2-ff7b85665c4c297838963c80ecf481a3"
	},
	{
		"id": "5a049246-179f-42ad-87ac-8f080426c17c",
		"rev": "2-9d5401898196997853b5ac4163857a29"
	},
	{
		"id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
		"rev": "2-cbdef49ef3ddc127eff86350844a6108"
	}
]
```
{:codeblock}

### Inserting documents in bulk

To insert documents in bulk into a database,
you need to supply a JSON structure with the array of documents that you want to add to the database.
You can either include a document ID for each document,
or allow the document ID to be automatically generated.

_Example JSON for a bulk insert of three documents:_

```json
{
	"docs": [
		{
			"name": "Nicholas",
			"age": 45,
			"gender": "male",
			"_id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
			"_attachments": {

			}
		},
		{
			"name": "Taylor",
			"age": 50,
			"gender": "male",
			"_id": "5a049246-179f-42ad-87ac-8f080426c17c",
			"_attachments": {

			}
		},
		{
			"name": "Owen",
			"age": 51,
			"gender": "male",
			"_id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
			"_attachments": {

			}
		}
	]
}
```
{:codeblock}

The return code from a successful bulk insertion is [`201`](http.html#201).
The content of the returned structure indicates success
or other information messages on a per-document basis.

_Example response header after successful bulk insert of three documents:_

```http
201 Created
Cache-Control: must-revalidate
Content-Length: 269
Content-Type: application/json
Date: Mon, 04 Mar 2013 14:06:20 GMT
server: CouchDB/1.0.2 (Erlang OTP/R14B)
x-couch-request-id: e8ff64d5
```
{:codeblock}

The returned JSON contains a list of the documents that were created,
including their revision and ID values.

The content and structure of the returned JSON depends on the transaction semantics that are used for the bulk update.
For more information,
see [Bulk Documents Transaction Semantics](#bulk-documents-transaction-semantics).

Conflicts and validation errors that occur when you update documents in bulk must be handled separately.
For more information,
see [Bulk Document Validation and Conflict Errors](#bulk-document-validation-and-conflict-errors).

_Example response content after successful bulk insert of three documents:_

```json
[
	{
		"id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
		"rev": "1-54dd23d6a630d0d75c2c5d4ef894454e"
	},
	{
		"id": "5a049246-179f-42ad-87ac-8f080426c17c",
		"rev": "1-0cde94a828df5cdc0943a10f3f36e7e5"
	},
	{
		"id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
		"rev": "1-a2b6e5dac4e0447e7049c8c540b309d6"
	}
]
```
{:codeblock}

### Updating Documents in Bulk

The bulk document update procedure is similar to the insertion procedure,
except that you must specify the document ID and current revision for every document in the bulk update JSON string.

You might also choose to delete documents during a bulk update by adding a `_deleted` field with a value of `true`
to each affected document ID and revision combination within the request JSON structure.

_Example of using HTTP to do a bulk update:_

```http
POST /$DATABASE/_bulk_docs HTTP/1.1
Accept: application/json
```
{:codeblock}

_Example of using the command line to do a bulk update:_

```sh
curl -X POST "https://$ACCOUNT.cloudant.com/$DATABASE/_bulk_docs" \
	-d @request.json
```
{:codeblock}

_Example JSON structure to request bulk update of documents:_

```json
{
	"docs": [
		{
			"name": "Nicholas",
			"age": 45,
			"gender": "female",
			"_id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
			"_attachments": {

			},
			"_rev": "1-54dd23d6a630d0d75c2c5d4ef894454e"
		},
		{
			"name": "Taylor",
			"age": 50,
			"gender": "female",
			"_id": "5a049246-179f-42ad-87ac-8f080426c17c",
			"_attachments": {

			},
			"_rev": "1-0cde94a828df5cdc0943a10f3f36e7e5"
		},
		{
			"name": "Owen",
			"age": 51,
			"gender": "female",
			"_id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
			"_attachments": {

			},
			"_rev": "1-a2b6e5dac4e0447e7049c8c540b309d6"
		}
	]
}
```
{:codeblock}

The return JSON structure summarizes the updated documents,
with the new revision and ID information.

_Example JSON structure that is returned after bulk update:_

```json
[
	{
		"id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
		"rev": "2-ff7b85665c4c297838963c80ecf481a3"
	},
	{
		"id": "5a049246-179f-42ad-87ac-8f080426c17c",
		"rev": "2-9d5401898196997853b5ac4163857a29"
	},
	{
		"id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
		"rev": "2-cbdef49ef3ddc127eff86350844a6108"
	}
]
```
{:codeblock}

### Bulk Documents Transaction Semantics

If your request receives a [`202` response](http.html#202),
the only certainty is that _some_ of the document tasks were processed completely.
The response body contains the list of documents that were successfully inserted or updated during the process.

A successful document update is indicated by the presence of a new `_rev` parameter for the document,
indicating that a new document revision was successfully created.

If a document update failed,
then you get an `error` of type `conflict` for that document.
In this case,
no new revision was created.
You must submit the document update again,
with the same revision tag,
to retry the document update.

_Example bulk update response with errors:_

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
{:codeblock}

### Bulk Document Validation and Conflict Errors

The JSON returned by the `_bulk_docs` operation consists of an array of JSON structures,
one for each document in the original submission.
The returned JSON structure must be examined
to ensure that all of the documents that were submitted in the original request were successfully added to the database.

The structure of the returned information is as follows:

Field  | Description             | Type
-------|-------------------------|-----
`docs` | Bulk Documents Document | Array of objects

<div id="fields-of-objects-in-docs-array"></div>

Each `docs` array object has the following structure:

Field    | Description                        | Type
---------|------------------------------------|-----
`id`     | Document ID                        | String
`error`  | Error type.                        | String
`reason` | Error string with extended reason. | String

When a document (or document revision) is not correctly committed to the database because of an error,
you must check the `error` field to determine error type and course of action.
The error is one of [`conflict`](#conflict) or [`forbidden`](#forbidden).

#### `conflict`

The document as submitted is in conflict.
If you used the default bulk transaction mode,
then the new revision was not created.
You must resubmit the document to the database.

Conflict resolution of documents added by using the bulk docs interface is identical
to the resolution procedures used when you resolve conflict errors during replication.

#### `forbidden`

Entries with this error type indicate that the validation routine that was applied
to the document during submission returned an error.

_Example JavaScript to produce `forbidden` error as part of a validation function:_

```javascript
throw({forbidden: 'invalid recipe ingredient'});
```
{:codeblock}

_Example error message from a validation function:_

```json
{
	"id" : "7f7638c86173eb440b8890839ff35433",
	"error" : "forbidden",
	"reason" : "invalid recipe ingredient"
}
```
{:codeblock}

### The `_bulk_get` endpoint

You might need to access all the available information about multiple documents.
The `_bulk_get` endpoint is similar to the [`_all_docs`](database.html#get-documents) endpoint,
but returns information about the requested documents only.

Like the `_bulk_docs` endpoint,
the JSON document that is supplied in the request includes an array that identifies all the documents of interest.

_Example of using HTTP to do a 'bulk get' of document information:_

```http
POST /$DATABASE/_bulk_get HTTP/1.1
Accept: application/json
```
{:codeblock}

_Example of using the command line to do a 'bulk get':_

```sh
curl -X POST "https://$ACCOUNT.cloudant.com/$DATABASE/_bulk_get" \
	-H "Content-Type: application/json" \
	-d @request.json
```
{:codeblock}

_Example of a JSON object that is used to request a 'bulk get' of two documents:_

```json
{
	"docs": [
		{
			"id": "doc1"
		},
		{
			"id": "doc3"
		}
	]
}
```
{:codeblock}

_Example JSON structure that is returned after a 'bulk get':_

```json
{                                                         
	"results": [                                                         
		{                                                         
			"id": "doc01",
			"docs": [
				{
					"ok": {
						"_id": "doc01",
						"_rev": "1-f3751e2db1d92e13b0baa6bdeb874c8c",
						"simplekey": "somedata"
					}
				}
			]
		},
		{
			"id": "doc03",
			"docs": [
				{
					"ok": {
						"_id": "doc03",
						"_rev": "2-d4fc04ef748edf305a8c0ed347f269c4",
						"simplekey": "somemoredata"
					}
				}
			]
		}
	]
}
```
{:codeblock}

<div id="quorum"></div>

## Quorum - writing and reading data

In a distributed system,
it is possible that a request might take some time to complete.
A 'quorum' mechanism is used to help determine when a request,
such as a write or read,
completes successfully.

For help to understand quorum settings and their implications on dedicated Cloudant systems,
contact Cloudant support.

## TTL - Time to Live

[Time to Live ![External link icon](../images/launch-glyph.svg "External link icon")](https://en.wikipedia.org/wiki/Time_to_live){:new_window} (TTL) is a property of data,
where after a relative amount of time,
or at an absolute time,
the data is deemed to be expired.
The data itself might be deleted or moved to an alternative (archive) location.

Cloudant does _not_ support Time to Live functions.

The reason is that Cloudant documents are only 'soft' deleted,
not deleted.
The soft deletion involves replacing the original document with a [smaller record](#-tombstone-documents).
This small record or 'tombstone' is needed for replication purposes.
The record helps ensure that the correct revision to use can be identified during replication.

If the TTL capability was available in Cloudant,
the resulting potential increase in short-lived documents and soft deletion records
would mean that the database size might grow in an unbounded fashion.
