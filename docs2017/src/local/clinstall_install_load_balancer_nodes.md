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

# Installing load balancer nodes

Install and configure each load balancer node in the cluster by
following these steps.

1. Install a load balancer node by running the following command.

    ``` sh
    cast system install -lb
    ```
    {:codeblock}

## Options

Flag                  | Purpose
----------------------|--------
`-lb` _or_ `--lbnode` | Flag to install a load balancer node.


2.  Copy the load balancer node configuration file,
    `/opt/cloudant/cast/samples/lbnode.yaml`.

3.  Update the host name and IP address values for each database
    node in the cluster under the Nodes section of the
    configuration file.

4.  Replace the host name with the FQDN.

    ``` sh
    hostname: xxx.xx
    ipaddress: xxx
    ```
    {:codeblock}

5.  Change the default admin password from `pass` as shown in the
    sample.

    ``` sh
    # Sample CAST input file for configuring a load balancer in a three-node database cluster.
    
    lbnode:
    
    users: 
    haproxy_stat: pass 
    
    nodes: 
    - hostname: db1.vm 
    ipaddress: 192.168.211.101 
    
    - hostname: db2.vm 
    ipaddress: 192.168.211.102 
    
    - hostname: db3.vm 
    ipaddress: 192.168.211.103
    ```
    {:codeblock}

6.  Save the configuration file and update the node with the new
    values by running the following command.

    ``` sh
    cast node config lbnode.yaml
    ```
    {:codeblock}

    After you run the `cast node config` command, the load balancer
    node is configured. After you complete the installation of the
    database nodes and initialize the cluster, verify the
    installation by [Starting the Cloudant Local Dashboard](clinstall_start_cl_dashboard.html).
