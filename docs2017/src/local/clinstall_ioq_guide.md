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

# Configuring IOQ

Cloudant&reg; IO queue (IOQ) handles the prioritization of IO
operations in the database works and how you can configure and
tune it. IOQ provides configurable prioritization of interactive
requests and background tasks such as compaction and internal
replication, and equal prioritization for interactive requests by
the backend or database.
{:shortdesc}

From an operational perspective, IOQ carries out the following
fundamental operations.

1. Enqueuing requests into one of a number of available channels.

2. Selecting and submitting a request from the available channels
   according to configured priorities.

IOQ categorizes IO requests by class and by priority. The class
of a request dictates the channel into which it is enqueued and
the priority influences the probability that a request is
dequeued and run. The following table lists the IOQ classes and
the corresponding priorities.

>   **Note:** Mapping of IOQ classes to class priorities is not 1:1.

<table>
<thead>
<tr>
<th>IOQ class</th>
<th>IOQ priority</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>interactive</td>
<td>reads, writes</td>
<td>IO requests related to requests made by users through the HTTP layer.</td>
</tr>
<tr>
<td><code>db_update</code></td>
<td>writes</td>
<td>Interactive IO requests that are database write operations.</td>
</tr>
<tr>
<td><code>view_update</code></td>
<td>views</td>
<td>IO requests related to view index builds.</td>
</tr>
<tr>
<td><code>db_compact</code></td>
<td>compaction</td>
<td>IO requests related to database compactions.</td>
</tr>
<tr>
<td><code>view_compact</code></td>
<td>compaction</td>
<td>IO requests related to view compactions.</td>
</tr>
<tr>
<td><code>internal_repl</code></td>
<td>replication</td>
<td>IO requests related to internal replication, that is, replication between nodes in a
cluster.</td>
</tr>
<tr>
<td>low</td>
<td>low</td>
<td>IO requests related to requests made by users through the HTTP layer where the
<code>x-cloudant-priority</code> header is set to <code>low</code>.</td>
</tr>
<tr>
<td>other</td>
<td>undefined</td>
<td>IO requests that do not fit any of the previous classes, including search IO
requests.</td>
</tr>
</tbody>
</table>

## Internals

To understand the relationship between the IOQ classes and the
IOQ priorities, it is useful to understand the channels into
which IO requests are enqueued. IOQ uses the following channels.

*  Compaction
*  Internal replication
*  Low
*  Customer

The Customer channel is effectively a meta-channel where each
item in the queue represents a backend/database name combination
that consists of more channels.

*  Interactive
*  DB update
*  View update

Requests are enqueued according to the following scheme.

*  Requests with class `internal_repl`, `low`, `db_compact`, or
   `view_compact` are enqueued into Internal replication, Low, or
   Compaction channels.
*  Requests with class `interactive`, `db_update`, or `view_update` are
   enqueued into the Interactive, DB update, or View update
   channel of the relevant Customer channel for the
   backend/database combination.
*  Requests with class `other` are enqueued into the Interactive
   queue of a Customer channel that is reserved for other IOQ
   requests.

Requests are submitted by using the following processes.

*  The next item is selected from either the Compaction, Internal
   replication, Low, or Customer channel according to the
   configured priorities (compaction, replication, low, and
   customer).
*  If the item is obtained from the Compaction, Internal
   replication, or Low channels, the request is submitted for
   execution.
*  If the item is obtained from the Customer channel, the request
   is selected from either the Interactive, DB update, or View
   update channel according to the configured priorities (reads,
   writes, and views).

## Configuration

Initially, use the default IOQ configuration values. As more
becomes known about the behavior of a cluster under load, the IOQ
settings can be tuned to provide optimal performance for the
production workload. Tuning IOQ is not always the solution to
performance problems. You must also consider the total load on
the cluster, the capabilities of the underlying hardware, and the
usage patterns and design of the applications that sit on top of
the data layer.

### Priorities

The default IOQ configuration gives interactive
reads/writes and view builds a high priority (1.0) and
background requests a much lower priority (0.001 for
compaction and 0.0001 for replication and low). You can
set the priorities to other values with the `config` app
in a `remsh` session, as shown here.

``` sh
config:set("ioq", "views", "0.5", "FBXXXXX reduce views IOQ priority").
```
{:codeblock}

To return to the default value, delete the configuration
value.

``` sh
config:delete("ioq", "views", "FBXXXXX revert to default priority").
```
{:codeblock}

### Internal replication backlog

If cluster nodes are frequently exhibiting an internal
replication backlog, consider increasing the replication
priority. You can confirm a backlog by checking the logs
for `erlang.internal_replication_jobs`.

If this value is consistently elevated by more than a
few hundred changes, try increasing the replication IOQ
priority.

``` sh
config:set("ioq", "replication", "0.5", \
"FBXXXXX speed up internal replication").
```
{:codeblock}

When increasing the replication IOQ priority is
effective, you see a change in the rate at which the
metric decreases. It is worth experimenting with values
as high as 1.0. However, keep an eye on HTTP request
latencies to verify no adverse impact on other aspects
of cluster performance.

### Compactions not completing quickly enough

If disk usage is rising on cluster nodes and there is a
corresponding backlog in compaction work, consider
increasing the compaction priority. Check the volume of
pending changes for ongoing compaction in the logs by
looking for `changes_pending.*compaction`.

Increase the priority for compaction.

``` sh
config:set("ioq", "compaction", "0.5", \
"FBXXXXX speed up compaction").
```
{:codeblock}

Now, monitor the changes_pending metrics to see whether
the rate at which changes are being processed has
increased. Experiment with values as high as 1.0, if
necessary, and keep an eye on cluster performance.

### Interactive requests and views competing for IO resource

Metrics might show that read/write performance worsens
when views are building or conversely that view build
performance slows when read/write load increases. If the
performance requirements of the cluster are such that a
particular type of request is more critical to the
application it supports, consider reducing the other IOQ
priorities. Here is an example.

``` sh
config:set("ioq", "views", "0.1", \
"FBXXXXX attempt to improve read/write performance").
```
{:codeblock}

### Concurrency

Concurrency defines the total number of concurrent IO
operations that are allowed by IOQ. The default value is
20, but you might want to increase this number in the
following circumstances.

1.  The number of active requests or IOQ latency is
    consistently elevated.
2.  Disk usage is significantly less than 100%.

If performance is impacted by requests that are waiting
in the queues, consider increasing IOQ concurrency
(sensible values to try are 30, 50, and 100) and
observing the resulting effect. However, be aware that
increasing this value beyond a certain point can result
in the disks being overloaded and overall performance
degradation. The exact point depends on the cluster
workload and hardware, so it is important to monitor the
cluster when you make changes.

### Bypasses

In extreme cases, it is possible that IOQ is the
bottleneck for certain request classes. If so, you can
bypass IOQ for that request class as shown in the
following example for interactive requests.

``` sh
config:set("ioq.bypass", "interactive", "true", \
"FBXXXXX attempt to improve interactive performance").
```
{:codeblock}

Bypasses are set for IOQ classes, not IOQ priorities.
Therefore, if you want to bypass all compaction
requests, set a bypass for `db_compact` and `view_compact`.
When you consider setting an IOQ bypass, be aware of the
following possibilities.

*   Other request classes continue to be routed through
    IOQ and are not able to compete with the bypassed
    requests. Monitor the cluster carefully to determine
    whether overall performance is acceptable. In
    particular, keep an eye on compaction (unless it is
    being bypassed) because, if the rate of compaction
    slows too much, the disk might start filling up.
*   The bypass effectively shifts the bottleneck to
    another part of the system, which is typically
    evident in `couch_file` and `couch_db_updater` message
    queue backups.
*   Disk performance might also become saturated, which
    might lead to performance degradation.

Generally, it is a good idea to avoid IOQ bypasses.
