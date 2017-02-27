---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-27"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-02-27 -->

# Authorization

After [authenticating](authentication.html),
the next test is to decide whether you are allowed to do certain tasks.
This decision is called authorization.
{:shortdesc}

When you authenticate with the {{site.data.keyword.cloudant}} system,
it 'knows' who you are.
The next question is: what tasks are you allowed to do?

One way of answering that question might be to have a complete list of all the possible tasks that you are allowed to
do,
for each aspect of a {{site.data.keyword.cloudant_short_notm}} system such as a database or a document.
Although simple,
this approach would require many lengthy lists.
Keeping those lists correct and complete would be impractical.

A better approach uses the idea of 'roles'.
The various tasks can be grouped into collections that are typical of some generic roles.
For example,
the task of creating or deleting a database is characteristic of someone with an administrative role.
Similarly,
the task or creating or updating a document is characteristic of someone with a 'writing' role.

Rather than explicitly listing every task you can do,
you are given one or more roles.
If you have a role,
then you can do all the tasks that are associated with that role.

## Roles

{{site.data.keyword.cloudant_short_notm}} has a number of roles available.
The roles can be assigned to user accounts or [API keys](#creating-api-keys).

The three core roles are as follows:

Role          | Description
--------------|------------
`_admin`      | Change security settings, including adding roles.
`_reader`     | Read documents from the database.
`_writer`     | Create, update, and delete documents (except design documents) in the database.

>   **Note:** The `_reader` and `_writer` roles are exclusive. If a user has the `_writer` role, they cannot read documents they create unless they _also_ have the `_reader` role.

You might want to assign more than one role.
For example,
a user might need to read from or write to documents within a database,
but would not need full administrative control of the database.
To fulfill this requirement,
the user's account is granted the `_reader` and `_writer` roles,
but not the `_admin` role.

A number of 'focused' roles are also available.
These provide permissions for specific API endpoints.
The focused role permissions are similar to the core role permissions,
but apply _only_ to the specific API endpoint.

The focused roles are as follows:

Role          | Description                                                       | API Endpoints
--------------|-------------------------------------------------------------------|--------------
`_db_updates` | Use the global changes feed.                                      | [`_db_updates`](advanced.html#-get-_db_updates-)
`_design`     | Create, read, update, and delete design documents.                | [`_design`](design_documents.html), [`_find`](cloudant_query.html#finding-documents-using-an-index), [`_index`](cloudant_query.html)
`_replicator` | Replicate data within a database, including creating checkpoints. | [`_local`](replication.html#the-since_seq-field), [`_replicate`](replication.html#the-_replicate-endpoint), [`_replicator`](replication.html#replicator-database)
`_security`   | Work with the `/$DATABASE/_security` endpoint.                    | [`_security`](#viewing-permissions)
`_shards`     | Access to the `/$DATABASE/_shards` endpoint.                      | [`_shards`](advanced.html#-get-database-_shards-)

For example,
the `_design` role allows a user or [API key](#creating-api-keys) to create,
read,
modify,
or delete design documents,
but has the advantage of not requiring assignment of the more widely applicable `_reader` or `_writer` roles.
This distinction is useful because otherwise the authorized account would be able to read from or write to documents within the database,
other than the design documents.

The credentials that you use to log in to the dashboard automatically have the `_admin` role for all databases you create.
Everyone and everything else,
including users you share databases with,
and API keys you create,
must be given a role explicitly to do corresponding tasks.

>   **Note:** The `_admin` role aggregates the permissions of the `_reader`, `_writer`, `_db_updates`, `_design`, `_replicator`, `_security`, and `_shards` roles.

The special `nobody` user name applies for anyone or any application that tries to do tasks,
but that did not authenticate with the system.
In other words,
the `nobody` user name applies to all unauthenticated connection attempts.
For example,
if an application attempts to read data from a database,
but did not identify itself,
the task can proceed only if the `nobody` user has the role `_reader`.

It is possible to grant more powerful roles to an <i>un</i>authenticated user than to an authenticated user.
For example,
if the `nobody` user name is intentionally granted `_admin`,
`_reader`,
and `_writer` roles,
but an authenticated user account such as `alexone` is granted only the `_reader` role,
then an unauthenticated user might do more than the authenticated `alexone` user. 

>   **Note:** It is important to understand that the `nobody` user name is _not_ way of providing a default set of permissions. Instead, the `nobody` user name is used to determine permissions for _unauthenticated_ users.

### The role 'hierarchy'

Clearly,
some roles are more 'powerful' than others.

In the following list,
roles that appear at the beginning of the list are more 'powerful' than roles that appear towards the end of the list.
In general,
a role is authorized to do more tasks than the roles underneath.

Role          | Authorized tasks
--------------|------------------|--------------
`_admin`      | Many.            |
`_writer`     |                  |
`_reader`     | Few.          

### Determining the role to assign

When you determine the role or roles to assign to a user account or API key,
it is best to give the lowest possible role necessary to do the tasks that are expected of that account or API key.

If the tasks are for a specific aspect,
such as working with design documents or the security settings,
then it might be possible to assign one of the focused roles,
such as `_design` or `_security`.

## Viewing Permissions

To see who has permissions to read,
write,
and manage the database,
send a `GET` request to `https://$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security`.

_Example of using an HTTP request to determine permissions:_

```http
GET /_api/v2/db/$DATABASE/_security HTTP/1.1
```
{:codeblock}

_Example of using a command line request to determine permissions:_

```sh
curl https://$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security
```
{:codeblock}

<!--

_Example request to determine permissions, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
account.request({
	db: $DATABASE,
	path: '_security'
	},
	function (err, body, headers) {
		if (!err) {
			console.log(body);
		}
	}
});
```
{:codeblock}

-->

The `cloudant` field in the response object contains an object with keys that are the user names
that have permission to interact with the database.
The `nobody` user name indicates what permissions are available to unauthenticated users,
that is,
any request made without authentication credentials.

In the following example response,
the `nobody` user name has `_reader` permissions.
This combination means that the database is publicly readable to unauthenticated users.

_Example response to request for permissions:_

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
{:codeblock}

## Modifying Permissions

To modify who has permissions to read,
write,
or manage a database,
send a `PUT` request to `https://$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security`.
To see what roles you can assign,
see [Roles](#roles).

_Example of using HTTP to send an authorization modification request:_

```http
PUT /_api/v2/db/$DATABASE/_security HTTP/1.1
Content-Type: application/json
```
{:codeblock}

_Example of using the command line to send an authorization modification request:_

```sh
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/_api/v2/db/$DATABASE/_security \
	-X PUT \
	-H "Content-Type: application/json" \
	-d "$JSON"
```
{:codeblock}

<!--

_Example of sending an authorization modification request, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");
account.request(
	{
		db: $DATABASE,
		path: '_security',
		method: 'PUT',
		body: '$JSON'
	},
	function (err, body, headers) {
		if (!err) {
			console.log(body);
		}
	}
);
```
{:codeblock}

-->

The request must provide a document in JSON format,
describing a `cloudant` field.
The field contains an object with keys that are the user names that have permission to interact with the database.
The `nobody` user name indicates what permissions are available to unauthenticated users,
that is,
anybody.

In the following example request,
the `nobody` user name is given `_reader` permissions.
This authorization makes the database publicly readable.

_Example of an authorization modification request document:_

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
{:codeblock}

The response indicates whether the update was successful.

_Example response after a successful authorization modification request:_

```json
{
	"ok" : true
}
```
{:codeblock}

You must run the `GET` command first to retrieve the security object.
Then,
you can modify that security object with new permissions.
If you do not run the `GET` command and retrieve the security object before you run an API call,
the result might disrupt your environment.
For example,
if you want to add a `nobody` user with read-only access,
the  following incorrect request removes _all_ the other users with access to the database.

_Example of an incorrect authorization modification request document:_

```json
{
    "cloudant": {
        "nobody": [
            "_reader"
        ]
    }
}
```
{:codeblock}

## Creating API Keys

>	**Note**: An earlier method of generating API keys by `POST`ing to
the `https://cloudant.com/api/generate_api_key` endpoint is deprecated.

Give access to a person or application without having to create a new Cloudant account,
by using API keys.
An API key consists of a randomly generated user name and password.
The key is given the wanted access permissions.

When generated,
the API key can be used in the same way as a normal user account,
for example by granting read,
write,
or admin access permissions.

API keys are not the same as normal user accounts.
In particular,
an API key does not have access to the dashboard.

An API key is primarily used to enable applications to access a database,
with a determined level of access control.

>	**Note**: If you choose to generate an API key through the dashboard,
remember to record the key name and password.
These values are both randomly generated,
and cannot be retrieved if lost or forgotten.

>	**Note**: [IBM Cloudant Data Layer Local Edition ("Cloudant Local") ![External link icon](../images/launch-glyph.svg "External link icon")](https://www.ibm.com/support/knowledgecenter/SSTPQH_1.0.0/com.ibm.cloudant.local.doc/SSTPQH_1.0.0_welcome.html){:new_window}
does not support API Keys.
For a similar capability,
create "CouchDB" style users,
as described in the [IBM Knowledge Center ![External link icon](../images/launch-glyph.svg "External link icon")](http://www-01.ibm.com/support/knowledgecenter/SSTPQH_1.0.0/com.ibm.cloudant.local.install.doc/topics/clinstall_db_security.html){:new_window}.

_Example of using an HTTP request to create an API key:_

```http
POST https://<username>.cloudant.com/_api/v2/api_keys HTTP/1.1
```
{:codeblock}

_Example of using a command line request to create an API key:_

```sh
curl -X POST https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/_api/v2/api_keys
```
{:codeblock}

<!--

_Example request to create an API key, using Javascript:_

```javascript
var nano = require('nano');
var account = nano("https://$USERNAME:$PASSWORD@cloudant.com");
account.request(
	{
		db: '_api',
		path: 'v2/api_keys',
		method: 'POST'
	},
	function (err, body) {
		if (!err) {
			console.log(body);
		}
	}
);
```
{:codeblock}

-->

The response contains the generated key and password.

_Example response to request for an API key:_

```json
{
	"password": "YPNCaIX1sJRX5upaL3eqvTfi",
	"ok": true,
	"key": "blentfortedsionstrindigl"
}
```
{:codeblock}

After you generate an API key,
you can assign the API key to a database by sending a `PUT` request to
`https://<username>.cloudant.com/_api/v2/db/<database>/_security`.
When assigned to a database,
the key can be granted access permissions.
By default,
an API key has no permissions for anything,
and must be given permissions explicitly.

## Deleting API keys

### To remove an API key by using the Dashboard

1.	Click `Databases` -> `Permissions`.
2.	Hover over the API key you would like to delete.
3.	Click the '`X`' that appears when you hover over the API key.

### To remove an API key by using the Cloudant API

Use the [modifying permissions](#modifying-permissions) technique to remove the API key from the list of users with access permission.

This technique works because an API key is similar to a user,
and was granted access permissions.
By removing the API key from the list of users that have access permissions,
the effect is to delete the API key.

To remove the API key,
send an HTTP `PUT` request to the same `_security` API endpoint you used to [create the API key](#creating-api-keys).
Provide an updated list of the user names that have access permission.
The updated list must _omit_ the API key.

## Enabling the `_users` database with Cloudant

You can use the
[_users database ![External link icon](../images/launch-glyph.svg "External link icon")](http://docs.couchdb.org/en/1.6.1/intro/security.html#authentication-database){:new_window}
to manage roles in Cloudant.
However,
you must turn off Cloudant security for those roles first.
To turn off Cloudant security,
`PUT` a JSON document to the `_security` endpoint of the database.
For example, `https://<username>.cloudant.com/<database>/_security`.

_Example of using HTTP to submit a modification request:_

```http
PUT /$DATABASE/_security HTTP/1.1
Content-Type: application/json
```
{:codeblock}

_Example of using the command line to submit a modification request:_

```sh
curl https://$USERNAME:$PASSWORD@$USERNAME.cloudant.com/$DATABASE/_security \
	-X PUT \
	-H "Content-Type: application/json" \
	-d @request-body.json
```
{:codeblock}

_Example modification request, in JSON format:_

```json
{
	"couchdb_auth_only": true,
	"members": {
		"names": ["member"],"roles":[]
	},
	"admins": {
		"names": ["admin"],"roles":[]
	}
}
```
{:codeblock}

_Example response:_

```json
{
	"ok" : true
}
```
{:codeblock}
