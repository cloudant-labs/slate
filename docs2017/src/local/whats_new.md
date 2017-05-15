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

# What's New in Cloudant Data Layer Local Edition

Read about the new features in Cloudant&reg; Data Layer Local Edition
release version 1.1.0.
{:shortdesc}

## Eliminate plain text passwords

Since intercepting plain text passwords and gaining access to
your system is simple, you can no longer use plain text passwords
with Cloudant Local.

## Self-extracting archive installer

When you use the self-extracting archive, it is no longer necessary to
unpack archive files.

## Python wheels

Python wheels reduce, or even eliminate, the need for you to
download dependencies and can decrease incompatibilities.

## CouchDB 2.0 compatible

Cloudant Local is now compatible with CouchDB 2.0.

## Python virtual environments

Each Python application now runs within its own virtual environment,
eliminating version incompatibility between each application's Python modules.

## Database logging

Simplified the following database logging issues.

Database logging no longer requires a separate configuration
file, but can be configured by using `.ini` files.

By default, the database uses syslog to log to
`/var/log/cloudant/cloudant.log`, but you can direct it to other
hosts by setting `syslog_host = your_host` in the `[log]` section of
the `local.ini`.

Additionally, the `cloudant.log`, `clouseau.log`, and `metrics.log`
files, located in `/var/log/cloudant/`, are automatically rotated
using the configuration at `/etc/logrotate.d/cloudant`.

## Multiple bug fixes

Implemented additional bug fixes to improve performance and
correct other issues.

## Rolling upgrade not supported

Cloudant Local does not support rolling upgrades.
