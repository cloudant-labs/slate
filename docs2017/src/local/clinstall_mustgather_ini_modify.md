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

# Modifying the `mustgather.ini` file

The `mustgather.ini` file is configured when you run the MustGather
tool. However, if you need to, you can update certain information
in the `mustgather.ini` file after you run the MustGather tool.

The following example of the `mustgather.ini` file is in the
`/opt/cloudant/etc` directory.

```
# Properties file
#
# Enter a comma-separated list of the cluster nodes in the NODES field.
#
# This example shows how to specify a cluster that includes three databases and one load balancer node.
#
# NODES: lb.your_locale.your_company.com,
#   db1.your_locale.your_company.com,
#   db2.your_locale.your_company.com,
#   db3.your_locale.your_company.com

[cluster]
nodes:
os_messages: /var/log/messages*
haproxy_cfg: /etc/haproxy/haproxy.cfg
haproxy_logs: /var/log/haproxy*
nginx_cfg: /etc/nginx/nginx.conf
nginx_dashboard_cfg: /etc/nginx/conf.d/cloudant-dashboard.conf
nginx_logs: /var/log/nginx*
cloudant_properties_cfg: /opt/cloudant/etc
cloudant_version: /root/cloudant/version.txt
cloudant_logs: /var/log/cloudant
```
{:codeblock}

>   **Note:**  To collect log files from different nodes, port 22 must be open.
