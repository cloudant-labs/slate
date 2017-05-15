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

# Putting a new node into production mode

You must take the new node out of maintenance mode so it can
serve traffic for the moved shards, while the rebalancing is in
progress.
{:shortdesc}

1.  Run the cast node command to take the node out of maintenance
    mode.

    ``` sh
    cast node maintenance --false
    ```
    {:codeblock}

2.  Run the following command on the new database node to verify
    the status of that node.

    ``` sh
    cast node maintenance
    ```
    {:codeblock}

    If the node is functioning normally in production mode, you
    receive this response.

    ``` sh
    The node is OUT of maintenance mode.
    ```
    {:codeblock}
