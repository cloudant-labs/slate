---

copyright:
  years: 2017
lastupdated: "2017-05-19"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# Configuring Cloudant for Cross Region Disaster Recovery

The [{{site.data.keyword.cloudant_short_notm}} Disaster Recovery guide](disaster-recovery-and-backup.html)
explains that one way to enable disaster recovery is to use
[{{site.data.keyword.cloudantfull}} replication to create redundancy across regions.

To do this,
you can configure {{site.data.keyword.cloudant_short_notm}} in an 'active-active' or 'active-passive' topology
across data centres.

The following diagram shows a typical configuration which uses two {{site.data.keyword.cloudant_short_notm}} accounts,
one in each region:

![Example active-active architecture](../images/active-active.png)

Note the following points:

* Within each datacentre,
  {{site.data.keyword.cloudant_short_notm}} already offers high availablity
  by storing data in triplicate across three servers.
* Replication occurs at the database rather than account level
  and must be explicitly configured.
* {{site.data.keyword.cloudant_short_notm}} does not provide any Service Level Agreements (SLAs)
  or guarantees about replication latency.
* {{site.data.keyword.cloudant_short_notm}} does not monitor individual replications.
  Your own strategy for detecting failed replications and restarting them is advisable.

## Before You Begin

> **Note**: For an active-active deployment,
  it is essential that a strategy for managing conflicts is in place.
  Therefore, be sure to understand how [replication](../api/replication.html) and
  [conflicts](mvcc.html#distributed-databases-and-conflicts) work
  before considering this architecture.

Contact [{{site.data.keyword.cloudant_short_notm}} support ![External link icon](../images/launch-glyph.svg "External link icon")](mailto:support@cloudant.com){:new_window}
if you need help with how to model data to handle conflicts effectively.

## Overview

In the following material,
a bi-directional replication is created.
This configuration allows two databases to work in an active-active topology.

The configuration assumes you have 2 accounts in different regions:

* `myaccount-dc1.cloudant.com`
* `myaccount-dc2.cloudant.com`

Once these accounts are in place,
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

[Create the databases](../api/database.html#create) you want to replicate between
within each account.

In this example,
we create a database called `mydb`.

The names used for the databases are not important,
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
This characteristic means that we can create a single API key,
then grant that key suitable database permissions for both accounts.

For example,
the following command requests an API key got the account `myaccount-dc1`:

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

### Step 3: Give API Key reader and writer permissions on both databases

If you also want to replicate indexes, assign admin permissions as well.

Use the Cloudant Dashboard, or alternatively see the [authorization](../api/authorization.html) section of the API docs to do this programatically.

### Step 4: Set up replications

Replications in Cloudant are uni-directional so we need to set up
two - one for each direction. We'll put one in each account, using the
API Key we just created.

```sh
curl -XPOST 'https://myaccount-dc1.cloudant.com/_replicator'
	-u myaccount-dc1
	-H 'Content-type: application/json'
	-d '{ "_id": "mydb-myaccount-dc1-to-myaccount-dc2",
	"source": "https://blentfortedsionstrindigl:YPNCaIX1sJRX5upaL3eqvTfi@myaccount-dc1.cloudant.com/mydb",
	"target": "https://blentfortedsionstrindigl:YPNCaIX1sJRX5upaL3eqvTfi@myaccount-dc2.cloudant.com/mydb",
	"continuous": true
}'
```
{:codeblock}

```sh
curl -XPOST 'https://myaccount-dc2.cloudant.com/_replicator'
	-u myaccount-dc2
	-H 'Content-type: application/json'
	-d '{ "_id": "mydb-myaccount-dc2-to-myaccount-dc1",
	"source": "https://blentfortedsionstrindigl:YPNCaIX1sJRX5upaL3eqvTfi@myaccount-dc2.cloudant.com/mydb",
	"target": "https://blentfortedsionstrindigl:YPNCaIX1sJRX5upaL3eqvTfi@myaccount-dc1.cloudant.com/mydb",
	"continuous": true
}'
```
{:codeblock}

If this step fails because the `_replicator` database doesn't exist, create it.

### Step 5: Test your replication

You should now be able to create/modify/delete documents in either database and see the changes reflected in its peer.

### Step 6: Configure your application

At this point, the databases are set up to remain in sync with each
other. The next decision is whether to use the databases in an
active-active or active-passive manner.

#### Active-Passive

Here all instances of the application should be configured to use
a primary database, but have facilities in place to failover to the
backup database. This could be implemented within the application
logic itself, via a load balancer or using any other means.

See below for further information on failover options.

A useful heartbeat is the main database endpoint, for example,
`https://myaccount-dc1.cloudant.com/mydb`.

#### Active-Active

For active-active, different application instances will write to
different databases. This means that, for example:

- Load can be spread over several accounts.
- Applications can be configured to access an account with
	lower latency (not always the geographically closest).

The application could be set up to communicate with the most "local"
Cloudant account. For application server(s) in DC1, set their Cloudant
URL to `"https://myaccount-dc1.cloudant.com/mydb"`. For application
server(s) in DC2, set their Cloudant URL to `"https://myaccount-dc2.cloudant.com/mydb"`.

#### Other variations

Hybrid approaches can also be used.

- Write-Primary, Read-Replicas: all writes go to one database, but
	read load is spread amongst the replicas.

### Step 7: Next steps

*	Consider monitoring the [replications](../api/advanced_replication.html)
*	Consider how design documents/indexes will be deployed. Most likely, you'll want this automated in some fashion.


## Failing over between Cloudant regions

Typically, failover between regions/datacentres is handled higher up in the stack, e.g. via application server failover/load balancing.

Cloudant doesn't offer any facility for customers to failover/re-route requests between regions, partly for technical reasons and partly because the conditions under when this should happen tend to be very application-specific (e.g. you may want to failover based on some custom performance metric).

If you decide you do need this capability, some possible options would be:

*	Put your own [HTTP proxy in front of Cloudant ![External link icon](../images/launch-glyph.svg "External link icon")](https://cloudant.com/blog/green-man-gaming-cross-cloud-nginx-config/){:new_window}. Have your application talk to the proxy and then changing between Cloudant instances can be handled through a change in proxy config rather than an application setting. Many proxies have load balancing capabilities based on user-define defined health checks.
*	Use a global load balancer (e.g. [Traffic Director ![External link icon](../images/launch-glyph.svg "External link icon")](http://dyn.com/traffic-director/){:new_window} to route to Cloudant. You'd need to create your own CNAME which routes to different Cloudant accounts based on a health check/latency rule.


## Recovering from failover

If a single Cloudant instance is unreachable, you should not redirect traffic back to it as soon as it becomes reachable again. It will likely take some time to synchronise state from any peers, ensure indexes are up to date, etc.

You should have a process for monitoring these tasks and deciding when a database is in a suitable state to service your production traffic.

As a guide, here is a minimum list of tasks you likely want to check:

### Replications

*	Are there any in an error state? Do they need restarting?
*	How many pending changes are there to be replicated into the database; see [monitoring replication status](../api/advanced_replication.html#replication-status). Note that if a database is continuously written to, this will likely never be 0 - you should decide what threshold is tolerable / represents an error state.

### Indexes

*	Are indexes up to date (enough)? You can check this using the [active tasks](../api/active_tasks.html) endpoint.
*	You can also test "index readiness" by issuing a query to the index and observing whether it returns within acceptable latency.

If you implement request routing/failover based on a health check, you may want to incorporate the above checks into that.
