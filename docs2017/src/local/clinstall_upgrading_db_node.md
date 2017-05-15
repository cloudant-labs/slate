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

# Upgrading a database node

Follow these steps to upgrade each Cloudant&reg; Local database node.
{:shortdesc}

<ol>
<li>Put the database node in maintenance mode.
<ol type=a>
<li>From the `/opt/cloudant` directory, put the database node
        in maintenance mode by running the command.
        <p>`cast node maintenance --true`</p></li>
<li>Verify that the database node is in maintenance mode: `curl localhost:5984/_up`.
<p>You see this response.</p>
<p>`{"status":"maintenance_mode"}`</p></li>
<li>Verify that this node is not available for traffic from
        your load balancer URL.
        <p>`http://load_balancer/_haproxy`</p>
<p>The node status must be stopped for maintenance.</p></li>
</ol>
</li>
<li>Uninstall the existing Cloudant Local version binary files.
<ol type=a>
<li>Uninstall the current version by running the command.
<p>`cast system uninstall`</p>
<p>This command also stops the services.</p></li>
<li>Run the InstallShield uninstall command.
<p>`/root/cloudant/uninstall/uninstall.bin`</p></li>
<li>Check for Cloudant processes.
<p>`ps -ef | grep clo`</p></li>
<li>Stop any Cloudant processes that are running.
<p>`kill -9 (pid)`</p></li>
</ol>
</li>
<li>Install the database node by using the steps in [Installing the
    first database node](clinstall_install_first_db_node.html).

<p>**Note:** Ensure that when you run the `cast system install` command you start the node with a maintenance mode flag and pass the current cluster configuration to your `dbnode.yaml` file.</p>
<ol type=a>
<li>Find the current values of database node cluster
        credentials and IDs from the `local.ini`, `vm.args`, and
        `default.ini` files on other nodes or from the backed-up
        directories, such as `/opt/cloudant/etc.bak`.</li>
<li>Configure these values as-is in the `dbnode.yaml` file.
<p>Use encrypted or hashed values for fields `admin`,
        `cloudant`, `httpd_auth` and `cookie`. Leave the `uuid` and
        `monitor_role` values as `open_ssl`.</p>
</li>
<li>After you configure the `dbnode.yaml` file, you can
        distribute and use it for other database node upgrades.
<p>For example, you can get a sample of `dbnode.yaml` from
        `/opt/cloudant/cast/samples/dbnode.yaml` and run the
        following command.</p>
<p>`cast system install --maintenance -db -c /{path_to}/dbnode.yaml`</p>
</li>
</ol>  
</li>
<li>Check status of the database node update.
<ol type=a>
<li>Verify the status of the database node.

<p>`curl -X GET http://localhost:5984`</p>
<p>The response shows the new version.</p>

<p>        `{`<br>
            `"couchdb": "Welcome",`<br>
            `"version": "2.0.0",`<br>
            `"vendor": {`<br>
                `"name": "IBM Cloudant",`<br>
                `"version": "1.1.0",`<br>
                `"variant": "local"`<br>
            `},`<br>
            `"features": [`<br>
                `"geo"`<br>
            `]`<br>
        `}`</li>
<li>Verify that the database node is in maintenance mode and
        is not receiving traffic on the load balancer.
<p>`cast node maintenance`</p>
<p>The response shows the status of the node.</p>
<p>`The node is IN maintenance mode.`</p></li>
<li>Verify the status of the upgraded node as a member of the
        cluster.
<p>`cast cluster status`</p>
<p>The response lists all the cluster nodes.</p></li>
<li>Check the health of the database node by using the
        Weatherreport application, [Monitor cluster health with
        Weatherreport](clinstall_checking_health_cluster_with_weatherreport.html).</li>
</ol>
</li>
<li>Bring the database node out of maintenance mode and check its
    availability.
<ol type=a>
<li>Run the following command to bring the database node out
        of maintenance mode.
<p>`cast node maintenance --false`</p>
<p>The response shows the status of the node.</p>
<p>`The node is OUT of maintenance mode.`</p>
        </li>
<li>Verify that the database node is up and available for
        traffic from your load balancer.
<p>`http://{load_balancer}/_haproxy`</p>
<p>If the upgrade was successful, the response shows that
        the node is up and available.</p></li>
</ol>
</li>
</ol>
