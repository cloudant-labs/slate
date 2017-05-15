## Active tasks

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Active tasks topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/active_tasks.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

The `/_active_tasks` endpoint provides a list of the tasks running on the server.
For more examples on using this endpoint,
see the [Managing tasks](managing_tasks.html) guide.

### Retrieving a list of active tasks

> Example request to retrieve list of active tasks:

```http
GET /_active_tasks HTTP/1.1
```

```shell
curl https://$USERNAME.cloudant.com/_active_tasks \
     -u $USERNAME
```

```javascript
var nano = require('nano');
var account = nano('https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com');

account.request({
  path: '_active_tasks'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example JSON response array, containing details of currently running tasks:

``` json
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
  },
  
  {
    "user": "acceptly",
    "updated_on": 1363273779,
    "type": "indexer",
    "node": "dbcore@db11.julep.cloudant.net",
    "pid": "<0.20723.4070>",
    "changes_done": 189,
    "database": "shards/00000000-3fffffff/acceptly/acceptly_my_chances_logs_live.1321035717",
    "design_document": "_design/MyChancesLogCohortReport",
    "started_on": 1363273094,
    "total_changes": 26389
  },
  
  {
    "user": "username",
    "updated_on": 1371118433,
    "type": "search_indexer",
    "total_changes": 5466,
    "node": "dbcore@db7.meritage.cloudant.net",
    "pid": "<0.29569.7037>",
    "changes_done": 4611,
    "database": "shards/40000000-7fffffff/username/database_name",
    "design_document": "_design/lucene",
    "index": "search1",
    "started_on": 1371118426
  },
  
  {
    "view": 1,
    "user": "acceptly",
    "updated_on": 1363273504,
    "type": "view_compaction",
    "total_changes": 26095,
    "node": "dbcore@db11.julep.cloudant.net",
    "pid": "<0.21218.4070>",
    "changes_done": 20000,
    "database": "shards/80000000-bfffffff/acceptly/acceptly_my_chances_logs_live.1321035717",
    "design_document": "_design/MyChancesLogCohortReport",
    "phase": "view",
    "started_on": 1363273094
  },
  
  {
    "updated_on": 1363274040,
    "node": "dbcore@db11.julep.cloudant.net",
    "pid": "<0.29256.4053>",
    "changes_done": 272195,
    "database": "shards/00000000-3fffffff/heroku/app3245179/id_f21a08b7005e_logs.1346083461",
    "started_on": 1363272496,
    "total_changes": 272195,
    "type": "database_compaction"
  }
]
```

-   **Method**: `GET`
-   **Path**: `/_active_tasks`
-   **Response**: List of running tasks, including the task type, name, status and process ID
-   **Roles permitted**: `_admin`

You can obtain a list of active tasks by using the `/_active_tasks` URL. The result is a JSON array of the currently running tasks, with each task being described with a single object.

The returned structure includes the following fields for each task:

-   **pid**: Erlang Process ID
-   **type**: Operation Type
-   **updated\_on**: Time when the last update was made to this task record. Updates are made by the job as progress occurs. The value is an integer containing the Unix time UTC.
-   **started\_on**: Time when the task was started. The value is an integer containing the Unix time UTC.
-   **total\_changes**: Total number of documents to be processed by the task. The exact meaning depends on the type of the task.
-   **database**: The database and shard on which the operation occurs.

In the `type` field, possible values include:

-   `database_compaction`
-   `view_compaction`
-   `replication`
-   `indexer`
-   `search_indexer`

The meaning of other fields in the JSON response depends on the type of the task.

#### Specific response fields for compaction tasks

-   **total\_changes**: Number of documents in the database.
-   **changes\_done**: Number of documents compacted.
-   **phase**: Reports the stage of compaction.

In the `phase` field, the value indicates the stage that compaction has reached:

1. `ids`: Document compaction is in progress.
2. `views`: View compaction is in progress.

#### Specific response fields for replication tasks

-   **replication\_id**: Unique identifier string of the replication that can be used to cancel the task.
-   **user**: User who started the replication, expressed as a string, or `null` if the replication was not initiated by a user.
-   **changes\_pending**: Number of documents needing to be changed in the target database, expressed as an integer.
-   **revisions\_checked**: Number of document revisions for which it was checked whether they are already in the target database.
-   **continuous**: Boolean value indicating whether the replication is continuous.
-   **docs\_read**: Number of documents read from the source database, expressed as an integer.
-   **source**: An obfuscated URL string indicating the database from which the task is replicating.
-   **target**: An obfuscated URL string indicating the database to which the task is replicating.

#### Specific response fields for indexing tasks

-   **design\_document**: The design document containing the view or index function or functions.
-   **total\_changes**: The number of unindexed changes to process. This count includes deleted documents, though these are automatically skipped by the indexer.
-   **changes\_done**: Number of document revisions processed by this task. A document can have one or more revisions.
