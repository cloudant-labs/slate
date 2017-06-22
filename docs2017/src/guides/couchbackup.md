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

<!-- Acrolinx: 2017-05-02 -->

# Back up your data by using CouchBackup

The distributed nature of {{site.data.keyword.cloudant}} provides an inherent form of data backup.
CouchBackup is a command line tool that provides you with a more powerful and flexible way for you to back up your data.
{:shortdesc}

## Overview

The distributed benefits of {{site.data.keyword.cloudant_short_notm}} are achieved by using clusters.
In a cluster,
data within a database is stored in multiple copies.
The copies are spread across at least three separate physical servers.
Using clusters for data storage gives {{site.data.keyword.cloudant_short_notm}}
inherent High Availability (HA) and Disaster Recovery (DR) characteristics.
Using clusters helps {{site.data.keyword.cloudant_short_notm}} tolerate the loss of a node
from within a cluster without losing data.

However,
even with these HA and DR characteristics,
there are other use cases where you might want enhanced backup of data.

<div id="activepassive"></div>

### Data Center outage and Disaster Recovery

[Continuous replication](../api/replication.html#continuous-replication) between clusters is a good solution to the problem of
when a {{site.data.keyword.cloudant_short_notm}} cluster is not completely available.
Continuous replication is an 'active-passive' model.
The 'active' part of the model is the continuous replication.
The 'passive' part of the model acknowledges that the replica is not normally intended to respond to requests from applications.
Instead,
the replica is primarily used as a clone of the original database.
If necessary,
the data can be accessed from the clone.
Alternatively,
the data in the clone might be restored somewhere else by using [replication](../api/replication.html).

>	**Note:** Restoring a large database by replicating from a clone might take a long time.

### High Availability, automatic fail-over, and geo-load balancing

An alternative to the ['active-passive'](#activepassive) approach is where you configure two data centers to use an 'active-active' model.

In this model,
any changes that are made to a database in cluster A are replicated to a database in cluster B.
Similarly,
any changes that are made to the database in cluster B are replicated to the database in cluster A.

>	**Note:** This model can be set up by using the {{site.data.keyword.cloudant_short_notm}} dashboard.
It does not require action by {{site.data.keyword.cloudant_short_notm}} support.

With this model in place,
you can design your database applications to 'fail over' to one of the clusters if some availability criteria is met.
You can define the availability criteria as part of your application design.

You can also include geographic 'load balancing' in your application design.
For example,
a client application that is used in one geographical area would normally expect better performance
when the application accesses data that is stored within a cluster in a 'nearby' geographical area.
Designing the client application to identify the 'closest' cluster and connect to that for database queries
would help the application performance.

A tutorial explaining how to set up a multi-region application environment is available
[here ![External link icon](../images/launch-glyph.svg "External link icon")](http://www.ibm.com/developerworks/cloud/library/cl-multi-region-bluemix-apps-with-cloudant-and-dyn-trs/index.html){:new_window}.

### Accidental or malicious or data modification

{{site.data.keyword.cloudant_short_notm}} does not provide a mechanism for creating a snapshot of your database.
If you need this kind of capability,
for example to facilitate document-level roll-back to a previous known state,
you might achieve the same effect in one of two ways:

1.	By using replication. Do this by replicating the database. Make sure you record the final sequence ID. On a schedule that you determine, replicate the database to a new database. Start the replication from the last recorded sequence ID. By retaining the sequence IDs for the replications, you can produce the effect of a roll-up mechanism. The result would be similar to creating regular 'weekly' snapshots from the 'daily' snapshots. A limitation of this approach is that it also replicates deleted or 'tombstone' document revisions, and also unresolved conflicts.

2.	By dumping the database contents to file. Various tools exist that might be used to dump the database contents to a file. The resulting dump file can be stored on a cheaper block-oriented device or service. A limitation of such an approach is that it normally dumps the current document revisions only. This limitation means that unresolved conflicts are not included.

Creating a database dump is an effective way of enabling a variety of backups solutions.
Therefore,
the remainder of the discussion focuses on this approach.

<!--
https://developer.ibm.com/clouddataservices/2016/03/22/simple-couchdb-and-cloudant-backup/

A useful approach is to have couchbackup's snapshots placed on the Bluemix Object Storage service, as described here:

https://developer.ibm.com/recipes/tutorials/object-storage-cloudant-backup/
-->