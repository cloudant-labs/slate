---

copyright:
  years: 2017
lastupdated: "2017-05-04"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# Cloudant Backup and Recovery

This cookbook forms part of the [Cloudant Disaster Recovery guide](disaster-recovery-and-backup.html). It's worth starting there if you are new to the subject to understand where backup fits in with Cloudant's other features for Disaster Recovery and High Availability.

Although data is stored redundantly within a Cloudant cluster, it's important to consider further backup measures. For example, redundant data storage does not protect against mistaken changes to data.

## CouchBackup (and CouchRestore)

Cloudant provides supported tooling for snapshot backup and restore. This tool is called `couchbackup` and is open source. It is a node.js library and is [available to install on npm ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}.

In addition to the library, the CouchBackup package contains two command line tools:

1. `couchbackup` -- this dumps the JSON data from a database to a backup text file.
2. `couchrestore` -- restores data from a backup text file to a database.

### Backup

A simple backup looks like the following:

    couchbackup --url https://examples.cloudant.com -db animaldb > backup.txt

The npm readme details the full options.

### Restore

Restoring data requires using the included `couchrestore` tool. Use `couchrestore` to first import the backup file into a new Cloudant database. Then ensure you build all indexes before pointing application servers to the restored data.

To restore the data backed up in the previous example:

    couchrestore --url https://myaccount.cloudant.com --db newanimaldb < backup.txt

Again, see the readme for the full details.

### Limitations

CouchBackup backs up a Cloudant database to a plain text file. This file contains only the JSON data in the database, including index definitions (but not index content).

<strong style="color:red;">Warning!</strong> This appoach comes with a number of limitations, detailed in [Cloudant Disaster Recovery guide](disaster-recovery-and-backup.html).

## Examples

The [npm page ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window} details the basics of using the command line tools to both backup and restore data.

As noted above, the `couchbackup` package provides two ways of using its core functionality.

1.	Two command line tools that can be embedded into standard Unix command pipelines. For many scenarios, a combination of `cron` and simple shell scripting of the `couchbackup` application may prove sufficient.
2.	A library usable from node.js. This allows more complicated backup processes to be orchestrated, such as dynamically determining the databases to be backed up.

Below we examine using both the command line backup tool and library to embed backup from Cloudant databases into more complicated situations. In particular, scheduling backups using `cron` and automatically uploading data to [Cloud Object Storage](http://www-03.ibm.com/software/products/en/object-storage-public) for long term retention.

[1]: https://www.npmjs.com/package/couchbackup

### Command Line Scripting Examples

We'll look at two examples:

1.	Zipping the backup file to save disk space.
2.	Creating a daily or hourly backup of a database.

#### Zipping a backup file

CouchBackup can either write a backup file to disk directly or stream the backup to `stdout`. Streaming to `stdout` allows for the data to be transformed before writing to disk. We'll use that to zip data before writing.

```sh
couchbackup --url "https://examples.cloudant.com" \
	--db "animaldb" | gzip > backup.gz
```
{:codeblock}

To supply a set of credentials, use a URL form `https://user:pass@foo.cloudant.com`.

One can imagine lengthening the pipeline if one wanted to transform the data in other ways -- say to encrypt the data before it's written to disk. It's also possible to write directly to object storage services using their command line tooling.

#### Hourly or Daily Backups using Cron

It's straightforward to use `cron` to set up periodic snapshots of data.

To start with, here's how to get couchbackup to write a backup to a file including the current UTC datetime:

```sh
couchbackup --url "https://username:password@mikerhodes.cloudant.com" \
	--db "animaldb" > animaldb-backup-`date -u "+%Y-%m-%dT%H:%M:%SZ"`.bak
```
{:codeblock}

Once you have this command, it can be entered into a cron job. On the server storing the backups, install couchbackup and create a folder to store the backups, then add a cron entry. Edit your crontab using `crontab -e` and for a daily backup enter the following:

```sh
0 5 * * * couchbackup --url "https://username:password@mikerhodes.cloudant.com" --db "animaldb" > /path/to/folder/animaldb-backup-`date -u "+%Y-%m-%dT%H:%M:%SZ"`.bak
```
{:codeblock}

This will create a daily backup at 05:00. Alter the cron pattern to do hourly, daily, weekly or monthly backups as required.

### Using couchbackup as a library

The `couchbackup` and `couchrestore` command line tools are wrappers around a library that's usable from your own node.js applications. This is useful for more complicated scenarios, like:

*	Backing up several databases (e.g., read `_all_dbs` and backup each).
*	Easier error handling in longer pipelines.

There are details on the library usage on [the npm page ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}.

Here's a script showing how to combine the `couchbackup` library with using IBM's Cloud Object Storage -- Cross Region S3 API to backup a database to object storage.

First, initialise the S3 client object for Cloud Object Storage by following [these instructions][cosclient].

[cosclient]: https://developer.ibm.com/recipes/tutorials/cloud-object-storage-s3-api-intro/

```javascript
/*
  Backup directly from Cloudant to an S3 bucket via a stream.
  @param {string} couchHost - URL of database root
  @param {string} couchDatabase - backup source database
  @param {object} s3Client - S3 client object
  @param {string} s3Bucket - Destination S3 bucket (must exist)
  @param {string} s3Key - Destination object's key (shouldn't exist)
  @param {boolean} shallow - Whether to use couchbackup's shallow mode
  @returns {Promise}
*/
function backupToS3(sourceUrl, s3Client, s3Bucket, s3Key, shallow) {
  return new Promise((resolve, reject) => {
    debug(`Setting up S3 upload to ${s3Bucket}/${s3Key}`);

    // A pass through stream that has couchbackup's output
    // written to it and it then read by the S3 upload client.
    // It has a 10MB internal buffer.
    const streamToUpload = new stream.PassThrough({highWaterMark: 10485760});

    // Set up S3 upload.
    const params = {
      Bucket: s3Bucket,
      Key: s3Key,
      Body: streamToUpload
    };
    s3Client.upload(params, function(err, data) {
      debug('S3 upload done');
      if (err) {
        debug(err);
        reject(new Error('S3 upload failed'));
        return;
      }
      debug('S3 upload succeeded');
      debug(data);
      resolve();
    }).httpUploadProgress = (progress) => {
      debug(`S3 upload progress: ${progress}`);
    };

    debug(`Starting streaming data from ${sourceUrl}`);
    couchbackup.backup(
      sourceUrl,
      streamToUpload,
      (err, obj) => {
        if (err) {
          debug(err);
          reject(new Error('CouchBackup failed with an error'));
          return;
        }
        debug(`Download from ${sourceUrl} complete.`);
        streamToUpload.end();  // must call end() to complete S3 upload.
        // resolve() is called by the S3 upload
      }
    );
  });
}
```
{:codeblock}

## Other disaster recovery options

Return to the [Cloudant Disaster Recovery guide](disaster-recovery-and-backup.html) to find out about the other features Cloudant offers for a full disaster recovery set up.
