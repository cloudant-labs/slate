---

copyright:
  years: 2017
lastupdated: "2017-05-22"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-05-22 -->

# Configuring Cloudant for Cross Region Disaster Recovery

The [{{site.data.keyword.cloudant_short_notm}} Disaster Recovery guide](disaster-recovery-and-backup.html)
explains that one way to enable disaster recovery is to use
[{{site.data.keyword.cloudantfull}} replication to create redundancy across regions.

You can configure replication in {{site.data.keyword.cloudant_short_notm}} using an 'active-active'
or 'active-passive' topology across data centers.

The following diagram shows a typical configuration that
uses two {{site.data.keyword.cloudant_short_notm}} accounts,
one in each region:

![Example active-active architecture](../images/active-active.png)

It is helpful to remember:

* Within each datacenter,
  {{site.data.keyword.cloudant_short_notm}} already offers high availability
  by storing data in triplicate across three servers.
* Replication occurs at the database rather than account level
  and must be explicitly configured.
* {{site.data.keyword.cloudant_short_notm}} does not provide any Service Level Agreements (SLAs)
  or certainties about replication latency.
* {{site.data.keyword.cloudant_short_notm}} does not monitor individual replications.
  Your own strategy for detecting failed replications and restarting them is advisable.

## Before You Begin

> **Note**: For an active-active deployment,
  a strategy for managing conflicts must be in place.
  Therefore, be sure to understand how [replication](../api/replication.html) and
  [conflicts](mvcc.html#distributed-databases-and-conflicts) work
  before you consider this architecture.

Contact [{{site.data.keyword.cloudant_short_notm}} support ![External link icon](../images/launch-glyph.svg "External link icon")](mailto:support@cloudant.com){:new_window}
if you need help with how to model data to handle conflicts effectively.

## Overview

In the following material,
a bidirectional replication is created.
This configuration allows two databases to work in an active-active topology.

The configuration assumes that you have two accounts in different regions:

* `myaccount-dc1.cloudant.com`
* `myaccount-dc2.cloudant.com`

When these accounts are in place,
the basic steps are as follows:

1. [Create](#step-1-create-your-databases) a pair of peer databases within the accounts.
2. [Set up](#step-2-create-an-api-key-for-your-replications) API keys
  to use for the replications between these databases.
3. Grant appropriate permissions.
4. Set up replications.
5. Test replications are working as expected.
6. Configure application and infrastructure for either active-active
  or active-passive use of the databases.

## Step 1: Create your databases

[Create the databases](../api/database.html#create) that you want to replicate between
within each account.

In this example,
a database that is called `mydb` is created.

The names that are used for the databases in this example are not important,
but using the same name is clearer.

```sh
curl https://myaccount-dc1.cloudant.com/mydb -XPUT -u myaccount-dc1
curl https://myaccount-dc2.cloudant.com/mydb -XPUT -u myaccount-dc2
```
{:codeblock}

## Step 2: Create an API key for your replications

It is a good idea to use an [API key](../api/authorization.html#api-keys) for continuous replications.
The advantage is that if your primary account details change,
for example after a password reset,
your replications can continue unchanged.

API keys are not tied to a single account.
This characteristic means that a single API key can be created,
then granted suitable database permissions for both accounts.

For example,
the following command requests an API key for the account `myaccount-dc1`:

```sh
$ curl -XPOST https://myaccount-dc1.cloudant.com/_api/v2/api_keys -u myaccount-dc1
```
{:codeblock}

A successful response is similar to the following abbreviated example:

```json
{
  "password": "YPN...Tfi",
  "ok": true,
  "key": "ble...igl"
}
```
{:codeblock}

> **Note**: Take careful note of the password.
  It is not possible to retrieve the password later.

### Step 3: Grant access permission

[Give the API Key permission](../api/authorization.html#modifying-permissions)
to read and to write on both databases.

If you also want to replicate indexes,
assign admin permissions.

Use the {{site.data.keyword.cloudant_short_notm}} Dashboard,
or alternatively see the [authorization](../api/authorization.html) information
for details of how to grant permissions programmatically.

### Step 4: Set up replications

Replications in {{site.data.keyword.cloudant_short_notm}} are always uni-directional:
from one database to another database.
Therefore,
to replicate both ways between two databases,
two replications are required,
one for each direction.

A replication is created in each account,
that uses the API Key created [earlier](#step-2-create-an-api-key-for-your-replications).

First,
create a replication from database `myaccount-dc1.cloudant.com/mydb` to
database `myaccount-dc2.cloudant.com/mydb`.

```sh
curl -XPOST 'https://myaccount-dc1.cloudant.com/_replicator'
	-u myaccount-dc1
	-H 'Content-type: application/json'
	-d '{ "_id": "mydb-myaccount-dc1-to-myaccount-dc2",
	"source": "https://ble...igl:YPN...Tfi@myaccount-dc1.cloudant.com/mydb",
	"target": "https://ble...igl:YPN...Tfi@myaccount-dc2.cloudant.com/mydb",
	"continuous": true
}'
```
{:codeblock}

Next,
create a replication from database `myaccount-dc2.cloudant.com/mydb` to
database `myaccount-dc1.cloudant.com/mydb`.

```sh
curl -XPOST 'https://myaccount-dc2.cloudant.com/_replicator'
	-u myaccount-dc2
	-H 'Content-type: application/json'
	-d '{ "_id": "mydb-myaccount-dc2-to-myaccount-dc1",
	"source": "https://ble...igl:YPN...Tfi@myaccount-dc2.cloudant.com/mydb",
	"target": "https://ble...igl:YPN...Tfi@myaccount-dc1.cloudant.com/mydb",
	"continuous": true
}'
```
{:codeblock}

> **Note:** If this step fails because the `_replicator` database doesn't exist,
  create it.

### Step 5: Test your replication

Test the replication processes by creating,
modifying,
and deleting documents in either database.

After each change in one database,
check that you can also see the change reflected in the other database.

### Step 6: Configure your application

At this point,
the databases are set up to remain synchronized with each other.

The next decision is whether to use the databases in an
[active-active](#active-active) or [active-passive](#active-passive) manner.

#### Active-Active

In an active-active configuration,
different application instances can write to
different databases.

For example,
application 'A' might write to database `myaccount-dc1.cloudant.com/mydb`,
while application 'B' might write to database `myaccount-dc2.cloudant.com/mydb`.

This configuration offers several benefits:

- Load can be spread over several accounts.
- Applications can be configured to access an account with
  lower latency (not always the geographically closest).

An application can be set up to communicate with the 'nearest'
Cloudant account.
For applications hosted in DC1,
it is appropriate to set their {{site.data.keyword.cloudant_short_notm}}
URL to `"https://myaccount-dc1.cloudant.com/mydb"`.
Similarly,
for applications that are hosted in DC2,
you would set their Cloudant URL to `"https://myaccount-dc2.cloudant.com/mydb"`.

#### Active-Passive

In an active-passive configuration,
all instances of an application are configured to use a primary database.
However,
the application can fail over to the other backup database,
if circumstances make it necessary.
The fail over might be implemented within the application logic itself,
or by using a load balancer,
or by using some other means.

A simple test of whether a fail over is required would be to
use the main database endpoint as a 'heartbeat.
For example,
a simple `GET` request that is sent to the main database endpoint normally returns
[details about the database](../api/database.html#getting-database-details).
If no response is received,
it might indicate that a fail over is necessary.

#### Other configurations

You might consider other hybrid approaches for your configuration.

For example,
in a 'Write-Primary, Read-Replica' configuration,
all writes go to one database,
but the read load is spread among the replicas.

### Step 7: Next steps

* Consider monitoring the [replications](../api/advanced_replication.html) between the databases.
  Use the data to determine whether your configuration might be optimized further.
*	Consider how your design documents and indexes are deployed and updated.
  You might find it more efficient to automate these tasks.

## Failing over between Cloudant regions

Typically,
the process of managing a fail over between regions or datacenters is handled higher up within your application stack,
for example by configuring application server fail over changes,
or by balancing the load.

{{site.data.keyword.cloudant_short_notm}} does not provide a facility for you
to manage explicitly any fail over or reroute requests between regions.
This constraint is partly for technical reasons,
and partly because the conditions under when it might happen tend to be application-specific.
For example,
you might want to force a fail over in response to a custom performance metric.

However,
if you decide that you do need an ability to manage fail over,
some possible options include:

* Put your own [HTTP proxy in front of {{site.data.keyword.cloudant_short_notm}} ![External link icon](../images/launch-glyph.svg "External link icon")](https://cloudant.com/blog/green-man-gaming-cross-cloud-nginx-config/){:new_window}.
  Configure your application to talk to the proxy rather than the {{site.data.keyword.cloudant_short_notm}} instance.
  This configuration means that the task of changing the {{site.data.keyword.cloudant_short_notm}}
  instances that are used by applications can be handled through a modification to the proxy configuration
  rather than a modification to the application settings.
  Many proxies have the capability to balance the load,
  based on user-defined health checks.
* Use a global load balancer such as [Traffic Director ![External link icon](../images/launch-glyph.svg "External link icon")](http://dyn.com/traffic-director/){:new_window} to route to {{site.data.keyword.cloudant_short_notm}}.
  This option requires a `CNAME` definition that routes to
  different {{site.data.keyword.cloudant_short_notm}} accounts,
  based on a health check or latency rule.

## Recovering from fail over

If a single {{site.data.keyword.cloudant_short_notm}} instance is unreachable,
avoid redirecting traffic back to it as soon as it becomes reachable again.
The reason is that some time is required for intensive tasks
such as synchronizing the database state from any peers,
and ensuring that indexes are up to date.

It is helpful to have a mechanism for monitoring these tasks
to help decide when a database is in a suitable state to service your production traffic.

As a guide,
a typical list of checks to apply include:

* [Replications](#replications)
* [Indexes](#indexes)

> **Note:** If you implement request rerouting or fail over based on a health test,
  you might want to incorporate corresponding checks to avoid premature rerouting back to
  a service instance that is still recovering.

### Replications

* Are any replications in an error state?
* Do any replications need restarting?
* How many pending changes are still waiting for replication into the database?

More information on [monitoring replication status](../api/advanced_replication.html#replication-status)
is available.

> **Note:** If a database is being changed continuously,
  the replication status is unlikely to 0.
  You must decide what status threshold is acceptable,
  or that represents an error state.

### Indexes

* Are the indexes sufficiently up-to-date?
  Check this using the [active tasks](../api/active_tasks.html) endpoint.
* Test the level of 'index readiness' by sending a query to the index,
  and deciding whether it returns within an acceptable time.
