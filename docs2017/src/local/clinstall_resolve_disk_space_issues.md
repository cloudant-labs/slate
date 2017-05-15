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

# Disk space issues

Identify and resolve disk space issues by checking metrics,
compacting shards, auto-compaction, and Smoosh.
{:shortdesc}

## Checking Metrics

1.  Check metrics to get background information on the cluster,
    such as the current request load and the status of compaction
    tasks.

2.  Assess the space on the disk.

3.  Log in to the remote server.

    ```
    ssh db1
    ```
    {:codeblock}

4.  Run `du -h -s /srv/*` to get a basic outline of how disk space
    is distributed.

    You can see what is taking up the most space in the database
    or view data.

5.  Run `durep` to monitor disk usage.

    ``` sh
    durep -x -hs 5000M /srv | less
    ```
    {:codeblock}

    In this example, the following results returned.

    ```
    50.5G [################              ]  53.56% prod_features.1342146305.couch
    ```
    {:codeblock}

    The example output shows that the `prod_features` shards are large.

## Compacting specific, oversized shards

Shards can grow larger than needed. If they do, you can compact a
specific shard.

### Compact a shard and reduce its size.

``` sh
durep -x -hs 5000M /srv | less
```
{:codeblock}

Run this command to move the biggest shards to the beginning of the
list.

``` sh
$ pwd
/srv/db/shards/f5555546-ffffffff/foo
$ ls -lah bar.1332615163.couch
-rw-r--r-- 1 dbcore dbcore 944G Sep 30 09:01 bar.1332615163.couch
```
{:codeblock}

>   **Note:** If a shard is large, such as 80%+ of the space, you can manually compact it.

In `remsh`, you see the following information.

```
{ok, Db} = couch_db:open(<<"shards/f5555546-ffffffff/foo/bar.1332615163">>,
    [{user_ctx, {user_ctx, null, [<<"_admin">>], undefined}}]).
couch_db:start_compact(Db).
```
{:codeblock}

Run `_active_tasks` for the cluster and pipeline through `jq` to watch
progress.

``` sh
jq '.[] | select(contains({node: "db1", type: "database_compaction", database: "shards/f5555546-ffffffff"}))'
```
{:codeblock}

When a compaction fails, the compact files (`compact.data` and
`compact.meta`) are saved to the directory, `/srv/db/shards/`,
alongside the shard. You can see the orphaned `.compact` files by
date or by running this command:

``` sh
sudo lsof dbname.1332615163.couch.compact.data
```
{:codeblock}

This command returns
nothing if a compaction process that uses the file no longer
exists (that is, no process has an active file-handle to that
file).

## Compaction

Smoosh is the auto-compactor for the databases. If Smoosh is not
functioning properly, it can result in compactions not happening
or compacting inappropriate shards (for example, shards that do
not reclaim much space). For more information, see the guide for
compaction.
