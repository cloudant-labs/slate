---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-13"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Replacing a database node


You can rebuild or replace a database node by using the following
instructions.


<ol>
<li>Run the following `safe_to_rebuild` command on the node to
    determine whether you can decommission the node: /opt/cloudant/bin/weatherreport safe_to_rebuild.

<ol type=a>
<li>If you can rebuild or replace the node, no diagnostic messages are displayed in response to this command.
</li>
<li>If it is not safe, one or more shard ranges are reduced to one or zero live copies. 
<p>In that case, an error message (for one live copy) or a critical message (for zero live copies) is displayed with the shard ranges affected.</p>
</li>
<li>If any messages are returned, make sure that the shards
    have enough copies in live nodes before you replace the
    node.
<p>**Note:** `Weatherreport` is a command-line application that provides information about the status of a Cloudant node or cluster. It is useful in troubleshooting cluster issues, such as increased latencies, low disk space, or node failures. For more information about `Weatherreport`, see [Monitor cluster health with Weatherreport](clinstall_checking_health_cluster_with_weatherreport.html).</p>
</li>
</ol>
</li>
<li>If the node is running, stop any services that are running on
    the node and shut it down.</li>
<li>Repair or replace the node.</li>
<li>Install Cloudant Local on the database node, as described in
    [Installing additional database nodes](clinstall_install_addl_db_node.html).</li>
<li>Run `cast system install`.

<ol type=a>
<li>Pass the `--maintenance` flag and the original `cluster_dbnode.yaml` file that was used to set up the node initially.
<p>`cast system install --maintenance -db -c cluster_dbnode.yaml`</p>
</li>
<li>(Optional) If you do not have the original `cluster_dbnode.yaml` file, you can generate a new one by running the `cast cluster export` command from an existing node.
<p>`cast cluster export cluster_dbnode.yaml`</p></li>
</ol>
</li>
<li>Confirm that the node is in maintenance mode by using the
    following command.
<p>`cast node maintenance`</p>
</li>
<li>If the node is in maintenance mode, the response shows the
    status of the nodes.
<p>`The node is IN maintenance mode.`</p></li>
<li>In maintenance mode, the node starts the process to bring
    itself back into a working state and ready for traffic.
<ol type=a>
<li>Monitor the process by checking the node's log files to
    determine how many `pending_changes` wait for the internal
    replication and indexing processes.
    <p>See the following example.</p>
<p>`<0.3333.0> - mem3_sync shards/00000000-3fffffff/dbname.1407441053 cloudant@db1.cluster001.cloudant.net {pending_changes,62}`</p>
</li>
<li>Check the number of pending internal replication tasks by running the following command in a terminal window on one of the database nodes.
<p>`/opt/cloudant/bin/weatherreport -a -d info internal_replication`</p>
    ```
<p>If the internal replication is complete, the output from this command indicates that the number of pending internal replication jobs is 0 or close to 0 for the database node. Additionally, the active tasks section of the Metrics application shows the number of indexing processes.</p>
</li>
</ol>
</li>
<li>After the node reaches the point where only a few indexing
    tasks are running, take the node out of maintenance mode and
    put it in production mode.</li>
</ol>

