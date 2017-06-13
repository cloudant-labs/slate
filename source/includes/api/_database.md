## Databases

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the Databases topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/database.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Cloudant databases contain JSON objects.
These JSON objects are called [documents](document.html#documents).
All documents must be contained in a database.

### Create

> Create a database

```http
PUT /$DATABASE HTTP/1.1
HOST: $ACCOUNT.cloudant.com
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE -X PUT
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.db.create($DATABASE, function (err, body, headers) {
  if (!err) {
    console.log('database created!');
  }
});
```

To create a database, make a PUT request to `https://<account>.cloudant.com/$DATABASE`.

The database name must start with a lowercase letter and contain only the following characters:

 - Lowercase characters (a-z)
 - Digits (0-9)
 - Any of the characters _, $, (, ), +, -, and /
 
#### Database topology

It is possible to modify the configuration of a database sharding topology of a database on dedicated database clusters.
This can be done at the time a database is created.
However,
poor choice for configuration parameters can adversely affect database performance.

For more information about modifying database configuration in a dedicated database environment,
please contact Cloudant support.

<aside class="warning" role="complementary" aria-label="noconfigmod">It is not possible to modify the configuration used for databases on multi-tenant clusters.</aside>

#### Response

> Response for successful creation:

```
HTTP/1.1 201 Created

{
  "ok": true
}
```

If creation succeeds, you get a [201 or 202 response](http.html#201).
In case of an error,
the HTTP status code tells you what went wrong.

Code | Description
-----|--------------
201 |	Database created successfully
202 |	The database has been successfully created on some nodes, but the number of nodes is less than the write quorum.
403 |	Invalid database name.
412 |	Database already exists.

### Read

> Create a database

```http
GET /$DATABASE HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.db.get($DATABASE, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Making a GET request against `https://<account>.cloudant.com/$DATABASE` returns details about the database,
such as how many documents it contains.

<div></div>

> Example response:

```json
{
  "update_seq": "9824119-g1AAAAIjeJzLYWBg4MhgTmHQSElKzi9KdUhJMtYrKMrMTS1KLU5NLErOMDAw1EvOyS9NScwr0ctLLckB6mBKZEiS____f1YSg9DBKajazYjQnqQAJJPsoSbsfEC6A5IcQCbEQ03YI4BqgiExJiSATKiHmrC3l3Q35LEASYYGIAU0ZD7IlF1KqKYYEW3KAogp-0Gm7HYg1y0HIKbcB5myX4T0eIGY8gBiCiRcPmQBAB4CuUQ",
  "db_name": "db",
  "sizes": {
    "file": 46114703224,
    "external": 193164408719,
    "active": 34961621142
  },
  "purge_seq": 0,
  "other": {
    "data_size": 193164408719
  },
  "doc_del_count": 5564,
  "doc_count": 9818541,
  "disk_size": 46114703224,
  "disk_format_version": 6,
  "compact_running": true,
  "instance_start_time": "0"
}
```

The elements of the returned structure are shown in the following table. 

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
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><code>compact_running</code></td>
<td align="left">Set to true if the database compaction routine is operating on this database.</td>
</tr>
<tr class="odd">
<td align="left"><code>db_name</code></td>
<td align="left">The name of the database.</td>
</tr>
<tr class="odd">
<td align="left"><code>disk_format_version</code></td>
<td align="left">The version of the physical format used for the data when it is stored on disk.</td>
</tr>
<tr class="odd">
<td align="left"><code>disk_size</code></td>
<td align="left">Size in bytes of the data as stored on the disk. Views indexes are not included in the calculation.</td>
</tr>
<tr class="odd">
<td align="left"><code>doc_count</code></td>
<td align="left">A count of the documents in the specified database.</td>
</tr>
<tr class="odd">
<td align="left"><code>doc_del_count</code></td>
<td align="left">Number of deleted documents.</td>
</tr>
<tr class="odd">
<td align="left"><code>instance_start_time</code></td>
<td align="left">Always 0.</td>
</tr>
<tr class="odd">
<td align="left"><code>purge_seq</code></td>
<td align="left">The number of purge operations on the database.</td>
</tr>
<tr class="odd">
<td align="left"><code>update_seq</code></td>
<td align="left">An opaque string describing the state of the database. It should not be relied on for counting the number of updates.</td>
</tr>
<tr class="odd">
<td align="left"><code>other</code></td>
<td align="left">JSON object containing a `data_size` field.</td>
</tr>
<tr class="odd">
<td align="left"><code>sizes</code></td>
<td align="left">JSON object containing <code>file</code>, <code>external</code>, and <code>active</code> fields which are 
described here.
<ul>
<li><code>file</code>: Size in bytes of data stored on the disk. Indexes are not included in the calculation. The <code>disk_size</code> field is an alias for the <code>file</code> field. Note that this size includes data pending compaction.</li> 
<li><code>external</code>: Size in bytes of uncompressed user data. This is the billable data size. The <code>other/data_size</code> field is an alias for the <code>external</code> field.</li> 
<li><code>active</code>: Size in bytes of data stored internally (excluding old revisions). </li>
</ul>
</td> 
</tr>
</tbody>
</table>


### Get Databases

> Get all databases

```http
GET /_all_dbs HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_all_dbs \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.db.list(function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

To list all the databases in an account,
make a GET request against `https://<account>.cloudant.com/_all_dbs`.

<div></div>

> Example response:

```json
[
   "_users",
   "contacts",
   "docs",
   "invoices",
   "locations"
]
```

The response is an array with all database names.

### Get Documents

> Getting all documents in a database:

```http
GET /_all_docs HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_all_docs
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.list(function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

> Getting all documents in a database that match at least one of the specified keys:

```http
GET /_all_docs?keys=["somekey","someotherkey"] HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_all_docs?keys=["somekey","someotherkey"]
```

To list all the documents in a database, make a GET request against `https://<account>.cloudant.com/$DATABASE/_all_docs`.

The `_all_docs` endpoint accepts these query arguments:

Argument | Description | Optional | Type | Default
---------|-------------|----------|------|--------
`conflicts` | Can only be set if `include_docs` is `true`. Adds information about conflicts to each document. | yes | Boolean | false
`deleted_conflicts` | Returns information about deleted conflicted revisions | yes | boolean | false
`descending` | Return the documents in descending by key order | yes | boolean | false
`endkey` | Stop returning records when the specified key is reached | yes | string |  
`include_docs` | Include the full content of the documents in the return | yes | boolean | false
`inclusive_end` | Include rows whose key equals the endkey | yes | boolean | true
`key` | Return only documents with IDs that match the specified key | yes | string |  
`keys` | Return only documents with IDs that match one of the specified keys | yes | list of strings |  
`limit` | Limit the number of the returned documents to the specified number | yes | numeric | 
`meta` | Short-hand combination of all three arguments: `conflicts`, `deleted_conflicts`, and `revs_info`. Using `meta=true` is the same as using `conflicts=true&deleted_conflicts=true&revs_info=true` | yes | boolean | false
`r` | Specify the [read quorum](document.html#quorum---writing-and-reading-data) value | yes | numeric | 2
`revs_info` | Includes detailed information for all known document revisions | yes | boolean | false
`skip` | Skip this number of records before starting to return the results | yes | numeric | 0
`startkey` | Return records starting with the specified key | yes | string |

<aside class="warning" role="complementary" aria-label="includedocsperformance">Note that using `include_docs=true` might have [performance implications](creating_views.html#include_docs_caveat).</aside>

<aside class="warning" role="complementary" aria-label="usepostnotget">When using the `keys` argument,
it might be easier to use `POST` rather than `GET` if you need a large number of strings to list the desired keys.</aside>

<div></div>

> Example response after requesting all documents in a database:

```json
{
  "total_rows": 3,
  "offset": 0,
  "rows": [{
    "id": "5a049246-179f-42ad-87ac-8f080426c17c",
    "key": "5a049246-179f-42ad-87ac-8f080426c17c",
    "value": {
      "rev": "2-9d5401898196997853b5ac4163857a29"
    }
  }, {
    "id": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
    "key": "96f898f0-f6ff-4a9b-aac4-503992f31b01",
    "value": {
      "rev": "2-ff7b85665c4c297838963c80ecf481a3"
    }
  }, {
    "id": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
    "key": "d1f61e66-7708-4da6-aa05-7cbc33b44b7e",
    "value": {
      "rev": "2-cbdef49ef3ddc127eff86350844a6108"
    }
  }]
}
```

The response is a JSON object containing all documents in the database matching the parameters. The following table describes the meaning of the individual fields:

Field |	Description |	Type
------|-------------|-------
offset |	Offset where the document list started |	numeric
rows |	Array of document objects |	array
total_rows |	Number of documents in the database/view matching the parameters of the query |	numeric
update_seq |	Current update sequence for the database |	string

### Get Changes

> Example request to get list of changes made to documents in a database:

```http
GET /$DATABASE/_changes HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_changes \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.db.changes($DATABASE, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Making a GET request against `https://<account>.cloudant.com/$DATABASE/_changes` returns a list of changes made to documents in the database,
including insertions,
updates,
and deletions.

When a `_changes` request is received,
one replica for each shard of the database is asked to provide a list of changes.
These responses are combined and returned to the original requesting client.

However,
the distributed nature of Cloudant databases,
and in particular the shard and fault-tolerant characteristics,
means that the response provided by the `_changes` request might be different
to the behavior you expect.

In particular,
if you ask for a list of changes `_since` a given sequence identifier,
you get the requested information in response,
_but_ you might also get changes that were made before the change indicated by the sequence identifier.
The reason for this,
along with implications for applications,
is explained in the
[replication guide](replication-guide.html#how-does-replication-affect-the-list-of-changes?).

<aside class="warning" role="complementary" aria-label="cloudantNotCouch">It is essential that any application using the <code>_changes</code> request should be able to process correctly a list of changes that might:
<ul>
<li>Have a different order for the changes listed in the response,
when compared with an earlier request for the same information.</li>
<li>Include changes that are considered to be prior to the change specified by the sequence identifier.</li>
<ul></aside>

`_changes` accepts several optional query arguments:

Argument | Description | Supported Values | Default 
---------|-------------|------------------|---------
`conflicts` | Can only be set if `include_docs` is `true`. Adds information about conflicts to each document. | boolean | false 
`descending` | Return the changes in sequential order. | boolean | false | 
`doc_ids` | To be used only when `filter` is set to `_doc_ids`. Filters the feed so that only changes to the specified documents are sent. <br>**Note**: The `doc_ids` parameter only works with versions of Cloudant that are compatible with CouchDB 2.0. See [API: GET / documentation](https://docs.cloudant.com/advanced.html#get-/) for more information. | A JSON array of document IDs | |
`feed` | Type of feed required. For details see the [`feed` information](database.html#the-feed-argument). | `"continuous"`, `"longpoll"`, `"normal"` | `"normal"`
`filter` | Name of [filter function](design_documents.html#filter-functions) to use to get updates. The filter is defined in a [design document](design_documents.html). | string | no filter
`heartbeat` | Time in milliseconds after which an empty line is sent during `feed=longpoll` or `feed=continuous` if there have been no changes. | any positive number | no heartbeat | 
`include_docs` | Include the document as part of the result. | boolean | false |
`limit` | Maximum number of rows to return. | any non-negative number | none |  
`since` | Start the results from changes _after_ the specified sequence identifier. For details see the [`since` information](database.html#the-since-argument). | sequence identifier or `now` | 0 | 
`style` | Specifies how many revisions are returned in the changes array. The default, `main_only`, only returns the current "winning" revision; `all_docs` returns all leaf revisions, including conflicts and deleted former conflicts. | `main_only`, `all_docs` | `main_only` | 
`timeout` | Number of milliseconds to wait for data before terminating the response. If the `heartbeat` setting is also supplied, it takes precedence over the `timeout` setting. | any positive number | |

<aside class="warning" role="complementary" aria-label="includedocsperformance2">Note that using `include_docs=true` might have [performance implications](creating_views.html#include_docs_caveat).</aside>

#### The `feed` argument

The `feed` argument changes how Cloudant sends the response.
By default,
`_changes` reports all changes,
then the connection closes.

If you set `feed=longpoll`,
requests to the server remain open until changes are reported.
This can help monitor changes specifically instead of continuously.

<div id="continuous-feed"></div>

> Example response, continuous changes feed:

```
{
  "seq": "1-g1AAAAI7eJyN0EsOgjAQBuD6SPQWcgLSIm1xJTdRph1CCEKiuHClN9Gb6E30JlisCXaDbGYmk8mXyV8QQubZRBNPg6r2GGsI_BoP9YlS4auiOuqkrP0S68JcjhMCi6Zp8sxMO7OYISgUK3AF1iOAZyqsv8jog4Q6YIxyF4n6kLhFNs4nIQ-kUtJFwj5k2yJnB0lxSbkIhgdSTk0lF9OMc-0goCpikg7PxUI3C907KMKUM9AuJP9CDws9O0ghAtc4PB8LvSz0k5HgKTCU-RtU1qyw",
  "id": "2documentation22d01513-c30f-417b-8c27-56b3c0de12ac",
  "changes": [{
    "rev": "1-967a00dff5e02add41819138abb3284d"
  }]
}
{
  "seq": "2-g1AAAAI7eJyN0E0OgjAQBeD6k-gt5ASkRdriSm6iTDuEEIREceFKb6I30ZvoTbBYE-wG2cxMmubLyysIIfNsoomnQVV7jDUEfo2H-kSp8FVRHXVS1n6JdWF-jhMCi6Zp8sxcO_MwQ1AoVuAKrEcAz0xYf5HRBwl1wBjlLhL1IXGLbJwkIQ-kUtJFwj5k2yJnJ0mKS8pFMLyQcmomuZhlnGuXBqiKmKTDe7HQzUL3Doow5Qy0C8m_0MNCzw5SiMA1Du_HQi8L_RQteAoMZf4GVgissQ",
  "id": "1documentation22d01513-c30f-417b-8c27-56b3c0de12ac",
  "changes": [{
    "rev": "1-967a00dff5e02add41819138abb3284d"
  }]
}
{
  "seq": "3-g1AAAAI7eJyN0EsOgjAQBuD6SPQWcgLSIqW4kpso0w4hBCFRXLjSm-hN9CZ6EyyUBLtBNjOTyeTL5M8JIct0poijQJZHjBR4boWn6kJp4Mq8PKu4qNwCq1xfTmMCq7qus1RPB71YIEgMNmALbEAAR1fYdsikRXzlMUa5jYRDSNQgO-sTn3tCSmEj_hCyb5Brh0xbJME15YE3PpBiriu56aade_8NUBkyQcfnYqCHgZ49FGLCGSgbEn-hl4HePSQRgSscn4-BPgb6CTrgCTAU2RdXOqyy",
  "id": "1documentation22d01513-c30f-417b-8c27-56b3c0de12ac",
  "changes": [{
    "rev": "2-eec205a9d413992850a6e32678485900"
  }],
  "deleted": true
}
{
  "seq": "4-g1AAAAI7eJyN0EEOgjAQBdAGTfQWcgLSIm1xJTdRph1CCEKiuHClN9Gb6E30JlisCXaDbGYmTfPy80tCyDyfaOJrUPUeEw1h0OChOVEqAlXWR51WTVBhU5qfXkpg0bZtkZtrZx5mCArFClyBDQjgmwnrL-J9kEiHjFHuIvEQknTIxkkS8VAqJV0kGkK2HXJ2kmS4pFyE4wuppmaSi1nGufZpgKqYSTq-FwvdLHTvoRgzzkC7kPwLPSz07CGFCFzj-H4s9LLQT9GCZ8BQFm9Y9qyz",
  "id": "2documentation22d01513-c30f-417b-8c27-56b3c0de12ac",
  "changes": [{
    "rev": "2-eec205a9d413992850a6e32678485900"
  }],
  "deleted": true
}
```

If you set `feed=continuous`,
new changes are reported without closing the connection.
This means that the database connection stays open until explicitly closed,
and that all changes are returned to the client as soon as possible after they occur.

Each line in the continuous response is either empty or a JSON object representing a single change.
This ensures that the format of the report entries reflects the continuous nature of the changes,
while maintaining validity of the JSON output.

<div></div>

#### The `filter` argument

The `filter` argument designates a pre-defined [filter function](design_documents.html#filter-functions) to apply to the changes feed.
Additionally, there are several built-in filters available:

*	`_design`: The `_design` filter accepts only changes to design documents.
*	`_doc_ids`: This filter accepts only changes for documents whose ID is specified in the `doc_ids` parameter.
*	`_selector`: accepts only changes for documents which match a specified selector, defined using the same [selector syntax](cloudant_query.html#selector-syntax) used for [`_find`](cloudant_query.html#finding-documents-using-an-index).
*	`_view`: allows you to use an existing [map function](creating_views.html#a-simple-view) as the filter.

<div></div>

#### The `since` argument

The `since` argument enables you to get a list of changes that occurred _after_ a specified sequence identifier.
If the `since` identifier is 0 (the default),
or omitted,
the request returns all changes.
If the `since` identifier is `now`,
the request asks for changes made after the current time.

The distributed nature of Cloudant can affect the results you get in a response.
For example,
if you request a list of changes twice,
using the same `since` sequence identifier both times,
the order of changes in the resulting list might not be the same.

You might also see some results that appear to be from _before_ the `since` parameter.
The reason is that you might be getting results from a different replica of a shard (a shard replica).

Shard replicas automatically and continuously replicate to each other
and therefore eventually have the same data.
However,
at any given point in time,
a shard replica might differ from another shard replica
because the replication between them has not completed yet.

When you request a list of changes,
normally the same replicas are used to respond.
But if the node holding the shard replica is unavailable,
the system substitutes a corresponding shard replica held on another node.
To guarantee that you see all the applicable changes,
the most recent checkpoint between the replicas is used -
effectively 'rolling back' to the most recent point in time when the shard replicas were confirmed to be in agreement with each other.
This 'rolling back' means you might see changes listed that took place 'before' your `since` sequence identifier.

It is very important that your application is able to deal with a given change being reported more than once if you issue a `_changes` request several times.

More information about the behavior of the `_changes` response is
provided in the
[replication guide](replication_guide.html#how-does-replication-affect-the-list-of-changes?).

<div id="changes_responses"></div>

#### Responses from the `_changes` request

> Example response:

```
{
  "results": [{
    "seq": "1-g1AAAAI9eJyV0EsKwjAUBdD4Ad2FdQMlMW3TjOxONF9KqS1oHDjSnehOdCe6k5oQsNZBqZP3HiEcLrcEAMzziQSB5KLeq0zyJDTqYE4QJqEo66NklQkrZUr7c8wAXzRNU-T22tmHGVMUapR2Bdwj8MBOvu4gscQyUtghyw-CYJ-SOWXTUSJMkKQ_UWgfsnXIuYOkhCCN6PBGqqmd4GKXda4OGvk0VCcCweHFeOjmoXubiEREIyb-KMdLDy89W4nTVGkqhhfkoZeHvkrimMJYrYo31bKsIg",
    "id": "foo",
    "changes": [{
      "rev": "1-967a00dff5e02add41819138abb3284d"
    }]
  }],
  "last_seq": "1-g1AAAAI9eJyV0EsKwjAUBdD4Ad2FdQMlMW3TjOxONF9KqS1oHDjSnehOdCe6k5oQsNZBqZP3HiEcLrcEAMzziQSB5KLeq0zyJDTqYE4QJqEo66NklQkrZUr7c8wAXzRNU-T22tmHGVMUapR2Bdwj8MBOvu4gscQyUtghyw-CYJ-SOWXTUSJMkKQ_UWgfsnXIuYOkhCCN6PBGqqmd4GKXda4OGvk0VCcCweHFeOjmoXubiEREIyb-KMdLDy89W4nTVGkqhhfkoZeHvkrimMJYrYo31bKsIg",
  "pending": 0
}
```

The response from a `_changes` request is a JSON object containing a list of the changes made to documents within the database.
The following table describes the meaning of the individual fields:

Field | Description | Type
------|-------------|------
`changes` | An array listing the changes made to the specific document. | Array
`deleted` | Boolean indicating if the corresponding document was deleted. If present, it always has the value `true`. | Boolean
`id` | Document identifier. | String
`last_seq` | Identifier of the last of the sequence identifiers. Currently this is the same as the sequence identifier of the last item in the `results`. | String
`results` | Array of changes made to the database. | Array
`seq` | Update sequence identifier. | String

#### Important notes about `_changes`

When using `_changes`,
you should be aware that:

-	The results returned by `_changes` are partially ordered. In other words, the order is not guaranteed to be preserved for multiple calls. You might decide to get a current list using `_changes` which includes the [`last_seq` value](database.html#changes_responses), then use this as the starting point for subsequent `_changes` lists by providing the `since` query argument.
-	Although shard copies of the same range contain the same data, their `_changes` history is often unique. This is a result of how writes have been applied to the shard. For example, they may have been applied in a different order. To be sure all changes are reported for your specified sequence, it might be necessary to go further back into the shard's history to find a suitable starting point from which to start reporting the changes. This might give the appearance of duplicate updates, or updates that are apparently prior to the specified `since` value.
-	`_changes` reported by a given shard are always presented in order. But the ordering between all the contributing shards might appear to be different. For more information, see [this example](https://gist.github.com/smithsz/30fb97662c549061e581).
-	Sequence values are unique for a shard, but might vary between shards. This means that if you have sequence values from different shards, you cannot assume that the same sequence value refers to the same document within the different shards.

<div id="post"> </div>

#### Using `POST` to get changes

> Example of `POST`ing to the `_changes` endpoint

```http
<<<<<<< HEAD
POST /$DATABASE/_changes HTTP/1.1
Host: <account>.cloudant.com
=======
POST /$DB/_changes?filter=_selector HTTP/1.1
Host: $USERNAME.cloudant.com
>>>>>>> master
Content-Type: application/json
```

```shell
<<<<<<< HEAD
curl -X POST "https://$ACCOUNT.cloudant.com/$DATABASE/_changes" -d @request.json
=======
curl -X POST "https://$USERNAME.cloudant.com/$DB/_changes?filter=_selector" -d @request.json
>>>>>>> master
```

```json
{
  "selector": {"z" : {"$gte" : 1}}
}
```

Instead of `GET`, you can also use `POST` to query the changes feed.
The only difference if you are using `POST` _and_ you are using either of the `docs_ids` or `selector` filters,
is that it is possible to include the `"doc_ids" : [...]` or `"selector": {...}` parts in the request body.
All other parameters are expected to be in the query string,
the same as using `GET`.

### Deleting a database

> Example request to delete a Cloudant database:

```http
DELETE /$DATABASE HTTP/1.1
Host: <account>.cloudant.com
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE \
     -X DELETE \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.db.destroy($DATABASE, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

To delete a databases and its contents, make a DELETE request to `https://<account>.cloudant.com/$DATABASE`.

<aside class="warning" role="complementary" aria-label="deletecheck">There is no additional check to ensure that you really intended to delete the database ("Are you sure?").</aside>

<div></div>

> Example response:

```
{
  "ok": true
}
```

The response confirms successful deletion of the database or describes any errors that occurred, i.e. if you try to delete a database that does not exist.

