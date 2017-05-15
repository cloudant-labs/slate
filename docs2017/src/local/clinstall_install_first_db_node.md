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

# Installing the first database node

Install and configure the first database node in the cluster.
{:shortdesc}

1. Run the CAST installation command to install the first
   database node of the cluster.

   ``` sh
   cast system install -p dbadmin_password -db
   ```
   {:codeblock}

## Options

Flag                  | Purpose
----------------------|--------
`-db` _or_ `--dbnode` | Flag to install a database node.
`-p` _or_ `--password` | An optional flag to specify the database admin password. If you do not provide a password, the password defaults to `pass`.

2. Run the `export` command to export configuration values to a
   file.

   ``` sh
   cast cluster export cluster_dbnode.yaml
   ```
   {:codeblock}

   >    **Note**: For each additional database node in the cluster, you must use the same configuration file. To join the nodes together into a cluster, the configuration file must be the same on each host and contain the same passwords and cookie values for each user.

3. Copy the resulting `cluster_dbnode.yaml` file to a place that is
   accessible when you install more database nodes.
