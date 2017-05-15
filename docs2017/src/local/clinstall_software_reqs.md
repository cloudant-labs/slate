---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-20"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Software requirements

The following tasks can help you maintain your Cloudant&reg; Local
cluster.
{:shortdesc}

## Cluster server requirements

A minimum of five servers are recommended to create a fully
functional Cloudant cluster that ensures 24 x 7 availability.

### Database Nodes

*  Cloudant Local must be installed on at least three database
   nodes for replication purposes.
*  (Optional) Cloudant Local can be installed on as many other
   nodes as needed to scale for your business requirements.

### Load Balancers

*  One load balancer must be installed on a server that is
   separate from the servers that are used in the Cloudant
   cluster.
*  It is a good practice to install two load balancers in case
   the primary load balancer fails. If a second load balancer is
   installed, you must install it on a separate server to ensure
   uninterrupted service.

## Supported architecture and platforms

You can install Cloudant Local on the following platforms.

### x86_64 architecture

#### Debian-derived Linux distributions

*  Ubuntu Server 12.04 (precise)
*  Ubuntu Server 14.04 (trusty)

#### Red Hat-derived Linux distributions

*  Red Hat Enterprise Linux Server 6.x
*  Red Hat Enterprise Linux Server 7.x
*  Community ENTerprise Operating System (CentOS) 6.x
*  Community ENTerprise Operating System (CentOS) 7.x
*  Oracle Enterprise Linux Operating System (OEL) 6.x
*  Oracle Enterprise Linux Operating System (OEL) 7.x

#### SUSE Linux distributions

*  SUSE Linux Enterprise Server (SLES) 12

### IBM System z s390x architecture

#### Linux on IBM&reg; System z&reg;

*  Linux on IBM System z - Red Hat Enterprise Linux 7.x
*  SUSE Linux Enterprise Server (SLES) 12
