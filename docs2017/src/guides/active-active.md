---

copyright:
  years: 2017
lastupdated: "2017-05-18"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# Configuring Cloudant for Cross Region Disaster Recovery

Configuring Cloudant in an active-active or active-passive topology
across data centres for disaster recovery is a common requirement.

The following is a standard pattern for achieving this using two Cloudant accounts, one in each region:

![active-active architecture](../images/active-active.png)

Some things to note:

*	Within each datacentre, Cloudant already offers high availablity
	by storing data in triplicate across three servers.
*	Replication occurs at the database rather than account level
	and must be explicitly configured.
*	Cloudant does not provide any SLA/guarantees around replication latency.
*	Cloudant does not monitor individual replications. You should have a strategy for detecting failed replications and restarting them.

## Before You Begin

For an active-active deployment it is essential that a strategy for
managing conflicts is in place. Therefore, be sure to understand
how [replication](../api/replication.html) and [conflicts](mvcc.html#distributed-databases-and-conflicts) work before considering this architecture.

Contact Cloudant support if you need help with how to model data to
handle conflicts effectively.

## Setup guide

In the guide below, we configure bi-directional replication, allowing two databases to be used in an active-active fashion.

We'll assume 2 accounts in different regions - `myaccount-dc1.cloudant.com` and `myaccount-dc2.cloudant.com`.

Once these are in place, the steps are:

1. Create a pair of peer databases within the accounts.
2. Set up API keys to use for the replications between these databases.
3. Grant appropriate permissions.
4. Set up replications.
5. Test replications are working as expected.
6. Configure application and infrastructure for either active-active
	or active-passive use of the databases.

### Step 1: Create your databases

First, create the databases you want to replicate between in each
account. For this example, we'll create a database called `mydb`.
While the names used for the databases are unimportant, using the same
name is clearer.

```sh
curl https://myaccount-dc1.cloudant.com/mydb -XPUT -u myaccount-dc1
curl https://myaccount-dc2.cloudant.com/mydb -XPUT -u myaccount-dc2
```
{:codeblock}

### Step 2: Create an API key for your replications

It's good practice to use an API key for continuous replications.
This means that if your primary account details change (e.g.
password reset), your replications won't break.

API keys once are not tied to a single account so we can create a single
one and grant that key permissions for databases on both accounts.

```sh
$ curl -XPOST https://myaccount-dc1.cloudant.com/_api/v2/api_keys -u myaccount-dc1
```
{:codeblock}

returns, for example:

```json
{
	"password": "YPNCaIX1sJRX5upaL3eqvTfi",
	"ok": true,
	"key": "blentfortedsionstrindigl"
}
```
{:codeblock}

Make a note of the password as you won't be able to retrieve it again.

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
