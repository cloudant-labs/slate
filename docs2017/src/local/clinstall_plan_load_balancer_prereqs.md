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

# Load balancer prerequisites

Before you install Cloudant&reg; Local, verify that you meet the load
balancer prerequisites.
{:shortdesc}


1. You must install and configure a load balancer on a separate
   server from the ones that are used in the Cloudant cluster. To
   ensure uninterrupted service, you can install a second
   (failover) load balancer server.

2. If you are deploying multiple load balancers in a failover
   configuration, confirm that all load balancers are on the same
   Layer 2 LAN segment. This step is required for VRRP-based
   failover to function correctly.

3. Confirm that DNS entries exist for both the public and private
   IP addresses for each Load Balancer node.

4. Record the following information for your primary load
   balancer (Load Balancer 1) for future reference.

   *  Public DNS Name
   *  Public IP
   *  Private DNS Name
   *  Private IP

   >    **Note:** If you use a single IP address per node, complete only the "Public" lines for your primary and secondary load balancers. The "Public" IP addresses for these database nodes do not have to be public IP spaces. They are public only in the sense that they provide the actual database service. In general, this network would be a separate network segment from the "private" side of the servers, where all node-to-node and out-of-band communication takes place.

   If you use a failover load balancer, record the same
   information for your second load balancer (Load Balancer 2).

   *  Public DNS Name
   *  Public IP
   *  Private DNS Name
   *  Private IP

5. Confirm that the virtual IP address is available for the load
   balancers to share. This address is the IP address that
   clients use to access the cluster. Record this IP address for
   future reference.

   *  Virtual IP address
