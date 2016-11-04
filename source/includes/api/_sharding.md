##	Sharding with Cloudant


##	(How is data stored in Cloudant?)
Every database in Cloudant is formed of Q distinct shards, where Q is one or, almost always, more. A shard is a distinct subset of documents from the database and is physically stored in triplicate. Each shard copy is called a shard replica. Each replica is stored on a different server.

A document is assigned to a particular shard via consistent hashing of its ID, so will always reside on a given shard and so a given set of servers.
One caveat to a document being always on the same set of servers is that sometimes shards will be rebalanced which involves moving replicas to different servers; the number of shards and replicas stays the same, and documents remain assigned to the same shard, but the nodes each replica is written to disk on changes.

The default Q value is different for different clusters. We tend to tune this over time.

Technically, the number of replicas is also configurable. However, long experience has lead us to strongly recommend three in all cases for both performance and data safety. We would never consider storing our own data with a different replica count.


##	How does sharding affect performance?
The number of shards for a database is configurable because it interacts with database performance in a number of ways.

When a request comes into the database cluster, one node in the cluster is assigned as the coordinator of that request. This coordinator is in charge of making internal requests to the nodes holding the data relevant to the request and in returning the result to the client.

Because of this, single document lookup or write requests are in tension with the needs of aggregating query requests when considering the number of shards for a database:

*	As each document is stored on a single shard, many shards allows for higher parallelism for single document lookup and write because the coordinator only has to make requests of the nodes holding that document.
*	As queries need to process results from all shards, more shards introduce higher overheads for querying data because the coordinator must make one request per replica and combine the results in a streaming fashion before returning data to the client.

Therefore the request pattern should be established – mostly single document operations or mostly queries, and which operations are time-sensitive – before considering shard count.

In addition, from the above you’ll note that queries read data from all replicas. This is because each replica maintains its own copy of the indexes which power queries. An important implication of this is that more shards will enable index building to be more parallelized, presuming document writes are evenly distributed across the shards in the cluster. However, it is hard to predict indexing load across the nodes in the cluster, so in practice this tends to be less useful than considering request patterns – large number of document writes lead to larger shard counts anyway.

For data sizing, there are considerations with the number of documents per shard. Each shard essentially holds its documents in a large B-Tree on disk. Indexes are also stored in the same way. As more documents are added to a shard, the depth an average document lookup or query must traverse the B-Tree increases thereby slowing down the request as more data must be read from caches or disk.

In general, our current thought is to not exceed 10 million documents per shard. In terms of overall shard size, keeping shards under 10GB is helpful for our operations but isn’t super important for performance.

Given these competing requirements, it’s not possible for a single Q value to work optimally for all cases. We tune the defaults for clusters over time, but for particular databases it’s worth taking the time to consider future sizing issues and, most importantly, request patterns in order to select the best number of shards. Testing with representative data and request patterns is essential for accurate estimations of good Q values, but be prepared for production experience to alter those expectations.


##	tl;dr

Some simple guidelines, though do bear in mind the above considerations and particularly for larger databases consider testing with representative data:

*	If your data is trivial in size – a few tens or hundreds of MB, or thousands of documents – there is little need for more than a single shard.
*	For databases of a few GB or few million documents, single-digit shard counts work fine. Say 8.
*	For larger databases of tens to hundreds of millions of documents or tens of GB, consider 16.

Above this, consider manually sharding your data into several databases. Also consider shooting us a quick email or support request for advice, if your data is going to be this large.

These numbers are currently a bit more folklore than fact, derived from experience. We’re currently working on validating these experimentally.

##	API
Setting shard count

The number of shards, Q, for a database is set when the database is created. It cannot be changed later. To do this, use the q query string parameter:

curl -XPUT -u myaccount https://myaccount.cloudant.com/mynewdatabase?q=8
Note that setting Q for databases is currently disabled on most multi-tenant clusters. For these clusters, trying to set Q will result in a 403 response with the body:

{"error":"forbidden","reason":"q is not configurable"}

Setting the replica count

You may note that CouchDB 2+ allow changing the replica count. However, we don’t suggest changing this from the default under any circumstances so I’m not going to document it.

I refer you to Cloudant support for help here – they will probably be able to explain why changing the replica count isn’t wise for your use-case. If we find use-cases where it is a valid choice, I’ll update this.

##	What about these R and W arguments I hear about?

Certain individual document requests can have arguments which affect the coordinator’s behaviour. These are known as R and W after their names in the request querystring. They can be used for single document operations; they have no effect for query-style operations.

Typically, these are not that useful. A common misapprehension is that setting either R or W to a higher number increases the consistency for that read or write. This is incorrect.

##	What is R?

R can be used for single document lookups. It affects how many responses from that the coordinator waits to receive from nodes hosting the replicas of the shard hosting the node before it will respond to the client.

Setting R to 1 can improve throughput because the coordinator is able to send a response sooner. The default for R is 2, which is a majority of replicas (if replicas is higher or lower than 3, the default for R changes appropriately).

##	What is W?

W can be specified on single document write requests. Again, it affects how many responses the coordinator waits to receive before it replies to the client. It’s important to reiterate that W doesn’t affect actual write behavior in any way, however.

Specifying W as 1 again can improve response times to the client, but the coordinator is still issuing all three write requests within the database (one to each replica holding the document). Specifying 2, the default, or more as W allows the client to receive notification that more replicas have been updated with the new document – explaining why W doesn’t change the actual behavior of writes, so doesn’t change the databases consistency properties for that request.
