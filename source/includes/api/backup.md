## Backup

<aside class="warning">The information in this topic is very much preliminary content, and at this time should not be considered complete, accurate, or reliable.</aside>

The content of your databases is likely to change over time.
As with all valuable information, it is important to protect the data against possible loss or corruption.
One way to do this is by creating data backups.
Within IBM Cloudant, a data backup is simply a checkpoint of the database content. It is possible to 'roll back' to a specific checkpoint.
The checkpoint is not specific to a precise time; instead it is a record of the database following replication of changes that occurred during the backup period.

The overall process for creating an IBM Cloudant database backup is as follows:

1.	Request the creation of a backup task.
2.	Run scheduled backups, to create 'deltas' of the database content changes.
3.	At regular intervals:
  -	Run 'roll-up' tasks to combine deltas.
  -	Run 'clean-up' tasks to remove the 'rolled-up' backups.

### Concepts

#### Backup Run

During a 24 hour period, the source database is repeatedly replicated to a target database.
The replication uses sequence values to identify the documents changed during that 24 hour period.
This becomes a daily backup.

#### Backup Rollup

Daily backups are combined into weekly rolled up databases.
These combine the daily deltas into a coarser time slice.
Weekly databases are rolled up into monthly databases.
Monthly databases are rolled up into yearly databases.

All of these operations are called rollups. Rollup frequencies and settings are managed via the Backup Task.

#### Backup Cleanup

To conserve space when databases have been rolled up, the input databases to the rollups are removed after a configurable time period.

This enables optimization of data retention, at a high level of granularity against the cost of storage.

### Backup 'granularity'

A backup can take place at regular intervals.
Each interval is no shorter than one day.
This means you can take daily backups, but not hourly backups, for example.

### Requesting a backup task

To enable backups for your IBM Cloudant database, you must first request the creation of a backup task.
Do this by contacting IBM Cloudant Support, and requesting a backup task for your chosen database.

It is not possible for you to create the backup task yourself.

<aside class="notice">The reason you cannot create the backup task is that additional processes and storage capacity must be enabled to support the backup activities.</aside>

#### Information required for a backup task

When contacting the IBM Cloudant Operations or Support Engineers to request a backup task, you should supply the following information:

-	Your preferred backup task name, for example `towed_vehicles_backup`.
-	The database to be backed-up, for example `towed_vehicles`.
-	Frequency of running the backup task.<aside class="warning">A minimum of 24 hours is required between each run. It is not possible to request a specific time for a run to start.</aside>

Behind the scenes, a backup task is created that uses replication to take a checkpoint of the database, and store it for later use.
The checkpoint is another database, with an internal name derived from a combination of the date and the backup task name. This makes it easier to identify checkpoints for recovery or rollup purposes.

### Working with backups

#### Backup rollup

You can request that a rollup should take place for the following intervals:

-	`daily`, to combine daily checkpoints into a weekly checkpoint.
-	`weekly`, to combine weekly checkpoints into a monthly checkpoint.
-	`monthly`, to combine monthly checkpoints into a yearly checkpoint.

These are one-off requests, and do not repeat automatically. If you request a daily rollup to create a weekly checkpoint, then want another weekly checkpoint the following week, you must request the daily rollup again.

<aside class="warning">A rollup does not remove the original checkpoints. If you have requested a daily rollup, the daily checkpoints still exist.
To remove the rolled-up checkpoints, and therefore save storage costs, request a [backup cleanup](#backup-cleanup).</aside>

#### Backup status

You can request information about the status of the most recent backup replication.

#### Backup history

You can request history information about all the backup replications that have run for a specific backup task.

#### Backup cleanup

You can request the removal of backup checkpoints that have already been rolled up and combined into a higher level checkpoint.

#### Backup restore

You can request the restoration of data from a backup checkpoint.
You can specify either a specific document, or the entire database.

