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

# Joining nodes in a cluster

After you install and configure all the database nodes, you must
join them together to form the cluster.
{:shortdesc}

1. Log in to the first database node.

2. Run the `cast cluster add` command for each node in the cluster
   except for the database node from which you are running the
   command.

   ``` sh
   cast cluster add FQDN1 FQDN2
   ```
   {:codeblock}

   For example, if your environment includes three database
   nodes, the Fully Qualified Domain Name (FQDN) might be `db1.vm`,
   `db2.vm`, or `db3.vm`. In this case, if you are on the `db1.vm`
   node, you must add both database nodes, `db2.vm` and `db3.vm`, by
   running the following command.

   ``` sh
   cast cluster add db2.vm db3.vm
   ```
   {:codeblock}

3. Verify the status of each cluster by running the following
   command.

   ``` sh
   cast cluster status
   ```
   {:codeblock}

   Each node in the cluster shows an online or offline status. An
   offline status indicates that the node did not join the
   cluster correctly. If a node did not join the cluster
   correctly, remove the node, and repeat the installation and
   configuration steps.

4. If you need to remove a node from the cluster, run the
   following command.

   ``` sh
   cast cluster remove FQDN1 FQDN2
   ```
   {:codeblock}

   For example, this command adds `db2.vm` and `db3.vm`.

   ``` sh
   cluster remove db2.vm db3.vm
   ```
   {:codeblock}

   After you join the cluster the first time, you must initialize
   it.
