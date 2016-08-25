## Sharding

A shard, or data shard, is a database partition that separates large databases into smaller, faster, more easily managed parts. Each data shard runs on a separate database server instance to spread the load. 

### Sharding Parameters

To set appropriate shard values, you need to understand the parameters and when it is appropriate to adjust the parameters values. The four sharding parameters, N, Q, R, and W, are described below. 

####"N" - Number of copies or replicas 
You can store N copies of data and configure them by database. The value rarely changes. Default N value is N=3.  

The node computes.

* key=f(doc._id)
* get_shards(key ==> shard
* get_nodes(shard) ==> [N1,N3,N4]
* Nodesforeach: store(doc)

Here is an example.  

```json
{
	"author" : "John Smith",
	"subject" : "I like fish", 
	"posted_date" : "2013-02-8",
	"tags" : ["fish","ocean","food"],
	"body" : "I like to cook and eat fish."
}
```
`PUT /db10/docid92`

The database computes.

* Key = f("docid92")
* get_shards(key) ==> shard
* get_node(shard) ==> [N1,N3,N4]
* nodes.foreach: store(doc)


####"Q" - Sharding
You configure sharding by database, dedicated and local tenants only. When you create the database, you specify the configuration for the shards. To change the Q value, you must replicate to a new database. It is a good idea to create more shards than the number of cluster nodes in your environment. 

The formula to calculate the total number of shards is Q * N = total shards. Default Q value is Q=4 for multi-tenant and Q=8 for dedicated/local tenant. Q is degree of parallelism.  

When you configure the Q value, keep the following recommendations in mind. 

| Rule | Description |
|-----|--------------|
|General | Few large databases use large. <br>Many small databases use small.|
| Maximum shards > degree of parallelism | Approximately equal to the number of spindles in the cluster or number of cores in the cluster.|
|Shard file size | 10GB or less <br>100GB maximum size. A file size larger then 100GB affects compaction.|
|Read versus write rate | Large numbers of writes/views builds require more shards. <br>Small numbers of writes require fewer shards. <br>More shards require more work for requests, particularly views.|

#####Q example

Database | Docs | Avg Doc Size | Read/sec | Write/sec | # Views | Doc to view/read ratio | Q value 
---------|------|--------------|----------|-----------|---------|------------------------|---------
Activities | 240m | 1k | 150 | 25 | 5 | 0.5 | 16-24
Users | 24m | 2k | 150 | 25 | 4 | 0.1 | 8-12 
Social feed | 50m | .2k | 40 | 8 | 4 | 0.1 | 4-8

####Indexing – Views, Search, Geo
Cloudant builds indexes locally for each shard. Shards run in parallel and use all available CPUs to distribute the load. During a query, the mergesort runs. 

####"R" - Read quorum 
R value measures the reads served by the database as query results. For example, the results occur when the database provides the answer or when enough nodes provide the answer. "Enough" means the shard attempted to read from N nodes and R nodes replied and agreed. 

Default R value is R=2 (majority). To minimize latency, set R=1, or to maximize consistency, set R=N. 

####"W" - Write quorum 
The W value measures the times a database writes data and when enough nodes write data. "Enough" means the shard tried to store all replicas (N copies) when W nodes replied after fsyncing to disk. 

Default W value is W=2 (majority). To maximize throughput, set W=1, or to maximize consistency, set W=N. 



