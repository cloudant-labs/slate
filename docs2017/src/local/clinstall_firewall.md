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

# Configuring firewall ports

Cloudant&trade; Local requires that specific ports must be open before the 
load balancer and  database nodes can communicate with each other.
If you plan to use a firewall, you must  explicitly open the 
ports required by Cloudant Local.
You can use Linux network configuration commands, 
such as `iptables` and `yast`, 
or CloudantLocal's Cluster Admin and Support Tool (CAST).
{:shortdesc}

See [Cloudant Local architecture and ports](clinstall_architecture_ports.html) for more information.

<!-- reset markdown parser -->

<blockquote>
**Note:** Running the CAST firewall command enables the firewall on your server if it is not already on. As a result, you might be locked out of your SSH session if you do not open the SSH ports first.
<p>If you use SUSE Linux Enterprise Server (SLES) platform, you must take special precautions and ensure SSH port 22 is open before you run the CAST firewall commands. These ports are not open by default on this platform.</p>
<p>From the command line, you can run these commands to open the SSH ports on SLES platform.
<code>systemctl enable SuSEfirewall2.service
systemctl start SuSEfirewall2.service
yast firewall services add tcpport=22 zone=EXT</code></p>
<p>Alternatively, you can run the `yast firewall` command on SLES and add the SSH Service to open the SSH ports.</p>
</blockquote>

Use the following instructions to open or remove the Cloudant Local ports.

1.  Open the Cloudant Local ports in the firewall.

    ``` sh
    cast system firewall --open
    ```
    {:codeblock}

2.  Remove any previously added Cloudant Local ports from the firewall.

    ``` sh
    cast system firewall --close
    ```
    {:codeblock}
