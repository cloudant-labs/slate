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

# Tune parameters for common replication cases

Tune parameters for common replication cases by using the
following parameters to impact the performance of a replication
task. Reference the following scenarios and their recommended
values to resolve issues with performance.
{:shortdesc}

The following parameters impact the performance of a replication
task.

*   `connection_timeout`  
    Number of milliseconds until an HTTP connection times
    out.
*   `http_connections`  
    Maximum total number of HTTP connections.
*   `worker_batch_size`  
    Number of documents each worker processes in a single
    batch.
*   `worker_processes`  
    Number of concurrent processes for this replication.

The optimal values for these parameters depend on several
factors.

*   Document size
*   Number/size of attachments
*   Write load of the database
*   Number of replication tasks that are running concurrently
*   Total load of the cluster

## High throughput, small documents

If you want to optimize for high throughput, and most documents
in your database are small (about 1 KB), try to keep
`worker_processes` under the number of cores on the mediating
server. The `worker_batch_size` must not be larger than 500 to
avoid errors (such as dropped connections) that would lead the
replicator to retry a large write request. The `connection_timeout`
value is increased from the default of 30,000 for the same
reason.


``` json
{
    "source": "...",
    "target": "...",
    "worker_processes": 20,
    "worker_batch_size": 500,
    "http_connections": 300,
    "connection_timeout": 60000
}
```
{:codeblock}

## High throughput with attachments

A database that contains documents with large or variable numbers
of attachments requires different treatment. Increase worker
count (`worker_processes`) and decrease the amount of work that is
done by each worker (`worker_batch_size`) to avoid workers being
limited to replicating one slow attachment each.

``` json
{
    "source": "...",
    "target": "...",
    "worker_processes": 100,
    "worker_batch_size": 20,
    "http_connections": 150,
    "connection_timeout": 60000
}
```
{:codeblock}

## Many concurrent replications

If you want to run many replications concurrently, each
replication job must not use too many resources. Set the value
for `worker_processes` to `1`.

``` json
{
    "source": "...",
    "target": "...",
    "worker_processes": 1,
    "worker_batch_size": 100,
    "http_connections": 1,
    "connection_timeout": 60000
}
```
{:codeblock}

## Background replication

To keep performance impact on the source or target server to a
minimum, you can use these settings. However, these settings
might not deliver much throughput. Increase the
`connection_timeout` because the server is heavily loaded and it
might push this replication into the background.

``` json
{
    "source": "...",
    "target": "...",
    "worker_processes": 1,
    "worker_batch_size": 100,
    "http_connections": 5,
    "connection_timeout": 300000
} 
```
{:codeblock}
