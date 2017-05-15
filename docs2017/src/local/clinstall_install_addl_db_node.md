---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-08"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Installing additional database nodes

You can add a database node to your cluster after the first node
is installed.
{:shortdesc}

Run the `cast system install` command to add a database node.

``` sh
cast system install -c cluster_dbnode.yaml -db
```
{:codeblock}

## Options

Flag                  | Purpose
----------------------|--------
`-db` _or_ `--dbnode` | Flag to install a database node.
`-c` _or_ `--config`  | The cluster configuration file exported from the first node.
`--maintenance`       | Start the system in maintenance mode. 

You added a database node. Next, you must join the cluster.
