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

# Managing the Metrics database

The metrics database will grow in size over time. Depending on
your retention requirements, you can manage growth and remove old
data as described here.
{:shortdesc}


<ol>
<li> Discard metrics data.
<p>**Note:** If you discard metrics data, you lose the performance data that has been collected to date. You will no longer be able to view the performance data from the Metrics dashboard. After this operation, disk space in the database will be available again, and new data will be collected as usual.</p>
<ol type=a>
<li>Stop the Metrics service on all database nodes.
<p>`sv stop cloudant-local-metrics`</p></li>
<li>Delete the Metrics database. 
    <p>You can delete the Metrics database from the Cloudant
    dashboard.</p></li>
<li>Create a Metrics database manually and name it `metrics`. 
    <p>You can create a new database from the Cloudant dashboard.</p></li>
<li>Restart the Metrics service on all database nodes.
<p>`sv start cloudant-local-metrics`</p>
<p>You can access the new metrics data from the Metrics dashboard via the URL.</p></li>
</ol>
</li>
<li>Keep old metrics data.
<p>**Note:** With this option, the performance data collected to date are preserved and can be viewed from the Metrics dashboard. You can delete the data later if you need more disk space.</p>

<ol type=a>
<li>Create an empty second Metrics database on the cluster and name it `metrics2`.
<p>You can create an empty database from the Cloudant dashboard.</p></li>
<li>Log in as the `root` user.</li>
<li>Stop the Metrics service.
<p>`sv stop cloudant-local-metrics`</p></li>
<li>Update the `metrics.ini` file from `/opt/cloudant/etc` to specify the new Metrics database, `metrics2`, and save the file.</li>
<li>Restart the Metrics service on all database nodes.
<p>`sv start cloudant-local-metrics`</p>
<p>You can view new metrics data from the Metrics dashboard via the URL.</p></li>
<li>In the Cloudant dashboard, enter `metrics2` as the database name or `metrics` to view older data.
<p>Depending on your retention requirements, you can keep the Metrics database and delete it later when it is not needed.</p>
<p>**Note:** In addition to the metrics database, the stats database will grow in size over time although at a slower rate. The IOQ application periodically dumps its internal stats to disk via the stats database. Currently, Cloudant Local does not use that data. You can delete the database and not incur any loss of functionality. However, you might notice an error in the log that says the database does not exist. To prevent the error, you can recreate a new empty stats database.</p>
<p>To manage the Cloudant Metrics application, see [Cloudant Metrics application](clinstall_config_metrics_app.html).</p>
</li>
</ol>
</li>
</ol>
