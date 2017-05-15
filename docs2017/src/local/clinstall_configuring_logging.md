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

# Configuring logging

Use these instructions to configure logging for your Cloudant&reg;
Local installation.
{:shortdesc}

## Overview

Several components within a Cloudant Local installation generate
log files. These log files are valuable for monitoring
performance, troubleshooting, and other administrative tasks. In
particular, the database node and load balancer components of
your Cloudant Local cluster generate log information.

By default, a Cloudant Local installation configures local
logging for these components. The effect is that all the log
information is stored on the same system as the active component.

For database nodes, the default of local logging is suitable only
for test or non-production environments.

>   **Note:** For a production environment, you must configure the database node for remote logging.

Remote logging helps ensure optimum system performance because
local logging adversely affects performance. Remote logging also
makes it easier to combine logs from all database nodes.

For the load balancer node, you can keep the default value: local
logging. For heavy load, or to log to a separate logging server,
the load balancer logs can be configured for remote logging.

As an option for managing the logs of your Cloudant Local
cluster, you might choose to use the load balancer node as the
central logging server for your cluster. In other words, all the
database nodes can be configured to use the load balancer server
as the remote logging server. The load balancer itself continues
to use the default local logging configuration. This option has
the advantage that all the key logs from the cluster nodes are
available on the load balancer server.

## Summary of logs and locations

### Database nodes

<table>
<thead>
<tr>
<th>Log type</th>
<th>Purpose</th>
<th>Configuration file</th>
<th>Local logging default log file location</th>
<th>Remote logging default <code>rsyslog</code>
<code>facility</code></th>
</tr>
</thead>
<tbody>
<tr>
<td>Cloudant database core logs</td>
<td>Contains data about events such as runtime errors, warnings, or crashes that were encountered
by the Cloudant database core.</td>
<td><code>/opt/cloudant/etc/local.ini</code></td>
<td><code>/var/log/cloudant/cloudant.log</code><p><code>/var/log/cloudant/cloudant-crash.log</code></p></td>
<td><code>local2.*</code><p><code>/var/log/cloudant/cloudant.log</code></p></td>
</tr>
<tr>
<td>Clouseau Search Service log</td>
<td>Contains information after the search indexes are built and committed. Also includes service
start or stop status, and any errors encountered.</td>
<td><code>/opt/cloudant/etc/log4j.properties</code></td>
<td><code>/var/log/cloudant/clouseau.log</code><p>Uses <code>rsyslog</code>
<code>facility</code>
<code>local5</code> for local logging.</p></td>
<td><code>local5.*</code><p><code>/var/log/cloudant/clouseau.log</code></p></td>
</tr>
<tr>
<td>Metrics Service log</td>
<td>Contains information about service start and stop status, and any errors in the Cloudant Metrics data gathering service.</td>
<td><code>/opt/cloudant/etc/metrics.ini</code></td>
<td><code>/var/log/cloudant/metrics.log</code><p>Uses <code>rsyslog</code>
<code>facility</code>
<code>local3</code> for local logging.</p></td>
<td><code>local3.*</code><p><code>/var/log/cloudant/metrics.log</code></p></td>
</tr>
<tr>
<td>Apache CouchDB Service log</td>
<td>Contains information about service start or stop status, and any errors in the Cloudant Apache CouchDB.</td>
<td><code>/opt/cloudant/etc/local.ini</code></td>
<td><code>/var/log/cloudant/cloudant-svlogd/current</code></td>
<td>None.</td>
</tr>
</tbody>
</table>

### Load balancer node

<table>
<thead>
<tr>
<th>Log type</th>
<th>Purpose</th>
<th>Configuration file</th>
<th>Local logging default log file location</th>
<th>Remote logging default <code>rsyslog</code>
<code>facility</code></th>
</tr>
</thead>
<tbody>
<tr>
<td>HAProxy logs</td>
<td>Contains information about service start or stop status, and runtime errors. Can be extended
to record access and other request information.</td>
<td><code>/etc/haproxy/haproxy.cfg</code></td>
<td>
<p><code>/var/log/haproxy.log</code></p>
<note>Uses <code>rsyslog</code>
<code>facility</code>
<code>local4</code> for local logging.</note>
</td>
<td><code>local4.*</code><p><code>/var/log/haproxy.log</code></p></td>
</tr>
<tr>
<td>NGINX logs</td>
<td>Contains information about service start or stop status, any errors, and access
details.</td>
<td><code>/etc/nginx/nginx.conf</code></td>
<td><code>/var/log/nginx/access.log</code><p><code>/var/log/nginx/error.log</code></p></td>
<td>None.</td>
</tr>
</tbody>
</table>

### All nodes

<table>
<thead>
<tr>
<th>Log type </th>
<th>Purpose</th>
<th>Local logging default log file location</th>
<th>Remote logging default <code>rsyslog</code>
<code>facility</code></th>
</tr>
</thead>
<tbody>
<tr>
<td>System logs</td>
<td>General system and security logs on the server.</td>
<td>On Debian and Ubuntu<p><code>/var/log/auth.log</code></p>
<p><code>/var/log/syslog</code></p> On Red Hat-derived <tm trademark="Linux" tmtype="tm"
>Linux</tm> distributions only
<p><code>/var/log/secure</code></p><p><code>/var/log/messages</code></p></td>
<td>None.</td>
</tr>
</tbody>
</table>
