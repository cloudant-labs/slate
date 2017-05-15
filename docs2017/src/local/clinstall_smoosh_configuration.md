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

# Configuring `Smoosh`


`Smoosh` is the Cloudant&reg; auto-compaction daemon. Cloudant notifies
`Smoosh` when databases and views are updated. `Smoosh` might elect
to enqueue them for compaction.

## Top-Level Settings

These settings are the main settings that you use with `Smoosh`.

*   `db_channels`

    A comma-separated list of channel names for databases.

*   `staleness`

    The number of minutes that the (expensive) priority
    calculation can be stale before it is recalculated. The
    default value is 5 minutes.

*   `view_channels`

    A comma-separated list of channel names for views.

Sometimes it is necessary to run the following processes.

*   `cleanup_index_files`

    `Smoosh` cleans up the files for indexes that were
    deleted. The setting defaults to false. The setting must
    not be changed unless the cluster is running low on disk
    space. Be cautious when you change this setting.

*   `wait_secs`

    The time a channel waits before compaction begins. This
    time allows `Smoosh` to observe and analyze what to
    compact first. Rarely change this setting from the
    default value, which is 30 seconds.

## Channel Settings

A channel has several important settings that control runtime
behavior.

*   `capacity`

    The maximum number of items the channel can hold (lowest
    priority item is removed to make room for new items).
    Defaults value is 9999.

*   `concurrency`

    The maximum number of jobs that can run concurrently.
    Default value is 1.

*   `max_priority`

    The value must have a priority lower than this setting
    to be enqueued. Default value is infinity.

*   `max_size`

    The value must not be larger than the value specified in
    length to be enqueued. Default value is infinity.

*   `min_priority`

    The value must have a priority at least as high as this
    setting to be enqueued. Default value is 5.0 for ratio
    and 16 MB for slack.

*   `min_size`

    The value must be at least the value that is specified
    in length to be enqueued. Default value is 1 MB (1048576
    bytes).

*   `priority`

    The method that is used to calculate priority. It can be
    ratio (calculated as disk_size/data_size) or slack
    (calculated as disk_size-data_size). Default value is
    ratio.

## Compaction Scheduling Algorithm

`Smoosh` determines whether to compact a database or view it by evaluating the
item against the selection criteria of each channel in the order they are configured.
By default,
two channels for databases (`ratio_dbs` and `slack_dbs`) and two
channels for views (`ratio_views` and `slack_views`) exist.
`Smoosh` enqueues
the new item to the first channel that accepts it. If no channel
accepts, the item is not enqueued for compaction.

## Example config commands

Change the set of database channels.

``` sh
config:set("Smoosh", "db_channels", "small_dbs,medium_dbs,large_dbs").
```
{:codeblock}

Change the set of database channels on all live nodes in the
cluster.

``` sh
rpc:multicall(config, set, ["Smoosh", "db_channels", "small_dbs,medium_dbs,large_dbs"]).
```
{:codeblock}

Change the concurrency of the ratio_dbs database channel to 2.

``` sh
config:set("Smoosh.ratio_dbs", "concurrency", "2").
```
{:codeblock}

Change the concurrency of all live nodes in the cluster.

``` sh
rpc:multicall(config, set, ["Smoosh.ratio_dbs", "concurrency", "2"]).
```
{:codeblock}

## Example API commands

``` sh
Smoosh:status()
```
{:codeblock}

This command prints the state of each channel, how many jobs are
currently running, and how many jobs are enqueued, including the
lowest and highest priority of those enqueued items. The idea is
to provide, at a glance, sufficient insight into `Smoosh` that an
operator can assess whether `Smoosh` is adequately targeting the
reclaimable space in the cluster. In general, a working correctly
status output has items in the `ratio_dbs` and `ratio_views`
channels. Due to the default settings, `slack_dbs` and `slack_views`
contain items.

``` sh
Smoosh:enqueue_all_dbs(), Smoosh:enqueue_all_views()
```
{:codeblock}

You usually do not need to use these functions, since `Smoosh`
finds the best compaction candidates on its own. However, if you
experience disk space issues, these functions might help. If they
do, that indicates a bug or configuration issue with `Smoosh`.
Check your configuration and contact support.
