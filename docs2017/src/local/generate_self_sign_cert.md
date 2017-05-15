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

# Generating a self-signed certificate

If required, create a self-signed certificate for your internal
use.
{:shortdesc}

When a self-signed certificate is used for a website, an error
message is displayed in the browser when a user attempts to
connect to the site. The message warns the user that the
certificate for the specified website is signed by an unknown and
untrusted certificate authority. In a production environment, a
CSR is sent to a certificate authority (CA) for certification.
After the CA confirms that the site is valid, the CA returns a
signed certificate to reassure users that the certificate for the
site is valid.

Use this command to generate a self-signed certificate that is
valid for 365 days, and that is suitable for testing.

``` sh
openssl x509 -req -days 365 -in rsa.csr -signkey rsa.key -out rsa.crt
```
{:codeblock}

This example shows how this command is used to generate a
self-signed certificate.

``` sh
[root@lb1centos haproxy]# openssl x509 -req -days 365 -in rsa.csr -signkey rsa.key -out rsa.crt
Signature ok
subject=/C=US/ST=New Jersey/L=Princeton/O=IBM/OU=Cloudant/CN=lb1centos.princeton.usnj.ibm.com/
emailAddress=silvagni at us dot ibm dot com
Getting Private key
[root@lb1centos haproxy]# 
```
{:codeblock}
