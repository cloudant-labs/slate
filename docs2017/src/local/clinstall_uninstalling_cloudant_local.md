---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-20"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Uninstalling Cloudant Local

Uninstall Cloudant&reg; Local with the `cast system uninstall` command.
{:shortdesc}


<ol>
<li>Stop the database node before you run the `cast system uninstall` command.
<p>`cast node stop`</p></li>
<li>To uninstall Cloudant Local, log in with the same user
    ID that you used during your first installation.
    <p>For example, if you installed Cloudant Local as the
    root user, you must uninstall Cloudant Local as the
    root user.</p></li>
<li>Run the `cast system uninstall` command to uninstall Cloudant
    Local services and the CAST tool.
    <p>`cast system uninstall`</p></li>
<li>Verify that no processes are running.
<p>If any processes are running, reboot the system to clean up hanging processes.</p>
<ol type="a">
<li>Log in as the root user or a user with sudo privileges.</li>
<li>Run the `sudo reboot` command.
<p>`sudo reboot`</p>
<p>Cloudant Local is uninstalled.</p></li>
</ol></li>
</ol>
