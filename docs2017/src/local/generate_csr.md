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

# Generating a CSR

Generate a certificate signing request (CSR) by using the RSA
private key. In a production environment, the CSR is sent to a
certificate authority (CA) who supplies a signed certificate to
reassure users that the certificate is valid. In the Cloudant&reg;
Local environment, the CSR is self-signed because the certificate
is for internal use only. The **openssl** toolkit is used to generate
the CSR.
{:shortdesc}

1.  Generate a CSR by using the `openssl req` command.

    ``` sh
    openssl req -new -key rsa.key -out rsa.csr
    ```
    {:codeblock}

    During the CSR generation process, you are prompted for
    several pieces of information, such as your company name,
    email address, and a "challenge password." When prompted for a
    Common Name, enter the domain name for the system where you
    want to install the certificate, for example a load balancer.

2.  Reply to the prompts with information for your environment.

    The following example shows how this command generates a CSR.

    ``` sh
    [root@lb1centos haproxy]# openssl req -new -key rsa.key -out rsa.csr
    You are about to be asked to enter information that will be incorporated into your certificate request.
    Enter a Distinguished Name or a DN.
    There are a number of fields, but you can leave some blank.
    Some fields have a default value, if you enter '.', the field is left blank.
    -----
    Country Name (2 letter code) [XX]:US
    State or Province Name (full name) []:New Jersey
    Locality Name (eg, City) [Default City]:Princeton
    Organization Name (eg, company) [Default Company Ltd]:IBM
    Organizational Unit Name (eg, section) []:Cloudant
    Common Name (eg, your name or your server's host name) []:lb1centos.princeton.usnj.ibm.com
    Email Address []:smith at us dot ibm dot com
    
    Enter the following 'extra' attributes to be sent with your certificate request.
    A challenge password []:
    An optional company name []:
    [root@lb1centos haproxy]#
    ```
    {:codeblock}
