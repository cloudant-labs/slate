---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-10"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Configuring failover load balancers

Configure load balancing to eliminate downtime if a load balancer
fails to respond.
{:shortdesc}

A load balancer node assists with distributing Cloudant&reg; Local
requests to enable rapid response. It is possible for a load
balancer node to become unavailable, for example, as part of a
system administration activity. This task describes how to
configure extra or replacement node balancers for a Cloudant
Local system.

Assume that each load balancer has its own unique and public IP
address. A single, separate IP address is used as the actual
front-end address where all requests are directed from outside
the Cloudant Local system.

## Example load balancer configuration

IP address | System
-----------|-----------------
10.10.50.5 | Front-end system
10.10.50.6 | Load balancer 0
10.10.50.7 | Load balancer 1


<ol><li>Perform the load balancer installation task for each of the
    load balancer systems (Load Balancer 0 and Load Balancer 1).
    See [Installing load balancer nodes](clinstall_install_load_balancer_nodes.html).</li>
<li>Log in to each load balancer node as the root user.</li>
<li>Modify the `haproxy.cfg` file to identify the front-end address.</li>
<li>Change the following line: <br> 
    `listen dbfarm 0.0.0.0:80`  <br>
    to:  <br>
    `listen dbfarm 10.10.50.5:80`<br>  
    The new IP address is that of the front-end system.</li>
<li>Install the `keepalived` application on each load balancer node
    as the root user.
<ol type=a>
<li>Install `keepalived` on CentOS or RHEL by running the command:<br>
        `yum install keepalived`
</li>
<li>Install `keepalived` on Debian or Ubuntu by running the command:<br>
        `apt-get install keepalived`</li>
</ol>
</li>
<li>Create a `/etc/keepalived/keepalived.conf` file on each load
    balancer by using the following lines.

<p><code>
    ! Configuration file for keepalived<br>
    <br>
    global_defs {<br>
      notification_email {<br>
        failover@domain.com<br>
      }<br>
      notification_email_from lb@domain.com<br>
      smtp_server localhost<br>
      smtp_connect_timeout 30<br>
    }<br>
    <br>
    vrrp_instance VI_1 {<br>
       state MASTER<br>
       interface eth1<br>
       virtual_router_id 51<br>
       priority 100<br>
       advert_int 1<br>
       authentication {<br>
           auth_type PASS<br>
           auth_pass 1111<br>
       }<br>
       virtual_ipaddress {<br>
    10.10.50.5<br>
        }<br>
    }<br>
</code></p></li>
<li>Ensure that each load balancer has a unique priority value.  
<p>For example, Load Balancer 0 might be set to priority 100
    while Load Balancer 1 might be set to priority 101.</p></li>
<li>Set the `virtual_ipaddress` IP to the IP address for the
    front-end server.</li>
<li>Configure `keepalived` so that it runs automatically when the
    server starts.  
<ol type=a>
<li>Run the `chkconfig keepalived` then `service keepalived start`
        commands to install `keepalived` on CentOS or RHEL.</li>
<li>Run the `service keepalived start` command to install
        `keepalived` on Debian or Ubuntu.</li>
</ol>
</li>
<li>Verify that the front-end IP address can be accessed
    successfully by going to the IP address in a browser.</li>
<li>Verify that load balancing is working correctly.  
<ol type=a>
<li>Disconnect the highest priority load balancer.</li>
<li>Revisit the front-end IP address.</li>
</ol>
</li>
<li>Reconnect the highest priority load balancer.</li>
<li>Disconnect the lower priority load balancer.</li>
<li>Recheck that you can access the front-end IP address successfully by going to the IP address in a browser.</li>
</ol>
