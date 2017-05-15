---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-10"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Stop and start Cloudant Local services

Start, stop, and restart your Cloudant&reg; Local services with the
cast node command by specifying the correct option. You can also
display the status of various processes and test the Cloudant
Local API.
{:shortdesc}

*   Start all Cloudant Local services.

    ``` sh
    cast node start
    ```
    {:codeblock}

*   Stop all Cloudant Local services.

    ``` sh
    cast node stop
    ```
    {:codeblock}

*   Restart all Cloudant Local services. Use the `restart` command
    to restart your services after you change the configuration
    file.

    ``` sh
    cast node restart
    ```
    {:codeblock}

*   (Optional) Display the syntax help text for the CAST command.

    ``` sh
    cast system install --help
    ```
    {:codeblock}
