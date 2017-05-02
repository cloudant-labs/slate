---

copyright:
  years: 2017
lastupdated: "2017-05-02"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-04-20 -->

# Back up your data using CouchBackup

The distributed nature of {{site.data.keyword.cloudant}} provides an inherent form of data backup.
The CouchBackup is a command line tool that provides you with a more powerful and flexible way for you to backup your data.
{:shortdesc}

## Overview

The distributed benefits of {{site.data.keyword.cloudant_short_notm}} are achieved by using clusters.
In a cluster,
data in a database are stored in multiple copies.
The copies are spread across at least three separate physical servers.
Using clusters for data storage gives {{site.data.keyword.cloudant_short_notm}}
an inherent High Availability (HA) and Disaster Recovery (DR) capability.
A {{site.data.keyword.cloudant_short_notm}} cluster can tolerate the loss of a node
from within a cluster without losing data.
Replication between databases also helps enable high availability and access to data.

However,
even with these inherent capabilities,
there are some use cases where you might want enhanced backup of data.

### Data Center outage and Disaster Recovery

If a the data center hosting your Cloudant cluster becomes unavailable, having a continuous replication to a different cluster is the solution. This is an active-passive model where the purpose of the spare is not to serve requests, but to act purely as a clone. The data can if needed be accessed from the clone, or restored somewhere else through replication. Note that restoring a large database this way can take a long time.

High Availability, automatic fail-over and geo-load balancing

Another use case is to use two DCs in an active-active configuration. This means that any changes made to a database in cluster A will be replicated to a database in cluster B, and any changes made to the database in cluster B will be replicated to the database in cluster A. This can be set up in the Cloudant dashboard without involvement from Cloudant support. With this in place, it is possible to have an application fail over if some availability criteria is met. This is something that is best implemented in your application's logic, as what constitutes 'available' will vary with use case. Such a set-up can also be used to achieve geographic load balancing, such that clients prefer to connect to the cluster nearest to them for performance reasons.

A good tutorial on how to achieve such a set-up within the Bluemix environment can be found here:

http://www.ibm.com/developerworks/cloud/library/cl-multi-region-bluemix-apps-with-cloudant-and-dyn-trs/index.html

Malicious or Accidental Data Modification

Cloudant does not provide built-in means for snapshotting your databases to facilitate document-level roll-back to a previous state. If you need this kind of functionality, this can be achieved in several ways:

1. Through replication. Replicate the database and record the final sequence id. On a set schedule, replicate to a new database, starting from the last recorded sequence id. This approach can be combined with a roll-up mechanism to regularly create weeklies from the daily snapshots, for example. This will include tombstone (deleted) revisions and unresolved conflicts.

2. Dump the database contents to file. Several tools exist to dump the database contents to a file which can be stored on a cheaper block-oriented device or service. Such an approach will only back up winning revisions, so unresolved conflicts will not be included. An introduction to using the couchbackup tool can be found here:

https://developer.ibm.com/clouddataservices/2016/03/22/simple-couchdb-and-cloudant-backup/

A useful approach is to have couchbackup's snapshots placed on the Bluemix Object Storage service, as described here:

https://developer.ibm.com/recipes/tutorials/object-storage-cloudant-backup/