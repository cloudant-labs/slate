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

# Copying the SSL security files to the database node

To enable SSL security, the prerequisite security certificate
files must be available on the database node.
{:shortdesc}

Copy the following files to any convenient location within the
file system of the respective database node.

``` sh
ca.pem
serverX.key
serverX.pem
```
{:codeblock}

>   **Note:** The `serverX.key` file is the "secret" necessary to unlock
    self-generated certificates. Be careful to protect this file with
    appropriate access controls and security permissions.

The `ca.pem` file is the certificate authority (CA) file, generated
in the
[Generating the certificate authority file for a database node](generate_db_ca.html)
step, or provided by a third party. The same `ca.pem` file is
used by all the database nodes.

The `serverX.key` and `serverX.pem` files are unique and specific to
each database node. The files were generated while
[Generating the server certificate file for a database node](generate_db_server_cert.html),
or provided by a third party.
