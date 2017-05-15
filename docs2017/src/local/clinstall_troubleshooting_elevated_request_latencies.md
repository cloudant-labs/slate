---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-09"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Elevated request latencies

Latencies on any cluster vary in response to various internal and
external factors. In this context, "elevated" means "elevated
beyond an acceptable tolerance." The level of latencies that is
acceptable to you depends on your application. Elevated latencies
are difficult to debug. While a predefined solution is
impossible, the following paragraphs offer some guidance.
{:shortdesc}

## Is there a wider context?

The increased latency might be related to ongoing work. Determine
whether any other operations' work is ongoing and be aware of the
following issues.

*   Cluster expansions or contractions
*   Node replacements
*   Planned maintenance

## Did anything change?

It is unusual for latencies to increase of their own accord. The
following examples show changes that can affect request latency.

### Workload

Determine whether a correlation exists between request
volume and latency. Request volume alone does not give a
clear picture of the workload. It is worth breaking down
the traffic by HTTP request type and request size when
you are looking for changes. You can derive this
information from the logs that are generated for each
node. Also, look for changes in the number of
`active_tasks` ongoing on the cluster. For example, a
correlating increase in `changes_pending` for an indexer
job might indicate that a new design document was
uploaded and the cluster is undertaking an extra
indexing workload. You can find information about
indexing tasks in the logs and through the
`/_active_tasks` endpoint. If the workload profile
changed, you might be able to manage the increased
latency by using IOQ priorities.

### Cluster configuration

Determine whether any changes were made recently to the
cluster configuration. You can get a list of recent
configuration changes for a cluster from the logs. If
any changes were made that correlate with increased
latency, determine the context in which those changes
were made to determine whether they can be reverted.

### Hardware failure

This problem might be the result of the full or partial
failure of servers, disks, networking components, or
related failures. When you diagnose the problem, watch
for the following changes.

*   Disk errors on cluster nodes
*   Changes in disk operation times
*   Unexpected volumes on one or more cluster nodes
*   Recently unavailable cluster nodes

## Are elevated latencies isolated to a particular account, database, or request type?

Check whether the elevated latencies are isolated to a particular
account, database, or request type.

*   Logs show that most requests go to one or a few databases
*   Have the same request type (such as the same HTTP method)
*   Have the same backend name

### Latencies for a specific database

If latencies are only elevated for a specific database,
confirm whether a corresponding change in the traffic
profile for that database exists.

Check that the database is evenly balanced across the
cluster by inspecting the shard map.

``` sh
ssh db1.cluster001.cloudant.com curl \
    -X GET http://localhost:5986/dbs/backend_name%2Fdatabase_name | python -m json.tool | less
```
{:codeblock}

Look at the `by_node` key and determine whether the shards
are spread evenly across the cluster. If the shards are
not evenly distributed, rebalancing the shards might
improve the situation. For more information, see the
documentation about rebalancing a cluster.

### Latencies for view requests

If latencies are elevated only for a specific view (or
view group/design_doc), check whether the affected
requests are using `stale=ok`. If they are using `stale=ok`,
check the distribution of ushards for that view by
running the following command in remsh.
 
``` sh
> mem3:ushards("db_name").
```
{:codeblock}

If the ushards are not evenly distributed (meaning every
node has the same number of ushards), you can change the
order of the nodes for each range under `by_range`.

If they are not using `stale=ok`, check for ongoing view
builds for the related design documents. If index builds
are ongoing, which might be a result of a new design
document version or a large volume of data ingress,
increased latency for `stale=false` queries is expected.
You might be able to speed up the index builds by
increasing the IOQ priority or setting an IOQ bypass.
However, this approach can cause other changes in
cluster performance, so proceed carefully. For example,
change one thing at a time and monitor the situation
closely.

To change IOQ priority for views, do the following steps
in a remsh.

``` sh
> rpc:multicall(config, set, ["ioq", "views", "1", "Speed up index builds"]).
```
{:codeblock}

Set an IOQ bypass.

``` sh
> rpc:multicall(config, set, ["ioq.bypass", "view_update", "true", "Speed up index builds"]).
```
{:codeblock}

## Are the elevated latencies converging on a specific value?

If the request times for affected requests are converging around
specific values, an internal timeout might be triggering. Typical
timeout values are 5000ms, 60000ms, and 3600000ms, though check
`/opt/cloudant/etc/local.ini` to see whether any custom timeout
values are set.

If a timeout is triggering, that might help you determine which
part of the system is slowing down the requests. If you can
determine that one node is responsible for the timeouts, put that
node into maintenance mode to see whether performance improves.
However, first do the appropriate checks to determine whether
maintenance mode is safe.

Set maintenance mode in remsh.

``` sh
> config:set("cloudant", "maintenance_mode", "true").
```
{:codeblock}

## Do any recorded metrics correlate with latency increases?

Increased IOQ latencies (check the metrics application) often
correlate with increased HTTP request latencies. However, this
metric alone is not enough to determine whether requests are IOQ
bound or IO bound.

### IOQ latency

If `disk.sdb.disk_time` is not elevated, the request might
be genuinely IOQ bound, in which case you might achieve
some gains by tuning IOQ. Consider increasing
IOQ/concurrency.

``` sh
> rpc:multicall(config, set, ["ioq", "concurrency", "50", "Attempt to reduce IOQ latency"]).
```
{:codeblock}

Also, consider doing the following steps.

Increase IOQ priority for a particular request class.

``` sh
> rpc:multicall(config, set, ["ioq", "writes", "1", "Attempt to reduce IOQ latency"]).
```
{:codeblock}

Decrease IOQ priority for a competing request class, but
first verify in metrics whether another class of request
is competing.

``` sh
> rpc:multicall(config, set, ["ioq", "views", "0.1", "Attempt to reduce IOQ latency"]).
```
{:codeblock}

Set an IOQ bypass for a particular request class.

``` sh
> rpc:multicall(config, set, \
    ["ioq.bypass", "interactive", "true", "Attempt to reduce IOQ latency"]).
```
{:codeblock}

### Load average and the Erlang run queue

These metrics are analogous. Load average is the number
of processes in a runnable state that is waiting to run
or display by top or uptime. Erlang run queue length is
the number of processes in the Erlang VM in a runnable
state (available in the Metrics application).

If correlating increases exist here, the system might be
overloaded. Check whether the metrics are elevated
across the cluster or whether the problem is limited to
one node. If the problem is local to a subset of nodes,
investigate those nodes and check the shard distribution
on the cluster.

If load average is growing, but the Erlang run queue is
not, check the affected nodes for other processes. The
JVM or the `collectd` process might be using too many
resources, leading to poor performance of the Erlang VM.
If no obvious signs of a specific problem exist, the
cluster is balanced and the increases are not limited to
a single node, the cluster might be overloaded. Verify
that a correlating increase in requests exists and
consider adding more nodes to the cluster.
