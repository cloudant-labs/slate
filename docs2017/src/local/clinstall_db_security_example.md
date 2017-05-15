---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-17"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Database-level security example

If you are not familiar with the CouchDB model for database-level
security, the following example illustrates how it works.
{:shortdesc}

In the sample commands,
replace the following variables:

<p><ul><li>Replace `admin:password` with the user ID and password for your admin user.</li>
<li>Replace `loadbalancer.example.com` with the host name of your configured cluster load balancer.</li>
<li>Replace `db1` with the name of your database.</li></ul></p>

<code></code>

<ol>
<li>Confirm that the `admin` user is specified in the `local.ini` file in the `[admins]` section.</li>
<li>Create the `db1` and `db2` databases.
<p>`$ curl -X PUT -u admin:password https://loadbalancer.example.com/db1`<br>
`$ curl -X PUT -u admin:password https://loadbalancer.example.com/db2`</p>
<p>You receive an `{"ok":true}` message after the databases
    are created.</p></li>
<li>Create a test document in the `db2` database by running these
    commands as an unauthenticated user.

 <p>`$ curl -X POST http://loadbalancer.example.com/db2 \`<br>
    `> -H "Content-Type: application/json" \`<br>
    `> -d "{\"likes\": \"turtles\"}"`
</p>

<p>You receive an `{"ok":true}` message after the document is
    created, and the message includes the document ID and revision
    number for the document.</p>

<p>`{"ok":true,"id":"171806ad7968475970bf5450e91a5259","rev":"1-e6accc814683c1cadf6c74b492570c42"}`</p>
   
<p>The unauthorized user was allowed to add the test document
    because no database-level security is in place for db2. By
    default, CouchDB and Cloudant&reg; Local allow anonymous reads and
    writes, which is called "admin party" mode. Many CouchDB users
    choose to use this approach and put their databases behind a
    firewall without configuring any additional database-level
    security.</p></li>
<li>Create a `_users` database and two test users who are named
    `member` and `outsider` using your administrator credentials:
<ol type=a>
<li>Create the `_users` database.
<p>`$ curl -X PUT http://loadbalancer.example.com/_users -u admin:password`</p>

<p>After the database is created, you receive an `{"ok":true}`
        message.</p></li>
<li>Create the `member` user.
<p>`$ curl -X PUT http://loadbalancer.example.com/_users/org.couchdb.user:member \`<br>
        `> -H "Accept: application/json" \`<br>
        `> -H "Content-Type: application/json" \`<br>
        `> -d '{"name": "member", "password": "f1wu8tvp5gGe", "type": "user"}' \`<br>
        `> -u admin:password`
        
        <p>The password for the `member` user is specified on the
        fourth line.</p>

        <p>After the document is created, you receive an `{"ok":true}`
        message that includes the document ID and revision number
        for that user document as seen in this example.</p>
<p>`{"ok":true,"id":"org.couchdb.user:member", "rev":"1-d9bdb39bac9288b154cdf5cc4d643ce9"}`</p></li>
<li>Create the `outsider` user.

<p>`$ curl -X PUT http://loadbalancer.example.com/_users/org.couchdb.user:outsider \`<br>
        `> -H "Accept: application/json" \`<br>
        `> -H "Content-Type: application/json" \`<br>
       `> -d '{"name": "outsider", "password": "ncGfv9bcDBn0", "type": "user"}' \`<br>
        `> -u admin:password`
</p>
<p>The password for the `outsider` user is specified on the
        fourth line.</p>

<p>For example, after the document is created, the message
        `{"ok":true}` appears that includes the document ID and
        revision number for that user document.</p>

<p>`{"ok":true,"id":"org.couchdb.user:outsider","rev":"1-7d2b68aca9a2634fee51c49e4d7d39ca"}`</p>

<p>Both users are now listed as valid users in the `_users`
        database and were granted permission to create JSON
        documents. However, neither user has the authority to add
        documents to a database that includes database-level
        security.</p>
</li>
</ol>
</li>
<li>Add database-level security by adding the `_security` object on
    one of your test databases.

<p>`$ curl -X PUT http://loadbalancer.example.com/db1/_security \`<br>
`> -u admin:password \`<br>
`> -H "Content-Type: application/json" \`<br>
`> -d "{"admins": {"names": ["admin"], "roles": []}, "members": {"names": ["member"], "roles": []}}"`
</p>
    
    <p>You receive an `{"ok":true}` message after the security is set
    up.</p>
    
    <p>In the preceding example, security is set up for the `db1`
    database only. Moreover, only the `member` user is granted
    authority to create JSON documents in that database, other
    than the `admin` user, who always has authority to create JSON
    documents.</p></li>
<li>Confirm that access to the `db1` database is restricted to
    authorized users only.
<ol type=a>
<li>Run this command to access the `db1` database as an
        unauthorized user.
<p>`$ curl http://loadbalancer.example.com/db1`</p>
<p>An unauthorized user is a user who is not in the `_users`
        database.</p>
<p>When the user is not authorized to access the `db1`
        database, you receive the following error message.</p>
<p>`{"error":"unauthorized","reason":"You are not authorized to access this db."}`</p>
</li>
<li>Run this command to access the `db1` database as the
        `outsider` user.
<p>`$ curl http://loadbalancer.example.com/db1 -u outsider:ncGfv9bcDBn0`</p>

<p>When the `outsider` user is not authorized to access the
        `db1` database, you receive the following error message.</p>

<p>`{"error":"unauthorized","reason":"You are not authorized to access this db."}`</p></li>
<li>Run this command to access the `db1` database as the `member`
        user.
<p>`$ curl http://loadbalancer.example.com/db1 -u member:f1wu8tvp5gGe`</p>
<p>When the `member` user is authorized to access the
        database, you receive a message like the one in this (abbreviated)
        example.</p>
<p>`{"db_name":"db1","update_seq":"10-g1A...bHo","sizes":{"file":107887,"external":76," active":1942},"purge_seq":0,"other":{"data_size":76},"doc_del_count":1,"doc_count":0,"disk_size":107887,"disk_format_version":6,"data_size":1942,"compact_running":false,"instance_start_time":"0"}`</p>
</li>
<li>Run this command to access the `db1` database as the `admin`
        user.
<p>`$ curl http://loadbalancer.example.com/db1 -u admin:password`</p>
<p>When the `admin` user is authorized to access any database,
        including `db1`, you receive a message like the one in this (abbreviated)
        example.</p>
<p>`{"db_name":"db1","update_seq":"11-g1A...bHp","sizes":{"file":128367,"external":175, "active":2282},"purge_seq":0,"other":{"data_size":175},"doc_del_count":1,"doc_count":1,"disk_size":128367,"disk_format_version":6,"data_size":2282,"compact_running":false,"instance_start_time":"0"}`</p>
</li>
</ol>
</li>
<li>Confirm that only authorized users can add JSON documents to
    the `db1` database.
<ol type=a>
<li>Add a document to the `db1` database as the `outsider` user.
<p>`$ curl -X PUT http://loadbalancer.example.com/db1/foo \`<br>
         `-H "Accept: application/json" \`<br>
         `-H "Content-Type: application/json" \`<br>
         `-d '{"bar": "baz"}' \`<br>
        `-u outsider:ncGfv9bcDBn0`
</p>

<p>When the `outsider` user is not authorized to access the
        database, you receive a message like the one in this
        example.</p>
<p>`{"error":"unauthorized","reason":"You are not authorized to access this db."}`</p>
</li>
<li>Add a document to the `db1` database as the `member` user.
<p>`$ curl -X PUT http://loadbalancer.example.com/db1/foo \`<br>
         `-H "Accept: application/json" \`<br>
         `-H "Content-Type: application/json" \`<br>
         `-d '{"bar": "baz"}' \`<br>
         `-u member:f1wu8tvp5gGe`</p>
<p>When the `member` user is authorized to add documents to
        the database, you receive a `{"ok":true}` message like the
        one in this example.</p>

<p>`{"ok":true,"id":"foo","rev":"1-c86e975fffb4a635eed6d1dfc92afded"}`</p>
<p>The message includes the following information about the
        document: document ID, which is `foo` in this example, and revision number.</p>
</li>
<li>Add a document to the `db1` database as the `admin` user.

<p>`$ curl -X PUT http://loadbalancer.example.com/db1/foo2 \`<br>
         `-H "Accept: application/json" \`<br>
         `-H "Content-Type: application/json" \`<br>
         `-d '{"bar": "baz"}' \`<br>
         `-u admin:password`</p>

<p>When the `admin` user is authorized to add documents to the
        database, you receive an `{"ok":true}` message like the one
        in this example.</p>
<p>`{"ok":true,"id":"foo2","rev":"1-c86e975fffb4a635eed6d1dfc92afded"}`</p>
<p>The message includes the following information about the
        document: document ID, which is `foo2` in this example, and revision number.</p></li></ol>
</li>
<li>Confirm that only authorized users can create design
    documents.
<p>Design documents are similar to materialized views or indexes
    in a relational database management system (RDBMS). In Couch
    DB and Cloudant, only admin-level users can create design
    functions like views, shows, and others, as illustrated in
    this step.
</p>
<ol type=a>
<li>Create a design document in the `db1` database as the
        `outsider` user.

<p>`$ curl -X PUT http://loadbalancer.example.com/db1/_design/all \`<br>
            `-H "Accept: application/json" \`<br>
            `-H "Content-Type: application/json" \`<br>
            `-d '{"language":"javascript", \`<br>
            `"views":{"all":"mapin ":function(doc){emit(doc._id, 1)};","reduce": "_count"}}' \`<br>
            `-u outsider:ncGfv9bcDBn0`</p>        
<p>When the `outsider` user is not authorized to create a
        design document, you receive a message like the one in
        this example.</p>       
<p>`{"error":"unauthorized","reason":"You are not authorized to access this db."}`</p>
</li>
<li>Create a design document in the `db1` database as the
        `member` user.
<p>`$ curl -X PUT http://loadbalancer.example.com/db1/_design/all \`<br>
            `-H "Accept: application/json" \`<br>
            `-H "Content-Type: application/json" \`<br>
            `-d '{"language":"javascript", \`<br>
            `"views":{"all":{"map":"function(doc){emit(doc._id, 1)};","reduce":"_count"}}}' \`<br>
            `-u member:f1wu8tvp5gGe`</p>
<p>When the `member` user is not authorized to create a
        design document, you receive a message like the one in
        this example.</p>
        
<p>`{"error":"unauthorized","reason":"You are not a db or server admin."}`</p>

<p>As the message indicates, you must be an administrator
        user to create a design document.</p></li>
<li>Create a design document in the `db1` database as the
        `admin` user.
<p>`$ curl -X PUT http://loadbalancer.example.com/db1/_design/all \`
        `-H "Accept: application/json" -H "Content-Type: application/json" \`
        `-d '{"language":"javascript", \`
        `"views":{"all":{"map":"function(doc){emit(doc._id,1)};","reduce":"_count"}}}'\`
        `-u admin:password`</p>
<p>When the `admin` user is authorized to create a design
        document, you receive a message like the one in this
        example.</p>

<p>`{"ok":true,"id":"_design/all","rev":"1-5c0878a3c1cabf82004ed85113fa59c6"}`</p>
<p>The message includes the following information about
        the design document: document ID, which is `_design/all` in this example,
        and revision number.</p>
</li>
</ol>
</li>
</ol>
