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

# Upgrading

Complete the Cloudant&reg; Local upgrade on each node independently.
{:shortdesc}

Select one of the following upgrade paths.

1.  [Upgrading to Cloudant Local](#upgrading-to-cloudant-local).
2.  [Upgrade to a new cluster](#upgrade-to-a-new-cluster).

## Upgrading to Cloudant Local

To upgrade Cloudant Local, complete the upgrade process on one
node at time until all the nodes of the cluster are upgraded. The
upgrade must be done when the cluster is offline to all
production traffic.

Since Cloudant Local draws upstream source code from CouchDB,
along with bug fixes and enhancements, it inherits commits that
can introduce runtime incompatibilities between different
released versions. Therefore, if your database nodes run code
from different releases concurrently, it is not always possible
to ensure that your cluster remains fully functional. To preserve
your production environment, perform an in-place upgrade to the
entire cluster during maintenance.

>   **Note:** Cloudant Local does not support upgrades to online or live environments.

See the steps to upgrade here, [Overview for upgrading a database
node and a load balancer node](#overview-for-upgrading-a-database-node-and-a-load-balancer-node).

## Upgrading to a new cluster

When you upgrade to a new cluster, you provision new servers and
install the new release to the Cloudant Local cluster. Now, you
can replicate the data from the existing live cluster and start
by using the new cluster by following these steps.

1.  Build a new cluster.
2.  Install the most recent Cloudant Local software on that
    cluster.
3.  Replicate data from the existing cluster to the new cluster.

After you replicate and synchronize both clusters, you can switch
your application to use the new cluster.

By upgrading to a new cluster, you avoid downtime that can be
prohibitive if the necessary downtime is unacceptable. You might
also use this time to upgrade the operating system for the new
server, add new hardware, or add more nodes to the cluster.

Regardless of the approach you choose, it is recommended that you
test your workloads on a cluster with the upgraded release.

## Overview for upgrading a database node and a load balancer node

Follow these steps to upgrade from a Cloudant Local version
1.0.0.5 installation to Cloudant Local version 1.1.0.

>   **Note:** After the upgrade is complete, you cannot roll back to an older version.

You can upgrade only one node at a time, which can eliminate
downtime. Upgrading a node is similar to replacing a node to a
cluster.

Follow the basic upgrade steps for a database node.

1.  Put the database node that you want to upgrade in maintenance
    mode.

2.  Uninstall the existing Cloudant Local version binaries.

3.  Install the new Cloudant Local packages.

4.  Start the upgraded node in maintenance mode.

5.  Check the status of the node.

6.  Bring the node out of maintenance mode.

Follow the basic upgrade steps for a load balancer node.

1.  Confirm that load balancer failover operates correctly if one
    load balancer node is being upgraded.

2.  Uninstall the existing Cloudant Local version binaries.

3.  Install the new Cloudant Local packages and start the upgraded
    node.

4.  Check the status of the node and confirm that traffic is being
    serviced through the upgraded node.
