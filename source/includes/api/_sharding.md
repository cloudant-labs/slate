## Sharding

In Cloudant and CouchDB 2.0, database sharding is the concept of dividing a database into separate parts to enable high-availability of data, and the division of work among the nodes inside a cluster.   

The number of total shards that a database is split into is set at the time of its creation. Shards cannot be increased or decreased in number after database creation. The number of shards in a Cloudant database is often described as its `Q` value. The number of replicas of those shards in the database is described as its `N` value. Each replica of a shard is a file, therefore, the total number of *files* the database has inside the cluster is equivalent to Q * N. 

In a dedicated Cloudant cluster, the default configuration for new databases might be Q=8 and N=3. Therefore, a database that is created without explicitly specifying `Q` or `N` will have its data and indexes divided among 8 shards. Each of those shards will have 3 replicas for redundancy within the cluster. 

Shards are distributed among the nodes of a cluster in round-robin fashion, with data distributed into them by using a hash of the document ID for each JSON document. For example, consider a scenario that uses a database with Q=4 shards that we designate as A, B, C, and D. Documents are distributed into the shards by taking a hash of their ID, and using it as a key within the range of each shard.

Shard A: 00000000-3FFFFFFF
<br>Shard B: 40000000-7FFFFFFF
<br>Shard C: 80000000-AFFFFFFF
<br>Shard D: B0000000-FFFFFFFF

For example, a document whose hash computes to 4A51341C would be contained within the B shard. Using the hash of the document’s ID makes even distribution of documents to shards more likely, which avoids certain nodes having busy shards.

With N=3, each of these shards has three replicas for redundancy, so the cluster has 4 shards, 12 files in total for the database: A1, B1, C1, D1, A2, B2, C2, D2, A3, B3, C3, and D3. In other words, three nodes of the cluster can go offline without data becoming inaccessible. In a cluster of 4 nodes, the cluster might distribute the shard replicas as shown in the following example.

<br>Node 1: A1, D2, C3
<br>Node 2: B1, A2, D3
<br>Node 3: C1, B2, A3
<br>Node 4: D1, C2, B3


### Sharding Parameters

To set appropriate shard values, you must understand the parameters. You must set N and Q at database create time. Some read/write requests also allow R and W to be set. The 4 parameters that interact with sharding are N, Q, R, and W. These parameters are described in this section.

####`Q` - Sharding
The number of shards for a database is set when creating the database. Only Dedicated and Local users can set the number of shards. When you create the database, you specify the configuration for the shards. You cannot change the Q value for a given database. Instead, you must replicate the data for the database into a new database with a different Q value. It is a good idea to create more shards than the number of cluster nodes in your environment. 
  

When you configure the `Q` value, remember the following recommendations. 

| Rule | Description |
|-----|--------------|
|General | Few large databases use large. <br>Many small databases use small.|
| Maximum shards > degree of parallelism | Approximately equal to the number of spindles in the cluster or number of cores in the cluster.|
|Shard file size | 10GB or less <br>50GB maximum size. A file size larger then 50GB affects compaction.|
|Read versus write rate | Large numbers of writes/views builds require more shards. <br>Small numbers of writes require fewer shards. <br>More shards require more work for reads, particularly views.|

#####`Q` example

Database | Docs | Avg Doc Size | Read/sec | Write/sec | # Views | Doc to view/read ratio | `Q` value 
---------|------|--------------|----------|-----------|---------|------------------------|---------
Activities | 240m | 1k | 150 | 25 | 5 | 0.5 | 16-24
Users | 24m | 2k | 150 | 25 | 4 | 0.1 | 8-12 
Social feed | 50m | .2k | 40 | 8 | 4 | 0.1 | 4-8

####`N` - Number of copies or replicas 
You can store `N` copies of data and configure them when you create a database. This value should almost never be changed from its default, 3.    

The node computes the following items.

```curl
key=f(doc._id)
get_shards(key) ==> shard
get_nodes(shard) ==> [N1,N3,N4]
Nodesforeach: store(doc)
```

`PUT /db10/docid92`

The database "computes."

####Indexing – Views, Search, Geo
Cloudant builds indexes locally for each shard. Shard indexing runs in parallel – shards are inert objects.

####`R` - Read quorum 
The `R` value measures the reads served by the database as query results. For example, the results occur when the database provides the answer or when enough nodes provide the answer. *Enough* means the shard attempted to read from `N` nodes, and `R` nodes replied and agreed. 

Default `R` value is R=2 (majority). To minimize latency, set R=1, or to maximize consistency, set R=N. 

####`W` - Write quorum 
The `W` value measures the times a database writes data and when enough nodes write data. *Enough* means the shard tried to store all replicas (`N` copies) when `W` nodes replied after fsyncing to disk. 

Default `W` value is W=2 (majority). To maximize throughput, set W=1, or to maximize consistency, set W=N. 

### Cloudant Sharding best practices

Each database has its own requirements. Here are a few best practices to remember.

For most databases, you do not need to adjust the default `Q` and `R` value. However, when you expect that your Cloudant database is going to be large, or if your application uses a per-user or per-device model with a large number of small databases, it is essential to evaluate the expected growth of your database and choose the right shard count from the beginning. Alternatively, if a database has grown much larger in size while in production than was initially predicted, you might want to take the following step.

1.	Create a new database with a more appropriate shard count.
2.	Migrate your data to that database using replication [LINK].
3.	Delete the previous database. 

Unfortunately, there is no exact formula to determine what the optimal shard count is for a database in Cloudant. Due to the multiple variables in a production database, the *best* “shard count should be determined through experimentation. However, consider these recommendations when you select the shard count for larger databases.

1.	Use a value of `Q` that will result in shards that are less than 20GB in size. 
2.	For larger databases, it is important to factor the number of nodes in the cluster into this equation. If you make the shard count divisible by the node count, it ensures that each node in the cluster has the same number of shards of the database, and make it more likely that the data is balanced.

As an illustration, let’s consider a cluster of 6 nodes, where you expect your database to grow to 500GB in size. When creating the database, thirty shards could be a reasonable number. This method satisfies the following conditions.

1.	At 500GB, each shard is ~17GB, which satisfies the recommendation of keeping shards below 50GB.
2.	With Q=30 and N=3, the N*Q count is 90. Since the total count is divisible by the node count of 6, this means that each node in the cluster has the same number of shards for this database, and disk space will probably remains balanced.

In addition, different application servers, such as IoTs or mobile devices, access large databases in Cloudant multiple times per second. If you have more unique shards, this allows for the database to accept more simultaneous connections from client devices or application servers.

Alternatively, let’s consider a scenario on the opposite end of the spectrum, where an application is using multiple small databases, thousands, or even millions. In this scenario, it might be preferable to reduce the value of `Q` below the default setting. Databases smaller than 1MB derive very little benefit from being split into multiple shards, because they often have only one user who makes relatively infrequent requests. For tiny databases like this, consider using a very low number of shards. Small databases are less likely to cause node imbalances, so the priority for evenly dividing them among database nodes is insignificant. If you use smaller shard counts for smaller databases, it helps performance. 



