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

# Monitor cluster health with Weatherreport

Use these instructions to use the Weatherreport utility to check
the health of your Cloudant&reg; cluster. Weatherreport is a
command-line application that provides information about the
status of a dbcore node or cluster. It is useful in
troubleshooting cluster issues, such as increased latencies, low
disk space, or node failures.
{:shortdesc}

## Running Weatherreport

Run the Weatherreport utility to check your cluster health. By
default, Weatherreport carries out checks for the local node. If
you run it with the `--all-nodes` option, the whole cluster is
checked.

1. As `root` or `cloudant` user, update that user profile file
   with the following PATH or set the PATH in your current SSH
   session by running the following command.

    ```sh
    export PATH=$PATH:/opt/cloudant/bin
    ```
    {:codeblock}

2. SSH into a dbcore node and use this command to run
   Weatherreport.

    ```sh
    /opt/cloudant/bin/weatherreport
    ```
    {:codeblock}

## Weatherreport checks

The Weatherreport utility reviews your cluster based on the
checks you specify when you run it.

```sh
$ /opt/cloudant/bin/weatherreport --list

Weatherreport check list

custodian            Shard safety/liveness checks
disk                 Data directory permissions and atime
internal_replication Check the number of pending internal replication jobs
ioq                  Check the total number of active IOQ requests
mem3_sync            Check there is a registered mem3_sync process
membership           Cluster membership validity
memory_use           Measure memory usage
message_queues       Check for processes with large mailboxes
node_stats           Check useful erlang statistics for diagnostics
nodes_connected      Cluster node liveness
process_calls        Check for large numbers of processes with the same current/initial call
process_memory       Check for processes with large mailboxes
safe_to_rebuild      Check whether the node can safely be taken out of service
search               Check the local search node is responsive
tcp_queues           Measure the length of tcp queues in the kernel			
```
{:codeblock}

To run one check, you can run Weatherreport with the name of the
check as the first parameter. For instance, you can check for
memory use issues on all nodes.

```sh 
$ /opt/cloudant/bin/weatherreport --all-nodes memory_use
```
{:codeblock}

A list of the command-line options and their meanings is
available by using this command.

``` sh 
$ /opt/cloudant/bin/weatherreport --help
```
{:codeblock}

## `memory_use`

### What it checks

You can check the amount of free RAM on a dbcore node
with `memory_use`.

### What an error for this check means

A node is running out of RAM. The `oom` might stop dbcore
soon, which can cause externally visible errors.

### How to fix it

It is worth attending to this problem quickly. You can
check the memory graphs in the metrics application to
see how urgent it is and whether memory use is
increasing quickly or slowly.

### Fast increase

If it is a sharp increase, a process might be getting a
long message queue backup. That probably means you can
stop the process. However, before you do that, use
`process_info` to find out more about the process. To find
processes that are using too much memory within dbcore,
log in to the node and start a `remsh` session. Find the
processes that are using the most memory.

```sh 
# Size is in bytes
(dbcore@db6.bigpark002.cloudant.net)1> recon:proc_count(memory, 10).
[{<0.101.0>,16365344,
  [lager_event,
   {current_function,{gen_event,fetch_msg,5}},
   {initial_call,{proc_lib,init_p,5}}]},
 {<0.267.0>,13090216,
  [rexi_server,
   {current_function,{gen_server,loop,6}},
   {initial_call,{proc_lib,init_p,5}}]},
 {<0.14538.4675>,9210944,
  [{current_function,{gen,do_call,4}},
   {initial_call,{erlang,apply,2}}]},
 {<0.25.0>,2917752,
  [file_server_2,
   {current_function,{gen_server,loop,6}},
   {initial_call,{proc_lib,init_p,5}}]},
....
```
{:codeblock}

The second parameter to `proc_count` is the number of
processes to show, in this case 10. So here <0.101.0> is
using 16 MB of memory, which is typically nothing to
worry about. It is possible for individual processes to
use several gigabytes of memory. As a rule, if the top
few processes are using more memory than others, it is
worth looking into whether you can stop those processes.

Use `process_info` to find out what process is running.

``` sh 
(dbcore@db1.slqs002.cloudant.net)3> process_info(pid(0,9900,0), [current_function,message_queue_len,initial_call]).
[{current_function,{couch_key_tree,merge_at,3}}, {message_queue_len,2270}, {initial_call,{proc_lib,init_p,5}}]
```
{:codeblock}

Now, use your judgment or contact support to see whether
it is safe to stop the process.

### Slower increase

It might be that "garbage" is building up. Check the
different types of memory for the node.

``` sh 
> recon:node_stats_print(1,1). 
{[{process_count,1362},
  {run_queue,0},
  {error_logger_queue_len,0},
  {memory_total,168628304},
  {memory_procs,83944688},
  {memory_atoms,486930},
  {memory_bin,19389792},
  {memory_ets,4410896}],
 [{bytes_in,76984},
  {bytes_out,275},
  {gc_count,25},
  {gc_words_reclaimed,17015},
  {reductions,11983462}]}
ok
```
{:codeblock}

Run a garbage collection from a remsh on the node.

``` sh 
[erlang:garbage_collect(Pid) || Pid <- processes()]
```
{:codeblock}

If that does not change the situation, check whether the
lines in the provided memory information add up to the
memory the OS is reporting for beam.smp by using top on
the node. If a significant discrepancy exists, the node
is probably leaking memory, and if the server is close
to running out, restart cloudant with this command.

``` sh
sv restart cloudant
```
{:codeblock}

## `message_queues`

The `message_queues` checks monitor the message queues for various
processes as you can see in the following list.

*  `couch_db_updater`
*  `couch_file`
*  `couch_server`
*  `custodian`
*  `ddoc_cache_opener`
*  `disk`
*  `global_changes_server`
*  `ioq`
*  `mem3_shards`
*  `rexi_server`
*  `search`

### `couch_db_updater`

#### What it checks

This check monitors the message queues of the various
`couch_db_updater` processes. These processes manage
access to a logical database; one `couch_db_updater`
process exists for each open database shard and one for
each open view shard. In general, `couch_db_updater`
processes do not exhibit the same pathological failure
modes that `couch_file` processes do. Regardless, a
failing or backed up `couch_db_updater` process is likely
to cause externally visible problems and must be acted
upon.

#### How to confirm the failure

SSH to the node where the failure occurred and create
the following function in a remsh.

``` sh 
FindTiredPids = fun(Mod, N) ->
    {monitors, M} = process_info(whereis(couch_stats_process_tracker), monitors),
    Candidates = [Pid || {process, Pid} <- M],
    lists:foldl(
        fun(Pid, Acc) ->
            case process_info(Pid, [message_queue_len, dictionary]) of
                undefined -> PI = [];
                PI -> ok
            end,
            case proplists:get_value('$initial_call', proplists:get_value(dictionary, PI, [])) of
                {Mod, init, 1} ->
                    case proplists:get_value(message_queue_len, PI) of
                        Len when Len > N -> [Pid|Acc];
                        _ -> Acc
                    end;
                _  ->
                    Acc
            end
        end,
        [],
        Candidates
    )
end.
```
{:codeblock}

Next, get a list of PIDs.

``` sh 
> Pids = FindTiredPids(couch_db_updater, 1000).
[<0.31017.4673>,<0.28837.3289>]
```
{:codeblock}

This command returns a list of PIDs with long > 1000
message queues.

#### How to remediate the failure

It is worthwhile to be patient in remediating this type
of failure because it is possible for the processes to
recover on their own. If you observe a process with a
message queue that is spiraling out of control (for
example, the mailbox has more than 100,000 messages),
stop the process immediately. If not, wait a few minutes
and see whether the system recovers.

If the process does not recover on its own, run this
remsh command to stop all backed-up CouchDB updaters.

``` sh 
> [exit(Pid, kill) || Pid <- Pids].
[true,true]
```
{:codeblock}

#### How to verify the remediation

Confirm that the list of backed up CouchDB updaters is
empty.

``` sh 
> FindTiredPids(couch_db_updater, 1000).
[]
```
{:codeblock}

### `couch_file`

#### What it checks

This check monitors the message queues of the various
couch_file processes. These processes manage access to
the underlying file system. One `couch_file` process
exists for each open database shard and one for each
open view shard.

Under heavy load, a `couch_file` process might be unable
to process messages as fast as it receives them. When
this problem occurs, you must stop the process because
the process might not recover.

#### How to confirm the failure

SSH to the node where the failure occurred and create
the following function in a remsh.

``` sh
FindTiredPids = fun(Mod, N) ->
    {monitors, M} = process_info(whereis(couch_stats_process_tracker), monitors),
    Candidates = [Pid || {process, Pid} <- M],
    lists:foldl(
        fun(Pid, Acc) ->
            case process_info(Pid, [message_queue_len, dictionary]) of
                undefined -> PI = [];
                PI -> ok
            end,
            case proplists:get_value('$initial_call', proplists:get_value(dictionary, PI, [])) of
                {Mod, init, 1} ->
                    case proplists:get_value(message_queue_len, PI) of
                        Len when Len > N -> [Pid|Acc];
                        _ -> Acc
                    end;
                _  ->
                    Acc
            end
        end,
        [],
        Candidates
    )
end.

```            
{:codeblock}

Next, get a list of PIDs with long > 1000 message
queues.

``` sh
> Pids = FindTiredPids(couch_file, 1000).
[<0.31017.4673>,<0.28837.3289>]
```
{:codeblock}

#### How to remediate the failure

In remsh, run this command to stop all processes in the
list.

``` sh
> [exit(Pid, kill) || Pid <- Pids].
[true,true]
```
{:codeblock}

#### How to verify the remediation

Use the same remsh function that you used to identify
the tired processes. This command returns an empty list.

``` sh
> FindTiredPids(couch_file, 1000).
[]
```
{:codeblock}

#### When to escalate the page

If you are paged multiple times for a cluster, that is,
the issue is recurring, escalate the page.

### `couch_server`

#### What it checks

This function checks whether the `couch_server` message
queues are growing larger, which indicates that they are
backing up.

#### What it means when it fails

The `couch_server` is on the critical path for many RPC
calls. The overall effect of a backed up `couch_server` is
dramatically increased latency on a subset of requests.
For example, requests that are on a critical path.

#### How to fix it

First, use the metrics application and check whether the
incident is ongoing or a spike. If it is a spike that is
subsiding, no further action is required. If it is not
decreasing, restart `couch_server` with this command.

``` sh
exit(whereis(couch_server), kill). src
```
{:codeblock}

### `ddoc_cache_opener`

#### What it checks

The `ddoc_cache_opener` message queue is backing up. Use
this command from a remsh to monitor the queue directly.

``` sh
process_info(whereis(ddoc_cache_opener), message_queue_len).
```
{:codeblock}

#### What it means when it fails

If it continues to back up, the server might not be able
to process HTTP requests.

#### How to fix it

If the message_queue size is not recovering on its own,
restart the ddoc_cache_opener process.

``` sh
exit(whereis(ddoc_cache_opener), kill).
```
{:codeblock}

If this approach does not resolve the problem, contact
support.

### `global_changes_server`

#### What it checks

This command check monitors the number of messages in
the `global_changes_server` message queue.

#### How to fix it

Check the logs for entries that mention
`erlang.message_queues.global_changes_server`. If the
total does not drop to zero, an ongoing problem exists.
If the number of messages is decreasing, but peaking
often, more action might be needed.

It is possible to reduce the pressure on the
`global_changes` server by increasing the
`global_changes/max_event_delay` and
`global_changes/max_write_delay` parameters. The default
value is 500ms, although values as high as 10000ms might
be useful.

In a remsh, run the following commands to increase the
intervals (in this case to 5000ms).

``` sh 
> rpc:multicall(config, set, ["global_changes", "max_event_delay", "5000",
    "Alleviate global_changes_server message queue pain"]).
```
{:codeblock}

It is also possible that the global_changes_server
message queue is a side effect of another issue. Watch
for the values in the logs to return to zero. If the
message queue size is not decreasing, contact support.

### `mem3_shards`

#### What it checks

The length of the `mem3_shards` message queue. The
`mem3_shards` process acts as a cache of the `/dbs`
database.

#### What it means when it fails

As it is a cache, the node probably still functions
correctly, although more slowly, as it reads from the
disk more often.

#### How to fix it

You can watch the increase on the node by using the
following process.

``` sh
> process_info(whereis(mem3_shards), message_queue_len)
```
{:codeblock}

This process shows a speedy increase in the message
queue length, such as 1000 per second.

First, put the node into maintenance_mode with this
command.

``` sh
> config:set("cloudant", "maintenance_mode", "true")
```
{:codeblock}

Next, see whether the message queue length decreases. If
it does decrease, wait for it to go to zero and bring
the node back up with this command.

``` sh
> config:set("cloudant", "maintenance_mode", "false")
```
{:codeblock}

Now, check whether the queue starts increasing or stays
at zero. If it starts to increase again, the final fix
is to stop the process.

``` sh
exit(whereis(mem3_shards), kill).
```
{:codeblock}

If it is still increasing, call support.

### `rexi_server`

#### What it checks

This check monitors the number of messages in the
various `rexi_server` message queues. Depending on cluster
configuration, this process might be a single Erlang
process, or a set of processes, one for each node in the
cluster.

These processes manage all inter-node communication. If
inter-node communication is not processing their
mailboxes correctly, communication is delayed.

#### How to confirm the failure

SSH to the node where the failure occurred and create
the following function in a remsh.

``` sh
ShowRexiServerMailboxes = fun() ->
    Names = case config:get("rexi", "server_per_node") of
        "true" ->
            [element(1, C) || C <- supervisor:which_children(rexi_server_sup)];
        _ ->
            [rexi_server]
    end,
    Mailboxes = lists:map(
        fun(Name) ->
            Pid = whereis(Name),
            {message_queue_len, Len} = process_info(Pid, message_queue_len),
            {Name, Len}
        end,
        Names
    ),
    lists:sort(fun(A, B) -> element(2, A) =< element(2, B) end, Mailboxes)
end,
```
{:codeblock}

Calling the function gives you a list of mailboxes and
their sizes.

``` sh
> ShowRexiServerMailboxes().
[{rexi_server,0}]
```
{:codeblock}

This function returns a list of
`{registered_process_name, mailbox_size}` tuples. The sum
of the message queue length values exceeds the alert
threshold.

#### How to fix it

As indicated previously, you can configure rexi
communication patterns in two ways. You probably need to
switch over to the newer server-per-node configuration.

In a remsh on the relevant node, verify that the
server-per-node configuration is set to false.

``` sh
> config:get("rexi", "server_per_node", "false").
```
{:codeblock}

This function returns the string "false." If the
function returns true, contact support. If the
server-per-node configuration is turned off, enable it
in a remsh.

``` sh
> F = fun() -> supervisor:restart_child(rexi_sup, rexi_server_mon), \
    supervisor:restart_child(rexi_sup, rexi_server_sup) end.
> rpc:multicall(erlang, apply, [F, []]).
> timer:sleep(60000).
> rpc:multicall(config, set, ["rexi", "server_per_node", "true"]).
```
{:codeblock}

Calling `restart_child` might return `{error,running}`, or
something similar, which is expected. They are restarted
as a fail-safe measure, and attempting to do so multiple
times does not have a negative impact.

#### How to verify that it is fixed

Run `ShowRexiServerMailboxes().` again and see whether the
size is decreasing. If the cluster is already using the
server-per-node configuration, but the problem persists,
contact support.

### `custodian`

#### What it checks

This function checks the number of shard replicas that
are currently reachable for all shard ranges for any
database that is equal to the default N, usually 3.

#### How it is checked

A program that is called Custodian runs on every
database node in the cluster and inspects the dbs
database. Documents in the dbs database are referred to
as shard maps or partition tables, and contain a mapping
of database shards to nodes.

Custodian raises an alarm if one of the following
situations occur.

*   Some shards have less than or more than the
    appropriate number of replicas that are listed in the
    shard table.
*   A shard is mapped to an unavailable node.

#### What it means when it fails

If n < N, it means that a database has shards that are
under protected, with fewer than N replicas available in
one or more shards ranges in one or more databases. If n > N,
it means that some shard ranges in some databases
have too many replicas. This issue is not as serious as
having too few, but must be addressed.

Often, this warning is a proxy for a disabled database
node (such as a dbcore restart or hardware failure), as
this disabled database node renders a good number of
shard replicas unreachable. If it is not caused by a
disabled node, it might be caused by one of the
following issues.

*   Someone deliberately created a database with less
    than N replicas.
*   A shard move failed, a shard disappeared, an extra
    copy was created, or the shard map was not properly
    updated.
*   Some other shard-map issue.
*   One or more nodes are not connected to all cluster
    nodes.
*   One or more shards have an N value greater than the
    default N.

#### How to fix it

Make sure that the problem is not caused by a server
that is disabled, unreachable, or not connected to the
other nodes. If that is not the case, contact support.

### `disk`

#### What it checks

This function checks whether the `/` and `/srv` file systems
are writable.

#### How it is checked

This check is done by writing a temporary file to `/tmp`
and `/srv/sensu` and making sure that it succeeds. A
failure of any kind or a 15-second timeout causes the
check to fail.

#### What it means when it breaks

The file system has most likely become read-only. A
read-only file system can cause dbcore to run in a
degraded mode that affects the rest of the cluster (if
it is the `/srv` file system that is read-only). If the `/`
file system is read-only, a number of other problems can
occur. At the least, chef does not run.

If a disk error occurs, this disk error can cause a file
system to be remounted as read-only.

If the disk is mounted read/write and enough space is
available, the file system uses the pool of free inodes.

#### How to fix it

To check the mount status, use `mount`. In the following
example, `rw` indicates mounted read/write, `ro` read-only.

``` sh
$ mount
/dev/sda1 on / type ext4 (rw)
...
/dev/sdc1 on /srv type ext4 (rw,noatime)
```
{:codeblock}

If `/srv` is read-only, stop dbcore:

``` sh
sudo sv stop cloudant
```
{:codeblock}

to keep it from affecting the rest of the cluster. You
also might investigate what is causing the check to
fail.

*   Was it remounted as read-only (possibly due to a disk
    error)? Run `mount` and check for `ro`.
*   Is there another reason the file cannot be written?
    Check for the existence of `/srv/` and that it is
    writable.
*   Check the load on the server (by using `uptime` or `top`)
    to see whether a high load is causing file system
    operations to time out.

You must restart the node. When it starts, it might work
or you might get disk errors. If you get disk errors,
you probably need to replace the drive. Then, do a
standard node replacement. If the disks are mounted
correctly, run `df -i` and look at the `IFree` column to
check the available inodes. If the number of inodes is
less than 1000, remedy the immediate situation by
disposing of unneeded and orphaned files. Additionally,
the file system might be configured incorrectly, in
which case:

``` sh
sudo tune2fs -m 0 <partition>
```
{:codeblock}

can help.
However, neither of these options is a permanent
solution.

### `ioq`

#### What it checks

This check monitors the number of requests that are
waiting to be processed by IOQ.

#### What it means when it fails

The IOQ has numerous pending requests, but it is not
necessarily stuck. To check, look at the volume of IOQ
requests being processed in the metrics application.

#### How to fix it

Verify that the situation is not caused by a sudden
"spike" in activity. Look for a relatively slow growth
in pending requests. If you see growth, do the following
steps.

Verify that the IOQ is not saturated with traffic. If
the number of IOQ reads and writes shown in the metrics
application is more than 20k, IOQ is probably saturated
with traffic. A quick fix to this problem is to bypass
interactive IOQ traffic.

``` sh
> config:set("ioq.bypass", "interactive", "true").
```
{:codeblock}

After you enable bypass, the pending request count
trends downward.

If the IOQ is not saturated, something else is
happening. As the best immediate action, put the node in
maintenance mode.

``` sh
> config:set("cloudant", "maintenance_mode", "true").
```
{:codeblock}

Next, wait approximately 30 seconds, and restart dbcore.

``` sh
$ sudo sv restart dbcore
```
{:codeblock}

If you get to this point, contact support to investigate
why IOQ failed.

### `search`

#### What it checks

This check monitors whether clouseau is running on the
node. Clouseau acts as a wrapper around the Lucene
library that does the generation, updating and querying
of search indexes at the shard level. If clouseau is not
running, the node cannot serve search requests.

#### How to fix it

Try disconnecting clouseau; it automatically reconnects.

``` sh
disconnect_node('clouseau@127.0.0.1').
```
{:codeblock}

Next, run Weatherreport search to see whether the
problem is fixed. You might need to repeat this cycle a
few times. If it is still not working, try this solution
instead.

``` sh
sudo sv restart clouseau
sudo sv restart clouseau
weatherreport search
```
{:codeblock}
