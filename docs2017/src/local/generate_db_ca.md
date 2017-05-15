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

# Generating the certificate authority file for a database node

If you are using self-signed certificates, generate a certificate
authority file for the database nodes.
{:shortdesc}

If you are using certificates that are provided by a third party,
you can proceed directly to [Copying the SSL security files to the database node](ssl_copy_files.html).

To use self-signed certificates on database nodes, you must
generate a certificate authority (CA) file. Only one CA file is
required. The same file is used by all the database nodes and all
the load balancer nodes within your cluster. The file can be
generated on any server.

To generate a self-signed CA file, use the following commands:

``` sh
openssl genrsa -out privkey.key
openssl req -new -x509 -key privkey.key -out ca.pem
```
{:codeblock}

The resulting `ca.pem` file is used on each database node and each
load balancer node.

>   **Note:** To use the `ca.pe`m file on a load balancer node, follow the
    instructions in [Connecting load balancer and database nodes by using SSL](connect_lb_and_db_using_ssl.html).
