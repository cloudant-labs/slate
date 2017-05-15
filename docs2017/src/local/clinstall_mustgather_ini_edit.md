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

# Editing the mustgather.ini file


Edit the `mustgather.ini` file and update the information on the
node where you want to run the tool.
{:shortdesc}

<ol>
<li>Open the `mustgather.ini` file.</li>
<li>Update the following information on the node where you want to
    run the tool.
<ol type=a>
<li>Update the nodes in the `[cluster]` section of the file
        with the information for your cluster nodes.
<p>**Note:** Specify multiple nodes in the cluster by entering a comma-separated node name. The node name can either be the host name or the IP address. If you specify a host name, make sure to update the `hosts` file as shown in the example.</p>
<p>`nodes: db1.cloudant-local.com,db2.cloudant-local.com,db3.cloudant-local.com,lb1.cloudant-local.com`<br>
        `nodes: 192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103`</li>
<li>(Optional) Update the other information in the `[cluster]`
        section.</li>
</ol></li>
</ol>
