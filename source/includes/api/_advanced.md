## Advanced

These endpoints provide information about the state of the cluster, details about revision history, and other miscellaneous tasks.

### GET /

> Example request to get server meta information:

```http
GET / HTTP/1.1
HOST: <account>.cloudant.com
```

```shell
curl https://$ACCOUNT.cloudant.com/
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '/'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example JSON response:

```json
{
  "couchdb": "Welcome",
  "version": "1.0.2",
  "vendor": {
     "cloudant_build":"1138"
  }
}
```

-  **Method**: `GET`
-  **Path**: `/`
-  **Response**: Welcome message and version

Accessing the root endpoint `/` returns meta information about the cluster. The response is a JSON object containing a welcome message and the version of the server. The `version` field contains the CouchDB version the server is compatible with.
The `vendor.cloudant_build` field contains the build number of Cloudant's CouchDb implementation.

### GET /_db_updates

> Example request to get a list of changes to the database:

```http
GET /_db_updates HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_db_updates \
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_db_updates'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response:

```json
{
  "results": [{
    "dbname": "$DATABASE_NAME",
    "type": "created",
    "account": "$ACCOUNT",
    "seq": "673-g1AAAAJAeJyN0Et..."
  }],
  "last_seq": "673-g1AAAAJAeJyN0Et..."
}
```

<aside class="warning" role="complementary" aria-label="dedicatedonly">This feature is only available to dedicated customers.</aside>

Obtains a list of changes to databases, like a global [changes feed](database.html#get-changes). Changes can be either updates to the database, creation, or deletion of a database. Like the changes feed, the feed is not guaranteed to return changes in the correct order and might contain changes more than once. Polling modes for this method works just like polling modes for [the changes feed](database.html#get-changes).


Argument | Description | Optional | Type | Default | Supported Values
---------|-------------|----------|------|---------|-----------------
feed | Type of feed | yes | string | normal | `continuous`: Continuous (non-polling) mode, `longpoll`: Long polling mode, `normal`: default polling mode
heartbeat | Time in milliseconds after which an empty line is sent during longpoll or continuous if there have been no changes | yes | numeric | 60000 | 
limit | Maximum number of results to return | yes | numeric | none |  
since | Start the results from changes immediately after the specified sequence number. If since is 0 (the default), the request will return all changes since the feature was activated. | yes | string | 0 | 
timeout | Number of milliseconds to wait for data in a `longpoll` or `continuous` feed before terminating the response. If both `heartbeat` and `timeout` are suppled, `heartbeat` supersedes `timeout`. | yes | numeric |  | 
descending | Whether results should be returned in descending order, i.e. the latest event first. By default, the oldest event is returned first. | yes | boolean | false | 

### GET /$DATABASE/_shards

> Example request

```http
GET /$DATABASE/_shards HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_shards \
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  database: $DATABASE,
  path: '_shards'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response:

```json
{
  "shards": {
    "e0000000-ffffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "c0000000-dfffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "a0000000-bfffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "80000000-9fffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "60000000-7fffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "40000000-5fffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "20000000-3fffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ],
    "00000000-1fffffff": [
      "dbcore@db1.testy004.cloudant.net",
      "dbcore@db2.testy004.cloudant.net",
      "dbcore@db3.testy004.cloudant.net"
    ]
  }
}
```

Returns informations about the shards in the cluster, specifically what nodes contain what hash ranges.

The response's `shards` field contains an object whose keys are the hash value range constituting each shard, while each value is the array of nodes containing that a copy of that shard.

### GET /$DATABASE/_missing_revs

> Example request

```http
GET /$DATABASE/_missing_revs
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_missing_revs \
     -X POST \
     -H "Content-Type: application/json" \
     -d @request-body.json
# where the file request-body.json contains the following:
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  database: $DATABASE,
  path: '_missing_revs',
  method: 'POST',
  body: '$JSON'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

```json
{
  "$DOCUMENT_ID": [
    "$REV_1",
    "$REV_2"
  ]
}
```

> Example response:

```json
{
  "missed_revs":{
    "$DOCUMENT_ID": [
      "$REV_1"
    ]
  }
}
```

Given a list of document revisions, returns the document revisions that do not exist in the database.

### POST /$DATABASE/_revs_diff

> Example request

```http
POST /$DATABASE/_revs_diff HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_revs_diff \
     -X POST \
     -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  database: $DATABASE,
  path: '_revs_diff',
  method: 'POST',
  body: '$JSON'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example request:

```json
{
  "190f721ca3411be7aa9477db5f948bbb": [
    "3-bb72a7682290f94a985f7afac8b27137",
    "4-10265e5a26d807a3cfa459cf1a82ef2e",
    "5-067a00dff5e02add41819138abb3284d"
  ]
}
```

> Example response:

```json
{
  "190f721ca3411be7aa9477db5f948bbb": {
    "missing": [
      "3-bb72a7682290f94a985f7afac8b27137",
      "5-067a00dff5e02add41819138abb3284d"
    ],
    "possible_ancestors": [
      "4-10265e5a26d807a3cfa459cf1a82ef2e"
    ]
  }
}
```

Given a set of document/revision IDs, returns the subset of those that do not correspond to revisions stored in the database.

### GET /$DATABASE/_revs_limit

> Example request

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_revs_limit'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

```http
GET /$DATABASE/_revs_limit HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_revs_limit \
     -X GET \
```

> Example response:

```
1000
```

Gets the number of past revisions of a document that Cloudant stores information on.

<aside class="warning" role="complementary" aria-label="tombstones1">Although the documents associated with past revisions are automatically removed, "tombstones" remain with the `_rev` value for that revision. If a document has more revisions than the value of `_revs_limit`, Cloudant deletes the tombstones of the oldest revisions.</aside>

### PUT /$DATABASE/_revs_limit

> Example request

```http
PUT /$DATABASE/_revs_limit HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_revs_limit \
     -X PUT \
     -d 1000
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_revs_limit',
  body: '1000',
  method: 'PUT'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

```
1000
```

> Example response:

```json
{
  "ok": true
}
```

Sets the maximum number of past revisions that Cloudant stores information on.

<aside class="warning" role="complementary" aria-label="tombstones2">Although the documents associated with past revisions are automatically removed, "tombstones" remain with the `_rev` value for that revision. If a document has more revisions than the value of `_revs_limit`, Cloudant deletes the tombstones of the oldest revisions.</aside>

### GET /_membership

> Example request to list nodes in the cluster:

```http
GET /_membership HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_membership \
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_membership'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response:

```json
{
  "cluster_nodes": [
    "dbcore@db1.testy004.cloudant.net",
    "dbcore@db2.testy004.cloudant.net",
    "dbcore@db3.testy004.cloudant.net"
  ],
  "all_nodes": [
    "dbcore@db1.testy004.cloudant.net",
    "dbcore@db2.testy004.cloudant.net",
    "dbcore@db3.testy004.cloudant.net"
  ]
}
```

Returns the names of nodes in the cluster. Currently active clusters are indicated in the `cluster_nodes` field, while `all_nodes` lists all nodes active or not.

-   **Method**: `GET`
-   **Path**: `/_membership`
-   **Response**: JSON document listing cluster nodes and all nodes
-   **Roles permitted**: \_admin

#### Response structure

-   `cluster_nodes`: Array of node names (strings) of the active nodes in the cluster
-   `all_nodes`: Array of nodes names (strings) of all nodes in the cluster

### GET /_uuids

> Example request for a single UUID:

```http
GET /_uuids HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_uuids \ 
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_uuids'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response to a request for a single UUID:

``` json
{
   "uuids" : [
      "7e4b5a14b22ec1cf8e58b9cdd0000da3"
   ]
}
```

> Example request for five UUIDs:

```http
GET /_uuids?count=5 HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_uuids?count=5 \
```

```javascript
var nano = require('nano');
var account = nano('https://$ACCOUNT.cloudant.com');

account.request({
  path: '_uuids?count=5'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response to a request for five UUIDs:

``` json
{
   "uuids" : [
      "c9df0cdf4442f993fc5570225b405a80",
      "c9df0cdf4442f993fc5570225b405bd2",
      "c9df0cdf4442f993fc5570225b405e42",
      "c9df0cdf4442f993fc5570225b4061a0",
      "c9df0cdf4442f993fc5570225b406a20"
   ]
}
```

This command requests one or more Universally Unique Identifiers (UUIDs). The response is a JSON object providing a list of UUIDs.

-   **Method**: `GET`
-   **Path**: `/_uuids`
-   **Response**: JSON document containing a list of UUIDs

Argument | Description | Optional | Type
---------|-------------|----------|-----
`count` | Number of UUIDs to return | yes | Positive integer, greater than 0 and less than or equal to 1,000.

