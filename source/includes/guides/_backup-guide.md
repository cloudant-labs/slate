## Back up your data

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the 'Back up your data' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/guides/backup-guide.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

<aside class="warning" role="complementary" aria-label="betaonly0">This guide refers to a <b>Beta</b> daily incremental backup capability,
available only on request to Enterprise customers.
This capability:
<ul>
<li>Is not enabled by default.</li>
<li>Is only available to Enterprise customers, who must specifically request it.</li>
<li>Must be explicitly configured before it is operational.</li>
<li>Is subject to [known limitations](backup-guide.html#known-limitations).</li>
<li>Is not applicable to [Cloudant Local](https://www.ibm.com/support/knowledgecenter/SSTPQH_1.0.0/com.ibm.cloudant.local.doc/SSTPQH_1.0.0_welcome.html).</li>
</ul>
For more information,
please contact the <a href="mailto:support@cloudant.com">IBM Cloudant support team</a>.</aside>

<aside class="warning" role="complementary" aria-label="notCloudantLocal">The daily incremental backup capability is not applicable for [Cloudant Local](https://www.ibm.com/support/knowledgecenter/SSTPQH_1.0.0/com.ibm.cloudant.local.doc/SSTPQH_1.0.0_welcome.html).
To back up data in Cloudant Local,
use [replication](https://docs.cloudant.com/replication.html) to make a copy of your database.</aside>

IBM Cloudant creates three copies of each document
and stores it on three different servers in a cluster to ensure high availability.
This practice is the default for all Cloudant users.
Even when your data is replicated in triplicate,
it is still  important to back it up.

Why is backing up important?
In general,
you could lose access to data in many ways.
For example,
if a hurricane destroys your data center and all three nodes are in that location,
you lose your data.
You can prevent the loss of your data in a disaster by replicating your data to a
cluster (dedicated or multi-tenant) in a different geographic location.
However,
if a faulty application deletes or overwrites the data in your database,
duplicate data is not helpful.

Having a comprehensive,
tested backup enables you to answer the following question with confidence:
"How can we restore data in case of loss or corruption?"

With Cloudant,
Enterprise customers can have daily incremental backups.

If you are not an Enterprise customer,
or you wish to create your own backup mechanism,
consider [using Replication to perform backups](backup-guide-using-replication.html).

<aside class="warning" role="complementary" aria-label="betaonly">Daily incremental backup for Enterprise customers is currently a <b>Beta</b> capability.
It is <b>not</b> enabled by default.</aside>

Daily incremental backups or 'deltas' enable document comparison,
and easier single document restoration.
At regular intervals,
which can be configured,
the smaller daily deltas are rolled up into weekly deltas.
Similarly,
weekly deltas are rolled up into monthly deltas,
and monthly deltas into yearly ones.
This process of rolling up deltas is a pragmatic compromise between
being able to restore exactly the correct version of a document,
and requiring a lot of storage space.

The backup facility allows you to restore individual documents manually.
Should you wish to restore and entire database,
for example as part of a disaster recovery scenario,
you can contact the support team and have your data restored to a specific day,
week,
month or year,
subject to the deltas you have available.

More information about how Cloudant backs up data is provided in the rest of this topic.
For further assistance,
or to request that data backup is enabled,
contact the Cloudant support team:
[support@cloudant.com](mailto:support@cloudant.com).

<aside class="warning" role="complementary" aria-label="enterpriseonly2">The Cloudant backup facility is available only to Enterprise customers.</aside>

<aside class="warning" role="complementary" aria-label="designdocsnotbackedup">By default,
`_design` documents are not backed up,
so that indexes are _not_ built on the incremental backup databases.
If you require backups of the `_design` documents,
you must maintain them in your preferred source control tool.</aside>

### Concepts

*	Backup run: For a backup period, the source database is replicated using sequence values to determine the documents that changed during the backup period. On completion, this replication is called the daily backup.
*	Daily backup: See Backup run.
*	Backup rollup: Daily backups are combined into weekly rolled up databases. These combine the daily deltas into a coarser (less granular) backup. Similarly, weekly databases are rolled up into monthly databases, and monthly databases into yearly databases.
*	Backup cleanup: After a delta database has been rolled up, the delta database is removed after a configurable time period. This allows you to balance data retention at a high granularity against the cost of storage.
*	High/low granularity: This indicates how precisely you can specify the period of change for a document. A high granularity rollup has a short timescale for the period of change, for example a day in the case of a daily backup. A low granularity rollup has a long timescale for the period of change, for example a year in the case of a yearly backup.

### Incremental backups

The first step in enabling incremental backups is to take a full backup of your entire database.
This provides a 'baseline' for the subsequent incremental backups.

Every day,
after the first 'baseline' backup,
a daily,
incremental backup is taken.
This daily incremental backup contains only the data that has changed in the database since the last backup. The daily backup is the 'daily delta'.

As part of the request to enable data backups,
you can specific a time of day for the backup to run.
The daily delta is created each day,
at the time you specified.

### Roll ups

A roll up combines daily backups into weekly,
rolled up databases.
These roll up databases combine the daily deltas into a coarser,
or 'less granular',
time slice.
Weekly databases roll up into monthly databases,
and monthly databases roll up into yearly databases.

![Illustration of roll up hierarchy](images/rollups.png)

When requesting that backups are enabled,
you should specify how many daily deltas to keep.
Once that number is reached,
the oldest daily delta is rolled up into the most recent weekly database.
Thereafter,
the weekly databases are rolled up to create the monthly databases,
and so on.

Once the delta databases have been rolled up,
they are removed to free up storage space.

### Restores

When you have backups for a database,
you can view individual documents within that database,
and also see changes made to that document.
You can also restore the document to the version that was current on a particular date,
if it is available within the granularity of the delta.

<aside class="warning" role="complementary" aria-label="mustbestatic">Documents must be static before restoring from backup.
In other words,
the document should not be constantly receiving changes and updates.</aside>

For more complex restores,
such as a full database restore,
request assistance from Cloudant support.

### Using the Dashboard

Enterprise customers can review the status and history of backups using the Cloudant Dashboard.

Tasks you can perform include:

-	View the status of the last backup, including its date and time.
-	View a list of backup document versions by date and time.
-	View a current document and the difference between it and any backed up version.
-	Restore a document from a backed up version.

#### Viewing database backup status

![Dashboard view of database backup status](images/dashboarddatabasesbackup.png)

When you select the Database tab within the Cloudant Dashboard,
you can see a backup status column for each of your databases.

#### Viewing document backup status

![Dashboard view of backup status for all documents](images/dashboarddatabasesbackupbutton.png)

Within a database,
you can view the backup status of a specific document.
To do this,
first check to see if there is a backup icon
![Dashboard backup icon](images/dashboarddatabasesbackupicon.png)
for your document.
This shows whether the specific document is included within the backup task.

When you select the document,
you can see a backup tab.

![Dashboard view of document backup status](images/dashboarddatabasesbackupdocument.png)

#### Viewing differences between document backup versions, and restoring

![Dashboard view of document backup status](images/dashboarddatabasesbackupdocumentdiff.png)

When you click the backup tab for a document,
you can see the differences between the current version of the document,
and any other backed-up version.

If you decide that you would like to restore a specific backup version of that document,
simply select the date of the backup to restore,
then click the 'Restore' button.

<aside class="warning" role="complementary" aria-label="mustbestable1">Documents must be in a stable state before restoring from backup.
In other words,
the document should not be constantly receiving changes and updates.</aside>

### Using the API

A number of REST API calls are available for working with the Cloudant backup facility.

#### Task configuration

> Retrieving the backup task configuration for the user, returning results in a list format (default).

```http
GET /_api/v2/backup/task HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_api/v2/backup/task \
     -X GET
```

> Retrieving the backup task configuration for the user, returning results in a mapping format.

```http
GET /_api/v2/backup/task?format=mapping HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_api/v2/backup/task?format=mapping \
     -X GET
```

The `task` call gets the backup task configuration for the user.

You can specify the format used in the response by using the `format` parameter.

<div></div>

> Example response following a list format request:

```
{
  "rows": [
    {
      "username": "$ACCOUNT",
      "task": "backup-0d0b0cf1b0ea42179f9c082ddc5e07cb",
      "source_db": "backmeup",
      "latest_completion": null
    },
    {
      "username": "$ACCOUNT",
      "task": "backup-d0ea6e8218074699a562af543db66615",
      "source_db": "backuptest",
      "latest_completion": "2016-01-17T05:57:44+00:00"
    },
    {
      "username": "$ACCOUNT",
      "task": "backup-24cd8359b94640be85b7d4071921e781",
      "source_db": "taskdb",
      "latest_completion": "2016-01-17T00:01:04+00:00"
    }
  ]
}
```

The default response format is a list.
You can request this format directly by using the `...backup/task?format=list` parameter.
The response contains a simple list of the backup tasks defined for the user.

For example, you might request a list format response using either of the following commands:
	`https://<account>.cloudant.com/_api/v2/backup/task`
	`https://<account>.cloudant.com/_api/v2/backup/task?format=list`

<div></div>

> Example response following a mapping format request:

```
{
  "backmeup": {
    "username": "$ACCOUNT",
    "task": "backup-0d0b0cf1b0ea42179f9c082ddc5e07cb",
    "source_db": "backmeup",
    "latest_completion": null
  },
  "backuptest": {
    "username": "$ACCOUNT",
    "task": "backup-d0ea6e8218074699a562af543db66615",
    "source_db": "backuptest",
    "latest_completion": "2016-01-17T05:57:44+00:00"
  },
  "taskdb": {
    "username": "$ACCOUNT",
    "task": "backup-24cd8359b94640be85b7d4071921e781",
    "source_db": "taskdb",
    "latest_completion": "2016-01-17T00:01:04+00:00"
  }
}
```

A more comprehensive response is available in the mapping format.
You can request this format directly by using the `...backup/task?format=mapping` parameter.

For example, you might request a mapping format response using the following command:
`https://<account>.cloudant.com/_api/v2/backup/task?format=mapping`

<div></div>

#### Determining backup tasks for specific databases

> Example command to find backup tasks for the `backuptest` and `taskdb` database:

```http
GET /_api/v2/backup/task?databases=backuptest,taskdb HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_api/v2/backup/task?databases=backuptest,taskdb \
     -X GET
```

> Example response to finding backup tasks for specific databases:

```
{
  "rows": [
    {
      "username": "$ACCOUNT",
      "task": "backup-d0ea6e8218074699a562af543db66615",
      "source_db": "backuptest",
      "latest_completion": "2016-01-17T05:57:44+00:00"
    },
    {
      "username": "$ACCOUNT",
      "task": "backup-24cd8359b94640be85b7d4071921e781",
      "source_db": "taskdb",
      "latest_completion": "2016-01-17T00:01:04+00:00"
    }
  ]
}
```

The `databases` parameter for the `task` request is used to find what backup tasks are associated with a specified database.

The response lists the backup task details for the database identified in the `source_db` field.
The `task` identified can be used in other backup API calls,
such as [database listing](backup-guide.html#list-of-databases).

<div></div>

#### List of databases

> Retrieving the list of databases created by a backup task, that contain a specific document.

```http
GET /_api/v2/backup/monitor/$TASKNAME/$DOCID?include_docs=true HTTP/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/_api/v2/backup/monitor/$TASKNAME/$DOCID?include_docs=true \
     -X GET
```

The `monitor` call gets a list of the databases created by the backup task `$TASKNAME`,
that also contain the document `$DOCID`.

The call supports an optional argument: `include_docs`.
The default value is `false`.
If set to `true`,
the `monitor` call returns the full document content for each backup database containing `$DOCID`.

<div></div>

#### Restore a document

> Restore a document from the most recent version held in a specific backup database.

```http
POST /_api/v2/backup/restore/document --data=@RESTORE.json HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/_api/v2/backup/restore/document --data=@RESTORE.json \
     -X POS \
     -H "Content-Type: application/json" \
     -d "$JSON"
```

```json
{
  "doc_id": $DOCID,
  "task_name": $TASKNAME,
  "task_date": $TASKDATE,
  "frequency": $FREQUENCY
}
```

The `restore` call replaces a document,
identified by `$DOCID`,
from a source database.
The source database is identified by the `$TASKNAME`.
The `$TASKDATE` is the timestamp of the specific backup,
and specifies when the backup was performed.
The `$FREQUENCY` is one of the following four values:
`"daily"`,
`"weekly"`,
`"monthly"`,
or `"yearly"`.

<aside class="warning" role="complementary" aria-label="mustbestable2">Documents must be in a stable state before restoring from backup.
In other words,
the document should not be constantly receiving changes and updates.</aside>

<div></div>

### How backup using incremental replication works

A very simple form of backup is to [replicate](replication.html) the database to a dated backup database.

This method works and is easy to do.
But if the database is big and you need backups for multiple points in time,
for example seven daily backups and four weekly ones,
you end up storing a complete copy of all the documents in each new backup database.
This is likely to require a lot of storage space.

Incremental backups are a good solution for storing only the documents that have changed since the last backup.

Initially,
you perform a backup of the entire database.
After the first backup,
you run regular,
incremental backups,
backing up only what has changed in the database since the last backup.
Typically these incremental backups take place once a day,
so this replication is a daily backup.

Incremental backups save only the delta between backups.
At regular intervals,
the source database is replicated to a target database.
Replication uses sequence values to identify the documents changed during the interval period.

The backup operation uses replication to get and store a checkpoint.
This checkpoint is another database with an internal name.

The replication process for a database starts by finding the value of the `since_seq` parameter.
The parameter indicates where the last replication finished.

The following steps outline how incremental backups are created:

1.	[Find the ID of the checkpoint document for the last replication.](backup-guide.html#find-the-id-of-the-checkpoint-document-for-the-last-replication)
2.	[Get the `recorded_seq` value.](backup-guide.html#get-the-recorded_seq-value)
3.	[Run an incremental backup.](backup-guide.html#run-an-incremental-backup)

#### Find the ID of the checkpoint document for the last replication

> Get checkpoint ID of the last incremental backup for a database called `original`:

```http
GET /_replicator/original HTTP/1.1
```

```shell
$ replication_id=$(curl "${url}/_replicator/original" | jq -r '._replication_id')
```

The checkpoint ID value is stored in the `_replication_id` field in the replication document in the `_replicator` database.

<div></div>

#### Get the `recorded_seq` value

> Get `recorded_seq` from database called `original`

```http
GET /original/_local/${replication_id} HTTP/1.1
```

```shell
$ recorded_seq=$(curl "${url}/original/_local/${replication_id}" | jq -r '.history[0].recorded_seq')
```

After you get the checkpoint ID,
you use it to get the `recorded_seq` value from the first element of the history array in the `/_local/${replication_id}` document in the original database.

<div> </div>

#### Run an incremental backup

> Start new incremental backup to an incremental database called `newbackup`:

```http
PUT /_replicator/newbackup HTTP/1.1
Content-Type: application/json
```

```shell
$ curl -X PUT "${url}/_replicator/newbackup" -H "${ct}" -d @newbackup.json
# where newbackup.json contains the following:
```

```json
{
  "_id": "newbackup",
  "source": "${url}/original",
  "target": "${url}/newbackup",
  "since_seq": "${recorded_seq}"
}
```

Now that you have the checkpoint ID and `recorded_seq`, you can start the new incremental backup.

### Known limitations

<aside class="warning" role="complementary" aria-label="betaonly2">Daily incremental backup for Enterprise customers is currently a Beta capability.
It is not enabled by default.</aside>

<ul>
<li>IBM Cloudant Backup,
and the associated restore capabilities,
are based on the underlying replication technology.
Factors affecting,
or even interrupting,
the replication will affect or even stall backup or restore processes.</li>
<li>Backup and restore processes could take a significant amount of time for large databases,
for example over 100GB in size.
This applies to the initial backup,
which could take a few days to complete for a large database.
<br/>Similarly,
the restore process could take from a few hours to several days,
again depending on the size of the database.</li>
<li>For large daily backups,
it is possible that the backup process cannot complete in one day (24 hours).
The backup process normally runs to completion,
therefore it would include incremental changes for more than a day.</li>
<li>There is currently no support for backing up a full user account.
Instead,
you must specify each of the databases within a user account that you want enabled for backup or restore.
<br/>Currently,
there is a limit of 50 databases enabled for backup within any one user account.</li>
<li>The IBM Cloudant Backup facility does not currently support backup or restore for
<a href="design_documents.html">"design documents"</a>.
<br/>If you require backups of design documents,
you must maintain them in your preferred source control tool.</li>
<li>Currently,
the target database for performing a database restore must be different from the original source database.</li>
</ul>
