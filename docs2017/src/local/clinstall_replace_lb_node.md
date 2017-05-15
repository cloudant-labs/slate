---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-13"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Replacing a load balancer node


You can rebuild or replace a load balancer node by using the
following instructions.
{:shortdesc}


<ol>
<li>Stop traffic to the load balancer node before you remove it. You stop your load balancer based on your setup.
<ol type=a>
<li>If you run a failover load balancer, confirm that it is
    operating correctly and can access the cluster with that
    load balancer.</li>
<li>Make any required changes, such as changes to DNS
    settings, to reroute all traffic through the failover
    load balancer.</li>
</ol>
</li>
<li>If the node is running, stop any services that are running on
    the node and shut it down.</li>
<li>Repair or replace the node.</li>
<li>Install Cloudant&reg; Local on the load balancer node, as
    described in [Installing load balancer nodes](clinstall_install_load_balancer_nodes.html).</li>
<li>Configure the `lbnode.yaml` file with your current cluster
    configuration when you run the `cast system install` commands.
</li>
<li>Verify that the replacement load balancer is operational.
<p>You can check by directly accessing the load balancer and
    confirming that you get a valid response.</p></li>
<li>Send traffic to the load balancer again.
<ol type=a>
<li>If you are running a failover load balancer, confirm that
    it is running correctly.</li>
<li>To reroute all traffic through the failover or
    replacement load balancer, make the required changes,
    such as DNS settings.</li>
</ol></li>
</ol>
