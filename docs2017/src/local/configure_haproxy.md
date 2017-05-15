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

# Configuring HAProxy for SSL connections

Configure HAProxy for SSL connections. The RSA key and
certificate must be protected by using appropriate access
permissions. HAProxy 1.5 includes native support for SSL
connections.
{:shortdesc}

The `haproxy.cfg` file that is delivered with Cloudant&reg; Local
includes commented-out configuration lines. You must uncomment
those lines to enable SSL.

After you modify the `haproxy.cfg` file, you must restart HAProxy.

1.  As root, open the `haproxy.cfg` file on each load balancer.

    ``` sh
    /etc/haproxy/haproxy.cfg
    ```
    {:codeblock}

2. In the `haproxy.cfg` file, uncomment the two lines in the
   example by removing the `#` at the start of the line.

    ``` sh
    #bind :443 ssl crt /etc/haproxy/certificate.pem
    #redirect scheme https if dashboard_assets !{ ssl_fc }
    ```
    {:codeblock}
