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

# Changing the default directories

The Cloudant&reg; Local packages create the Cloudant
software and database directories.
The software
directory contains the Cloudant binary files, scripts,
configuration files, and other executable files. The database
directory stores your data files.
{:shortdesc}

The packages create the Cloudant Local software and database
directories in the following locations.

*  The software is installed in a directory named `/opt/cloudant`.
*  The database is installed in a directory named `/srv/cloudant`.

<code></code>

<ol><li>Move these directories, if needed, to another drive or
    partition by creating at least one mount point for the
    Cloudant software and database directories.
<ol type=a><li>If you want the Cloudant software and database directories on the same mount point, create one mount point for the two directories.</li>
<li>If you want the Cloudant software and database directories on separate mount points, create two mount points, one for the software directory and another for the database directory.
</li></ol>
</li>
<li>(Optional) Move the database location by running <code>cast database relocate</code>.
<ol type=a><li>Display the help text by running the help command, <code>cast database relocate --help</code>.
</li>
<li>Ensure that the new directory location is owned by `cloudant:cloudant` and is applied to all database nodes with the same path and name.</li>
</ol></li> 
<li>Create the following Cloudant directories on at least one mount point.
<p>To install Cloudant Local on a mount point, or move the
    product to a mount point after it is installed, install
    Cloudant Local on a partition other than your root partition.</p>
<ol type=a><li>Make a Cloudant software directory named <code>/<your_mount_point>/opt/</code>.
<p>The <code>/cloudant</code> directory is automatically appended.</p></li>
<li>Make a Cloudant database directory named <code>/<your_mount_point>/srv/cloudant</code>.
<p>The <code>/cloudant</code> directory is automatically appended.</p>
<p>For example, if your mount point for both directories is <code>/export/local</code>, use the following commands to create the
    Cloudant directories.</p>
<p>**Note**: The first command makes the Cloudant software directory on the mount point. The second command makes the Cloudant database directory on the mount point. You can put both directories on one mount point, or you can put the two directories on separate mount points.
</p>
<p><code>mkdir /export/local/opt/cloudant<br>
mkdir /export/local/srv/cloudant</code></p> </li>
      </ol></li>

<li>Install Cloudant Local on each database or load balancer node in your implementation. See [Installing a cluster](clinstall_install_a_cluster.html).</li>   
</ol>
