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

# Installing Cloudant Local offline

Install Cloudant&reg; Local offline by following these instructions.
{:shortdesc}

An online system has internet access and full access to the package
repositories, while an offline system has no access to the internet.
You must download the third-party dependencies, bundle them into a `tar`
file, and transfer them to the offline system for installation.

## Prerequisites

Before you install Cloudant Local offline, you must meet the
following prerequisites.

1.  You must be a root user or have sudo privileges.

2.  You must run a download-only or dry-run installation.  
    You run a dry-run installation from a system that has internet
    access and runs the same version of the operating system as the
    target system. The new system is called the online system.
