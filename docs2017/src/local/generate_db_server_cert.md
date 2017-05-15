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

# Generating the server certificate file for a database node

If you are using self-signed certificates, generate a unique
server certificate file for each database node.
{:shortdesc}

If you are using certificates that are provided by a third party,
you can proceed directly to Copying the SSL security files to the
database node.

Each database node requires its own server certificate file to
identify itself. A unique name is required for each server
certificate. In the instructions that follow, replace each
instance of the phrase `serverX` with whatever name you choose. You
can use any name that is unique to your cluster.

To generate server certificate file, use the following commands.

``` sh
openssl genrsa -out serverX.key 
openssl req -new -key serverX.key -out serverX.req
openssl x509 -req -in serverX.req -CA ca.pem -CAkey privkey.key -set_serial 01 -out serverX.pem
```
{:codeblock}

The `ca.pem` file was generated while [Generating the certificate
authority file for a database node](generate_db_ca.html).

>   **Note:** The `serverX.key` file is the "secret" necessary to unlock
    self-generated certificates. Be careful to protect this file with
    appropriate access controls and security permissions.
