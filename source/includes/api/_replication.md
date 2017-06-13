<div id="ReplicationAPI"></div>

## Replication

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the Replication topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/replication.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Cloudant replication is the process that synchronizes ('syncs') the state of two databases.
Any change which has occurred in the source database is reproduced in the target database.
You can create replications between any number of databases, whether continuous or not.

Depending on your application requirements, you use replication to share and aggregate state and content.

Replication takes place in one direction only.
To keep two databases synchronized with each other, you must replicate in both directions.
This means that you must replicate from `database1` to `database2`, and separately from `database2` to `database1`.

<aside class="warning" role="complementary" aria-label="performanceimpact">Replications can severely impact the performance of a Cloudant cluster. Performance testing is recommended to understand the impact on your environment under an increasing number of concurrent replications.</aside>

<aside class="warning" role="complementary" aria-label="continuousequalslotsofcalls">Continuous replication can result in a large number of internal calls. This might affect costs for multi-tenant users of Cloudant systems. Continuous replication is disabled by default.</aside>

<aside class="warning" role="complementary" aria-label="targetmustexist">The target database must exist. It is not automatically created if it does not exist. Add `"create_target":true` to the JSON document describing the replication if the target database does not exist prior to replication.</aside>

<aside class="warning" role="complementary" aria-label="lookafterdatabases">Replicator databases must be maintained and looked after,
just like any other valuable data store.
For more information,
see [replication database maintenance](replication.html#replication-database-maintenance).</aside>

Replications are created in one of two ways:

1. A replication can be created using a [replication document](#replication-document-format) in the `_replicator` database. Creating and modifying replications in this way allows you to control replication in the same as working with other documents. Replication jobs created this way will be resumed after a node restart. 
2. A replication can be started by `POST`ing a JSON document describing the desired replication directly to the `/_replicate` endpoint. Replication jobs created this way are not resumed if the node they run on is restarted. 

### Replication document format

<aside class="warning" role="complementary" aria-label="usefullurl">You must use the *full* URL when specifying the source and target databases in a replication document.</aside>

The format of the document used to describe a replication is as follows:

Field&nbsp;Name | Required | Description
-----------|----------|-------------
`source` | yes | Identifies the database to copy revisions from. Can be a database URL, or an object whose url property contains the full URL of the database.
`target` | yes | Identifies the database to copy revisions to. Same format and interpretation as source. Does not have to be the same value as the `source` field.
`continuous` | no | Continuously syncs state from the `source` to the `target`, only stopping when deleted.
`create_target` | no | A value of `true` tells the replicator to create the `target` database if it does not exist.
`doc_ids` | no | Array of document IDs; if given, only these documents are replicated.
`filter` | no | Name of a [filter function](design_documents.html#filter-functions), defined in a design document. The filter function determines which documents get replicated. Note that using the `selector` option provides performance benefits compared with using the `filter` option. You should use the `selector` option where possible.
`proxy` | no | Proxy server URL.
`selector` | no | Provide a simple filter to select the documents that are included in the replication. Using the `selector` option provides performance benefits compared with using the `filter` option. More information about `selector` is available [here](replication.html#selector-field).
`since_seq` | no | Sequence from which the replication should start. More information about `since_seq` is available [here](replication.html#since-seq-field).
<div id="checkpoints">`use_checkpoints`</div> | no | Indicate whether to create checkpoints. Checkpoints greatly reduce the time and resources needed for repeated replications. Setting this to `false` removes the requirement for write access to the `source` database. Defaults to `true`.
`user_ctx` | no | An object containing the username and optionally an array of roles, for example: `"user_ctx": {"name": "jane", "roles": ["admin"]} `. This is needed for the replication to show up in the output of `/_active_tasks`.

<div id="selector-field"></div>

#### The `selector` field

If you do not want to replicate the entire contents of a database,
you can specify a simple filter in the `selector` field.
The filter takes the form of a [Cloudant Query](cloudant_query.html) selector object.

Using a selector object provides performance benefits when compared with using a
[filter function](design_documents.html#filter-functions).
You should use the `selector` option where possible.

> Example `selector` object in a replication document:

```
{
	"source": "https://$USERNAME1:$PASSWORD1@$USERNAME1.cloudant.com/$DATABASE1",
	"target": "https://$USERNAME2:$PASSWORD2@$USERNAME2.cloudant.com/$DATABASE2",
	"selector": {
		"_id": {
			"$gte": "d2"
		}
	},
	"continuous": true
}
```

The selector object identifies a field (such as `_id` in the example),
and an expression (such as `"$gte": "d2"`) that must be true for that field
in order for the selector to allow the document to be replicated.
In the example,
only documents that have a `_id` field with a value greater than or equal to `"d2"` are replicated.

<div></div>

> Example error response if the selector is not valid:

```
{
	"error": "bad request",
	"reason": "<details of the problem>"
}
```

If there is a problem with the request,
an HTTP [`400`](http.html#400) error is returned,
with more details about the problem in the `"reason"` field of the response.
The reason might be one of:

-	The Cloudant Query selector object is missing.
-	The selector object is not valid JSON.
-	The selector object does not describe a valid Cloudant Query.

More information about using a `selector` object is available in the [Apache CouchDB documentation](http://docs.couchdb.org/en/2.0.0/api/database/changes.html#selector).

<div id="since-seq-field"></div>

#### The `since_seq` field

If you do not want to replicate the entire contents of a database,
you can specify a 'replication sequence value' in the `since_seq` field.

The replication sequence value indicates how far you have progressed 'through' a database,
for example as part of a replication.
Setting the contents of the `since_seq` field to this value ensures that the replication starts from that point,
rather than from the very beginning.

This field is especially useful for creating incremental copies of databases. To do this:

1.	Find the ID of the [checkpoint](replication.html#checkpoints) document for the last replication. It is stored in the  `_replication_id` field of the replication document in the [`_replicator` database](replication.html#replicator-database).
2.	Open the checkpoint document at `/$DATABASE/_local/<_replication_id>`, where `<_replication_id>` is the ID you found in the previous step, and `$DATABASE` is the name of the source or the target database. The document usually exists on both databases but might only exist on one.
3.	Search for the `recorded_seq` field of the first element in the history array.
4.	Set the `since_seq` field in the replication document to the value of the `recorded_seq` field.
5.	Start replicating to a new database.

<div id="replicator-database"></div>

### The `/_replicator` database

The `/_replicator` database is a special database where you can `PUT` or `POST` documents to trigger replications, or `DELETE` to cancel ongoing replications. These documents have exactly the same content as the JSON documents you can `POST` to the [`/_replicate/`](replication.html#the-/_replicate-endpoint) endpoint. The fields supplied in the replication document are `source`, `target`, `continuous`, `create_target`, `doc_ids`, `filter`, `proxy`, `query_params`, `use_checkpoints`. These fields are described in the [Replication document format](#replication-document-format).

Replication documents can have a user defined `_id`.

The names of the source and target databases do not have to be the same.

<aside class="warning" role="complementary" aria-label="ignorethesedocs">All design documents and `_local` documents added to the `/_replicator` database are ignored.</aside>

#### Creating a replication

> Example instructions for creating a replication document:

```shell
curl -X PUT https://$ACCOUNT.cloudant.com/_replicator/replication-doc -H 'Content-Type: application/json' -d @replication-document.json
#assuming replication-document.json is a json file with the following content:
```

```http
PUT /_replicator/replication-doc HTTP/1.1
Content-Type: application/json
```

> Example replication document:

```json
{
  "source": "https://<account1>.cloudant.com/<database1>",
  "target": "https://<account2>.cloudant.com/<database2>",
  "create_target": true,
  "continuous": true
}
```

To start a replication, [add a replication document](#replication-document-format) to the `_replicator` database.

<div></div>

####(Optional) Creating a replication to two Bluemix environments

You can replicate a Cloudant database to multiple Bluemix environments. When you set up the replication job for each environment, the source database and target database names you provide must use this format, `https://<account>.cloudant.com/$DATABASE`. You create the database name, `$DATABASE`, and add it to the URL format. Do not copy the `URL` field from the `VCAP_SERVICES` environment variable. 

#### Monitoring a replication

> Example instructions for monitoring a replication:

```shell
curl https://$ACCOUNT.cloudant.com/_active_tasks
```

```http
GET /_active_tasks HTTP/1.1
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.request({
  path: '_active_tasks'
}, function (err, body, headers) {
  if (!err) {
    console.log(body.filter(function (task) {
      return (task.type === 'replication');
    })); 
  }
});
```

> Example response of active task including continuous replication:

```json
[
  {
    "user": null,
    "updated_on": 1363274088,
    "type": "replication",
    "target": "https://repl:*****@tsm.cloudant.com/user-3dglstqg8aq0uunzimv4uiimy/",
    "docs_read": 0,
    "doc_write_failures": 0,
    "doc_id": "tsm-admin__to__user-3dglstqg8aq0uunzimv4uiimy",
    "continuous": true,
    "checkpointed_source_seq": "403-g1AAAADfeJzLYWBgYMlgTmGQS0lKzi9KdUhJMjTRyyrNSS3QS87JL01JzCvRy0styQGqY0pkSLL___9_VmIymg5TXDqSHIBkUj1YUxyaJkNcmvJYgCRDA5AC6tuflZhGrPsgGg9ANAJtzMkCAPFSStc",
    "changes_pending": 134,
    "pid": "<0.1781.4101>",
    "node": "dbcore@db11.julep.cloudant.net",
    "docs_written": 0,
    "missing_revisions_found": 0,
    "replication_id": "d0cdbfee50a80fd43e83a9f62ea650ad+continuous",
    "revisions_checked": 0,
    "source": "https://repl:*****@tsm.cloudant.com/tsm-admin/",
    "source_seq": "537-g1AAAADfeJzLYWBgYMlgTmGQS0lKzi9KdUhJMjTUyyrNSS3QS87JL01JzCvRy0styQGqY0pkSLL___9_VmI9mg4jXDqSHIBkUj1WTTityWMBkgwNQAqob39WYhextkE0HoBoBNo4MQsAFuVLVQ",
    "started_on": 1363274083
  }
]
```

> Example response of active task including single replication:

```json
[
  {
    "pid": "<0.1303.0>",
    "replication_id": "e42a443f5d08375c8c7a1c3af60518fb+create_target",
    "checkpointed_source_seq": 17333,
    "continuous": false,
    "doc_write_failures": 0,
    "docs_read": 17833,
    "docs_written": 17833,
    "missing_revisions_found": 17833,
    "progress": 3,
    "revisions_checked": 17833,
    "source": "http://<account>.cloudant.com/db/",
    "source_seq": 551202,
    "started_on": 1316229471,
    "target": "test_db",
    "type": "replication",
    "updated_on": 1316230082
  }
]
```

To monitor replicators currently in process, make a `GET` request to `https://<account>.cloudant.com/_active_tasks`.
This returns any active tasks, including replications. To filter for replications, look for documents with `"type": "replication"`.

If you monitor the `_active_tasks` and find that the state of a replication is not changing,
you might have a 'stalled' replication.
If you are sure that the replication has stalled,
contact Cloudant support for assistance.

For more details about the information provided by `_active_tasks`, see [Active tasks](active_tasks.html).

<div></div>

#### Delete

> Example instructions for deleting a replication document:

```http
DELETE /_replicator/replication-doc?rev=1-... HTTP/1.1
```

```shell
curl -X DELETE https://$ACCOUNT.cloudant.com/_replicator/replication-doc?rev=1-...
```

To cancel a replication, simply [delete its replication document](document.html#document-delete) from the `_replicator` database.

If the replication is in an [`error` state](advanced_replication.html#replication-status), the replicator makes repeated attempts to achieve a successful replication. A consequence is that the replication document is updated with each attempt. This also changes the document revision value. Therefore, you should get the revision value immediately before deleting the document, otherwise you might get an [HTTP 409 "document update conflict"](http.html#409) response.

### The /\_replicate endpoint

> Example instructions for starting a replication:

```shell
curl -H 'Content-Type: application/json' -X POST "https://$ACCOUNT.cloudant.com/_replicate" -d @replication-doc.json
#with the file replication-doc.json containing the required replication.
```

```http
POST /_replicate HTTP/1.1
Content-Type: application/json
```
> Example document describing the required replication:

```json
{
  "source": "http://<account>.cloudant.com/example-database",
  "target": "http://<account>.example.org/example-target-database"
}
```

It is preferable to use the [Replicator Database](replication.html#the-/_replicator-database) to manage replication.
Details of why are provided [here](replication.html#avoiding-the-/_replicate-endpoint).

However, replication can also be triggered by sending a `POST` request directly to the `/_replicate` API URL. The `POST` contains a JSON document that describes the desired replication.

-   **Method**: `POST`
-   **Path**: `/_replicate`
-   **Request**: Replication specification
-   **Response**: TBD
-   **Roles permitted**: \_admin

#### Return Codes

Code | Description
-----|------------
`200` | Replication request successfully completed.
`202` | Continuous replication request has been accepted.
`404` | Either the source or target database was not found.
`500` | JSON specification was invalid.

Use this call to request, configure, or stop, a replication operation.

The specification of the replication request is controlled through the JSON content of the request. The JSON should be an object with fields defining the source, target and other options. The fields of the JSON request are as follows:

-   **cancel**: (Optional) Cancels the replication.
-   **continuous**: (Optional) Configure the replication to be continuous.
-   **create\_target**: (Optional) Creates the target database.
-   **doc\_ids**: (Optional) Array of document IDs to be synchronized.
-   **proxy**: (Optional) Address of a proxy server through which replication should occur.
-   **source**: Source database URL, including user name and password.
-   **target**: Target database URL, including user name and password.

#### Avoiding the /\_replicate endpoint

You should use the `/_replicator` database in preference to the `/_replicate` endpoint.

A significant reason for this is that in the event of problem during replication,
such as a stall,
timeout,
or application crash,
a replication defined within the `/_replicator` database is automatically restarted by the system.

If you defined a replication by sending a request to the `/_replicate` endpoint,
it cannot be restarted by the system if a problem occurs because the replication request does not persist.

In addition,
replications defined in the `/_replicator` database are easier to [monitor](advanced_replication.html#replication-status).

### Replication Operation

> Example request to replicate between a database on the source server `example.com`, and a target database on Cloudant:

```
POST /_replicate
Content-Type: application/json
Accept: application/json

{
   "source" : "http://<account>.example.com/db",
   "target" : "http://<account>.cloudant.com/db",
}
```

> Example error response if one of the requested databases for a replication does not exist:

```json
{
   "error" : "db_not_found"
   "reason" : "could not open http://<account>.cloudant.com/ol1ka/",
}
```

The aim of replication is that at the end of the process, all active documents on the source database are also in the destination or 'target' database, and that all documents deleted from the source databases are also deleted from the destination database (if they existed there).

Replication has two forms: push or pull replication:

-   *Push replication* is where the `source` is a local database, and `destination` is a remote database.

-   *Pull replication* is where the `source` is the remote database instance, and the `destination` is the local database.

Pull replication is helpful if your source database has a permanent IP address, and your destination database is local and has a dynamically assigned IP address, for example, obtained through DHCP.
Pull replication is especially appropriate if you are replicating to a mobile or other device from a central server.

In all cases, the requested databases in the `source` and `target` specification must exist. If they do not, an error is returned within the JSON object.

### Creating a target database during replication

> Example request to create a target database and replicate onto it:

```
POST http://<account>.cloudant.com/_replicate
Content-Type: application/json
Accept: application/json

{
   "create_target" : true
   "source" : "http://<account>.example.com/db",
   "target" : "http://<account>.cloudant.com/db",
}
```

If your user credentials allow it, you can create the target database during replication by adding the `create_target` field to the request object.

The `create_target` field is not destructive. If the database already exists, the replication proceeds as normal.

### Canceling replication

> Example instructions for canceling a replication:

```shell
curl -H 'Content-Type: application/json' -X POST 'https://$ACCOUNT.cloudant.com/_replicate HTTP/1.1' -d @replication-doc.json
#the file replication-doc.json has the following content:
```

```http
POST /_replicate HTTP/1.1
Content-Type: application/json
```

> Example document to describe the replication to be canceled:

```json
{
  "source": "https://<account>.cloudant.com/example-database",
  "target": "https://<account>.example.org/example-database",
  "cancel": true
}
```

A replication triggered by `POST`ing to `/_replicate` can be canceled by `POST`ing the exact same JSON object but with the additional `cancel` property set to `true`.

<aside class="warning" role="complementary" aria-label="cancelerrorcode">If a replication is canceled, the request which initiated the replication fails with error 500 (shutdown).</aside>

The replication ID can be obtained from the original replication request if it is a continuous replication.
Alternatively, the replication ID can be obtained from `/_active_tasks`.

### Single Replication

> Example request for a single synchronization between the source database `recipes` and the target database `recipes2`.

```
POST /_replicate
Content-Type: application/json
Accept: application/json

{
   "source" : "http://<account>.cloudant.com/recipes",
   "target" : "http://<account>.cloudant.com/recipes2",
}
```

> Example response following a request for a single replication:

``` json
{
   "ok" : true,
   "history" : [
      {
         "docs_read" : 1000,
         "session_id" : "52c2370f5027043d286daca4de247db0",
         "recorded_seq" : 1000,
         "end_last_seq" : 1000,
         "doc_write_failures" : 0,
         "start_time" : "Thu, 28 Oct 2010 10:24:13 GMT",
         "start_last_seq" : 0,
         "end_time" : "Thu, 28 Oct 2010 10:24:14 GMT",
         "missing_checked" : 0,
         "docs_written" : 1000,
         "missing_found" : 1000
      }
   ],
   "session_id" : "52c2370f5027043d286daca4de247db0",
   "source_last_seq" : 1000
}
```

Replication of a database means that the two databases - the 'source' and the 'target' - are synchronized. By default, the replication process occurs one time, and synchronizes the two databases together.

The response to a request for a single replication is a JSON structure containing the success or failure status of the synchronization process. The response also contains statistics about the process.

The structure of the response includes details about the replication status:

-  **history [array]**: Replication History
  -  **doc\_write\_failures**: Number of document write failures
  -  **docs\_read**: Number of documents read
  -  **docs\_written**: Number of documents written to target
  -  **end\_last\_seq**: Last sequence number in changes stream
  -  **end\_time**: Date/Time replication operation completed
  -  **missing\_checked**: Number of missing documents checked
  -  **missing\_found**: Number of missing documents found
  -  **recorded\_seq**: Last recorded sequence number
  -  **session\_id**: Session ID for this replication operation
  -  **start\_last\_seq**: First sequence number in changes stream
  -  **start\_time**: Date/Time replication operation started
-  **ok**: Replication status
-  **session\_id**: Unique session ID
-  **source\_last\_seq**: Last sequence number read from source database

### Continuous Replication

> Example instructions for enabling continuous replication:

```shell
curl -H 'Content-Type: application/json' -X POST http://$ACCOUNT.cloudant.com/_replicate -d @replication-doc.json
# where the file replication-doc.json indicates that the replication should be continuous
```

```http
POST /_replicate HTTP/1.1
Content-Type: application/json
```

> Example document specifying that the replication should be continuous:

```json
{
  "source": "http://<account>.example.com/foo", 
  "target": "http://<account>.cloudant.com/bar", 
  "continuous": true
}
```

By default, the synchronization of a database during replication happens only once, at the time the replicate request is made. To ensure that replication from the source database to the target database takes place continually, set the `continuous` field of the JSON object within the request to `true`.

With continuous replication, changes in the source database are replicated to the target database forever, until you specifically cancel the replication.

Changes are replicated between the two databases as long as a network connection is available between the two instances.

When in operation, the replication process does not stop when it has processed all current updates.
Instead, the replication process continues to wait for further updates to the source database, and applies them to the target.

<aside class="warning" role="complementary" aria-label="continuouschecks">Continuous replication forces checks to be made continuously on the source database.
This results in an increasing number of database accesses, even if the source database content has not changed.
Database accesses are counted as part of the work performed by a multi-tenant database configuration.</aside>

#### Canceling Continuous Replication

> Example replication request to create the target database if it does not exist, and to replicate continuously:

```json
{
   "source" : "http://<account>.example.com/db",
   "target" : "http://<account>.cloudant.com/db",
   "create_target" : true,
   "continuous" : true
}
```

> Example request to cancel the replication, providing matching fields to the original request:

```json
{
    "cancel" : true,
    "continuous" : true
    "create_target" : true,
    "source" : "http://<account>.example.com/db",
    "target" : "http://<account>.cloudant.com/db",
}
```

Cancel continuous replication by including the `cancel` field in the JSON request object, and setting the value to `true`.

<aside class="warning" role="complementary" aria-label="identicalrequest">For the cancellation request to succeed, the structure of the request must be identical to the original request. In particular, if you requested continuous replication, the cancellation request must also contain the `continuous` field.</aside>

Requesting cancellation of a replication that does not exist results in a 404 error.

### Example replication sequence

> Example instructions for starting a replication:

```shell
$ curl -H 'Content-Type: application/json' -X POST 'http://$ACCOUNT.cloudant.com/_replicate' -d @replication-doc.json
#the file replication-doc.json describes the intended replication.
```

```http
POST /_replicate HTTP/1.1
Content-Type: application/json
```

> Example document describing the intended replication:

```json
{
  "source": "https://<account>.example.com/foo", 
  "target": "https://<account>.cloudant.com/bar", 
  "create_target": true, 
  "continuous": true
}
```

> Example response after starting the replication:

```json
{
  "ok": true,
  "_local_id": "0a81b645497e6270611ec3419767a584+continuous+create_target"
}
```

> Example instructions for canceling the replication:

```shell
curl -H 'Content-Type: application/json' -X POST http://$ACCOUNT.cloudant.com/_replicate -d @replication-doc.json
# where the file replication-doc.json specifies the replication task to be canceled.
```

```http
POST /_replicate HTTP/1.1
Content-Type: application/json
```

> Example document specifying the replication to be canceled:

```json
{
  "replication_id": "0a81b645497e6270611ec3419767a584+continuous+create_target",
  "cancel": true
}
```

> Example response after successfully canceling the replication, indicated by the `"ok":true` content:

```json
{
  "ok": true,
  "_local_id": "0a81b645497e6270611ec3419767a584+continuous+create_target"
}
```

A simple example of creating a replication task, then cancelling it.

### Replication database maintenance

A replication database should be looked after like any other database.
If you do not perform regular maintenance,
you might accumulate invalid documents caused by interruptions to the replication process.
A large number of invalid documents can result in excess load being placed on your cluster when the replicator process is restarted by Cloudant operations.

The main action you can perform to maintain a replication database is to remove old documents.
This can be done simply by determining the age of documents, and [deleting them](https://docs.cloudant.com/document.html#delete) if they are no longer required.
