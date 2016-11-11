## Sharding

###	 Data storage in Cloudant

Each Cloudant database is formed by `Q` distinct shards, where `Q` is one shard but usually more than one shard. A shard is a distinct subset of documents from the database and is physically stored in triplicate. A shard copy is called a shard replica. A shard replica is stored on a different server.

![Sharding a database](images/database_shard.png)

Each document is assigned to a particular shard using consistent hashing of its ID, and always resides on a specific shard and set of servers. 

![Assigning a document to a shard](images/database_shard.png)

However, during a rebalance, the disk each replica is written to changes. The number of shards and replicas stays the same, and the documents stored in the shard remain assigned to the same shard. 

You can tune the default `Q` value for different clusters as you learn more about your environment. Technically, the number of replicas can also be configured. However, it is a best practice to use three shard replicas to maintain performance and data integrity. 

###	Sharding and performance

You can configure, or tune, the number of shards for each database. Your configuration interacts with database performance in multiple ways.

When the database cluster receives a request, Cloudant assigns the request to one node in the cluster as the coordinator of that request. This coordinator makes internal requests to the nodes that hold the data relevant to the request. The coordinator also returns the results to the client.

When you consider the number of shards in a database, a single document lookup or write request can conflict with the needs of aggregating query requests.

*	The coordinator only makes requests of the nodes holding the document. Since each document is stored on a single shard, multiple shards allow higher parallelism for single document lookups and writes. 
*	As queries process results from all shards, multiple shards introduce higher overhead for querying data. In this case, the coordinator must make one request per replica and organize the results as a stream before returning data to the client.

Therefore, before you consider the shard count, the request pattern must be established as predominantly single document operations or queries, and time-sensitive operations. In addition, queries read data from all replicas, because each replica maintains its own copy of indexes that power queries. When document writes are evenly distributed across shards in the cluster, more shards enable index building which improves parallelism. It is difficult to predict indexing load across the nodes in a cluster. In practice, this task is less useful than considering request patterns because large numbers of document writes lead to larger shard counts.

For data sizing, consider the number of documents per shard. Each shard holds documents in a large B-tree on disk. Indexes are stored using the same method. As more documents are added to a shard, the depth that an average document lookup or query must traverse in the B-tree increases and slows down the request as more data must be read from a cache or disk.

As a best practice, your shard size must not exceed 10 million documents per shard. In terms of overall shard size, it is good to keep shards under 10GB, but this limit is not required. 

Given these competing requirements, a single `Q` value cannot work optimally in all cases. You can tune the defaults for a cluster over time. However, for large or complex databases, it is prudent to consider future sizing issues. It is also a good practice to analyze the request patterns so you can select the most appropriate number of shards. To make accurate estimates for good `Q` values, test the database with representative data and request patterns. However, when you move to production, be prepared for different results than those you learned from testing.  

###	Guidelines for using shards

Remember the considerations discussed earlier, especially for large databases. Consider testing with representative data using the guidelines described in the following table. 

| Database | Size | # of Shards |
|------|------|-------------|
| Small | 10 - 100 MB, or 1,000 documents | 1 |
| Medium | 100+ GB and a few million documents | Single digit shard, for example, 8 GB |
| Large | 10 GB, or 10 - 100 million documents | 16 |

Consider manually sharding your data into several databases. If your database is large, and you would like advice from support, send an email to [Cloudant support](support@cloudant.com).

###	API

####	Setting the shard count

You set the number of database shards, `Q`, when you create the database. The number of shards cannot be changed. To set the number of shards, run the following `Q` query-string parameter. 

```curl
	-XPUT -u myaccount https://myaccount.cloudant.com/mynewdatabase?q=
```

Remember the `Q` setting for databases is currently disabled on most multi-tenant clusters. If you try to set the `Q` parameter for these clusters, you might see a 403 response within the body, as seen in the following example. 

```
{"error":"forbidden","reason":"`q` is not configurable"}
```

####	Setting the replica count

CouchDB 2+ allows you to change the replica count. Cloudant does not recommend that you change from the default setting under any circumstances. If you need assistance with this, contact [Cloudant support](support@cloudant.com).

####	Using the `R` and `W` arguments

Some individual document requests contain arguments that affect the coordinator’s behavior. These arguments are known as `R` and `W` after their names in the request query string. You can use these arguments for single document operations since they have no effect on query-style operations. While you can set `R` or `W` arguments to higher numbers, that does not increase the consistency for the read or write operation. 

####	`R` arguments

The `R` argument can be used for single document lookups. When you set `r` value, it defines the number of responses the coordinator will wait to receive before responding to the client. The responses come from the nodes hosting the shard replicas. 

The coordinator can respond more quickly if you set `R` to 1. The default setting for `R` is 2. Most replicas use this setting. If a replica is higher or lower than 3, the default for `R` changes appropriately.

####	`W` arguments

The `W` argument can be specified on single document write requests. Like the `r` argument, `w` affects the number of responses the coordinator will wait to receive before it replies to the client. Keep in mind that `W` does not affect the write behavior in any way.

Setting `W` to 1 can improve response times to the client, but the coordinator is still issuing all three write requests within the database. For example, one write request is sent to each replica that holds the document. The default setting for `w` is 2. You can set a higher `w` value since `w` lets the client receive notifications when additional replicas are updated with the new document. Since `w` does not change the write behavior, it cannot change the database consistency properties for that request.
