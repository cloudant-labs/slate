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

# Initializing the cluster

During a new installation and after all the database nodes are
joined to the cluster, you must initialize the cluster.
{:shortdesc}

1. Run the following command from one of the database nodes to
   initialize the cluster.

   ``` sh
   cast cluster init
   ```
   {:codeblock}

2. Install a load balancer.
