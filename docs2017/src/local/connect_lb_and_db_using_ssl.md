---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-09"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Connecting load balancer and database nodes by using SSL

If you use SSL for communication between your Cloudant&reg; Local
load balancer and database nodes, enable the secure communication
on each load balancer node by making these load balancer
configuration changes.
{:shortdesc}

<ol><li>Copy the `ca.pem` file to each load balancer node.
<p>For more information about creating the `ca.pem` file, see
    [Generating the certificate authority file for a database node](generate_db_ca.html).</p>
    
</li>
<li>Update the `haproxy.cfg` file.
<ol type="a"><li>Find the section label.
<p>
`######`<br>
`# NOTE: Specify the appropriate host names and IP addresses below.`<br>
`######`</p></li>
<li>Verify that all the database nodes are included in the list.</li>
<li>For each server, change the port from `5984` to `6984`.</li>
<li>Add the following text to the end of each "server" line.
<p>`ssl verify required ca-file /<file_location>/ca.pem`
</p></li></ol>
<li>Save and close the `haproxy.cfg` file.</li>
<li>Restart **haproxy**.</li></ol>
