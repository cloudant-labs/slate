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

# Installing a single node

If you want to install Cloudant&reg; Local in a single-node
implementation instead of a cluster, you must install the load
balancer and database nodes to run on the same node. In most
cases, a stand-alone node is installed for development or
demonstration purposes and uses the default configuration
settings.
{:shortdesc}

>   **Note:** This implementation is not recommended for a production environment.

<!-- Reset markdown parser. -->

1.  Install a single node by running the following command.

    ``` sh
    cast system install -p dbadmin_password -lb -db
    ```
    {:codeblock}

## Options

Flag                  | Purpose
----------------------|--------
`-db` _or_ `--dbnode` | Flag to install a database node.
`-lb` _or_ `--lbnode` | Flag to install a load balancer node.
`-p` _or_ `-password` | (Optional) flag to set the database admin password. If you do not provide a password, the password defaults to `pass`. 
    
2.  Run the following command to initialize the single node cluster.

    ``` sh
    cast cluster init
    ```
    {:codeblock}
