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

# Upgrading a load balancer node

Upgrade each Cloudant&reg; Local load balancer node by following
these steps.
{:shortdesc}

<ol>
<li>Verify that the load balancer failover works correctly when
    one of two or more load balancers are taken offline during an
    upgrade.</li>
<li>Uninstall the current version by running the command.
<p>`cast system uninstall`</p>
<p>This command also stops the services.</p></li>
<li>Run the InstallShield `uninstall` command.
<p>`/root/cloudant/uninstall/uninstall.bin`</p></li>
<li>Install the new Cloudant Local packages and start the upgraded
    node, [Installing load balancer nodes](clinstall_install_load_balancer_nodes.html).
<ol type=a>
<li>Find the load balancer node's current credentials,
        cluster nodes, host name, and IP addresses in the current
        version of the `/etc/haproxy/haproxy.cfg` file.
</li>
<li>Configure the values in the `lbnode.yaml` file.

<p>You can get a sample from
        `/opt/cloudant/cast/samples/lbnode.yaml` file, and run the
        following command to install and pass the configuration.</p>
<p>`cast system install -lb -c /{path_to}/lbnode.yaml`</p></li>
</ol>
</li>
<li>Verify that the load balancer is reachable through its URL and
    that all cluster nodes are listed and available to receive
    traffic by using this URL:  
<p>`http://{upgrade node load balancer}/_haproxy`</p></li>
</ol>
