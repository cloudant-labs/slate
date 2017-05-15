---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-10"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Configuring the remote logging server to use `rsyslog`


Before you configure remote logging, you must set up the remote
logging server and verify that it is operational. The remote
logging server can be a separate enterprise log server that is
used by operations for centralized logging.
{:shortdesc}

Alternatively, you might choose to use the Cloudant&reg; load
balancer server as the remote log server to centralize the logs
from all the nodes. Confirm or enable a remote logging server by
following these steps.

<ol>
<li>Check whether the `syslog` daemon is running on the `syslog` server.
<p>`[root@lb1 tmp]# ps -ef | grep syslog`<br>
`root      6306     1  0 11:15 ?        00:00:00 /sbin/rsyslogd -i /var/run/syslogd.pid -c 5`<br> 
<br>
`[root@lb1 tmp]# service rsyslog status`<br>
`rsyslogd (pid  6306) is running...`</p>
<p>If the service is not running, start `rsyslog`.<br>
`service rsyslog start`</p>
<ol type="a">
<li>If `rsyslog` is not already installed, install it on the remote log server.
<ul><li>To install `rsyslog` on Debian or Ubuntu, use `apt-get`.</li>
<li>To install `rsyslog` on Red Hat-derived Linux&trade; distributions only, use `yum`.</li>
</ul>
<li>Start `rsyslog`.</li>
</ol>
<li>Check the configuration in `/etc/rsyslog.conf`.</li>
<li>Ensure that the `ModLoad` and `UDPServerRun` entries are not
    commented out.
<p>`# Provides UDP syslog reception`<br>
`$ModLoad imudp`<br>
`$UDPServerRun 514`</p></li>
<li>Create a file `cloudant.conf` in the `/etc/rsyslog.d` directory and add the following lines.
<p>`local2.*   /var/log/cloudant/cloudant.log`<br>
`local3.*   /var/log/cloudant/metrics.log`<br>
`local5.*   /var/log/cloudant/clouseau.log`</p>
<p>This configuration ensures that `rsyslog` receives the log messages according to the different facility configurations.</p>
<p>**Note:** A sample of the cloudant.conf file is available in `/etc/rsyslog.d` on any of the database nodes.</p></li>
<li>For the HAproxy, create a file `haproxy.conf` in the `/etc/rsyslog.d` directory.
<p>The file must contain the following line.<br>
`local4.* /var/log/haproxy.log`</p>
<p>This configuration ensures that `rsyslog` receives the log messages according to the different facility configurations.</p>
<p>**Note:** A sample of the `haproxy.conf` file is available in `/etc/rsyslog.d` on the load balancer nodes.</p></li>
<li>Restart `syslog` with the following command.<br>
`service rsyslog restart`</li>
<li>Check that the `syslog` daemon is running, as described in step 1.</li>
</ol>

