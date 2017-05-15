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

# Adding a node to a cluster

Add a node to a cluster, rebalance shards, and configure a node
by using the modified configuration process. The node must be in
maintenance mode to prevent errors when it is brought into the
cluster. The load balancers must know to direct traffic to the
new node.
{:shortdesc}

## Provision the new node.

1.  Install Cloudant&reg; Local on the database node that you are
adding, as described in [Installing additional database
nodes](clinstall_install_addl_db_node.html).

2.  Run the `cast system install` command by passing the
cluster configuration from your current `dbnode.yaml` file.

3.  Put the node in maintenance mode after installation.

    ``` sh
    cast node maintenance --true
    ```
    {:codeblock}

## Confirm that the node is in maintenance mode.

1.  Run the following command to confirm that the node is in
maintenance mode.

    ``` sh
    cast node maintenance
    ```
    {:codeblock}
    
    The response shows the status of the node.
    
    ``` sh
    The node is IN maintenance mode.
    ```
    {:codeblock}

## Add the new node to the nodes database on one of the existing nodes.

1.  SSH into one of the existing database nodes.

2.  Add the new node to its nodes database.

    ``` sh
    cast cluster add {new_node_hostname}
    ```
    {:codeblock}

3.  Verify that the node was successfully added to the nodes database.

    ``` sh
    cast cluster status
    ```
    {:codeblock}

##  Update the load balancer configuration.

The load balancers must know to direct traffic to the new
node.

1.  For each load balancer, add the new node to the list of
    nodes in the `lbnode.yaml` file.

2.  Restart `haproxy` after you save the changes.

3.  Verify that your load balancer can correctly access the new node.

    >   **Note:** Configuration changes and restarts to the load balancer can affect traffic. How these changes are made depends on your setup. If you are running a failover load balancer, confirm that it is running correctly and you can access the cluster through it. Then, make the required changes, such as DNS settings, to reroute all traffic through the failover load balancer.

4.  Edit the `lbnode.yaml` file that was created during initial
    cluster installation to add the new database node.

5.  Run the `cast node` config command as seen in the example.

    ``` sh
    cast node config /opt/cloudant/cast/samples/lbnode.yaml
    ```
    {:codeblock}

<!-- reset markdown parser -->

## Create a rebalancing plan.

1.  If you are using more than one load balancer, run the
    rebalancing process from any of your load balancers.

2.  If you do not have a configuration file for the
    rebalancer.

3.  Save the newly created `rebal.ini` to the home directory
    for the user on the load balancer.

4.  Remove the line breaks from the comment lines that start
    with the number sign (`#`).

    See the format of the configuration file in the following
    example.

    ``` sh
    [cloudant]
    # System user that runs the db process
    db_user = cloudant
    # Server-wide database admin credentials. These have to be identical for every node of the cluster.
    rebal_user =
    rebal_password =
    # Default filename for rebalance plans.
    rebal_plan = rebalance_plan
    # Mapping between public and private host names for nodes. This plan is only needed if
    # the host names have a private and a public interface and the load balancer does
    # not have access to the private interface. If the private host name can be used,
    # these fields can be left blank. Otherwise, the private host name extension
    # is replaced with the public host name extension to arrive at the public host name.
    # If you are unsure, leave these empty.
    
    private_host_ext =
    public_host_ext =
    [rebal]
    # Set to true to disable prompts on failure and just continue
    batch_mode = false
    ```
    {:codeblock}

5.  Verify that the admin credentials in the configuration
    file, `rebal_user` and `rebal_password`, are correct by
    logging in to one of the database nodes with SSH by
    running the following command.

    >   **Note:** Replace `admin:password` in the command with the credentials for the database administrator.

            ``` sh
            curl http://{admin:password}@localhost:5986/_active_tasks
            ```
            {:codeblock}

    If you specify the wrong credentials, you receive an
    error message.

## Set up remote access for the rebalancer.

On the load balancer, as the root user, generate a pair of
public and private keys for SSH access to the rebalancer.

See the following example.

``` sh
> cd ~/.ssh
> ssh-keygen -t rsa
```
{:codeblock}
