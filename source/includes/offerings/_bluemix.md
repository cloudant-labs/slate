## IBM Bluemix

Cloudant is also available as an [IBM Bluemix service](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db/).
Bluemix is an open-standards, cloud platform for building, running, and managing applications.
Find out more about Bluemix,
and start using it,
at the [home page](https://console.ng.bluemix.net/).

### Bluemix Public

Cloudant on Bluemix is available as a free [Lite plan](offerings.html#lite-plan),
and as several configurations within the paid [Standard plan](offerings.html#standard-plan).

The following table summarizes the performance measures for each of the plans.

<aside class="warning" role="complementary" aria-label="indicativetierpricing">The details in the table are indicative as at September 2016.
For current values,
contact [Cloudant Support](mailto:support@cloudant.com).</aside>

<aside class="warning" role="complementary" aria-label="pricing2">All currency values in this document are in US dollars ($).</aside>

<table border="1" role="presentation">
<tr valign="top">
<td colspan="2" id="planCharacteristic"><b>Plans</b></td>
<td id="litePlan"><b>Lite</b></td>
<td colspan="4" id="standardPlan" align="center"><b>Standard</b></td>
</tr>
<tr>
<td colspan="2" id="basePrice">Base Price (per hour)</td>
<td>$0.00</td>
<td colspan="4">See <a href="http://cloudant.com/bluemix" target="_blank">Pricing details</a>.</td>
</tr>
<tr>
<td rowspan="3" valign="center" id="throughputLabel">Provisioned Throughput<br/>Capacity<br/>(per second)</td>
<td id="lookups">Lookups</td>
<td>20</td>
<td>100</td>
<td>1,000</td>
<td>5,000</td>
<td>20,000</td>
</tr>
<tr>
<td id="writes">Writes</td>
<td>10</td>
<td>50</td>
<td>500</td>
<td>2,500</td>
<td>10,000</td>
</tr>
<tr>
<td id="queries">Queries</td>
<td>5</td>
<td>5</td>
<td>50</td>
<td>250</td>
<td>1,000</td>
</tr>
<tr>
<td rowspan="2" id="diskSpace">Disk Space</td>
<td id="diskSpaceIncluded">Included</td>
<td>1 GB</td>
<td colspan="4" align="center">20 GB</td>
</tr>
<tr>
<td id="diskOverage">Disk Overage<br/>(per GB/hour)</td>
<td>Not available</td>
<td colspan="4" align="center">See <a href="http://cloudant.com/bluemix" target="_blank">Pricing details</a>.</td>
</tr>
</table>

#### Lite plan

The Lite plan is free,
but limits you to a maximum of 1GB of data storage.
There are also limits on the provisioned throughput capacity for lookups, writes and queries.

If you would like to store more than 1GB of data,
or to have a greater throughput capacity,
you should move to the [Standard plan](offerings.html#standard-plan).

#### Standard plan

The Standard plan includes 20GB of data storage.
Above 20GB,
you are charged a defined cost per GB per hour.
See the <a href="http://cloudant.com/bluemix" target="_blank">Pricing</a> information for the current cost.
On the Standard plan,
you can also change the amount of provisioned throughput capacity for lookups, writes and queries.

<div id="servicetier"></div>

You can see details of the throughput capacity within the plans available for your account,
and select the level of provisioning that you want to use,
through the Account tab of your Cloudant account Dashboard.<br/>
![Account Dashboard](images/cloudant_capacity.png)

To move to a different throughput capacity,
select the provisioning you want,
then click the `Change Capacity` button.
You are asked to confirm the change,
and reminded that the provisioning change can take up to 24 hours to complete.<br/>
![Account Dashboard](images/cloudant_capacity_change.png)

<div id="throughput"></div>

##### Provisioned throughput capacity

Throughput provision is identified and measured as one of three kinds of events:

1.	A lookup, which is a read of a specific document, based on its `_id`.
2.	A write, which is a write of an individual document, or a write due to an index build.
3.	A query, which is a request made to one of the Cloudant query endpoints, including the following types:
	-	Primary Index ([`_all_docs`](database.html#get-documents))
	-	MapReduce View ([`_view`](creating_views.html#using-views))
	-	Search Index ([`_search`](search.html#queries))
	-	Geospatial Index ([`_geo`](geo.html#querying-a-cloudant-geo-index))
	-	Cloudant Query ([`_find`](cloudant_query.html#finding-documents-using-an-index))
	-	Changes ([`_changes`](database.html#get-changes))

The measurement of throughput is a simple count of the number of events of each type,
per second,
where the second is a _sliding_ window.
If your account exceeds the number of throughput events that are provisioned for the plan,
requests are rejected until the number of events within the sliding window
no longer exceeds the number provisioned.
It might help to think of the sliding one-second window as being any consecutive period of 1,000 milliseconds.

For example,
if you are on the Standard plan and have provisioned 200 lookups per second,
your account might make a maximum of 200 lookup requests during a consecutive period of 1,000 milliseconds (1 second).
Subsequent lookup requests made during the sliding 1,000 millisecond period
are rejected until the number of lookup requests in that period drops below 200 again.

When a request is rejected because the number of events is exceeded,
applications receive an HTTP response:
[`429` Too Many Requests](http.html#429).

Recent versions of the supported client libraries (for [Java](libraries.html#java),
[node.js](libraries.html#node.js),
and [Python](libraries.html#python) languages) have an ability to handle a `429` response.
For example,
the Java library throws a [`TooManyRequestsException`](http://static.javadoc.io/com.cloudant/cloudant-client/2.5.1/com/cloudant/client/org/lightcouch/TooManyRequestsException.html).

By default,
the supported client libraries do not automatically attempt to retry
a request when a `429` response is received.

<!--
It is possible to configure the client libraries to retry a request automatically,
however this is only suitable for temporary rather than frequent transgressions.
-->

It is better to ensure that your application handles `429` responses correctly.
The reason is that the number of retries is limited;
regularly transgressing the number of requests is a strong indicator
that you should move to a different plan configuration.

<aside class="warning" role="complementary" aria-label="movingFromNonCCM">If you are migrating an existing application,
it might not be configured to handle a `429` response correctly.
You should check this as part of your migration verification.</aside>

In summary,
you must ensure that your application is able to handle a `429` response correctly.

##### Disk Space Included

This value is the storage capacity included in the plan.
It is used for both data and index storage.

##### Disk Overage

All Standard and Lite plan service instances are monitored for disk space used.
If the account uses more than the amount of storage that is provided in your plan configuration,
it is considered to 'overflow'.
An overflow causes the account to be billed at the indicated price for each extra GB used beyond the plan allocation.

The extra amount of money that you must pay for using more disk space than is provided in the plan is called an 'overage'.
Overage is calculated on an hourly basis.
It is not possible to overflow the disk space available in the Lite plan.

For example,
assume that your Standard plan instance increases disk usage to 107 GB for half a day (12 hours).
This change means your instance caused an overflow of 87 GB more than the 20 GB plan allocation,
for 12 hours.
Therefore,
you would be billed an overage charge based on 87 GB x 12 hours = 1044 GB hours for that extra space.

Overage is calculated by using the maximum number of GB above the plan allocation during a particular hour within the billing cycle.

##### A worked overage example

Assume that you start a month of 30 days with a Standard plan service instance that uses 9 GB of storage.
Next,
your storage increases to 21.5 GB for 15 minutes during the hour beginning at 02:00 of day 3.
The instance drops back to 9.5 GB for the next 10 minutes of hour 02:00,
then increases to 108 GB for the next 25 minutes of hour 02:00.
Finally,
your instance finishes the hour and indeed the rest of month by dropping down to 28 GB.

This pattern means the maximum number of GB above the plan allocation was 88 GB during hour 2 of day 3.
For hour 03:00 of day 3,
and for the rest of the month,
your instance was 8 GB above the plan allocation.

Therefore,
for hour 02:00 of day 3,
you would be billed an overage based on 88 GB x 1 hour = 88 GB hours.

For hour 03:00 of day 3 to the end of day 3,
you would be billed an overage based on 8 GB x 21 hours = 168 GB hours.

For hour 00:00 of day 4 to the end of the month (of 30 days),
you would be billed an overage based on 8 GB x 24 hours x 27 days = 5184 GB hours.

The total overage bill for the month would be based on a total of 88 + 168 + 5184 = 5440 GB hours.

##### Locations

By default,
all plans are based on multi-tenant clusters.
As part of your plan selection,
you can choose from the following Bluemix Public regions:

-	US South
- United Kingdom
- Sydney

##### Security, Encryption, and Compliance

All plans are provided on servers with [at-rest](https://en.wikipedia.org/wiki/Data_at_rest) disk encryption.
Access is encrypted over a network connection by using HTTPS.
For more detail,
see [DBaaS Security](https://cloudant.com/product/cloudant-features/dbaas-security/).

The plans also offer [Security Compliance Certification](https://cloudant.com/product/cloudant-features/cloudant-compliance/).
[HIPAA](https://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act) compliance requires a [single-tenant environment](offerings.html#locations),
so request this environment before provisioning.

##### High Availability, Disaster Recovery, and Backup

To provide High Availability (HA) and Disaster Recovery (DR) within a data center,
all data is stored in triplicate across three separate physical servers in a cluster.
You can provision accounts in multiple data centers,
then use continuous data replication to provide HA/DR across data centers.

Cloudant data is not automatically backed up.
You can request enablement of an [incremental backup feature](https://docs.cloudant.com/backup-guide.html),
or alternatively implement your own solution by using one of several possible techniques that are described [here](https://developer.ibm.com/clouddataservices/2016/03/22/simple-couchdb-and-cloudant-backup/).  

#### Monitoring usage

Information about your usage is available in the Usage pane of the Activity tab within your Cloudant Dashboard.<br/>
![Monitoring usage on the dashboard](images/cloudant_usage.png).

Details are provided there,
illustrating your current [throughput](offerings.html#throughput),
and quantity of [stored data](offerings.html#disk-space-included).

If your monitoring indicates that a change to the provisioning in your plan might be advisable,
for example if you are frequently approaching the maximum number of database lookups,
then you can modify the provisioning through the [Service pane](offerings.html#servicetier) on the Account tab of the Dashboard.

#### Hardware specification

All plans are implemented on multi-tenant clusters.
All data is stored in triplicate,
across three separate physical nodes for High Availability and Data Recovery.

#### Support

Support for Standard plan service instances is optional.
It is provided by purchasing "Bluemix Standard Support".
Support is not available for the Lite plan.

A pricing calculator for Bluemix Standard Support is available
[here](https://console.ng.bluemix.net/?direct=classic/#/pricing/cloudOEPaneId=pricing&paneId=pricingSheet).
Information about the details of the Support Service Level Agreement (SLA) is available
[here](http://www-03.ibm.com/software/sla/sladb.nsf/pdf/6606-08/$file/i126-6606-08_05-2016_en_US.pdf).

### Bluemix Dedicated

Cloudant DBaaS Enterprise on single tenant dedicated hardware is available in a [Bluemix Dedicated](http://www.ibm.com/cloud-computing/bluemix/dedicated/) configuration.

### Bluemix Local

Cloudant on Bluemix Local is a service that is managed inside your data center. This service offers peace of mind by having Cloudant in-house without having to worry about day-to-day operations and maintenance.
Cloudant on Bluemix Local is delivered as-a-service,
and in constant collaboration with your IT team.

#### Requirements

To ensure that Cloudant on Bluemix Local installs correctly, you must meet the following requirements.

<ul><li>Customer-owned environment requirements
<ul><li>VMWare versions 5.5 or 6.0. </li>
<li>MTU set to 9000 on all virtual switches.</li></ul></li></ul>

<ul><li>Cloudant-owned deployment and maintenance requirements
<ul><li>The Bluemix Local platform requires a small internal cluster to run.  This cluster is required and is not available in your Bluemix catalog. If you would like Cloudant to be listed as a local service in the Bluemix catalog, you must purchase a separate cluster.</li>
<li>External internet access via the Bluemix tether.</li>
<li>A Logmet deployment sized to support Cloudant. Logmet is based on the ELK stack and houses all of the logs created on the local Cloudant clusters.  This data stays local to your environment but is accessible by the Cloudant team.</li></ul></li></ul>

#### Hardware Requirements for Cloudant on Bluemix Local
<table>
<tr>
<th>Type</th>
<th>Count</th>
<th>Optional?</th>
<th>VM name format</th>
<th>min vCPU</th>
<th>recommended vCPU</th>
<th>min RAM (GB)</th>
<th>recommended RAM (GB)</th>
<th>Disk-OS (GB)</th>
<th>Disk Config-OS</th>
<th>min Disk-Data (GB)</th>
<th>recommended Disk-Data (GB)</th>
<th>Disk Config-Data</th>
<th>Network (Gbps)</th>
</tr>

<tr>
<td>Infra</td>
<td>1</td>
<td>No</td>
<td>infra1.bml-&lt;customer&gt;</td>
<td>8</td>
<td>8</td>
<td>16</td>
<td>16</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>3000</td>
<td>3000</td>
<td>VMDK-thin/independent persistent</td>
<td>1</td>
</tr>

<tr>
<td>SAPI</td>
<td>2</td>
<td>No</td>
<td>sapi&lt;#&gt;.bml-&lt;customer&gt;</td>
<td>4</td>
<td>4</td>
<td>4</td>
<td>4</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>N/A</td>
<td>N/A</td>
<td>N/A</td>
<td>1</td>
</tr>

<tr>
<td>Load Balancer (Bluemix Ops Cluster)</td>
<td>2</td>
<td>No</td>
<td>lb&lt;#&gt;.bml-ops-&lt;customer&gt;001</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>N/A</td>
<td>N/A</td>
<td>N/A</td>
<td>1</td>
</tr>

<tr>
<td>Load Balancer (Customer Cluster)</td>
<td>2</td>
<td>No</td>
<td>lb&lt;#&gt;.bml-&lt;customer&gt;001</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>N/A</td>
<td>N/A</td>
<td>N/A</td>
<td>1</td>
</tr>

<tr>
<td>DB Node (Bluemix Ops Cluster)</td>
<td>3</td>
<td>No</td>
<td>db&lt;#&gt;.bml-ops-&lt;customer&gt;001</td>
<td>8</td>
<td>8</td>
<td>16</td>
<td>16</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>800</td>
<td>800</td>
<td>VMDK-thick eager zeroed/independent persistent</td>
<td>1</td>
</tr>

<tr>
<td>DB Node (Customer Cluster) </td>
<td>3</td>
<td>No</td>
<td>db&lt;#&gt;.bml-&lt;customer&gt;001</td>
<td>8</td>
<td>48</td>
<td>16</td>
<td>64</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>800</td>
<td>1600</td>
<td>VMDK-thick eager zeroed/independent persistent</td>
<td>1</td>
</tr>

<tr>
<td>Load Balancer (Backup Cluster)</td>
<td>2</td>
<td>Yes</td>
<td>lb&lt;#&gt;.bml-&lt;customer&gt;-bk001</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>8</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>N/A</td>
<td>N/A</td>
<td>N/A</td>
<td>1</td>
</tr>

<tr>
<td>DB Node (Backup Cluster)</td>
<td>3</td>
<td>Yes</td>
<td>db&lt;#&gt;.bml-&lt;customer&gt;-bk001</td>
<td>8</td>
<td>24</td>
<td>16</td>
<td>64</td>
<td>10</td>
<td>VMDK-thick eager zeroed</td>
<td>800</td>
<td>18000</td>
<td>VMDK-thin/independent persistent</td>
<td>1</td>
</tr>
</table>

#### Hardware Requirements for Logmet to support Cloudant on Bluemix Local
<table>
<tr>
<th>Type</th>
<th>Count</th>
<th>Optional?</th>
<th>min vCPU</th>
<th>recommended vCPU</th>
<th>min RAM (GB)</th>
<th>recommended RAM (GB)</th>
<th>min Disk (GB)</th>
<th>recommended Disk (GB)</th>
</tr>
<tr>
<td>Logmet Core</td>
<td>3</td>
<td>No</td>
<td>4</td>
<td>4</td>
<td>20</td>
<td>20</td>
<td>900</td>
<td>900</td>
</tr>
<tr><td>Logmet HAProxy
</td>
<td>2</td>
<td>No</td>
<td>1</td>
<td>1</td>
<td>4</td>
<td>4</td>
<td>40</td>
<td>40</td></tr>
<tr>
<td>Logmet Manager
</td>
<td>1</td>
<td>No</td>
<td>1</td>
<td>1</td>
<td>4</td>
<td>4</td>
<td>40</td>
<td>40</td></tr>
<tr><td>Logmet Expansion
</td>
<td>3</td>
<td>Yes</td>
<td>3</td>
<td>3</td>
<td>12</td>
<td>12</td>
<td>600</td>
<td>600</td>
</tr>
<td>CFS Ops
</td>
<td>1</td>
<td>No</td>
<td>2</td>
<td>2</td>
<td>8</td>
<td>8</td>
<td>350</td>
<td>350</td>
</tr>
</table>

#### Cloudant virtual machine distribution and physical host recommendations			
These recommendations assume that you are using the required hardware for Cloudant on Bluemix Local and a backup cluster.		

<table>
<tr>
<th>Host</th>
<th>vCPU</th>
<th>RAM used (GB)</th>
<th>VMs deployed (number of cores)</th>
</tr>

<tr><td>1</td>
<td>48</td>
<td>64</td>
<td>db1.bml-&lt;customer&gt;001</td>
</tr>
<tr><td>2</td>
<td>48</td>
<td>64</td>
<td>db2.bml-&lt;customer&gt;001</td>
</tr>
<tr><td>3</td>
<td>48</td>
<td>64</td>
<td>db3.bml-&lt;customer&gt;001</td>
</tr>
<tr><td>4</td>
<td>48</td>
<td>96</td>
<td>lb1.bml-&lt;customer&gt;001
lb1.bml-ops-&lt;customer&gt;001
db1.bml-ops-&lt;customer&gt;001
db1.bml-&lt;customer&gt;-bk0011</td>
</tr>
<tr><td>5</td>
<td>48</td>
<td>96</td>
<td>lb2.bml-&lt;customer&gt;001
lb2.bml-ops-&lt;customer&gt;001
db2.bml-ops-&lt;customer&gt;001
db2.bml-&lt;customer&gt;-bk0011</td>
</tr>
<tr><td>6</td>
<td>44</td>
<td>92</td>
<td>lb1.bml-&lt;customer&gt;-bk001
db3.bml-ops-&lt;customer&gt;001
db3.bml-&lt;customer&gt;-bk001
sapi1.bml-&lt;customer&gt;</td>
</tr>
<tr><td>7</td>
<td>20</td>
<td>38</td>
<td>lb2.bml-&lt;customer&gt;-bk001
sapi2.bml-&lt;customer&gt;
infra1.bml-&lt;customer&gt;</td>
</tr>
</table>

#### Frequently Asked Questions about Cloudant on Bluemix Local

##### How is Cloudant for Bluemix Local deployed?

You must download the OVA and ISO files and upload them to the datastore. You then
provide your network, datastore, and locations of the OVA and ISO files to Cloudant. Cloudant runs a script and wraps the ovftool, which creates VMs that are ISO mounted and use the proper settings. A startup script, packaged in the OVA, configures the networking and sets up reverse SSH tunneling. The remaining provisioning tasks are run by Chef configuration management.

##### Where are the Cloudant virtual machines deployed?

The VMs deploy within the private VLANs inside your Bluemix Local deployment.

##### Can Cloudant be deployed within a normal customer maintenance window?

Deploying Cloudant in your data center is a lengthy process. Currently, Cloudant needs approximately 1-2 weeks to deploy and verify your installation. Support is working to improve the deployment and automation process.

##### Does Cloudant follow the same Bluemix CR/DR process?

Cloudant does not follow the Bluemix CR/DR process.

##### Can I decide when changes are deployed? Can I review the changes before they are deployed?

Cloudant is delivered as a service and manages thousands of
machines between public DBaaS and Bluemix Local. Support uses [`Chef`](https://en.wikipedia.org/wiki/Chef_(software)) to handle configuration management across
the infrastructure, including clusters in Bluemix Local. As a result, non-disruptive changes are delivered
regularly multiple times a week and potentially several times per day. Therefore, changes and updates are not
bound to predetermined maintenance windows. Cloudant does not require customer sign-off on
changes and updates to their clusters in Bluemix Local.

##### What about changes that are potentially disruptive?

While the vast majority of updates are not disruptive, Cloudant may deploy changes that cause a temporary outage. These outages are rare. If an outage occurs, Cloudant will coordinate with you to find a maintenance window that minimizes any disruption to your business.

##### What name displays in the catalog for Cloudant service?

The Cloudant service name displays as "Local".

##### How does Cloudant obtain IP addresses for the virtual machines?

Cloudant is on the private network inside Bluemix Local and only requires private IPs, which are provided by the Bluemix team.

##### Does Cloudant have an architecture diagram for deployments in Bluemix Local?

![Bluemix Local architecture diagram](images/bml_architecture_diagram.png).

##### Who is responsible for the Cloudant service broker?

Cloudant makes the appropriate changes to the service broker. If you have an existing dedicated cluster, Cloudant configures the broker to point to the new local cluster and follows the normal Bluemix
CR/DR process.

##### How will Cloudant operations access my Bluemix Local environment?

The Cloudant team uses the existing tether/relay provided by Bluemix. No new networking
requirements are required for Cloudant to access your environment.

##### What is Logmet? Why does Cloudant need it?

Logmet is our logging infrastructure. Logmet requires its own hardware resources. Cloudant sends logs to
Logmet so that your information can be stored locally. Logmet is a separate deployment. You do not need one
Logmet deployment per Cloudant cluster. All Cloudant clusters, within one Bluemix Local environment, share the same Logmet instance.

##### Where do you send metrics and monitoring information?

Cloudant receives metrics and monitoring information through the tether. Without it, we cannot properly maintain your local cluster.

##### How is VMware clustering set up for Cloudant, Logmet, and Bluemix?

Cloudant must be on a VMware cluster separate from Bluemix to prevent noisy neighbor
problems. Logmet must be in the same cluster with Bluemix.

##### How are virtual machines distributed across hosts?

Cloudant determines which VMs deploy and on which hosts. The goal is to keep database nodes and
load balancers separate, so if one host goes down, the cluster continues to operate. Research is in progress to  determine how to enable DRS with specific rules in order to keep VMs separate.

##### Does Cloudant feed logs to the QRadar deployment that is included with Bluemix Local?

Yes. Cloudant sends `auth` and `auditd` logs to QRadar and stores them for one year.

##### How does backup work?

Cloudant offers a backup service that schedules and runs incremental backups of your data. It is strongly
recommended that you purchase a separate cluster, specifically dedicated to storing backup data. The Cloudant backup cluster must be inside the same Bluemix Local environment. More information on backing up your data can be found [here](https://docs.cloudant.com/backup-guide.html).

Both the customer and ops cluster can backup to the same location. If you do not want to use the Cloudant
backup product, you are responsible for backing up your data.

##### Where can I find Bluemix Local documentation?

Bluemix documentation is located [here](https://console.ng.bluemix.net/docs/local/index.html#local).
