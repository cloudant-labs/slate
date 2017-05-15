---

copyright:
  years: 2015, 2017
lastupdated: "2017-03-01"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Installing Third-party Package Dependencies

Cloudant&reg; Local depends on several third-party packages. Before
you install Cloudant Local, the third-party packages must be
installed on the offline system. You can use the dry-run
installation option to bundle and transfer the dependencies to
your offline system. The dry-run installation option is supported
by the operating system package managers that Cloudant Local
uses.
{:shortdesc}

Before you begin,
you must configure access to the following external repositories
on the online system.

*   Operating system-specific package repositories (EPEL, and so on)
*   Python Package Index (PyPI) site
