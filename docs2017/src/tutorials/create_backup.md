---

copyright:
  years: 2017
lastupdated: "2017-06-21"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Creating a backup

This tutorial demonstrates how to use the 
[CouchBackup](https://www.npmjs.com/package/couchbackup) command-line 
utility to back up and restore a CouchDB or Cloudant instance. CouchBackup backs up 
the database to a file. If the database fails, you can use the backup file to 
restore the information to an existing database. 
{:shortdesc}

## Before you begin

Install CouchBackup by running the `install` command. 

`npm install -g couchbackup`
 

## Creating a database

Create the sample `couchbackup-demo` database. This database is the one
we use in this tutorial.
 
<ol><li>Create a database by running this command.
<p><code>curl https://username:password@myhost.cloudant.com/couchbackup-demo -X PUT</code></p></li>
<li>Review the results. 
<p><code>{"ok":true}</code></p></li></ol>

## Creating documents in the database

The documents that you create in this exercise contain the data that you 
back up and restore in later exercises. 

<ol><li>Copy the sample text to a data file named <code>bulkcreate.dat</code> to create all five documents.
<p><pre>{
"docs": 
   [
	{ 
		"_id": "doc1",
		"firstname": "Sally",
		"lastname": "Brown",
		"age": 16,
		"location": "New York City, NY"
    },
     { 
		"_id": "doc2",
        "firstname": "John",
	    "lastname": "Brown",
	    "age": 21,
        "location": "New York City, NY"
    },
     {
		"_id": "doc3",
		"firstname": "Greg",
		"lastname": "Greene",
		"age": 35,
		"location": "San Diego, CA"
    },
     {
		"_id": "doc4",
		"firstname": "Anna",
		"lastname": "Greene",
		"age": 44,
		"location": "Baton Rouge, LA"
    },
     {
		"_id": "doc5",
		"firstname": "Lois",
		"lastname": "Brown",
		"age": 33,
		"location": "Syracuse, NY"
    }
  ]
}</pre></p></li>
<li>Run this command to create the documents. 
<p><code>curl https://username:password@myhost.cloudant.com/couchbackup-demo/_bulk_docs -X POST -H "Content-Type: application/json" -d \@bulkcreate.dat</code></p>
</li>
<li>Review the results. 
<p><pre>[{"ok":true,
"id":"doc1","rev":"1-57a08e644ca8c1bb8d8931240427162e"},
{"ok":true,"id":"doc2","rev":"1-bf51eef712165a9999a52a97e2209ac0"},
{"ok":true,"id":"doc3","rev":"1-9c9f9b893fcdd1cbe09420bc4e62cc71"},
{"ok":true,"id":"doc4","rev":"1-6aa4873443ddce569b27ab35d7bf78a2"},
{"ok":true,"id":"doc5","rev":"1-d881d863052cd9681650773206c0d65a"}]</pre></p>
</li></ol>

## Setting the environment variables

You can use environment variables or command-line options to specify the 
URL and database for the CouchDB or Cloudant instance that you want to work 
with CouchBackup. 

1.  Set the `COUCH_URL` environment variable to specify the URL for the CouchDB or Cloudant instance.
  
    `export COUCH_URL=https://username:password@myhost.cloudant.com`
    
2.  Set the `COUCH_DATABASE` environment variable to specify the name of the database to back up and restore. 
 
    `export COUCH_DATABASE=couchbackup-demo`


## Backing up a database

The CouchBackup utility backs up your database to a text file to preserve 
your data and make it easier to restore. 

1.  Run the `couchbackup` command to direct the contents of your database to a text file. 
 
    `couchbackup > couchbackup-demo-backup.txt`

2.  Review the results. 

    <pre>================================================================================
    Performing backup on https://****:****@myhost.cloudant.com/couchbackup-demo using configuration:
    {
        "bufferSize": 500,
        "log": "/var/folders/r7/vtctv4695hj_njxmr2hj4jyc0000gn/T/tmp-3132gHPWk9A9yGVe.tmp",
        "mode": "full",
        "parallelism": 5
    }
    ================================================================================
    Streaming changes to disk:
     batch 0
        couchbackup:backup written 0  docs:  5 Time 0.604 +0ms
        couchbackup:backup finished { total: 5 } +4ms
    </pre>
    
3.  Check the directory to verify that the `couchbackup-demo-backup.txt` file was created. 
4.  Open the file and review the list of documents from the database.  

## Creating a log file

A log file records the progress of your backup. With CouchBackup, you use the `--log` parameter 
to create the log file. You can also use it to restart a backup from where it stopped 
and specify the output file name. 

The `couchbackup` command uses these parameters to specify the database, 
log file, and resume option. 

*   `--db` = `couchbackup-demo`
*   `--log` = `couchbackup-demo.log`
*   `--resume` = `true`


1.  Run the `couchbackup` command to create a log file. 
 
    `couchbackup --db couchbackup-demo --log couchbackup-demo-backup.log`
    
2.  Review the results.

    You can also open the log file, `couchbackup-demo-backup.log`, and review the actions taken
    during a backup or restore.
    
    <pre>================================================================================
    Performing backup on https://****:****@myhost.cloudant.com/couchbackup-demo using configuration:
        {
          "bufferSize": 500,
          "log": "couchbackup-demo-backup.log",
          "mode": "full",
          "parallelism": 5
        }
    ================================================================================
    Streaming changes to disk:
     batch 0
        [{"_id":"doc2","_rev":"1-2c5ee70689bb75af6f65b0335d1c92f4",
            "firstname":"John","lastname":"Brown","age":21,
            "location":"New York City, NY",
            "_revisions":{"start":1,"ids":["2c5ee70689bb75af6f65b0335d1c92f4"]}},
        {"_id":"doc4","_rev":"1-0923b723c62fe5c15531e0c33e015148",
            "firstname":"Anna","lastname":"Greene","age":44,
            "location":"Baton Rouge, LA",
            "_revisions":{"start":1,"ids":["0923b723c62fe5c15531e0c33e015148"]}},
        {"_id":"doc1","_rev":"1-cce7796c7113c5498b07d8e11d7e0c12",
            "firstname":"Sally","lastname":"Brown","age":16,
            "location":"New York City, NY",
            "_revisions":{"start":1,"ids":["cce7796c7113c5498b07d8e11d7e0c12"]}},
        {"_id":"doc5","_rev":"1-19f7ecbc68090bc7b3aa4e289e363576",
            "firstname":"Lois","lastname":"Brown","age":33,
            "location":"Syracuse, NY",
            "_revisions":{"start":1,"ids":["19f7ecbc68090bc7b3aa4e289e363576"]}},
        {"_id":"doc3","_rev":"1-f6055e3e09f215c522d45189208a1bdf",
            "firstname":"Greg","lastname":"Greene","age":35,
            "location":"San Diego, CA",
            "_revisions":{"start":1,"ids":["f6055e3e09f215c522d45189208a1bdf"]}}]
                couchbackup:backup written 0  docs:  5 Time 0.621 +0ms
                couchbackup:backup finished { total: 5 } +4ms
    </pre>
    
##  Restoring from a backup text file

From the `couchbackup-demo-backup.txt` file, you can restore your data to an 
existing database using the `couchrestore` command. 

1.  Run the `couchrestore` command.

    `cat couchbackup-demo-backup.txt | couchrestore --db couchbackup-demo`
    
2.  Review the results. 

    <pre>================================================================================
    Performing restore on https://****:****@myhost.cloudant.com/couchbackup-demo using configuration:
    {
      "bufferSize": 500,
      "parallelism": 5
    }
    ================================================================================
      couchbackup:restore restored 5 +0ms
      couchbackup:restore finished { total: 5 } +1ms
      </pre>

You can find more information about [disaster recovery and backup](../guides/disaster-recovery-and-backup.html#disaster-recovery-and-backup), [configuring Cloudant for cross region disaster recovery](../guides/active-active.html#configuring-cloudant-for-cross-region-disaster-recovery), and [Cloudant backup and recovery](../guides/backup-cookbook.html#cloudant-backup-and-recovery) in the Cloudant Documentation.  

