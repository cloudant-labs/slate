## Authorization

When you have authenticated, the next test is to decide whether you
are permitted to perform certain tasks. This is called authorization.

### Roles

Role&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description
-------------------|------------
`_reader`          | Gives the user permission to read documents from the database.
`_writer`          | Gives the user permission to create, update, and delete documents (except design documents) in the database.
`_admin`           | Gives the user the ability to change security settings, including adding roles.
`_replicator`      | Gives the user permission to replicate a database, including creating checkpoints.
`_db_updates`      | Gives the user permission to use the global changes feed.
`_design`          | Gives the user permission to read design documents.
`_shards`          | Gives the user access to the `/$DB/_shards` endpoint.
`_security`        | Gives the user permission to read from the `/_api/v2/db/$DB/_security` endpoint

The credentials you use to log in to the dashboard automatically have `_admin` permissions to all databases you create. Everyone and everything else, from users you share databases with to API keys you create, must be given a permission level explicitly.

### Viewing Permissions

> Example request to determine permissions:

```http
GET /_api/v2/db/$DATABASE/_security HTTP/1.1
```

```shell
curl https://$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security \
     -u $USERNAME
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");

account.request({
  db: $DATABASE,
  path: '_security'
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

To see who has permissions to read, write, and manage the database, make a GET request against `https://$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security`.

<div></div>

> Example response:

```json
{
  "cloudant": {
    "antsellseadespecteposene": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "garbados": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "nobody": [
      "_reader"
    ]
  },
  "_id": "_security"
}
```

The `cloudant` field in the response object contains an object with keys that are the usernames that have permission to interact with the database.
The `nobody` username indicates what rights are available to unauthenticated users -- that is, any request made without authentication credentials.
In the example response, for instance, `nobody` has `_reader` permissions, making the database publicly readable.

### Modifying Permissions

> Modification request:

```http
PUT /_api/v2/db/$DATABASE/_security HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security \
     -X PUT \
     -H "Content-Type: application/json" \
     -d "$JSON"
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");

account.request({
  db: $DATABASE,
  path: '_security',
  method: 'PUT',
  body: '$JSON'
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

```json
{
  "cloudant": {
    "antsellseadespecteposene": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "garbados": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "nobody": [
      "_reader"
    ]
  }
}
```

To modify who has permissions to read, write, and manage a database, make a PUT request against `https://$USERNAME.cloudant.com/_api/v2/db/$DB/_security`. To see what roles you can assign, see [Roles](#roles).

The request object's `cloudant` field contains an object whose keys are usernames with permissions to interact with the database. The `nobody` username indicates what rights are available to unauthenticated users -- that is, anybody. In the example request, for instance, `nobody` has `_reader` permissions, making the database publicly readable.

<div></div>

The response tells you whether the update has been successful.

> Add user PUT request

```http
PUT /_api/v2/db/$DATABASE/_security HTTP/1.1
Content-Type: application/json

{
  "cloudant": {
    "antsellseadespecteposene": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "garbados": [
      "_reader",
      "_writer",
      "_admin"
    ],
    "nobody": [
      "_reader"
    ]
  }
}
```
To add the new user, `nobody`, you can make a PUT request.

<div></div>

> Example incorrect request 

```http
PUT /_api/v2/db/$DATABASE/_security HTTP/1.1
Content-Type: application/json

{
  "cloudant": {
    "nobody": [
      "_reader"
    ]
  }
}
```

You must run the GET command first to retrieve the security object. Then, you can modify that 
security object with new permissions. If you do not run the GET command and retrieve the 
security object before you run an API call, the result will be disruptive to your 
environment. For example, if you want to add a new user with read-only access, the 
following incorrect request removes all the other users with access to the database.

<div></div>



> Example response:

```json
{
  "ok" : true
}
```
<div></div>



### Creating API Keys

<aside class="warning" role="complementary" aria-label="apibypostdeprecated">The earlier method of generating API keys by `POST`ing to `https://cloudant.com/api/generate_api_key` is now deprecated.</aside>

API keys allow you to give access to a person or application without having to create a new Cloudant account.
An API key consists of a randomly generated username and password.
The key is given the desired access permissions.
Once generated,
the API key can be used in the same way as a normal user account,
for example by granting read,
write,
or admin access permissions.

API keys are not the _same_ as normal user accounts.
In particular,
an API key does not have access to the dashboard.
An API key is primarily used to enable applications to access a database,
with a determined level of access control.

<aside class="warning" role="complementary" aria-label="oneoffgeneration">If you choose to generate an API key through the dashboard,
remember to record the key name and password.
These are both randomly generated,
and cannot be retrieved if lost or forgotten.</aside>

<aside class="warning" role="complementary" aria-label="noapikeysforcl">IBM Cloudant Data Layer Local Edition ("Cloudant Local") does not support API Keys.
For a similar capability,
create "CouchDB" style users,
as described in the [IBM Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSTPQH_1.0.0/com.ibm.cloudant.local.install.doc/topics/clinstall_db_security.html).</aside>

<div></div>

> Example request to create an API key:

```http
POST https://<username>.cloudant.com/_api/v2/api_keys HTTP/1.1
```

```shell
curl -X POST https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/_api/v2/api_keys
```

```javascript
var nano = require('nano');
var account = nano("https://$USERNAME:$PASSWORD@cloudant.com");

account.request({
  db: '_api',
  path: 'v2/api_keys',
  method: 'POST'
}, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

> Example response:

```json
{
  "password": "YPNCaIX1sJRX5upaL3eqvTfi",
  "ok": true,
  "key": "blentfortedsionstrindigl"
}
```

To generate an API key,
use `https://<username>.cloudant.com/_api/v2/api_keys`.
Next,
assign the API key to a database by using a `PUT` request to `https://<username>.cloudant.com/_api/v2/db/<database>/_security`.
Once assigned to a database,
the key can be granted access permissions.
By default,
an API key has no permissions for anything,
and must be given permissions explicitly.

The response contains the generated key and password.

### Deleting API keys

#### To remove an API key using the Dashboard

1.	Click on `Databases` -> `Permissions`.
2.	Hover over the API key you would like to delete.
3.	Click the '`X`' that appears when you hover over the API key.

#### To remove an API key using the Cloudant API

Use the [modifying permissions](#modifying-permissions) technique to remove the API key from the list of users with access permission.

This works because an API key is similar to a user,
and has been granted access permissions.
By removing the API key from the list of users that have access permissions,
the effect is to delete the API key.

To remove the API key,
send an HTTP `PUT` request to the same `_security` API endpoint you used to [create the API key](#creating-api-keys).
Provide an updated list of the usernames that have access permission.
The updated list should _omit_ the API key.


### Enabling the `_users` database with Cloudant

> Modification request:

```http
PUT /$DATABASE/_security HTTP/1.1
Content-Type: application/json
{
  "couchdb_auth_only": true,
 "members": {
   "names": ["member"],"roles":[]
   },
  "admins": {
     "names": ["admin"],"roles":[]
   }
 }
}
```

```shell
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/_security \
-X PUT \
-H "Content-Type: application/json" \
-d '{
  "couchdb_auth_only": true,
 "members": {
   "names": ["member"],"roles":[]
   },
  "admins": {
     "names": ["admin"],"roles":[]
   }
 }'
```

You can use the [_users database](http://docs.couchdb.org/en/1.6.1/intro/security.html#authentication-database) to manage roles in Cloudant. However, you must turn off Cloudant security for those roles first. To do this, `PUT` a JSON document to the `_security` endpoint of the database. For example, `https://<username>.cloudant.com/<database>/_security`.

<div></div>

> Example response:

```json
{
 "ok" : true
}
```
