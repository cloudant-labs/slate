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

# Generating an RSA private key

RSA is a public-key cryptosystem and is widely used for secure
data transmission. RSA involves a public key and a private key.
The public key is available to anyone and is used to encrypt
messages, while the private key is required to decrypt the
messages. RSA also signs a Certificate Signing Request or CSR.

This example shows how this command is used to generate an RSA
key.

``` sh
[root@lb1centos haproxy]# openssl genrsa -out rsa.key 1024
Generating RSA private key, 1024 bit long modulus
.++++++
...................++++++
e is 65537 (0x10001)
[root@lb1centos haproxy]#
```
{:codeblock}

1.  Generate an RSA private key in the `/etc/haproxy` directory by
    using the openssl toolkit.

    The key is 1024 bit and is stored in PEM format, which is
    readable as ASCII text.
    
    >   **Note:** PEM is a container format that can include just the public certificate, or it can include an entire certificate chain, including a public key, private key, and root certificates. PEM was originally developed to secure email, and the PEM acronym was derived from the phrase Privacy Enhanced Email.
    
2.  Generate an RSA key by using the openssl `genrsa` command.

    ``` sh
    openssl genrsa -out rsa.key 1024
    ```
    {:codeblock}

    This example shows how this command is used to generate an RSA
    key.

    ``` sh
    [root@lb1centos haproxy]# openssl genrsa -out rsa.key 1024
    Generating RSA private key, 1024 bit long modulus
    .++++++
    ...................++++++
    e is 65537 (0x10001)
    [root@lb1centos haproxy]#
    ```
    {:codeblock}
