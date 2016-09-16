## Back up your data using replication

Database backups protect your data against potential loss or corruption.
You can use Cloudant’s replication facility to create a database backup,
and store it on a Cloudant cluster.
You can then restore data,
entire databases,
or specific JSON documents,
from these backups to your production cluster.

Using Cloudant replication,
a database backup stores your database content to a checkpoint.
It is possible to ‘roll back' to a specific checkpoint.
The checkpoint is not specific to a precise time.
Instead,
it is a record of the database as it was after specific changes occurred during the backup period.
In this way,
a backup can preserve the state of your database at a selected time.

### Incremental backups

If you are an Enterprise customer,
a daily incremental backup capability is [available](backup-guide.html).

If you are not an Enterprise customer,
or you prefer to create your own backups,
you can use Cloudant’s replication facility to create a database backup.

A simple approach is to replicate the entire database to a dated backup database.
This method works and is easy to do.
But if you need backups for multiple points in time,
such as seven daily backups and four weekly ones,
you have to store a complete copy of the database in each new backup database.
This quickly requires significant disk usage,
especially if your database is large.

As an alternative,
incremental backups are a good solution for storing only the documents that have changed since the last backup.

The process is simple.
Initially,
you perform a backup of the entire database.
After the first backup,
you run daily 'incremental' backups,
backing up _only_ what has changed in the database since the last backup.
This replication becomes a daily backup.

<aside class="warning" role="complementary" aria-label="triggerintervals">You can configure a backup to trigger at regular intervals.
However,
each interval must be 24 hours or more.
In other words,
you can run daily backups but not hourly backups.</aside>

### Creating an incremental backup

Incremental backups save only the differences or 'deltas' between backups.
Every 24 hours,
the source database is replicated to a target database.

Replication uses sequence values to identify the documents changed during the 24-hour period.
The backup operation works by using replication to get and store a checkpoint.
A checkpoint is simply another document with an internal name.
The backup operation creates the name from a combination of the date and the backup task name.
This name makes it easier to identify checkpoints during the recovery or roll up process.

To create an incremental backup,
you must perform the following steps:

1.	Find the ID of the checkpoint document for the last replication. It is stored in the  `_replication_id` field of the replication document, found in the `_replicator` database.
2.	Open the checkpoint document at `/<database>/_local/<_replication_id>`, where `<_replication_id>` is the ID you found in the previous step, and `<database>` is the name of the source or the target database. The document usually exists on both databases but might only exist on one.
3.	Search for the `recorded_seq` field of the first element in the history array found in the checkpoint document.
4.	Start replicating to the new incremental backup database, setting the `since_seq` field in the replication document to the value of the `recorded_seq` field found in the previous step.

### Restoring a database

To restore a database from incremental backups,
you replicate each incremental backup to a new database,
starting with the most recent increment.

You could start with the oldest backup,
then apply the subsequent  backups in order.
However,
replicating from the latest incremental backup first is faster because updated documents are only written to the target database once.
Any documents older than a copy already present in the new database are skipped.


### An example

This example shows how to:

-	Setup databases to use incremental backup.
-	Run a full backup.
-	Set up and run an incremental backup.
-	Restore a backup.

> Constants used in this guide

```
# save base URL and the content type in shell variables
$ url='https://<account>.cloudant.com'
$ ct='Content-Type: application-json'
```

Assume you need to back up one database.
You want to create a full backup on Monday,
and an incremental backup on Tuesday.

You can use the `curl` and [`jq`](http://stedolan.github.io/jq/) commands to run these operations.
In practice,
you could use any http client.

<div></div>

#### Step 1: Check you have three databases

> Check you have three databases to use with this example

```shell
$ curl -X PUT "${url}/original"
$ curl -X PUT "${url}/backup-monday"
$ curl -X PUT "${url}/backup-tuesday"
```

```http
PUT /original HTTP/1.1
```

```http
PUT /backup-monday HTTP/1.1
```

```http
PUT /backup-tuesday HTTP/1.1
```

For this example,
you require three databases:

-	The original database, holding the data you want to backup.
-	Two incremental databases, for Monday (`backup-monday`) and Tuesday (`backup-tuesday`).

<div></div>

#### Step 2: Create the `_replicator` database

> Create the `_replicator` database

```shell
$ curl -X PUT "${url}/_replicator"
```

```http
PUT /_replicator HTTP/1.1
```

If it does not exist, create the `_replicator` database.

<div> </div>

#### Step 3: Back up the entire (original) database

> Run a full backup on Monday

```http
PUT /_replicator/full-backup-monday HTTP/1.1
Content-Type: application/json
# using the following json document:
```

```shell
$ curl -X PUT "${url}/_replicator/full-backup-monday" -H "$ct" -d @backup-monday.json
# where backup-monday.json has the following contents:
```

```json
{
  "_id": "full-backup-monday",
  "source": "${url}/original",
  "target": "${url}/backup-monday"
}
```

On Monday,
you want to back up all your data for the first time.
Do this by replicating everything from `original` to `backup-monday`.

<div> </div>

#### Step 4: Get checkpoint ID

> Get checkpoint ID to help find the `recorded_seq` value:

```http
GET /_replicator/backup-monday HTTP/1.1
# Search for the value of _replication_id
```

```shell
$ replication_id=$(curl "${url}/_replicator/backup-monday" | jq -r '._replication_id')
```

On Tuesday,
you want to do an incremental backup,
rather than another full backup.

To start the incremental backup,
you need two values:

-	The checkpoint ID.
-	The `recorded_seq` value.

These values identify where the last backup ended,
and determine where to start the next incremental backup.
After you get these values, you can run the incremental backup.

You start by finding the checkpoint ID value.
This is stored in the `_replication_id` field of the replication document,
within the `_replicator` database.

<div> </div>

#### Step 5: Get `recorded_seq` value

> Get `recorded_seq` from original database

```http
GET /original/_local/${replication_id} HTTP/1.1
# Search for the first value of recorded_seq in the history array
```

```shell
$ recorded_seq=$(curl "${url}/original/_local/${replication_id}" | jq -r '.history[0].recorded_seq')
```

After you get the checkpoint ID,
use it to get the `recorded_seq` value.
This is found in the first element of the history array in the `/_local/${replication_id}` document,
within the original database.

You now have the `recorded_seq` value.
This tells you the last document replicated from the original database.

<div> </div>

#### Step 6: Run an incremental backup

> Start Tuesday's incremental backup

```http
PUT /_replicator/incr-backup-tuesday HTTP/1.1
Content-Type: application/json
# using the following json document:
```

```shell
$ curl -X PUT "${url}/_replicator/incr-backup-tuesday" -H "${ct}" -d @backup-tuesday.json
# where backup-tuesday.json contains the following:
```

```json
{
  "_id": "incr-backup-tuesday",
  "source": "${url}/original",
  "target": "${url}/backup-tuesday",
  "since_seq": "${recorded_seq}"
}
```

Now that you have the checkpoint ID and `recorded_seq`,
you can start Tuesday's incremental backup.
This replicates all the document changes made _since_ the last replication.

When the replication finishes,
you have a completed incremental backup.
The backup consists of all the documents in the original database,
and may be restored by retrieving the content of both the `backup-monday` _and_ `backup-tuesday` databases.

<div> </div>

#### Step 7: Restore the Monday backup

> Restore from the `backup-monday` database

```http
PUT /_replicator/restore-monday HTTP/1.1
Content-Type: application/json
# using the following json document:
```

```shell
$ curl -X PUT "${url}/_replicator/restore-monday" -H "$ct" -d @restore-monday.json
# where restore-monday.json contains the following:
```

```json
{
  "_id": "restore-monday",
  "source": "${url}/backup-monday",
  "target": "${url}/restore",
  "create-target": true  
}
```

To restore from a backup,
you replicate the initial full backup,
and any incremental backups,
to a new database.

For example,
to restore Monday's state,
you would replicate from the `backup-monday` database.

<div> </div>

#### Step 8: Restore the Tuesday backup

> Restore Tuesday's backup to get the latest changes first

```http
PUT /_replicator/restore-tuesday HTTP/1.1
Content-Type: application/json
# using the following json document:
```

```shell
$ curl -X PUT "${url}/_replicator/restore-tuesday" -H "$ct" -d @restore-tuesday.json
# where restore-tuesday.json contains the following json document:
```

```json
{
  "_id": "restore-tuesday",
  "source": "${url}/backup-tuesday",
  "target": "${url}/restore",
  "create-target": true  
}
```

> Finish by restoring Monday's backup last

```http
PUT /_replicator/restore-monday HTTP/1.1
Content-Type: application/json
# using the following json document:
```

```shell
$ curl -X PUT "${url}/_replicator/restore-monday" -H "$ct" -d @restore-monday.json
# where restore-monday.json contains the following json document:
```

```json
{
  "_id": "restore-monday",
  "source": "${url}/backup-monday",
  "target": "${url}/restore"
}
```

To restore Tuesday's database,
you first replicate from `backup-tuesday` and then from `backup-monday`.

You could restore in chronological sequence,
but by using the reverse order,
documents updated on Tuesday only need to be written to the target database once;
older versions of the document stored in the Monday database are ignored.

<div> </div>

### Best practices

While the previous information outlines the basic backup process,
each application needs its own requirements and strategies for backups.
Here are a few best practices you might want to keep in mind.

#### Scheduling backups

Replication jobs can significantly increase the load on a cluster.
If you are backing up several databases,
it is best to stagger the replication jobs for different times,
or to a time when the cluster is less busy.

##### Changing the IO priority of a backup

> Setting the IO priority

```json
{
  "source": {
    "url": "https://<account>@example.com/db",
    "headers": {
      "x-cloudant-io-priority": "low"
    }
  },
  "target": {
    "url": "https://user:pass@example.net/db",
    "headers": {
      "x-cloudant-io-priority": "low"
    }
  }
}
```

You can change the priority of backup jobs by adjusting the value of the `x-cloudant-io-priority` field within the replication document.

1.	In the source and target fields, change the `headers` object.
2.	In the headers object, change the `x-cloudant-io-priority` field value to `"low"`.

<div id="design-documents"> </div>

#### Backing up design documents

If you backup design documents, the backup operation creates indexes on the backup destination. This practice slows down the backup process and uses unnecessary amounts of disk space. If you don't require indexes on your backup system, use a filter function with your replications to filter out design documents. You can also use this filter function to filter out other documents that are not required.

#### Backing up multiple databases

If your application uses one database per user, or allows each user to create several databases, you need to create a backup job for each new database. Make sure that your replication jobs do not begin at the same time.

### Need help?

Replication and backups can be tricky. If you get stuck,
check out the [replication guide](./replication_guide.html),
talk to us on IRC (#cloudant on freenode), or email <a href="mailto:support@cloudant.com">support</a>.
