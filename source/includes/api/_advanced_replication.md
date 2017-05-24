## Advanced replication

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Advanced replication topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/advanced_replication.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

This section contains details about more advanced replication concepts and tasks.

You might also find it helpful to review details of the underlying [replication protocol](http://dataprotocols.org/couchdb-replication/), as well as reviewing the [Advanced Methods](advanced.html) material.

### Replication Status

> Example replication document, `PUT` into `/_replicator`:

```json
{
  "_id": "my_rep",
  "source":  "https://<account>.<myserver>.com:5984/fromthis",
  "target":  "https://<account>.cloudant.com/tothat",
  "create_target":  true
}
```

> Example of automatic document update once replication starts:

```json
{
  "_id": "my_rep",
  "source":  "https://<account>.<myserver>.com:5984/fromthis",
  "target":  "https://<account>.cloudant.com/tothat",
  "create_target":  true
  "_replication_id":  "c0ebe9256695ff083347cbf95f93e280",
  "_replication_state":  "triggered",
  "_replication_state_time":  "2011-06-07T16:54:35+01:00"
}
```

When replication is managed by storing a document in the `/_replicator` database, the contents of the document are updated as the replication status changes.

In particular, once replication starts, three new fields are added automatically to the replication document. The fields all have the prefix: `_replication_`

Field | Detail
------|-------
`_replication_id` | This is the internal ID assigned to the replication. It is the same ID that appears in the output from `/_active_tasks/`.
`_replication_state` | The current state of the replication. The possible states are:<dl><dt>`triggered`</dt><dd>The replication has started and is in progress.</dd><dt>`completed`</dt><dd>The replication completed successfully.</dd><dt>`error`</dt><dd>An error occurred during replication.</dd></dl>
`_replication_state_time` | An <a href="https://www.ietf.org/rfc/rfc3339.txt" target="_blank">RFC 3339</a> compliant timestamp that reports when the current replication state defined in `_replication_state` was set.

> Example replication document once replication has completed:

```json
{
  "_id": "my_rep",
  "source":  "https://<account>.<myserver>.com:5984/fromthis",
  "target":  "https:/<account>.cloudant.com/tothat",
  "create_target":  true,
  "_replication_id":  "c0ebe9256695ff083347cbf95f93e280",
  "_replication_state":  "completed",
  "_replication_state_time":  "2011-06-07T16:56:21+01:00"
}
```

When the replication finishes, it updates the `_replication_state` field with the value `completed`, and the `_replication_state_time` field with the time that the completion status was recorded.

A continuous replication can never have a `completed` state.

### Authentication

> Example of specifying username and password values for accessing source and target databases during replication:

```json
{
  "source": "https://<account>.<example>.com/db", 
  "target": "https://<account>.cloudant.com/db"
}
```

In any production application, security of the source and target databases is essential.
In order for replication to proceed, authentication is necessary to access the databases.
In addition, checkpoints for replication are [enabled by default](replication.html#checkpoints), which means that replicating the source database requires write access.

To enable authentication during replication, include a username and password in the database URL. The replication process uses the supplied values for HTTP Basic Authentication.

### Filtered Replication

> Simple example of a filter function:

```
function(doc, req) {
  return !!(doc.type && doc.type == "foo");
}
```

Sometimes you do not want to transfer all documents from source to target.
To choose which documents to transfer,
include one or more filter functions in a design document on the source.
You can then tell the replicator to use these filter functions.

<aside role="complementary" aria-label="filtersimilartochanges">Filtering documents during replication is similar to the process of [filtering the `_changes` feed](design_documents.html#filter-functions).</aside>  

A filter function takes two arguments:

- The document to be replicated.
- The replication request.

A filter function returns a true or false value. If the result is true, the document is replicated.

<div></div>

> Simple example of storing a filter function in a design document:

```json
{
  "_id": "_design/myddoc",
  "filters": {
    "myfilter": "function goes here"
  }
}
```

Filters are stored under the topmost `filters` key of the design document.

<div></div>

> Example JSON for invoking a filtered replication:

```json
{
  "source": "http://<account>.<example>.org/<example-database>",
  "target": "http://<account>.cloudant.com/<example-database>",
  "filter": "myddoc/myfilter"
}
```

Filters are invoked by using a JSON statement that identifies:

- The source database.
- The target database.
- The name of the filter stored under the `filters` key of the design document.

<div></div>

> Example JSON for invoking a filtered replication with supplied parameters:

```json
{
  "source": "http://<account>.<example>.org/example-database",
  "target": "http://<account>.cloudant.com/example-database",
  "filter": "myddoc/myfilter",
  "query_params": {
    "key": "value"
  }
}
```

Arguments can be supplied to the filter function by including key:value pairs in the `query_params` field of the invocation.

### Named Document Replication

> Example replication of specific documents:

```json
{
  "source": "http://<account>.example.org/example-database",
  "target": "http://<account>.127.0.0.1:5984/example-database",
  "doc_ids": ["foo", "bar", "baz"]
}
```

Sometimes you only want to replicate some documents. For this simple case, you do not need to write a filter function. To replicate specific documents, add the list of keys as an array in the `doc_ids` field.

### Replicating through a proxy

> Example showing replication through a proxy:

```json
{
  "source": "http://<account>.cloudant.com/<example-database>",
  "target": "http://<account>.<example>.org/<example-database>",
  "proxy": "http://<my-proxy>.com:8888"
}
```

If you want replication to pass through an HTTP proxy, provide the proxy details in the `proxy` field of the replication data.

### The *user\_ctx* property and delegations

> Example delegated replication document:

```json
{
  "_id": "my_rep",
  "source":  "https://<account>.<myserver>.com:5984/foo",
  "target":  "https://<account>.cloudant.com/bar",
  "continuous":  true,
  "user_ctx": {
    "name": "joe",
    "roles": ["erlanger", "researcher"]
  }
}
```

Replication documents can have a custom `user_ctx` property.
This property defines the user context under which a replication runs.
For the old way of triggering replications (`POST`ing to `/_replicate/`),
this property was not needed (it didn't exist in fact).
This is because at the moment of triggering the replication,
it has information about the authenticated user.
With the replicator database,
since it's a regular database,
the information about the authenticated user is only present at the moment the replication document is written to the database - the replicator database implementation is like a `_changes` feed consumer (with `?include_docs=true`) that reacts to what was written to the replicator database - in fact this feature could be implemented with an external script/program.
This implementation detail implies that for non admin users,
a *user\_ctx* property,
containing the user's name and a subset of his/her roles,
must be defined in the replication document.
This is ensured by the document update validation function present in the default design document of the replicator database.
This validation function also ensures that a non admin user can set a user name property in the `user_ctx` property that doesn't match his/her own name (same principle applies for the roles).

For admins, the `user_ctx` property is optional, and if it's missing it defaults to a user context with name *null* and an empty list of roles - this means design documents will not be written to local targets. If writing design documents to local targets is desired, then a user context with the roles *\_admin* must be set explicitly.

Also, for admins the `user_ctx` property can be used to trigger a replication on behalf of another user. This is the user context that will be passed to local target database document validation functions.

<aside class="warning" role="complementary" aria-label="ctxonlylocal">The `user_ctx` property only has an effect for local endpoints.</aside>

As stated before, for admins the `user_ctx` property is optional, while for regular (non admin) users it's mandatory. When the roles property of `user_ctx` is missing, it defaults to the empty list *[ ]*.

### Performance related options

> Example of including performance options in a replication document:

```json
{
  "source": "https://<account>@example.com/example-database",
  "target": "https://<account>@example.org/example-database",
  "connection_timeout": 60000,
  "retries_per_request": 20,
  "http_connections": 30
}
```

These options can be set for a replication by including them in the replication document.

-   `worker_processes` - The number of processes the replicator uses (per replication) to transfer documents from the source to the target database. Higher values can imply better throughput (due to more parallelism of network and disk IO) at the expense of more memory and eventually CPU. Default value is 4.
-   `worker_batch_size` - Workers process batches with the size defined by this parameter (the size corresponds to number of ''\_changes'' feed rows). Larger values for the batch size might result in better performance. Smaller values mean that checkpointing is done more frequently. Default value is 500.
-   `http_connections` - The maximum number of HTTP connections per replication. For push replications, the effective number of HTTP connections used is min(worker\_processes + 1, http\_connections). For pull replications, the effective number of connections used corresponds to this parameter's value. Default value is 20.
-   `connection_timeout` - The maximum period of inactivity for a connection in milliseconds. If a connection is idle for this period of time, its current request will be retried. Default value is 30000 milliseconds (30 seconds).
-   `retries_per_request` - The maximum number of retries per request. Before a retry, the replicator will wait for a short period of time before repeating the request. This period of time doubles between each consecutive retry attempt. This period of time never goes beyond 5 minutes and its minimum value (before the first retry is attempted) is 0.25 seconds. The default value of this parameter is 10 attempts.
-   `socket_options` - A list of options to pass to the connection sockets. The available options can be found in the [documentation for the Erlang function setopts/2 of the inet module](http://www.erlang.org/doc/man/inet.html#setopts-2). Default value is `[{keepalive, true}, {nodelay, false}]`.

### Attachments

Having large numbers of attachments on documents might cause an adverse effect on replication performance.

For more information about the effect of attachments on replication performance,
see [here](attachments.html#performance-considerations).