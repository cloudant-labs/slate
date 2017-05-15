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

# Verifying node configuration

Before you install Cloudant&reg; Local on any database or load
balancer node, you must verify that all nodes in your cluster are
named and configured properly with static IP addresses. When
Cloudant is installed, it is configured to start automatically.
If your nodes are not named and configured correctly, the wrong
node names are included in the memberships for your Cloudant
cluster.
{:shortdesc}

Run the `hostname -f` command on each node in your cluster to
verify that the node is named and configured correctly. The
`hostname -f` command returns a Fully Qualified Domain Name (FQDN),
such as `db1.domain.com`. If the displayed host name is incorrect,
select from the following instructions.

<ol><li>If your operating system is Red Hat or CentOS, follow these steps.
<ol type="a">
<li>Append the following line to the <code>/etc/hosts</code> file on each node.
<p><code>node IP address<br>
hostname</code></p>

<ul type="1">
<li>Specify the external IP address for the node, <code>node IP address</code>, not the loop-back interface IP address.</li>
<li>Specify the appropriate host name, <code>hostname</code>, such as the one in the following example.
<p><code>107.170.185.247 db2.millay-centos65-cloudant-local.com</code></p></li></ul></li>

<li>Confirm that the correct host name is specified in the <code>/etc/sysconfig/network</code> file.</li>
<li>Use the <code>hostname -f</code> command to confirm that the name is correct.</li>
<li>If the host name is correct, restart the server for the new entry to take effect. If not, correct the invalid host name.</li></ol>
</li>

<li>If your operating system is Debian or Ubuntu, confirm that your DNS entries are set up correctly and follow these steps.
<ol type=a>
<li>In the <code>/etc/hosts</code> file, edit the line that starts with <code>127.0.1.1</code> and change the entry to suit your environment as in the following example.
<p><code>127.0.1.1 db1.clustername.domain.net db1</code></p></li>
<li>Edit the <code>/etc/hostname</code> file and change the content of that file to reflect the short-form host name. 
<p>Do not change the fully qualified name. For example, in the previous step, the short-form host name is <code>db1</code>.</p></li>
<li>Run the <code>sudo hostname --file /etc/hostname</code> command to update the operating system host name, based on the name that is specified in the <code>/etc/hostname</code> file.</li>
<li>Confirm that the correct host name is specified with the <code>hostname -f</code> command. 
<p>If the specified host name is incorrect, correct it and repeat the previous step. </p>
<p>** Note:** You can configure your database nodes for either local logging or remote logging to a separate syslog logging server. The default setting is local, but the local setting is recommended only in test environments. In a production environment, you must use remote logging to ensure optimum system performance. If you want to set up logging, see [Configuring logging](clinstall_configuring_logging.html).</p></li>
</ol></li></ol>

