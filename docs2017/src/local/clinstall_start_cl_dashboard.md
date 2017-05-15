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

# Starting the Cloudant Local Dashboard

Start the Cloudant&reg; Local Dashboard to verify that Cloudant Local
was successfully installed on each load balancer.
{:shortdesc}

1.  Start and stop the dashboard by using the following commands.

    ``` sh
    cast node start
    cast node stop
    ```
    {:codeblock}

2.  Enter the following URL in a web browser to access the dashboard.

    ``` sh
    http://your_load_balancer_IP_address/dashboard.html
    ```
    {:codeblock}

    In this URL, `your_load_balancer_IP_address` is the fully
    qualified host name of your load balancer.

3.  Include the `/dashboard.html` part of the URL to display the
    dashboard. If you omit `/dashboard.html`, the standard Cloudant
    welcome message is displayed instead of the dashboard.

    ``` json
    {
        "couchdb": "Welcome",
        "version": "2.0.0",
        "vendor": {
            "name": "IBM Cloudant",
            "version": "1.1.0",
            "variant": "local"
            },
        "features": [
            "geo"
        ]
    }
    ```
    {:codeblock}

4.  Enter your database administration credentials at the Cloudant Dashboard.

    When you successfully authenticate to the Cloudant Local
    Dashboard, your installation is complete.
