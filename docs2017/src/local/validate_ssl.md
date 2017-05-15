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

# Validating your SSL connection

Check that your SSL connection is working correctly.
{:shortdesc}

1.  Connect to a load balancer with a browser by using the https
    protocol.

    ``` sh
    https://lb1centos.princeton.usnj.ibm.com/dashboard.html
    ```
    {:codeblock}

2.  Enter your database administration credentials at the
    Cloudant&reg; Dashboard.

    If your SSL connection is working correctly, the Cloudant
    Local dashboard opens in your browser.
    
    >   **Note:** If you are using self-signed security certificates, your browser warns you that the SSL certificates are not from a recognized certificate authority.
