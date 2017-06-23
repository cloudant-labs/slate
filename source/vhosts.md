---
title: Cloudant Documentation - Virtual Hosts

language_tabs:
  - http 
  - shell: curl
#  - javascript: node.js
#  - python

toc_footers:
  - <a href="https://cloudant.com/">Cloudant</a>
  - <a href="https://cloudant.com/sign-up/">Sign up</a> / <a href="https://cloudant.com/sign-in/">Sign in</a>
  - <a href="http://stackoverflow.com/questions/tagged/cloudant">Cloudant on StackOverflow</a>
  - <a href='http://github.com/tripit/slate'>Documentation Powered by Slate</a>
  - <a href="https://github.com/cloudant-labs/slate">Documentation Source</a>

---

## Virtual hosts

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the 'Virtual hosts' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/vhosts.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Virtual hosts (vhosts) are a way to make cloudant serve data from a different domain than the one normally associated with your Cloudant account. You can create as many vhosts as needed and point them to any endpoint in your Cloudant account. Vhosts are often used to point to a `_rewrite` endpoint of a design document in order to use Cloudant as a web server. You need to have the admin role in order to use any of the vhost endpoints.

### Listing virtual hosts

> Listing all vhosts

```shell
curl "https://$ACCOUNT.cloudant.com/_api/v2/user/virtual_hosts"
```

```http
GET /_api/v2/user/virtual_hosts HTTP/1.1
Host: $ACCOUNT.cloudant.com
```

> Example response

```json
{
  "virtual_hosts": [
    [
      "system1.business.org", 
      ""
    ], 
    [
      "system2.business.org", 
      "/specificpath"
    ]
  ]
}
```

To list all virtual hosts in your account, send a `GET` request to `/_api/v2/user/virtual_hosts`.

The JSON response details all of the virtual hosts,
and any virtual path associated with each host.

### Creating a virtual host

> Creating a vhost

```shell
curl "https://$ACCOUNT.cloudant.com/_api/v2/user/virtual_hosts" -X POST -d '@vhost.json' -H 'Content-Type: application/json'
```

```http
POST /_api/v2/user/virtual_hosts HTTP/1.1
Host: $ACCOUNT.cloudant.com
Content-Type: application/json
```

```json
{
  "host": "www.example.com",
  "path": "/_api/v2/user/virtual_hosts"
}
```

> Example response

```json
{
  "ok": true
}
```

To create a virtual host, you send a `POST` request to the `/_api/v2/user/virtual_hosts` endpoint with a description of the vhost in a JSON object in the request body. The JSON document contains these fields:

 * `host`: The domain name you want to use for the vhost.
 * `path`: An (optional) endpoint in your Cloudant account the vhost should point to.

### Deleting a virtual host

> Deleting a vhost

```shell
curl "https://account.cloudant.com/_api/v2/user/virtual_hosts" -X DELETE -d '@vhost.json' -H 'Content-Type: application/json'
```

```http
DELETE /_api/v2/user/virtual_hosts HTTP/1.1
Host: $ACCOUNT.cloudant.com
Content-Type: application/json
```

```json
{
  "host": "www.example.com"
}
```

> Example response

```json
{
  "ok": true
}
```

To delete a vhost, send a `DELETE` request to `/_api/v2/user/virtual_hosts` with the host to delete specified in the request body as shown in the example.
