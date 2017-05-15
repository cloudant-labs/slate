---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-17"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Hardware requirements

Cloudant&reg; Local hardware requirements vary based on different
factors for the database and load balancers.
{:shortdesc}

## x86_64 hardware requirements

The following hardware requirements apply to the x86_64
architecture.

### Database Nodes

*  The minimum requirements include four cores and eight threads,
   such as Xeon E3-1270 V2, 8 GB of RAM and 1-GB network.
*  For larger implementations, the minimum requirements include
   12 cores and 24 threads, such as dual Xeon E5 2620, 64 GB of
   RAM, and local SSD drives to meet data volume requirements of
   your usage and a 1-GB network.

Disk space requirements for the data vary based on how much data
you want to store. At minimum, the standard per-node storage
setup is as follows.

*  If you use spinning disks, 4 x 600 GB 15k SAS drives in RAID 0
   can provide about 2.2 TB of usable storage.
*  If you use solid-state drives (SSDs), 2 x 800 GB SSDs in RAID
   0 can provide about 1.5 TB of usable storage.
*  An ext4 file system that is mounted with the noatime option is
   recommended for performance reasons.

>   **Note:** A storage area network (SAN) is not recommended. If you use
    a centralized location to store all the database files, such as a
    SAN, you might lose high-availability. If the SAN goes down, all
    of your database nodes are unavailable. However, if all of your
    database nodes use directly attached storage, you can lose
    two-thirds of your system and remain operational.

For the operating system and Cloudant binaries, the disk that is
allocated must be 10 GB in RAID 1.

### Load Balancer Nodes

*  The minimum requirements are dual-core processor and 4 GB RAM,
   1 TB local hard disk drive with enough disk space for the OS
   and any log files kept locally,
   and a 1-gigabit network.
*  For larger implementations, the minimum requirements include a
   quad-core processor and 8 GB RAM, 1 TB local hard disk drive,
   and a 1-gigabit network.

## Linux on IBM System z

Confirm that your environment meets the following hardware
requirements.

### Models

*  z13&trade;
*  zEnterprise&reg; - zBC12 and zEC12
*  zEnterprise - z114 and z196

### Processors and Memory

*  Database Nodes
   *  2 IFLs in SMT mode
   *  8 GB memory for each node
*  Load Balancer Nodes
   *  2 IFLs
   *  4 GB memory for each node
