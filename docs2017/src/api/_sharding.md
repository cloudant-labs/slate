---
layout: post
date:   2016-11-04
title: Sharding
tags:
- toc
---

## How is data stored in Cloudant?

Every database in Cloudant is formed of one or more distinct _shards_, where the number of shards is referred to as _Q_. A shard is a distinct subset of documents from the database and is physically stored in triplicate. Each shard copy is called a shard _replica_. Each shard replica is stored on a different server.

![sharding](images/sharding-database.png)

A document is assigned to a particular shard using consistent hashing of its ID, so will always reside on a given shard and a given set of servers.

![document consistent hashing](images/sharding-document.png)

One caveat to a document being always on the same set of servers is that sometimes shards will be _rebalanced_ which involves moving replicas to different servers; the number of shards and replicas stays the same, and documents remain assigned to the same shard, but where each shard replica is stored changes.

The default _Q_ value is different for different clusters. We tend to tune this over time.

Technically, the number of replicas is also configurable. However, long experience has led us to strongly recommend three in all cases for both performance and data safety. We would never consider storing our own data with a different replica count.


## How does sharding affect performance?

The number of shards for a database is configurable because it interacts with database performance in a number of ways.

When a request comes into the database cluster, one node in the cluster is assigned as the _coordinator_ of that request. This coordinator makes internal requests to the nodes holding the data relevant to the request and returns the result to the client.

Because of this, single document lookup or write requests are in tension [conflict?] with the needs of aggregating query requests when considering the number of shards for a database:

- As each document is stored on a single shard, many shards allow for higher parallelism for single document lookup and write because the coordinator only has to make requests of the nodes holding that document.
- As queries need to process results from all shards, more shards introduce higher overheads for querying data because the coordinator must make one request per replica and combine the results in a streaming fashion before returning data to the client.

Therefore the request pattern should be established -- mostly single document operations or mostly queries, and which operations are time-sensitive -- before considering shard count.

From the above you'll note that for queries, the coordinator issues read requests to all replicas. This is because each replica maintains its own copy of the indexes which power queries. An important implication of this is that more shards will enable index building to be more parallelized, presuming document writes are evenly distributed across the shards in the cluster. However, it is hard to predict indexing load across the nodes in the cluster, so in practice this tends to be less useful than considering request patterns -- large number of document writes lead to larger shard counts anyway.

For data sizing, there are considerations with the number of documents per shard. Each shard holds its documents in a large B-tree on disk. Indexes are stored in the same way. As more documents are added to a shard, the depth an average document lookup or query must traverse the B-tree increases and slows down requests as more data must be read from caches or disk.

In general, Cloudant's [Did you mean Cloudant support or Cloudant's current experience?] current thought is to not exceed 10 million documents per shard. In terms of overall shard size, keeping shards under 10GB is helpful for operational reasons (smaller shards are easier to move over the network during rebalancing, for example) but isn't super important for performance.

Given these competing requirements, a single _Q_ value cannot work optimally for all cases. While Cloudant tunes the defaults for clusters over time as we observe usage patterns, for particular databases it's worth taking the time to consider future request patterns and sizing issues in order to select an appropriate number of shards. Testing with representative data and request patterns is essential for accurate estimations of good _Q_ values, but be prepared for production experience to alter those expectations.

### tl;dr

Some simple guidelines, though do bear in mind that the above considerations and particularly for larger databases consider testing with representative data:

- If your data is trivial in size -- a few tens or hundreds of MB, or thousands of documents -- there is little need for more than a single shard.
- For databases of a few GB or few million documents, single-digit shard counts work fine, consider 8.
- For larger databases of tens to hundreds of millions of documents or tens of GB, consider 16.

Above this, consider manually sharding your data into several databases. For larger databases, consider sending Cloudant a quick email or support request for advice.

These numbers are currently a bit more folklore than fact, derived from experience. We're currently working on validating these experimentally.

## API

### Setting shard count

The number of shards, _Q_, for a database is set when the database is created. It cannot be changed later. To do this, use the _q_ query string parameter:

```
curl -XPUT -u myaccount https://myaccount.cloudant.com/mynewdatabase?q=8
```

Note that setting _Q_ for databases is currently disabled on most multi-tenant clusters. For these clusters, trying to set _Q_ will result in a `403` response with the body:

```
{"error":"forbidden","reason":"q is not configurable"}
```

### Setting the replica count

CouchDB 2+ allows changing the replica count. Cloudant, however, doesn't suggest changing this from the default (3) under any circumstances and disallows specifying different values when creating a database. For further help, contact Cloudant support.

### What about these _R_ and _W_ arguments I hear about?

Certain individual document requests can have arguments which affect the coordinator's behaviour. These arguments are known as _R_ and _W_ after their names in the request querystring. They can be only be used for single document operations and have _no effect_ for query-style operations.

Typically, _R_ and _W_ are not that useful to specify. In particular, specifying either _R_ or _W_ does not alter consistency for that read or write.

#### What is _R_?

_R_ can be used for single document lookups. It affects how many responses that the coordinator waits to receive from nodes hosting the replicas of the shard hosting the document before it will respond to the client. 

Setting _R_ to _1_ can improve throughput because the coordinator is able to send a response sooner. The default for _R_ is _2_, which is a majority of replicas (if the number of replicas is higher or lower than _3_, the default for _R_ changes appropriately).

#### What is _W_?

_W_ can be specified on single document write requests. Like _R_, _W_ affects how many responses the coordinator waits to receive before it replies to the client. It's important to reiterate that _W_ doesn't affect actual write behaviour in any way, however.

The value of _W_ doesn't affect whether the document is written within the database or not. Instead, the only effect of specifying _W_ is that the client can learn from a request's HTTP status code whether or not _W_ nodes responded to the coordinator: the coordinator waits up to a timeout for _W_ responses from nodes hosting copies of the document, then sends its response to the client.
