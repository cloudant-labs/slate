## Bluemix Local

Cloudant on Bluemix Local is a service that is managed inside your data center. This service offers peace of mind by having Cloudant in-house without having to worry about day-to-day operations and maintenance.
Cloudant on Bluemix Local is delivered as-a-service,
and in constant collaboration with your IT team.

### Requirements

To ensure that Cloudant on Bluemix Local installs correctly, you must meet the following requirements.

<ul><li>Customer-owned environment requirements
<ul><li>VMWare versions 5.5 or 6.0. </li>
<li>MTU set to 9000 on all virtual switches.</li></ul></li></ul>

<ul><li>Cloudant-owned deployment and maintenance requirements
<ul><li>The Bluemix Local platform requires a small internal cluster to run.  This cluster is required and is not available in your Bluemix catalog. If you would like Cloudant to be listed as a local service in the Bluemix catalog, you must purchase a separate cluster.</li>
<li>External internet access via the Bluemix tether.</li>
<li>A Logmet deployment sized to support Cloudant. Logmet is based on the ELK stack and houses all of the logs created on the local Cloudant clusters.  This data stays local to your environment but is accessible by the Cloudant team.</li></ul></li></ul>

### Hardware Requirements for Cloudant on Bluemix Local

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

### Hardware Requirements for Logmet to support Cloudant on Bluemix Local

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

### Cloudant virtual machine distribution and physical host recommendations

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

### Frequently Asked Questions about Cloudant on Bluemix Local

#### How is Cloudant for Bluemix Local deployed?

You must download the OVA and ISO files and upload them to the datastore. You then
provide your network, datastore, and locations of the OVA and ISO files to Cloudant. Cloudant runs a script and wraps the ovftool, which creates VMs that are ISO mounted and use the proper settings. A startup script, packaged in the OVA, configures the networking and sets up reverse SSH tunneling. The remaining provisioning tasks are run by Chef configuration management.

#### Where are the Cloudant virtual machines deployed?

The VMs deploy within the private VLANs inside your Bluemix Local deployment.

#### Can Cloudant be deployed within a normal customer maintenance window?

Deploying Cloudant in your data center is a lengthy process. Currently, Cloudant needs approximately 1-2 weeks to deploy and verify your installation. Support is working to improve the deployment and automation process.

#### Does Cloudant follow the same Bluemix CR/DR process?

Cloudant does not follow the Bluemix CR/DR process.

#### Can I decide when changes are deployed? Can I review the changes before they are deployed?

Cloudant is delivered as a service and manages thousands of
machines between public DBaaS and Bluemix Local. Support uses [`Chef`](https://en.wikipedia.org/wiki/Chef_(software)) to handle configuration management across
the infrastructure, including clusters in Bluemix Local. As a result, non-disruptive changes are delivered
regularly multiple times a week and potentially several times per day. Therefore, changes and updates are not
bound to predetermined maintenance windows. Cloudant does not require customer sign-off on
changes and updates to their clusters in Bluemix Local.

#### What about changes that are potentially disruptive?

While the vast majority of updates are not disruptive, Cloudant may deploy changes that cause a temporary outage. These outages are rare. If an outage occurs, Cloudant will coordinate with you to find a maintenance window that minimizes any disruption to your business.

#### What name displays in the catalog for Cloudant service?

The Cloudant service name displays as "Local".

#### How does Cloudant obtain IP addresses for the virtual machines?

Cloudant is on the private network inside Bluemix Local and only requires private IPs, which are provided by the Bluemix team.

#### Does Cloudant have an architecture diagram for deployments in Bluemix Local?

![Bluemix Local architecture diagram](images/bml_architecture_diagram.png).

#### Who is responsible for the Cloudant service broker?

Cloudant makes the appropriate changes to the service broker. If you have an existing dedicated cluster, Cloudant configures the broker to point to the new local cluster and follows the normal Bluemix
CR/DR process.

#### How will Cloudant operations access my Bluemix Local environment?

The Cloudant team uses the existing tether/relay provided by Bluemix. No new networking
requirements are required for Cloudant to access your environment.

#### What is Logmet? Why does Cloudant need it?

Logmet is our logging infrastructure. Logmet requires its own hardware resources. Cloudant sends logs to
Logmet so that your information can be stored locally. Logmet is a separate deployment. You do not need one
Logmet deployment per Cloudant cluster. All Cloudant clusters, within one Bluemix Local environment, share the same Logmet instance.

#### Where do you send metrics and monitoring information?

Cloudant receives metrics and monitoring information through the tether. Without it, we cannot properly maintain your local cluster.

#### How is VMware clustering set up for Cloudant, Logmet, and Bluemix?

Cloudant must be on a VMware cluster separate from Bluemix to prevent noisy neighbor
problems. Logmet must be in the same cluster with Bluemix.

#### How are virtual machines distributed across hosts?

Cloudant determines which VMs deploy and on which hosts. The goal is to keep database nodes and
load balancers separate, so if one host goes down, the cluster continues to operate. Research is in progress to  determine how to enable DRS with specific rules in order to keep VMs separate.

#### Does Cloudant feed logs to the QRadar deployment that is included with Bluemix Local?

Yes. Cloudant sends `auth` and `auditd` logs to QRadar and stores them for one year.

#### How does backup work?

Cloudant offers a backup service that schedules and runs incremental backups of your data. It is strongly
recommended that you purchase a separate cluster, specifically dedicated to storing backup data. The Cloudant backup cluster must be inside the same Bluemix Local environment. More information on backing up your data can be found [here](https://docs.cloudant.com/backup-guide.html).

Both the customer and ops cluster can backup to the same location. If you do not want to use the Cloudant
backup product, you are responsible for backing up your data.

#### Where can I find Bluemix Local documentation?

Bluemix documentation is located [here](https://console.ng.bluemix.net/docs/local/index.html#local).
