## Sharding

###	 Data storage in Cloudant

Each Cloudant database is formed by `Q` distinct shards, where `Q` is one shard but usually more than one shard. A shard is a distinct subset of documents from the database and is physically stored in triplicate. A shard copy is called a shard replica. A shard replica is stored on a different server.

![Sharding a database](images/database_shard.png)

Each document is assigned to a particular shard using consistent hashing of its ID, and always resides on a specific shard and set of servers, with one exception. 

![Assigning a document to a shard](images/database_shard.png)

A rebalance moves replicas to different servers. While the number of shards and replicas stay the same and the documents stored in the shard remain assigned to the same shard, the disk each replica is written to changes.  

You can tune the default `Q` value for different clusters as you learn more about your environment. Technically, the number of replicas can also be configured. However, it is a best practice to use three shard replicas to maintain performance and data integrity. 

###	Sharding and performance

You can configure, or tune, the number of shards for each database. Your configuration interacts with database performance in a number of ways.

When the database cluster receives a request, Cloudant assigns the request to one node in the cluster as the coordinator of that request. This coordinator makes internal requests to the nodes that hold the data that is relevant to the request and returns the result to the client.

When you consider the number of shards in a database, a single document lookup or write request can conflict with the needs of aggregating query requests.

*	Since each document is stored on a single shard, multiple shards allow higher parallelism for single document lookup and write, because the coordinator only makes requests of the nodes holding that document.
*	As queries process results from all shards, multiple shards introduce higher overhead for querying data. In this case, the coordinator must make one request per replica and organize the results as a stream before returning data to the client.

Therefore, the request pattern must be established as mostly single document operations or queries, and time-sensitive operations before considering the shard count. In addition, queries read data from all replicas, because each replica maintains its own copy of indexes that power queries. When document writes are evenly distributed across shards in the cluster, more shards enable index building which improves parallelism. It is difficult to predict indexing load across the nodes in a cluster. In practice, this task is less useful than considering request patterns, because large numbers of document writes lead to larger shard counts.

For data sizing, consider the number of documents per shard. Each shard holds its documents in a large B-tree on disk. Indexes are stored using the same method. As more documents are added to a shard, the depth that an average document lookup or query must traverse in the B-tree increases and slows down the request as more data must be read from a cache or disk.

As a best practice, your shard size must not exceed 10 million documents per shard. In terms of overall shard size, it is good to keep shards under 10GB, but not required. 

Given these competing requirements, a single `Q` value cannot work optimally in all cases. You can tune the defaults for a cluster over time. However, for large or complex databases, it is valuable to consider future sizing issues. It is a valuable practice to analyze the request patterns so you can select the best number of shards. To make accurate estimates for good `Q` values, test the database with representative data and request patterns. However, when you move to production, be prepared to alter the expectations that originated during testing.  

###	Guidelines for using shards

Remember the considerations discussed earlier, especially for large databases, and consider testing with representative data as described in the following table. 
 
 [TODO-ADD TABLE]


| Database Size&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Database Size | # of Shards |
|---------------|---------------|-------------|
| Small | 10 - 100 MB, or 1,000 documents | 1 |
| Medium | 100+ GB and a few million documents | Single digit shard, for example, 8 GB |
| Large | 10 GB, or 10 - 100 million documents | 16 |

 
*	A small database equals 10 - 100 MB, or 1,000 documents. Use a single shard for a small database. 
*	A mid-size database equals 100 GB, and a few million documents. Use a single-digit shard count, such as 8 GB, with a mid-size database. 
*	A large database equals 10 to 100 million documents or 10 GBs of data. For large databases, use 16 shards. 

Consider manually sharding your data into several databases. If your database is large, and you would like advice from support, send an email to Cloudant support [TODO-email address].

###	API

####	Setting the shard count

You set the number of database shards, `Q`, when you create the database. The number of shards cannot be changed. To set the number of shards, run the following `Q` query string parameter. 

```curl
	-XPUT -u myaccount https://myaccount.cloudant.com/mynewdatabase?q=
```

Remember the `Q` setting for databases is currently disabled on most multi-tenant clusters. If you try to set the `Q` parameter for these clusters, you might see a 403 response within the body, for example. 

```
{"error":"forbidden","reason":"`q` is not configurable"}
```

####	Setting the replica count

CouchDB 2+ allows you to change the replica count. Cloudant does not recommend that you change from the default setting under any circumstances. If you need assistance with this, contact Cloudant support.

####	Using the `R` and `W` arguments

Some individual document requests contain arguments that affect the coordinator’s behavior. These arguments are known as `R` and `W` after their names in the request querystring. You can use these arguments for single document operations since they have no effect for query-style operations. While you can set `R` or `W` arguments to higher numbers, that does not increase the consistency for that read or write operation. 

####	`R` arguments

`R` can be used for single document lookups. It affects how many responses from that the coordinator waits to receive from nodes hosting the replicas of the shard hosting the node before it will respond to the client.

When you set `R`, the 
`R` can be used for single document lookups. The `R` setting does affect the number of responses  how many responses from that the coordinator waits to receive from nodes hosting the replicas of the shard hosting the node before it will respond to the client

Setting `R` to 1 can improve throughput because the coordinator is able to send a response sooner. The default for `R` is 2, which is a majority of replicas (if replicas is higher or lower than 3, the default for `R` changes appropriately).

####	`W` arguments

`W` can be specified on single document write requests. Again, it affects how many responses the coordinator waits to receive before it replies to the client. It’s important to reiterate that `W` doesn’t affect actual write behavior in any way, however.

Specifying `W` as 1 again can improve response times to the client, but the coordinator is still issuing all three write requests within the database (one to each replica holding the document). Specifying 2, the default, or more as W allows the client to receive notification that more replicas have been updated with the new document – explaining why `W` doesn’t change the actual behavior of writes, so doesn’t change the databases consistency properties for that request.
