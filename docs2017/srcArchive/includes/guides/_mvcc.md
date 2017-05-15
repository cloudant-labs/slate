## Document Versioning and MVCC

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the 'Document Versioning and MVCC' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/guides/mvcc.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Multi-version concurrency control (MVCC) is how Cloudant databases ensure that all of the nodes in a database's cluster contain only the [newest version](document.html) of a document. Since Cloudant databases are [eventually consistent](cap_theorem.html), this is necessary to prevent inconsistencies arising between nodes as a result of synchronizing between outdated documents.

Multi-Version Concurrency Control (MVCC) enables concurrent read and write access to a Cloudant database. MVCC is a form of <a href="http://en.wikipedia.org/wiki/Optimistic_concurrency_control" target="_blank">optimistic concurrency</a>.
It makes both read and write operations on Cloudant databases faster because there is no need for database locking on either read or write operations. MVCC also enables synchronization between Cloudant database nodes.

### Revisions

Every document in a Cloudant database has a `_rev` field indicating its revision number.

A revision number is added to your documents by the server when you insert or modify them.
The number is included in the server response when you make changes or read a document.
The `_rev` value is constructed using a combination of a simple counter and a hash of the document.

The two main uses of the revision number are to help:

1.	Determine what documents must be replicated between servers.
2.	Confirm that a client is trying to modify the latest version of a document.

You must specify the previous `_rev` when [updating a document](document.html#update) or else your request will fail and return a [409 error](http.html#409).

<aside class="warning" role="complementary" aria-label="revnotVCS">`_rev` should not be used to build a version control system.
The reason is that it is an internal value used by the server.
In addition, older revisions of a document are transient, and therefore removed regularly.</aside>

You can query a particular revision using its `_rev`, however, older revisions are regularly deleted by a process called <a href="http://en.wikipedia.org/wiki/Data_compaction" target="blank">compaction</a>.
A consequence of compaction is that you cannot rely on a successful response when querying a particular document revision using its `_rev` to obtain a history of revisions to your document. If you need a version history of your documents, a solution is to [create a new document](document.html#documentCreate) for each revision.

### Distributed Databases and Conflicts

Distributed databases work without a constant connection to the main database on Cloudant, which is itself distributed, so updates based on the same previous version can still be in conflict.

To find conflicts, add the query parameter `conflicts=true` when retrieving a document. The document will contain a `_conflicts` array with all conflicting revisions.

To find conflicts for multiple documents in a database, write a view. An example map function is provided, that emits all conflicting revisions for every document with a conflict.


> map function to find conflicts:

```
function (doc) {
  if (doc._conflicts) {
    emit(null, [doc._rev].concat(doc._conflicts));
  }
}
```

You can then regularly query this view and resolve conflicts as needed, or query the view after each replication.

### How to resolve conflicts

Once you've found a conflict, you can resolve it in 4 steps.

 * [Get](#get-conflicting-revisions) the conflicting revisions.
 * [Merge](#merge-the-changes) them in your application or ask the user what he wants to do.
 * [Upload](#upload-the-new-revision) the new revision.
 * [Delete](#delete-old-revisions) old revisions.

Let's consider an example of how this can be done. Suppose you have a database of products for an online shop. The first version of a document might look like this example provided.

> first revision of the document

```json
{
  "_id": "74b2be56045bed0c8c9d24b939000dbe",
  "_rev": "1-7438df87b632b312c53a08361a7c3299",
  "name": "Samsung Galaxy S4",
  "description": "",
  "price": 650
}
```

As the document doesn't have a description yet, someone might add one.

> second revision of the document

```json
{
  "_id": "74b2be56045bed0c8c9d24b939000dbe",
  "_rev": "2-61ae00e029d4f5edd2981841243ded13",
  "name": "Samsung Galaxy S4",
  "description": "Latest smartphone from Samsung",
  "price": 650
}
```

At the same time, someone else - working with a replicated database - reduces the price.

> also second revision, conflicts with the previous one

```json
{
  "_id": "74b2be56045bed0c8c9d24b939000dbe",
  "_rev": "2-f796915a291b37254f6df8f6f3389121",
  "name": "Samsung Galaxy S4",
  "description": "",
  "price": 600
}
```

Then the two databases are replicated, leading to a conflict.

#### Get conflicting revisions

You get the document with `conflicts=true` like this:

`http://$USERNAME.cloudant.com/products/$_ID?conflicts=true`

And get the following response:

> example response showing conflicting revisions

```json
{
  "_id":"74b2be56045bed0c8c9d24b939000dbe",
  "_rev":"2-f796915a291b37254f6df8f6f3389121",
  "name":"Samsung Galaxy S4",
  "description":"",
  "price":600,
  "_conflicts":["2-61ae00e029d4f5edd2981841243ded13"]
}
```

The version with the changed price has been chosen arbitrarily as the latest version of the document and the conflict is noted in the `_conflicts` array. In most cases this array has only one element, but there can be many conflicting revisions.

#### Merge the changes

To compare the revisions to see what has been changed, your application gets all of the versions from the database with URLs like this:

* `http://$USERNAME.cloudant.com/products/$_ID`
* `http://$USERNAME.cloudant.com/products/$_ID?rev=2-61ae00e029d4f5edd2981841243ded13`
* `http://$USERNAME.cloudant.com/products/$_ID?rev=1-7438df87b632b312c53a08361a7c3299`

Since these two changes are for different fields of the document, it is easy to merge them.

Other conflict resolution strategies are:

* time based: first or last edit
* reporting conflicts to users and letting them decide on the best resolution
* more sophisticated merging algorithms, e.g. 3-way merges of text fields

For a practical example of how to implement these changes, see [this project with sample code](https://github.com/glynnbird/deconflict).

#### Upload the new revision

In this example, you create a document similar to the example provided, and update the database with it.

> third revision, merging changes from the two conflicting second revisions

```json
{
  "_id": "74b2be56045bed0c8c9d24b939000dbe",
  "_rev": "3-daaecd7213301a1ad5493186d6916755",
  "name": "Samsung Galaxy S4",
  "description": "Latest smartphone from Samsung",
  "price": 600
}
```

#### Delete old revisions

To delete an old revisions,
send a `DELETE` request to the URLs with the revision we want to delete.

> Example request to delete old revision

```http
DELETE https://$USERNAME.cloudant.com/products/$_ID?rev=2-61ae00e029d4f5edd2981841243ded13
```

```shell
curl "https://$USERNAME.cloudant.com/products/$_ID?rev=2-f796915a291b37254f6df8f6f3389121" -X DELETE
```

After this, conflicts are resolved.
You can verify this by `GET`ting the document again with the `conflicts` parameter set to `true`.
