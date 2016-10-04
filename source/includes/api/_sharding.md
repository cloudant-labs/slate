## Sharding

Database sharding in Cloudant and CouchDB 2.0 is the concept of dividing up a database into separate parts for the purpose of enabling high-availability of data, and the division of work among the nodes inside a cluster. These shards become roughly congruous to the number of files in the filesystem which contain the JSON data and indexes in the database.  

The number of total shards that a database contains is set at the time of its creation. While shards can be moved around a cluster for re-balancing purposes (during cluster expansion or contraction), shards cannot be increased or decreased in number. The number of unique shards in a Cloudant database is often described as its 'Q value'.  The number of replicas of those shards in the database is described as its 'N value'.  Therefore, the total number of 'files' the database has inside the cluster is equivalent to Q * N. 

In a dedicated Cloudant cluster, the default configuration for new databases is Q=8 and N=3. Therefore, a database that is created without explicitly specifying Q or N will have its data and indexes divided among 8 shards. Each of those shards will have 3 replicas for redundancy and quorum within the cluster. For more details about quorum, see this article. [need link]

Shards become distributed among the nodes of a cluster in round-robin fashion, with data distributed into them by using a hash of the content for each JSON document. For an example of how this works, consider a scenario that uses a database with Q=4 unique shards that we designate as A, B, C, and D. Documents are distributed into the shards by taking a hash of their contents, and using it as a key within the range of each shard.  

Shard A: 00000000-3FFFFFFF
<br>Shard B: 40000000-7FFFFFFF
<br>Shard C: 80000000-AFFFFFFF
<br>Shard D: B0000000-FFFFFFFF

For example, a document whose hash computes to 4A51341C would be contained within the B shard. This method is a better way to distribute documents in the cluster than using the unique ID of the documents, because the document ID can be custom-set by the application. With custom IDs, such a method might cause a shard imbalance or “hot node” situation. With the higher degree of randomization that happens with hashing the document’s content, this circumstance is rare.

With N=3, each of these shards has three replicas for quorum and redundancy, so the cluster has 12 files (shards) in total for the database: A1, B1, C1, D1, A2, B2, C2, D2, A3, B3, C3, and D3. In other words, two nodes of the cluster can go offline without data loss. In a cluster of 4 nodes, the cluster contains the shards.

<br>Node 1: A1, D2, C3
<br>Node 2: B1, A2, D3
<br>Node 3: C1, B2, A3
<br>Node 4: D1, C2, B3


### Sharding Parameters

To set appropriate shard values, you need to understand the parameters, and when it is appropriate to adjust the parameters values. The 4 sharding parameters, N, Q, R, and W, are described below. 

####`N` - Number of copies or replicas 
You can store N copies of data and configure them by database. The value rarely changes. Default N value is N=3.  

The node computes the following items.

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


####`Q` - Sharding
You configure sharding by database, dedicated and local tenants only. When you create the database, you specify the configuration for the shards. To change the Q value, you must replicate to a new database. It is a good idea to create more shards than the number of cluster nodes in your environment. 

The formula to calculate the total number of shards is Q * N = total shards. Default Q value is Q=4 for multi-tenant and Q=8 for dedicated/local tenant. Q is degree of parallelism.  

When you configure the Q value, keep the following recommendations in mind. 

| Rule | Description |
|-----|--------------|
|General | Few large databases use large. <br>Many small databases use small.|
| Maximum shards > degree of parallelism | Approximately equal to the number of spindles in the cluster or number of cores in the cluster.|
|Shard file size | 10GB or less <br>50GB maximum size. A file size larger then 50GB affects compaction.|
|Read versus write rate | Large numbers of writes/views builds require more shards. <br>Small numbers of writes require fewer shards. <br>More shards require more work for requests, particularly views.|

#####`Q` example

Database | Docs | Avg Doc Size | Read/sec | Write/sec | # Views | Doc to view/read ratio | Q value 
---------|------|--------------|----------|-----------|---------|------------------------|---------
Activities | 240m | 1k | 150 | 25 | 5 | 0.5 | 16-24
Users | 24m | 2k | 150 | 25 | 4 | 0.1 | 8-12 
Social feed | 50m | .2k | 40 | 8 | 4 | 0.1 | 4-8

####Indexing – Views, Search, Geo
Cloudant builds indexes locally for each shard. Shards run in parallel and use all available CPUs to distribute the load. During a query, the mergesort runs. 

####`R` - Read quorum 
R value measures the reads served by the database as query results. For example, the results occur when the database provides the answer or when enough nodes provide the answer. 'Enough' means the shard attempted to read from N nodes, and R nodes replied and agreed. 

Default R value is R=2 (majority). To minimize latency, set R=1, or to maximize consistency, set R=N. 

####`W` - Write quorum 
The W value measures the times a database writes data and when enough nodes write data. 'Enough' means the shard tried to store all replicas (N copies) when W nodes replied after fsyncing to disk. 

Default W value is W=2 (majority). To maximize throughput, set W=1, or to maximize consistency, set W=N. 

### Cloudant Sharding best practices

Sharing is described in the previous sections. However, each shard has its own requirements and strategies. Here are a few best practices you might want to keep in mind.

For many databases, you do not need to adjust the default shard value. However, when you expect that your Cloudant database is going to be large, or if your application uses a per-user or per-device model with a large number of small databases, it is essential to evaluate the expected growth of your database and choose the right shard count from the beginning. Alternatively, if a database has grown much larger in size in production than was initially predicted, you might want to take the following steps.

1.	Create a new database with a more appropriate shard count.
2.	Migrate your data to that database.
3.	Decommission the previous database. 

Unfortunately, there is no exact formula to determine what the optimal unique shard count is for a database in Cloudant. Due to the multiple variables in a production database, the 'best' shard count is most often determined through experimentation. However, consider these recommendations when you select the unique shard count for larger databases.

1.	Use a value of Q that will result in shards that are less than 20GB in size. 
2.	For larger databases, it is important to factor the number of nodes in the cluster into this equation. If you make the unique shard count divisible by the node count, it ensures that each node in the cluster has the same number of shards as the database, and ensures a better balance of data.

As an illustration, let’s consider a cluster of 6 nodes, where you expect your database to grow to 500GB in size. When creating the database, the value for Q must be set to 30. This satisfies the following conditions.

1.	At 500GB, each shard is ~17GB, which satisfies the recommendation of keeping shards below 50GB.

2.	With Q=30 and N=3, the total shard count is 90. Since the total count is divisible by the node count of 6, this means that each node in the cluster has the same number of shards for this database, and disk space remains balanced.

In addition, different application servers, such as IoTs or mobile devices, access large databases in Cloudant multiple times per second. If you have more unique shards, this allows for the database to accept more simultaneous connections from client devices or application servers.

Alternatively, let’s consider a scenario on the opposite end of the spectrum, where an application is using many (thousands, or even millions) small databases. In this scenario, it might be preferable to reduce the value of Q below the default setting. Databases smaller than 1MB derive very little benefit from being split into 24 pieces, because they often have only one user who makes relatively infrequent requests. For tiny databases like this, consider using a very low shard, such as Q=2. Small databases are less likely to cause node imbalances, so the priority for evenly dividing them among database nodes is insignificant. When there are thousands of databases or more in a cluster, reducing unnecessary amounts of parallelism by decreasing shard counts can improve memory utilization on the cluster, allowing a greater number of users to be housed on a smaller hardware footprint.




