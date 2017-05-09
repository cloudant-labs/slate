---

copyright:
  years: 2017
lastupdated: "2017-05-09"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# Disaster Recovery and Backup

Your data is important and valuable.
You want to protect your data,
to help ensure it is secure,
available,
and maintains integrity.
Cloudant provides several ways to protect your data and help keep your applications running.
{:shortdesc}

Some of these protection features are automatic.
For other forms of protection,
Cloudant provides you with supported tooling that
enables you to create your own high availability and disaster recovery capabilities.

This document provides an overview of the automatic capabilities and supported tools offered by Cloudant.

## Types and levels of protection

The type of protection you might want depends on the problem you are trying to solve.

For example,
you might want to have a high level of data availability.
For example,
you still want to access your data,
even if a limited amount of hardware within the system has failed.
This is a 'High Availability' (HA) requirement.
It means providing the best possible continuous data availability after a hardware failure.
Different HA techniques tolerate different levels of failure before operations are affected.

Alternatively,
you might want to have easy and quick ways of backing-up and restoring data.
For example,
after a more severe or extensive hardware failure,
you want to be able to make all the data available on an alternative system
as quickly as possible.
This is a 'Disaster Recovery' (DR) requirement.
A disaster generally means that a database is no longer available in one or more locations.
For example,
a power outage might cause all machines in a database cluster to fail.
Alternatively,
a large scale network failure might mean that machines in a cluster cannot be contacted,
even though they continue to work correctly.

Addressing your HA or DR requirements often begins by simplifying the problem into more generic requirements.
When you have identified your requirements,

You can apply the tools and features that help solve the generic needs can then be put toget

Different tools and features provide different levels of protection.
The different features might be more or less suitable for your specific HA or DR requirement.

Cloudant provides a number of tools and features that address general requirements:

1.	Data redundancy within a single region.
2.	Cross-region data redundancy and failover.
3.	Point in time snapshot backup for point-in-time restore.

## In-Region Automatic Data Redundancy

Within a single Cloudant account, data is stored in triplicate. This primarily protects your data against hardware failure. When hardware fails, only a single copy of your data is made unavailable. Your applications remain online as Cloudant automatically routes to copies of the data that are still available. Within a short period of time, full redundancy will be restored.

As a Cloudant account is located in a single region, data is stored across separate servers that are hosted within that single region. Therefore the limitations of this automatic feature are:

1.	Offers protection within a single region.
2.	Maintains current data -- so does not protect against application errors or malicious actors.

**Summary:** This can be considered in-region high availability for failures impacting single machines. As all machines are within the same region, this option offers no disaster recovery by the above definition.

## Cross-Region Redundancy for Disaster Recovery

Cloudant's replication feature is designed to help you build flexible disaster recovery and high availability into your applications. The primary way to go about this is to use replication to create redundancy across regions so your application is able to tolerate one (or more) regions going offline.

The basic steps in creating cross-region redundancy are:

1.	Create Cloudant accounts in two or more regions.
2.	Create databases in each region as needed.
3.	For databases that need to be redundantly stored cross-region, set up bi-directional continuous replications between the corresponding databases in each account.
4.	Direct application traffic appropriately depending on whether this is an Active-Passive or Active-Active deployment.

There is a detailed [guide to setting this up](active-active.html).

Once your data is stored across multiple regions, there are several ways to make use of it:

*	Application servers can make requests of the databases hosted nearest to their physical location. This lowers latency to increase response time to users (who can in turn be directed to the application servers nearest to their devices). This is an Active-Active method, as multiple copies of data are used concurrently. It is particularly important to have a [conflict handling strategy](mvcc.html#distributed-databases-and-conflicts) when using Cloudant in this way.
*	Instead, an application can by default use data from a single region. If that region becomes unavailable to them, the application can switch to requesting data from another region. This is an Active-Passive method, as only one set of data is in active use at a time.
*	An application could have a single account to which all writes are directed, and use the other locations as read-only. This is Active-Active for reads. Depending on whether failover is desired, it may be considered Active-Passive for writes.
*	In a disaster scenario, your application access data in the account(s) hosted in regions that are still online. Therefore your application needs to be able to detect the loss of a region and appropriately redirect its traffic.

**Summary:** This can be considered high availability for failures impacting an entire region. It also offers disaster recovery as the application can continue serving with one region's data unavailable. Cloudant can ensure data synchronisation between regions, but the application must ensure that it can failover to other copies of the data on regional failures.

## Database Backup and Recovery

While the cross-region data redundancy discussed so far offers disaster recovery and high availability, it still maintains only the current copy of your data.

Sometimes people make mistakes and change data in unintended ways. This can be protected against in applications, but sometimes changes get through. In this case, being able to restore data from a previous point in time is invaluable. Backups deal with this requirement. 

To complete your data protection and disaster recovery story, consider periodically dumping database data to a separate location. Cloudant's supported tooling will dump JSON database content to a file and restore databases from those files.

In summary the tooling offers:

*	Backup complete databases to a file suitable for further processing and off-site storage.
*	Restore complete databases from a previous state.

The tooling has limitations: 

*	The following are not backed up by the tooling:
	*	`_security` settings.
	*	Attachments.
*	Backups are not "point-in-time". The documents in the database are retrieved in batches, so the data in the database can change between the first and last batch being read.
*	While index definitions (design documents) are backed up, on restoring data indexes must be rebuilt which can take considerable amounts of time.

Customers can build on this basic functionality to enable more complex data protection strategies:

*	Restore single documents from previous states.
*	Store multiple previous states to allow for restores from long in the past.
*	Migrate older data to cheaper storage for cost-effective retention.

The backup tooling is an open source node.js command line application and library. It is available [on NPM ![External link icon](../images/launch-glyph.svg "External link icon")](https://www.npmjs.com/package/couchbackup){:new_window}.
For ideas on how to integrate the tooling into your data protection strategy,see the [Backup Cookbook guide](backup-cookbook.html).

**Summary:** Backup and restore offer disaster recovery presuming the data is stored in a different region to the data being backed up.