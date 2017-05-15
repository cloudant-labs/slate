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

# Creating a rebalancing plan


After the rebalancer is configured and the ssh-agent is set up,
you can start the rebalancing process by creating a rebalancing
plan.
{:shortdesc}

1.  Create a working directory to hold the plan and log files and
    change to that working directory by specifying these commands.

    ``` sh
    mkdir rebaldir
    cd rebaldir
    ```
    {:codeblock}

2.  Create the plan by running `rebal plan expand` with one of the
    database nodes as an argument, as shown in the following
    example.

    ``` sh
    rebal plan expand 'db1.cluster001.example.com'
    ```
    {:codeblock}

3.  Check the output from this command for any error messages
    similar to this one.

    ``` sh
    Retrying SSH connection
    ```
    {:codeblock}

4.  If you receive a similar error message, check the `ssh-agent`
    configurations and confirm that you can SSH to all database
    nodes, without specifying a password.

    Your current directory now contains a `rebalance_plan` file that
    includes a list of shard moves.
