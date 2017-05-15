---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-20"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Tune the Cloudant Local automatic compactor

Read these instructions to understand how the Cloudant&reg; Local
automatic compactor works and how you can tune it. The automatic
compactor for Cloudant databases is an application that is called
Smoosh. Smoosh automatically selects and processes the compacting
of database shards on each node.
{:shortdesc}

## Smoosh Channels

Smoosh uses the concept of channels. A channel is essentially a
queue of pending compactions. Database and view compactions use
separate channels. Each channel is assigned a configuration that
defines whether a compaction ends up in the queue for the channel
and how compactions are prioritized within that queue. Smoosh
takes each channel and works through the compactions queued in
each in priority order. Each channel is processed concurrently,
so the priority levels only matter within each channel. Finally,
each channel has an assigned number of active compactions, which
defines how many compactions happen in parallel for that channel.

For example, a cluster with many database writes but few views
might require more active compactions to the database channels. A
channel is local to a dbcore node, so each node maintains and
processes an independent set of compactions.

## Channel configuration options

You can configure channels by using the following processes and
options. The channel type is set with the priority configuration
setting.

### Channel types

Each channel has a basic type for the algorithm it uses
to select pending compactions for its queue and how it
prioritizes them. The following list describes two queue
types.

-   `ratio`

    Uses the ratio `total_bytes / user_bytes` as its
    driving calculation. The result `X` must be
    greater than some configurable value `Y` for a
    compaction to be added to the queue.
    Compactions are then prioritized for higher
    values of `X`.

-   `slack`

    Uses the `total_bytes - user_bytes` as its
    driving calculation. The result `X` must be
    greater than some configurable value `Y` for a
    compaction to be added to the queue.
    Compactions are prioritized for higher values
    of `X`.

In both cases, `Y` is set with the `min_priority`
configuration variable. The calculation of `X` is
described in [Priority calculation](#priority-calculation). Both algorithms use
the following two measures.

-   `user_bytes`

    The amount of data the user has in the file. It
    does not include storage, such as old revisions
    or on-disk btree structure.

-   `total_bytes`

    The size of the file on disk.

### Further configuration options

Beyond its basic type, you can apply several other
configuration options to a queue. All options must be
set as strings. For all settings and defaults, see the
Smoosh configuration section.

### Priority calculation

The algorithm type and certain configuration options
feed into the priority calculation. The priority is
calculated when a compaction is enqueued. Since each
channel has a different configuration, each channel ends
up with a different priority value. The enqueue code
checks each channel in turn to see whether the
compaction passes its configured priority threshold
(`min_priority`). After a channel is found that can accept
the compaction, the compaction is added to the queue for
that channel and the enqueue process stops. Therefore,
the ordering of channels has a bearing in what channel a
compaction ends up in.

### Background Detail

To get metadata about a shard, you can query
`$host:5986/shards%2F$shard%2f$dbname`, where `$host` is the
database node on which the shard is `$shard` and `$dbname`
is the name of the database. To get a list of all shards
on a database, query the `/$dbname/_shards` endpoint.

``` sh
$ curl -X GET 'http://localhost:5986/shards%2F$shard%2Fdefault%2F$database.$timestamp'
```
{:codeblock}

You can find the string to replace the `$timestamp` value
in this directory: `/srv/cloudant/db/shards/`. Look for
file names that start with the database name and copy
the number that follows the database name. For example,
the following files are in a database that is named
`authorization2` under the directory, `/srv/cloudant/`.

``` sh
./db/shards/20000000-3fffffff/default/authorization2.1434466035.couch
./db/shards/c0000000-dfffffff/default/authorization2.1434466035.couch
./db/shards/a0000000-bfffffff/default/authorization2.1434466035.couch
./db/shards/e0000000-ffffffff/default/authorization2.1434466035.couch
./db/shards/80000000-9fffffff/default/authorization2.1434466035.couch
./db/shards/00000000-1fffffff/default/authorization2.1434466035.couch
./db/shards/40000000-5fffffff/default/authorization2.1434466035.couch
./db/shards/60000000-7fffffff/default/authorization2.1434466035.couchss
```
{:codeblock}

You can use the following query to collect shard
metadata for this example.

``` sh
curl -X GET 'http://localhost:5986shards%2F00000000-1fffffff%2Fdefault%2Fauthorization2.1434466035'
```
{:codeblock}

This command returns a JSON structure like the one shown
in the following example, where the `data_size` field
corresponds to `user_bytes` in the priority calculation
for `ratio` or `slack` channels.

``` json
{
    "committed_update_seq": 4,
    "compact_running": false,
    "compacted_seq": 0,
    "data_size": 1115,
    "db_name": "shards/00000000-1fffffff/exampleDB",
    "disk_format_version": 6,
    "disk_size": 2740400,
    "doc_count": 0,
    "doc_del_count": 0,
    "instance_start_time": "1412077801084432",
    "other": {
        "data_size": 0
    },
    "purge_seq": 0,
    "sizes": {
        "active": 1115,
        "external": 0,
        "file": 2740400
    },
    "update_seq": 4,
    "uuid": "a1995bbab83dee7072b69b640942a81b"
}
```
{:codeblock}

The `user_bytes` are called `data_size` in `db_info` blocks.
It is the total of all bytes that are used to store docs
and their attachments. Since `.couch` files only append,
every update adds data to the file. When you update a
btree, a new leaf node is written and all the nodes back
up the root. In this update, old data is never
overwritten and these parts of the file are no longer
live, including old btree nodes and document bodies.
Compaction takes this file and writes a new file that
contains only live data. The `disk_size` is the number of
bytes in the file as reported by `ls -al <filename>`.

### Defining a channel

You define a channel through normal dbcore
configuration, with some convention as to the parameter
names. Channel configuration is defined by using
`smoosh.channel_name` top-level configuration options.
Defining a channel involves setting the options that you
want for the channel, then bringing it into the sets of
active channels for Smoosh by adding it to either
`db_channels` or `view_channels`. This process means that
Smoosh channels can be defined for a single node or
globally across a cluster, by setting the configuration
to globally or locally.

-   `ratio_dbs`

    A ratio channel for databases that use the
    default settings.

-   `slack_dbs`

    A slack channel for databases that use the
    default settings.

-   `ratio_views`

    A ratio channel for views that use the default
    settings.

-   `slack_views`

    A slack channel for views that use the default
    settings.

This standard definition channel name must be added
often.

-   `big_dbs`

    A ratio channel for enqueuing only large
    database shards. The term large is
    workload-specific.

In the following example, a new global channel is set
up. It is important to choose good channel names. The
following conventional channel names are defined by
default if no other channel names are set. Channels have
certain defaults for their configuration, which are
defined in the Smoosh configuration section. It is only
necessary to set up how this channel differs from those
defaults. In the following example, the `min_size` and
concurrency settings are set, and keep the priority as
the default to ratio, along with the other defaults.

``` sh
# Define the new channel
(dbcore@db1.cluster001.cloudant.net)3> \
rpc:multicall(config, set, ["smoosh.big_dbs", "min_size", "20000000000"]).
{[ok,ok,ok],[]}
(dbcore@db1.cluster001.cloudant.net)3> \
rpc:multicall(config, set, ["smoosh.big_dbs", "concurrency", "2"]).
{[ok,ok,ok],[]}

# Add the channel to the db_channels set -- note we need to get the original
# value first so we can add the new one to the existing list.
(dbcore@db1.cluster001.cloudant.net)5> \

rpc:multicall(config, get, ["ioq", "compaction"]).
{[undefined,undefined,undefined],[]}

(dbcore@db1.cluster001.cloudant.net)6> \
rpc:multicall(config, set, ["smoosh", "db_channels", "ratio_dbs,big_dbs"]).
{[ok,ok,ok],[]}
```
{:codeblock}

### Viewing active channels

``` sh
(dbcore@db3.cluster001.cloudant.net)3> \
    rpc:multicall(config, get, ["ioq", "compaction"]).
    {[undefined,undefined,undefined],[]}
(dbcore@db3.cluster001.cloudant.net)4> \
rpc:multicall(config, get, ["ioq", "compaction"]).
{[undefined,undefined,undefined],[]}
```
{:codeblock}

### Removing a channel

``` sh
# Remove it from the active set
(dbcore@db1.cluster001.cloudant.net)5> \
    rpc:multicall(config, get, ["ioq", "compaction"]).
{[undefined,undefined,undefined],[]}
(dbcore@db1.cluster001.cloudant.net)6> \
    rpc:multicall(config, set, ["smoosh", "db_channels", "ratio_dbs"]).
{[ok,ok,ok],[]}

# Delete the config -- you need to do each value
(dbcore@db1.cluster001.cloudant.net)3> \
rpc:multicall(config, delete, ["smoosh.big_dbs", "concurrency"]).
{[ok,ok,ok],[]}
(dbcore@db1.cluster001.cloudant.net)3> \
    rpc:multicall(config, delete, ["smoosh.big_dbs", "min_size"]).
{[ok,ok,ok],[]}
```
{:codeblock}

### Getting channel configuration

``` sh
(dbcore@db1.cluster001.cloudant.net)1> \
    rpc:multicall(config, get, ["ioq", "compaction"]).
    {[undefined,undefined,undefined],[]}
```
{:codeblock}

### Setting channel configuration

Set the channel configuration in the same way as
defining a channel by setting the new value.

``` sh
dbcore@db1.cluster001.cloudant.net)2> \
    rpc:multicall(config, set, ["smoosh.ratio_dbs", "concurrency", "1"]).
{[ok,ok,ok],[]}
```
{:codeblock}

It can take time for the change to take effect on disk
usage.

## Main Smoosh settings

These settings are the main settings that you use with Smoosh.

*   `db_channels`
    
    A comma-separated list of channel names for databases.
    
*   `staleness`
    
    The number of minutes that the (expensive) priority calculation
    can be stale before it is recalculated.
    The default value is 5 minutes.
    
*   `view_channels`
    
    A comma-separated list of channel names for views.
    
Sometimes it is necessary to run the following processes.

*   `cleanup_index_files`
    
    `Smoosh` cleans up the files for indexes that were deleted.
    The setting defaults to false.
    The setting must not be changed unless the cluster is running low on disk space.
    Be cautious when you change this setting.
    
*   `wait_secs`
    
    The time a channel waits before compaction begins.
    This time allows Smoosh to observe and analyze what to compact first.
    Rarely change this setting from the default value,
    which is 30 seconds.

## Channel settings

A channel has several important settings that control runtime behavior.

*   `capacity`
    
    The maximum number of items the channel can
    hold (lowest priority item is removed to make room for new items).
    Default value is 9999.
    
*   `concurrency`
    
    The maximum number of jobs that can run concurrently.
    Default value is 1.
    
*   `max_priority`
    
    The value must have a priority lower than this setting to be enqueued.
    Default value is infinity.
    
*   `max_size`
    
    The value must not be larger than the value
    specified in length to be enqueued.
    Default value is infinity.
    
*   `min_priority`
    
    The value must have a priority at least as high
    as this setting to be enqueued.
    Default value is 5.0 for `ratio` and 16 MB for `slack`.
    
*   `min_size`
    
    The value must be at least the value
    that is specified in length to be enqueued.
    Default value is 1 MB (1048576 bytes).
    
*   `priority`
    
    The method that is used to calculate priority.
    It can be ratio (calculated as `disk_size/data_size`)
    or slack (calculated as `disk_size-data_size`).
    Default value is ratio.

## Standard operating procedures

Operators must do a few standard things to respond to
issues. In addition to the following items, it is useful
in some circumstances to define new channels with
certain properties (`big_dbs` is a common one) if Smoosh
is not selecting and prioritizing compactions that well.

### Checking the status of Smoosh

You can see the queued items for each channel by going
into remsh on a node and running the `smoosh:status`
command.

``` sh
> smoosh:status().
{ok,[{"ratio_dbs",
      [{active,1},
       {starting,0},
       {waiting,[{size,522},
         {min,{5.001569007970237,{1378,394651,323864}}},
         {max,{981756.5441159063,{1380,370286,655752}}}]}]},
     {"slack_views",
      [{active,1},
       {starting,0},
       {waiting,[{size,819},
         {min,{16839814,{1375,978920,326458}}},
         {max,{1541336279,{1380,370205,709896}}}]}]},
     {"slack_dbs",
      [{active,1},
       {starting,0},
       {waiting,[{size,286},
          {min,{19004944,{1380,295245,887295}}},
          {max,{48770817098,{1380,370185,876596}}}]}]},
     {"ratio_views",
      [{active,1},
       {starting,0},
       {waiting,[{size,639},
         {min,{5.0126340031149335,{1380,186581,445489}}},
         {max,{10275.555632057285,{1380,370411,421477}}}]}]}]}
```
{:codeblock}

The results give you the node-local status for each
queue. You can see more information under each channel,
such as what is shown in the following list.

-   Active

    Number of current compactions in the channel.

-   Starting

    Number of compactions that are beginning.

-   Waiting

    Number of queued compactions.

The minimum and maximum values show the effectiveness of
the queued jobs. The values for these items depend on
whether the queue is ratio or slack.

For ratio queues, the default minimum for Smoosh to
enqueue a compaction is 5. In the previous example, you
can guess that 981,756 is high. However, this database
might be small, so it does not necessarily mean useful
compactions from the point of view of reclaiming disk
space.

For this example, many queued compactions are waiting,
but it is unknown which compaction would be most
effective to run to reclaim disk space. It is worth
noting that the waiting queue sizes are only meaningful
relative to other factors on the cluster, such as
database number and size.

### Smoosh IOQ priority

This setting is a global setting that affects all
channels. Increasing it allows each active compaction to
proceed faster as the compaction work is of a higher
priority relative to other jobs. Decreasing it has the
inverse effect. By this point, you know whether Smoosh
is backing up. If it is falling behind (large queues),
try increasing compaction priority. The IOQ priority for
Smoosh is controlled through the IOQ compaction queue.

``` sh
> rpc:multicall(config, get, ["ioq", "compaction"]).
    {[undefined,undefined,undefined],[]}
```
{:codeblock}

Priority by convention runs 0 - 1, though the priority
can be any positive number. The default for compaction
is 0.01. If it looks like Smoosh has too much work that
is not getting through, you can increase the priority.
However, be careful that this order does not adversely
impact request performance.

``` sh
rpc:multicall(config, set, ["ioq", "compaction", "0.5"]).
{[ok,ok,ok],[]}
```
{:codeblock}

In general, adjusting the Smoosh IOQ priority is a
temporary measure. For some clusters, a change from the
default might be required to help Smoosh keep up with
particular workloads.

### Granting specific channels more workers

Giving Smoosh a higher concurrency for each channel can
allow a backlog in that channel to be processed. Again,
some clusters run best when specific channels have more
workers. When you assess disk space, you must know
whether the biggest offenders are database or view
files. From your assessment, you can infer whether it is
worth giving a specific Smoosh channel a higher
concurrency. The current setting can be seen for a
channel like so.

``` sh
> rpc:multicall(config, get, ["ioq", "compaction"]).
    {[undefined,undefined,undefined],[]}
```
{:codeblock}

The undefined value means that the default is used.

If you know that databases are the major user of disk
space, you might want to increase a `_dbs` channel.
Experience shows `ratio_dbs` are often best, but you must
evaluate the databases based on their status. You can
increase the `ratio_dbs` setting by using the following
command.

``` sh
> rpc:multicall(config, set, ["smoosh.ratio_dbs", "concurrency", "2"]).
    {[ok,ok,ok],[]}
```
{:codeblock}

### Suspending Smoosh

If Smoosh is causing issues, you can suspend its
operation. Suspending Smoosh differs from stopping
(Smoosh) or setting the concurrency for all channels to
zero. Suspending Smoosh pauses ongoing compactions and
maintains the channel queues intact. For example, if the
compactions for a node are causing disk space issues,
you can suspend Smoosh while you determine which channel
is causing the problem. For example, a `big_dbs` channel
might be creating huge compaction-in-progress files if
there is not much in the shard to compact. Therefore, it
is useful to use when you are testing to see whether
Smoosh is causing a problem.

``` sh
# suspend
smoosh:suspend().

# resume a suspended smoosh
smoosh:resume().
```
{:codeblock}

Suspend is implemented by calling
`erlang:suspend_process(Pid, [unless_suspending])` for
each compaction process in each channel. The
`resume_process` is called for resume.

### Restarting Smoosh

Restarting Smoosh is a last-resort solution. It is a
brute force approach where you hope that Smoosh rescans
the databases and makes the right decision. If this step
is required, contact [support@cloudant.com ![External link icon](images/launch-glyph.svg "External link icon")](mailto:support@cloudant.com){:new_window}, since doing
this step can indicate a problem with Smoosh.

## Compaction Scheduling Algorithm

`Smoosh` determines whether to compact a database or view it by evaluating the
item against the selection criteria of each channel in the order they are configured.
By default,
two channels for databases (`ratio_dbs` and `slack_dbs`) and two
channels for views (`ratio_views` and `slack_views`) exist.
`Smoosh` enqueues the new item to the first channel that accepts it.
If no channel accepts,
the item is not enqueued for compaction.

## Example config commands

Change the set of database channels.

``` sh
config:set("smoosh", "db_channels", "small_dbs,medium_dbs,large_dbs").
```
{:codeblock}

Change the set of database channels on all live nodes in the cluster.

``` sh
rpc:multicall(config, set, ["smoosh", "db_channels", "small_dbs,medium_dbs,large_dbs"]).
```
{:codeblock}

Change the concurrency of the `ratio_dbs` database channel to 2.

``` sh
config:set("smoosh.ratio_dbs", "concurrency", "2").
```
{:codeblock}

Change the concurrency of all live nodes in the cluster.

``` sh
rpc:multicall(config, set, ["smoosh.ratio_dbs", "concurrency", "2"]).
```
{:codeblock}

## Example API commands

``` sh
smoosh:status()
```
{:codeblock}

This command prints the state of each channel,
how many jobs are currently running,
and how many jobs are enqueued,
including the lowest and highest priority of those enqueued items.
The idea is to provide,
at a glance,
sufficient insight into `Smoosh` that an operator can assess whether
`Smoosh` is adequately targeting the reclaimable space in the cluster.
In general,
a working correctly status output has items in the `ratio_dbs` and `ratio_views` channels.
Due to the default settings,
`slack_dbs` and `slack_views` contain items.

``` sh
smoosh:enqueue_all_dbs(), smoosh:enqueue_all_views()
```
{:codeblock}

You usually do not need to use these functions,
since `Smoosh` finds the best compaction candidates on its own.
However,
if you experience disk space issues,
these functions might help.
If they do,
that indicates a bug or configuration issue with `Smoosh`.
Check your configuration and contact support.
