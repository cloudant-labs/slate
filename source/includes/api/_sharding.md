## Sharding

A database partition that separates large databases into smaller, faster, more easily managed parts called data shards. Each data shard runs on a separate database server instance to spread load. 

### Sharding Parameters

To set appropriate shard values, you must understand the parameters and the circumstances under which it is appropriate to adjust values. The four parameters are N, Q, R, and W, as described below. 

N – number of copies or replicas of the data
Q – number of unique shards for a database
R – read quorum
W – write quorum

####"N" - Number of copies or replicas 
You can store N copies of data and configure them by database. The default value for N is 3. The value rarely changes. 

The node computes:
*	key=f(doc._id)
*	get_shards(key ==> shard
*	get_nodes(shard) ==> [N1,N3,N4]
*	Nodesforeach: store(doc)

For example: 

```
{
	"author" : "John Smith",
	"subject" : "I like fish", 
	"posted_date" : "2013-02-8",
	"tags" : ["fish","ocean","food"],
	"body" : "I like to cook and eat fish."
}
```
PUT /db10/docid92

Database computes:
*	Key = f("docid92")
*	get_shards(key) ==> shard
*	get_node(shard) ==> [N1,N3,N4]
*	nodes.foreach: store(doc)


####"Q" -  Sharding
You configure sharding by database, dedicated and local tenants only. When you create the database, you specify the configuration for the shards. To change the value of Q, you must replicate to a new database. It is a good idea to create more shards than the number of cluster nodes in your environment. 

The formula to calculate the total number of shards is Q * N = total shards. The default value for Q includes, Q=4 for multi-tenant and Q=8 for dedicated/local tenant. Q is degree of parallelism.  

When you configure the value for Q, keep the following recommendations in mind. 

Rule | Description
General | Few large databases use large 
 | Q Many small databases use small Q
Maximum shards > degree of parallelism | Approximately equal to the number of spindles in the cluster or number of cores in the cluster.
Shard file size | 10GB or less
 | 100GB maximum size. A larger file size affects compaction. 
Read versus write rate | Large numbers of writes/views builds - require more shards.
 | Small number of writes - require fewer shards.
 | More shards - require more work for requests, particularly views.

#####Q example

Database | Docs | Avg Doc Size | Read/sec | Write/sec | # Views | Doc to view read ratio | Q value 
-----|----------------------------------------------------
Activities | 240m | 1k | 150 | 25 | 5 | 0.5 | 16-24
Users | 24m | 2k | 150 | 25 | 4 | 0.1 | 8-12 
Social Feed | 50m | .2k | 40 | 8 | 4 | 0.1 | 4-8

####Indexing – Views, Search, Geo
Cloudant builds indexes locally for each shard. Shards run in parallel and use all available CPUs to distribute the load. During a query, the merge sort runs. 

####"R" - Read quorum 
The R value measures when the database serves the result of a query. For example, when the database provides the answer or when enough nodes provide the answer. "Enough" means the shard tries to read it from N nodes and R nodes reply and agree. 

The default R value is R=2 (majority). Set R=1 to minimize latency, and set R=N to maximize consistency. 

####"W" - Write quorum 
The W value measures the times a database writes data and when enough nodes write data. "Enough" means the shard tried to store all replicas (N copies) when W nodes replied after fsyncing to disk. 

The default W value is W=2 (majority). Set W=1 to maximize throughput and set W=N to maximize consistency. 



