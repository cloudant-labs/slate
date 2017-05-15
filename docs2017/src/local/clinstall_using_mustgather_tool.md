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

# Cloudant MustGather tool

The MustGather tool is a lightweight diagnostic tool that
collects system data, including Cloudant&reg; cluster data, logs, and
other data you can use for diagnosing issues. With the MustGather
Tool, you consolidate your collected system data into a
compressed file to send to IBM&reg; Support.
{:shortdesc}

The MustGather tool creates a snapshot of the local Cloudant
clusters that can be used to diagnose issues more quickly. The
MustGather tool is available on all database and load balancer
nodes. You can run the tool from any node. You specify the nodes
within the cluster in the `mustgather.ini` file. The MustGather
tool collects the relevant files from different nodes and
consolidates them into one compressed file that you send to IBM
Support to help them diagnose issues with Cloudant Local.
