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

# Configuring local system logs

In addition to the Cloudant&reg; Local database node and load
balancer node logs, you must enable and capture local system
logs.
{:shortdesc}

After you enable these logs, you can see security audit and
system level information. Logs are enabled on your OS platform by
default. If the logs are not enabled on your OS platform by
default, refer to platform-specific information for details about
configuring them.

Enable logs on your OS platform by referring to platform-specific
information for details about configuring them.

Debian and Ubuntu use the following logs.

*   `/var/log/auth.log`
*   `/var/log/syslog`

Red Hat-derived Linux distributions use the following logs.

*   `/var/log/secure`
*   `/var/log/messages`
