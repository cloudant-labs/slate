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

# Verifying the new node


Confirm that the new node is set up correctly.

1.  Log in to the new node with SSH and run `Weatherreport`.

    ``` sh
    /opt/cloudant/bin/weatherreport
    ```
    {:codeblock}

2.  If errors are reported during the run, see the
    [information](clinstall_checking_health_cluster_with_weatherreport.html) for
    `Weatherreport` checks, or call support.

3.  After the run finishes, check the rebalancing logs that are
    described in the [Run rebalancing](clinstall_add_node-run_rebalance_plan.html) step for any errors.

4.  Verify whether the shards for different databases are now
    distributed across the recently added node. The following
    command checks the shard map for a database.

    ``` sh
    curl -X GET http://localhost:5986/dbs/default%2Fdatabase_name | python -m json.tool | less
    ```
    {:codeblock}

    Look at the `by_node` key in the output from this command to
    determine whether the shards are spread evenly across the
    cluster nodes.

    >   **Note:** `Weatherreport` is a command-line application that provides information about the status of a dbcore node or cluster. `Weatherreport` is useful in troubleshooting cluster issues, such as increased latencies, low disk space, or node failures. For more information about `Weatherreport`, see [Monitor cluster health with `Weatherreport`](clinstall_checking_health_cluster_with_weatherreport.html).
