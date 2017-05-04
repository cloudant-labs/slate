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

This cookbook forms part of the [Cloudant Disaster Recovery guide](disaster-recovery-and-backup.md). It's worth starting there if you are new to the subject to understand where backup fits in with Cloudant's other features for Disaster Recovery and High Availability.

Although data is stored redundantly within a Cloudant cluster, it's important to consider further backup measures. For example, redundant data storage does not protect against mistaken changes to data.

## CouchBackup (and CouchRestore)

Cloudant provides supported tooling for snapshot backup and restore. This tool is called `couchbackup` and is open source. It is a node.js application and library and is [available to install on npm ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}. 

CouchBackup backs up a Cloudant database to a plain text file. This file contains all the JSON data in the database, including index definitions (but not index content). This implies the following limitations:

*	Attachments are not included in backup files.
*	Indexes need rebuilding when restoring data.

Restoring data requires using the included `couchrestore` tool. Use `couchrestore` to first import the backup file into a new Cloudant database. It's important to then build any indexes before pointing application servers to the restored data.

As the [npm page ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window} details the basics of using the command line tools to both backup and restore data, this document will give a few scripting ideas to demonstrate how the tool may be built into a wider pipeline. It'll also show library usage.

The `couchbackup` package provides two ways of using its core functionality.

1.	A command line tool that can be embedded into standard Unix command pipelines. For many scenarios, a combination of `cron` and simple shell scripting of the application may prove sufficient.
2.	A library usable from node.js. This allows more complicated backup processes to be orchestrated, such as dynamically determining the databases to be backed up.

Examples of the ways both of these forms can be used are presented below.

[1]: https://www.npmjs.com/package/couchbackup

## Command Line Scripting Examples

We'll look at two simple examples:

1.	Zipping the backup file to save disk space.
2.	Creating a daily or hourly backup of a database.

### Zipping a backup file

CouchBackup can either write a backup file to disk directly or stream the backup to `stdout`. Streaming to `stdout` allows for the data to be transformed before writing to disk. We'll use that to zip data before writing.

```sh
couchbackup --url "https://user:pass@mikerhodes.cloudant.com" \
	--db "animaldb" | gzip > backup.gz
```
{:codeblock}

One can imagine lengthening the pipeline if one wanted to transform the data in other ways -- say to encrypt the data before it's written to disk. It's also possible to write directly to S3 in this manner by piping into the S3 command line tooling.

### Hourly or Daily Backups using Cron

It's simple to use `cron` to set up periodic snapshots of data.

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

## Using couchbackup as a library

The `couchbackup` and `couchrestore` command line tools are wrappers around a library that's usable from your own node.js applications. This is useful for more complicated scenarios, like:

*	Backing up several databases (e.g., read `_all_dbs` and backup each).
*	Easier error handling in longer pipelines.
*	If, like me, you're not very good at Unix pipework.

There are details on the library usage on [the npm page ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}, but here's a script showing how to combine the `couchbackup` library with using IBM's Cloud Object Storage -- Cross Region S3 API to backup a database to object storage.

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
function backupToS3(couchHost, couchDatabase, s3Client, s3Bucket, s3Key, shallow) {
  return new Promise((resolve, reject) => {
    debug(`Setting up S3 upload to ${s3Bucket}/${s3Key}`);

    // A pass through stream that has couchbackup's output
    // written to it and it then read by the S3 upload client.
    // It's allowed a 10MB internal buffer before draining is requested.
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

    // Stream the data out of Couch/Cloudant into the stream
    // that the S3 upload is reading from.
    var couchOpts = {
      'COUCH_URL': couchHost,
      'COUCH_DATABASE': couchDatabase
    };
    if (shallow) {
      debug('Creating shallow backup; only stores latest revs');
      couchOpts['COUCH_MODE'] = 'shallow';
    }
    debug(`Starting streaming data from ${couchHost}/${couchDatabase}`);
    couchbackup.backupStream(
      streamToUpload,
      couchOpts,
      (err, obj) => {
        if (err) {
          debug(err);
          reject(new Error('CouchBackup failed with an error'));
          return;
        }
        debug(`Download from ${couchHost}/${couchDatabase} complete.`);
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
