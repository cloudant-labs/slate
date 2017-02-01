---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-01"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-02-01 -->

# Cloudant Basics

If it's your first time here,
read this information to find out more.
{:shortdesc}

The sections on [Client Libraries](../libraries/index.html#-client-libraries),
[API Reference](../api/index.html#-api-reference),
and [Guides](../guides/index.html#-guides) assume that
you know some basic things about {{site.data.keyword.IBM}} {{site.data.keyword.cloudant}}.

## Much More Than A Hosted database

{{site.data.keyword.cloudant_short_notm}} is a NoSQL database as a service (DBaaS) built from the ground up
to scale globally (think CDN for your database),
run non-stop,
and handle a wide variety of data types like JSON,
full-text,
and geo spatial.
{{site.data.keyword.cloudant_short_notm}} is an operational data store,
optimized to handle concurrent reads and writes,
and provide high availability and data durability.

## Scalable, Fault-tolerant JSON data stores

Self-describing JSON "documents" are automatically stored,
indexed,
and distributed across an elastic database cluster that can span multiple racks,
data centers,
or cloud providers to provide superior scalability and availability.

## Cloudant Sync for Occasionally Connected Apps

Cloudant Sync pushes database access to the farthest edge of the network.
Tools such as
mobile devices,
remote facilities,
sensors,
and Internet-enabled goods can connect.
Use Cloudant Sync to scale bigger,
and enable client apps to continue running offline.

## Lucene-powered Cloudant Search

The easiest way to build scalable search apps.
Cloudant Search features include:
ranked searching,
powerful query types,
results bookmarking,
faceted search,
fielded searching,
and more.

## Advanced 2D and 3D Geo-spatial indexing

Enrich your app with geo-location services by using built-in geo-hashing,
proximity,
bounding that uses box, radius, ellipse, and polygon objects,
and intersection queries.

## Analytics with Incremental MapReduce

Indexing and views are defined that use MapReduce functions
and can be based on any number of JSON fields in your database.
Indexes are updated incrementally as data changes to enable analytics.

## HTTP-based API

'`GET`',
'`PUT`',
index,
and query JSON documents directly from the browser by using an HTTP API over secure HTTP/S.

## [Security](security.html)

Data access control,
encryption,
and data backup features enable customers in financial services,
government,
e-commerce,
telecommunications,
healthcare,
and other security-minded industries to benefit from {{site.data.keyword.cloudant_short_notm}}.

## [Compliance](compliance.html)

{{site.data.keyword.cloudant_short_notm}} provides a trustworthy and secure cloud database system.
The service is built on best-in-industry standards,
including ISO 27001 and ISO 27002.

More details on {{site.data.keyword.cloudant_short_notm}} Data Privacy and
Governance [are available](dataprivacygovernance.html).

## Multiple hosting options

Never worry about cloud lock-in.
{{site.data.keyword.cloudant_short_notm}} supports various hosting options
to fit your budget and performance needs.
Choose between {{site.data.keyword.Bluemix}},
{{site.data.keyword.BluSoftlayer_full}},
AWS,
Windows&trade; Azure,
or Joyent,
and even change hosting environments on demand.

## Managed by Big Data experts at Cloudant

Big Data experts at {{site.data.keyword.cloudant_short_notm}} grow,
reconfigure,
repartition and rebalance clusters,
and protect and administer your data layer around the clock so you can get a good night’s sleep.

## Connecting to Cloudant

To access {{site.data.keyword.cloudant_short_notm}},
you must have either a [{{site.data.keyword.cloudant_short_notm}} account](../api/account.html),
or a [{{site.data.keyword.Bluemix_notm}} account](../offerings/bluemix.html).

## HTTP API

All requests to {{site.data.keyword.cloudant_short_notm}} go over the web.
This connection means any system that can speak to the web can speak to {{site.data.keyword.cloudant_short_notm}}.
All language-specific libraries for {{site.data.keyword.cloudant_short_notm}} are just wrappers that provide
some convenience and linguistic niceties to help you work with a simple API.
Many users choose to use raw HTTP libraries for working with {{site.data.keyword.cloudant_short_notm}}.

Specific details about how {{site.data.keyword.cloudant_short_notm}} uses HTTP are
provided in the [HTTP topic of the API Reference](../api/http.html).

{{site.data.keyword.cloudant_short_notm}} supports the following HTTP request methods:

-   `GET`

    Request the specified item.
    As with normal HTTP requests,
    the format of the URL defines what is returned.
    With {{site.data.keyword.cloudant_short_notm}},
    a request can include static items,
    database documents,
    and configuration and statistical information.
    In most cases,
    the information is returned in the form of a JSON document.

-   `HEAD`

    The `HEAD` method is used to get the HTTP header of a `GET` request without the body of the response.

-   `POST`

    Upload data.
    Within the API endpoints for {{site.data.keyword.cloudant_short_notm}},
    the `POST` method is used to set values,
    upload documents,
    set document values,
    and start some administration commands.

-   `PUT`

    Used to 'store' a specific resource.
    In the API for {{site.data.keyword.cloudant_short_notm}},
    `PUT` is used to create new objects,
    including databases,
    documents,
    views,
    and design documents.

-   `DELETE`

    Deletes the specified resource,
    including documents,
    views,
    and design documents.

-   `COPY`

    A special method that can be used to copy documents and objects.

If the client (such as some web browsers) does not support the use of these HTTP methods,
`POST` can be used instead with the `X-HTTP-Method-Override` request header set to the actual HTTP method.

### Method not allowed error

If you use an unsupported HTTP request type with a URL that does not support the specified type,
a [405](../api/http.html#405) error is returned,
listing the supported HTTP methods, as shown in the following example.

_Example error message in response to an unsupported request:_

```json
{
    "error":"method_not_allowed",
    "reason":"Only GET,HEAD allowed"
}
```
{:codeblock}

## JSON

{{site.data.keyword.cloudant_short_notm}} stores documents by using JSON (JavaScript Object Notation) encoding,
so anything encoded into JSON can be stored as a document.
Files containing media,
such as images,
videos,
and audio,
are called BLOBs (Binary Large OBjects),
and can be stored as attachments associated with documents.

More information about JSON can be found in the [JSON Guide](../guides/json.html).

<div id="distributed"></div>

## Distributed Systems

The {{site.data.keyword.cloudant_short_notm}} API enables applications to interact with a collaboration of numerous servers,
called a cluster.
The servers in a cluster must be in the same data center,
but can be within different 'pods' in that data center.
Using different pods helps improve the High Availability characteristics of {{site.data.keyword.cloudant_short_notm}}.

An advantage of clustering is that when you need more computing capacity,
you add more servers.
This approach is often more cost-effective and fault-tolerant than scaling up or enhancing an existing single server.

For more information about {{site.data.keyword.cloudant_short_notm}} and distributed system concepts,
see the [CAP Theorem](../guides/cap_theorem.html) guide.

## Replication

[Replication](../api/replication.html) is a procedure followed by {{site.data.keyword.cloudant_short_notm}},
[CouchDB ![External link icon](../images/launch-glyph.svg "External link icon")](http://couchdb.apache.org/){:new_window},
[PouchDB ![External link icon](../images/launch-glyph.svg "External link icon")](http://pouchdb.com/){:new_window},
and other distributed databases.
Replication synchronizes the state of two databases so that their contents are identical.

You can replicate continuously.
This form of replication means that a target database updates every time the source database changes.
Continuous replication can be used for backups of data,
aggregating data across multiple databases,
or for sharing data.

However,
continuous replication means testing continuously for any source database changes.
This testing requires continuous internal calls,
which might impact performance or the cost of using the database.

>   **Note**: Continuous replication can result in many internal calls.
    These calls might affect costs for multi-tenant users of Cloudant systems.
    By default,
    continuous replication is not enabled.
