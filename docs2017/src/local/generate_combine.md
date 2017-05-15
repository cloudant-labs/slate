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

# Combining the RSA certificate and key

The RSA certificate and key must be combined into a single file
for use in HAProxy 1.5 and higher.
{:shortdesc}

Combine the RSA certificate (`/etc/haproxy/rsa.crt`) and RSA key
(`/etc/haproxy/rsa.key`) into a new single file
(`/etc/haproxy/certificate.pem`) for use in HAProxy. Put the
certificate in the `certificate.pem` file first, with the key as
the final portion of the file.

Use this command to combine the files in the correct order.

``` sh
cat /etc/haproxy/rsa.crt /etc/haproxy/rsa.key > /etc/haproxy/certificate.pem
```
{:codeblock}
