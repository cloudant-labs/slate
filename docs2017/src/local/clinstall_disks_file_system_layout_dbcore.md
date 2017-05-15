---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-13"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Disks and file system layout on a DBCore node

Cloudant&reg; Local stores files on a single partition. Learn more
about disks and file system layout on a DBCore node.
{:shortdesc}

The partition layout of DBCore files includes the following
files.

*   CouchDB files for each shard of a database
*   View database files
*   Lucene search index files
*   Geo index files

## Database files

This example shows how a database node might look.

```
/srv/cloudant/db/dbs.couch            <---  node-local couch DB file of all DBs
/srv/cloudant/db/nodes.couch          <---  node-local couch DB file of all nodes in the cluster
/srv/cloudant/db/cluster001/          <--- cluster-based user
  users.couch                         <--- node-local couch DB file of users on this cluster
/srv/cloudant/db/shards/              <---- shards directory
  00000000-0aaaaaa9/                  <--- one dir per shard range
    cluster001/                       <--- all DBs for this user
      stats.1348021480.couch          <--- shard of cluster wide stats DB
      users.1348018682.couch          <--- older version of sharded users DB 
                                           (note timestamp in file name)
      users.1348020303.couch          <--- latest version of sharded users DB
    userfoo/                          <--- all DBs for user userfoo 
      testdb1.1351859018.couch        <--- sharded version testdb1 db for user userfoo
      testdb2.1348081688.couch
      testdb3.1348081700.couch
      testdb4.1348394170.couch
      testdb4.1348394460.couch
      ..
      testdb303.1348081734.couch
  0aaaaaaa-15555553
  ...
  eaaaaa9c-f5555545
  f5555546-ffffffff
```
{:codeblock}

## View Index files

```
/srv/cloudant/view_index/.shards/     <--- where view index shards are stored 
                                           (not different from DB files)
  00000000-0aaaaaa9/
  0aaaaaaa-15555553/                  <--- per shard directory
    cluster001/                       <--- cluster user 
      stats.1348021480_design         <--- stats DB design doc
      users.1348020303_design         <--- users DB design doc 
    userfoo/                          <--- user directory
      testdb1.1351859018_design       <--- design docs for DB testdb1
      testdb2.1348081688_design
      testdb3.1348081700_design
      testdb4.1348394460_design
      ... 
      testdb303.1348081734_design
  ...
  f5555546-ffffffff
```
{:codeblock}
 
## Search files

``` sh
/srv/cloudant/search_index/shards/    <--- search index shards
  00000000-0aaaaaa9/      
  0aaaaaaa-15555553/                  <--- per shard directory
    userfoo/                          <--- user directory
      testdb1.1350387023              <--- per user, per shard DB search index
      testdb2.1348081700
      testdb3.1354707402
      testdb4.1348081723
      testdb4.1351155794
  ...
  f5555546-ffffffff/
```
{:codeblock}

## Geo Index files

Geo index files are stored in `/srv/cloudant/geo_index/`.
