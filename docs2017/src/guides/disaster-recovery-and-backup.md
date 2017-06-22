---

copyright:
  years: 2017
lastupdated: "2017-05-19"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-05-10 -->

# Disaster Recovery and Backup

Your data is important and valuable.
You want to protect your data,
to help ensure it is secure,
available,
and maintains integrity.
Cloudant provides several ways to protect your data and help keep your applications operational.
{:shortdesc}

Some of these protection features are automatic.
For other forms of protection,
Cloudant provides you with supported tools that
help you to create your own high availability and disaster recovery capabilities.

This document provides an overview of the automatic capabilities and supported tools that are offered by Cloudant.

## Types and levels of protection

The type of protection you might want depends on the problem you are trying to solve.

For example,
you might want to have a high level of data availability so that you can still access your data,
even if a limited amount of hardware within the system failed.
This is a 'High Availability' (HA) requirement.
It means providing the best possible continuous data availability after a hardware failure.
Different HA techniques tolerate different levels of failure before operations are affected.

Alternatively,
you might want to have easy and quick ways of backing-up and restoring data.
For example,
after a severe or extensive hardware failure,
you want to be able to make all the data available on an alternative system
as quickly as possible.
This is a 'Disaster Recovery' (DR) requirement.
A disaster generally means that a database is no longer available in one or more locations.
For example,
a power outage might cause all systems in a database cluster to fail.
Alternatively,
a large-scale network failure might mean that systems in a cluster cannot be contacted,
even though they continue to work correctly.

Addressing your HA or DR requirements often begins by simplifying the problem into more generic requirements.
When you identify your requirements,
you can apply the tools and features that help solve the generic needs.
When put together,
the tools and features can then address your HA or DR requirements.

>	**Note**: Different tools and features provide different levels of protection.
	The different features might be more or less suitable for your specific HA or DR requirement.

Cloudant provides a number of tools and features that address general requirements:

1.	Data redundancy within a single region, also known as [In-Region Automatic Data Redundancy](#in-region-automatic-data-redundancy).
2.	Cross-region data redundancy and failover, also known as [Cross-Region Redundancy for Disaster Recovery](#cross-region-redundancy-for-disaster-recovery).
3.	Point in time snapshot backup for point-in-time restore, by using 'traditional' [Database Backup and Recovery](#database-backup-and-recovery).

## In-Region Automatic Data Redundancy

Within a single Cloudant account,
data is stored in triplicate by using internal and automatic processes.
You do not need to do anything to enable this internal data replication.

In-region data redundancy enables high availability protection.
Specifically,
in-region data redundancy provides protection for your data against hardware failure within the region.
When a hardware unit within the region fails,
only the copy of your data that is stored on that unit is no longer available.
Your applications remain usable because Cloudant automatically routes requests to the copies of your data
that are still available on other hardware units within the region.
Meanwhile,
automatic monitoring of systems detects the hardware unit failure,
prompting action and subsequent restoration of full redundancy.

Cloudant accounts are located within a single region.
This characteristic means that all the data that you store within your account is stored across separate servers,
each of which is hosted within that single region.

In-region automatic data redundancy is limited to:

1.	Providing protection within a single region only.
2.	Maintaining current data.

To provide protection across more than the single region associated with your account,
use [Cross-Region Redundancy for Disaster Recovery](#cross-region-redundancy-for-disaster-recovery).

To provide protection for the 'history' of your data,
for example to enable auditing of changes that are made to data by applications,
use data snapshots that are created by [Database Backup and Recovery](#database-backup-and-recovery) tools.

In summary,
in-region data redundancy enables a High Availability capability
by providing tolerance for failures that affect single systems within the region.

## Cross-Region Redundancy for Disaster Recovery

The Cloudant replication feature helps you build a flexible disaster recovery capability into your applications.
The main way to enable disaster recovery is to use Cloudant replication to create redundancy across regions.
The result is that your application is able to tolerate the situation where one or more region is not available.

The basic steps in creating cross-region redundancy are:

1.  Create Cloudant accounts in two or more regions.
2.  Create databases in each region as needed.
3.  For databases that must be stored with cross-region redundancy, set up bidirectional continuous replications between the corresponding databases in each account.
4.  Design and implement your applications so that data requests are routed depending on whether your environment is an Active-Passive or Active-Active configuration.
  A detailed guide to setting this up is [available](active-active.html).

When you design your applications to work with data across multiple regions,
consider the following points:

* Applications can send requests to the database hosted nearest to their physical location.
  This use of proximity can reduce network latency and improve response times.
  This configuration is referred to as an 'Active-Active' method.
  It is characterized by the concurrent use of multiple copies of data.
  Applications that work within an active-active configuration must have
  a [strategy for handling conflicts](mvcc.html#distributed-databases-and-conflicts) to avoid problems with multiple copies of data.
* Applications can request data from a single region by default.
  If the region is not available,
  the application can switch to requesting data from another region.
  This configuration is referred to as an 'Active-Passive' method.
  It is characterized by the active use of one set of data only at a time.
* An application might use a hybrid configuration,
  where a single account is used for all data write requests,
  and other locations as used exclusively for read-only requests.
  This configuration is considered Active-Active for reads.
* In a disaster scenario,
  your application must reroute data requests to access the accounts
  that are hosted in the regions that are still online.
  This requirement means that your application must be able to detect the loss of a region,
  and then reroute data requests.

In summary,
cross-region redundancy is similar to a high availability capability,
but applies to failures that affect an entire region.
However,
configuring your applications to work correctly with cross-redundancy configurations provides a true disaster recovery capability.
The reason is that the applications can continue working if the data in one region is not available for an amount of time.
Cloudant replication helps ensure data synchronization between regions.
However,
your applications must be able to 'fail over' to copies of your data that are stored in other regions.

## Database Backup and Recovery

[In-Region Automatic Data Redundancy](#in-region-automatic-data-redundancy) provides applications with high availability access to data.
[Cross-Region Redundancy for Disaster Recovery](#cross-region-redundancy-for-disaster-recovery) provides applications with a means of recovering from a disaster.
However,
both of these capabilities focus on maintaining access only to the _current_ copy of your data.

In practice,
people and applications can make mistakes and change data in unintended ways.
The applications themselves can implement some protection,
but sometimes undesirable changes get through.
In this case,
it is useful to be able to restore data from a previous point in time.
Database backups support this requirement.

In addition to protecting your data with high availability and disaster recovery features,
consider dumping your database data to a separate location at periodic,
regular intervals.
Ensure that you check and test the backups for confidence that they are complete and correct.

Cloudant supports tools that helps you dump the JSON content in databases to a file,
and later restore databases from those files.

Specifically,
the tools supported by Cloudant help you to:

*	Backup complete databases to a file,
	suitable for further processing and off-site storage.
*	Restore complete databases from a previous state that is contained in your backup file.

<strong style="color:red;">Warning!</strong> The tools supported by Cloudant have the following limitations: 

*	`_security` settings are not backed up by the tools.
*	Attachments are not backed up by the tools.
*	Backups are not precisely accurate "point-in-time" snapshots.
	The reason is that the documents in the database are retrieved in batches,
	but other applications might be updating documents at the same time.
	Therefore,
	the data in the database can change between the times when the first and last batches are read.
*	Index definitions held design documents are backed up,
	but when data is restored the indexes must be rebuilt.
	This rebuilding might take a considerable amount of time,
	depending on how much data is restored.

<div id="conclusion"></div>

## Next steps

You can develop applications that build on basic Cloudant functions and supported tools
to enable more complex data protection strategies.

Example scenarios include:

*	Restoring single documents from previous states.
*	Storing multiple previous document states, to allow for restores from long in the past.
*	Migrating older data to cheaper storage, for more cost-effective retention.

The backup tools consist of an open source node.js command line application and library.
It is available [on NPM ![External link icon](../images/launch-glyph.svg "External link icon")](https://www.npmjs.com/package/couchbackup){:new_window}.

For ideas and examples that show how to integrate the tools into your data protection strategy,
see the [Backup Cookbook guide](backup-cookbook.html).
