---

copyright:
  years: 2017
lastupdated: "2017-05-18"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# Cloudant Backup and Recovery

This cookbook forms part of the [{{site.data.keyword.cloudantfull}} Disaster Recovery guide](disaster-recovery-and-backup.html).
It's worth starting there if you are new to the subject and want to understand where backup fits in
with the other capabilities that {{site.data.keyword.cloudant_short_notm}} offers
to support Disaster Recovery (DR) and High Availability (HA) requirements.

Although data is stored redundantly within a {{site.data.keyword.cloudant_short_notm}} cluster,
it's important to consider additional backup measures.
For example,
redundant data storage does not protect against mistakes when data is changed.

## Introducing CouchBackup

{{site.data.keyword.cloudant_short_notm}} provides a supported tool for snapshot backup and restore.
The tool is called CouchBackup,
and is open source.
It is a `node.js` library,
and is [available to install on npm ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}.

In addition to the library,
the CouchBackup package contains two command line tools:

1. `couchbackup`, which dumps the JSON data from a database to a backup text file.
2. `couchrestore`, which restores data from a backup text file to a database.

<strong style="color:red;">Warning!</strong> The CouchBackup tools have [limitations](#limitations).

## Backing up your Cloudant data

You can do a simple backup using the `couchbackup` tool.
For example,
to backup the `animaldb` database to a text file called `backup.txt`,
you might use a command similar to the following:

```sh
couchbackup --url https://examples.cloudant.com --db animaldb > backup.txt
```
{:codeblock}

The npm readme details other options,
including:

* Environment variables to set the names of the database and URL.
* Using a log file to record the progress of a backup.
* The ability to resume an interrupted backup.
  **Note**: This option is only available in conjunction with the log file for the interrupted backup.
* Sending the backup text file to a named output file,
  rather than redirecting the `stdout` output.

<strong style="color:red;">Warning!</strong> The CouchBackup tools have [limitations](#limitations).

## Restoring your Cloudant data

To restore your data,
use the `couchrestore` tool.
Do this by using `couchrestore` to import the backup file
into a new {{site.data.keyword.cloudant_short_notm}} database.
Then,
ensure you build all indexes before any application attemps to use the restored data.

For example,
to restore the data backed up in the earlier example:

```sh
couchrestore --url https://myaccount.cloudant.com --db newanimaldb < backup.txt
```
{:codeblock}

The npm readme provides details of other restore options.

<strong style="color:red;">Warning!</strong> The CouchBackup tools have [limitations](#limitations).

## Limitations

<strong style="color:red;">Warning!</strong> The CouchBackup tools have the following limitations: 

* `_security` settings are not backed up by the tools.
* Attachments are not backed up by the tools.
* Backups are not precisely accurate "point-in-time" snapshots.
  The reason is that the documents in the database are retrieved in batches,
  but other applications might be updating documents at the same time.
  Therefore,
  the data in the database can change between the times when the first and last batches are read.
* Index definitions held in design documents are backed up,
  but the content of indexes is not backed up.
  This limitation means that when data is restored,
  the indexes must be rebuilt.
  The rebuilding might take a considerable amount of time,
  depending on how much data is restored.

## Examples

The [npm page ![External link icon](../images/launch-glyph.svg "External link icon")][1]{:new_window}
details the basics of using the command line tools for backup and restore of data.

The `couchbackup` package provides two ways of using its core functionality.

1.  Two command line tools can be embedded into standard Unix command pipelines.
  For many scenarios,
  a combination of `cron` and simple shell scripting of the `couchbackup` application is sufficient.
2.  A library usable from node.js.
  This library allows more complicated backup processes to be created and deployed,
  such as determining dynamically which databases must be backed up.

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
