---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-17"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Running a rebalancing plan

Before you continue, confirm that no other shard moves are
running on the same cluster. Moving multiple shards of the same
database concurrently can lead to data loss.
{:shortdesc}

<ol>
<li>Run your rebalancing plan, and replace `rebalance_plan_filename`
    with the filename for your rebalance plan.
<p>**Note:** The filename was specified earlier when you edited the `rebal.ini` file when you created a rebalancing plan. The command runs the shard moves identified in the plan. Shards moves are batched by database name with each batch that is run in a series. Multiple batches are run concurrently, with batches of 20 as the default. Progress and errors are logged to the `rebalance_plan.log`.</p>
<p>`rebal run rebalance_plan_filename`</p>  </li>
<li>Monitor progress by using the `tail` command.
<p>`tail -f rebalance_plan.log`</p>
</li>
<li>To troubleshoot errors, check the log files for the presence
    of `sudo` or `tty` errors. If you find errors, do the following
    tasks for the `/etc/sudoers` file on all the database nodes.
<ol type=a>
<li>Search for a line that contains.
<p>`Defaults requiretty`</p></li>
<li>Modify the line to read.
<p>`Defaults !requiretty`</p></li>
<li>Add the following lines to the file.
<p>`cloudantrebal   ALL=(ALL) NOPASSWD: ALL`<br>
`%cloudant       ALL=(ALL) NOPASSWD: ALL`</p>
</li>
</ol>
 </li>
<li>Check whether it is a problem with the configuration of `rebal`
    or `ssh-agent`.</li>
<li>Confirm that `ssh-agent` is set up correctly and that the `.rebal`
    file contains the right credentials.
</li>
<li>Check whether multiple `erl_call: failed to connect to node`
    messages in the `dbname.out` files exist. If multiple messages
    exist, you might need to reduce the concurrency of the
    rebalancing process.
<p>`rebal run --concurrency 5 rebalance_plan_filename`</p>

<p>This command reduces the number of concurrent shard moves to 5
    from the default of 20.</p></li>
<li>Run the rebalancing process again with the rebal `run` command
    and the appropriate `rebalance_plan_` filename. 
    <p>The problem
    might be a temporary issue, such as an unreachable or
    overloaded node, leading to a timeout. Rebalancing in this way
    does not cause a shard to have too few copies, but it might
    result in shards with more than the expected number of copies.</p></li>
<li>If you see `rsync` errors in the log file, verify that `rsync` is
    installed and operational on all database nodes. 
    <p>Otherwise,
    install `rsync` package on all the nodes. For example, on RedHat
    platforms, use the `yum install rsync` command to install `rsync`.
    If you checked the configuration and tried to rerun the shard
    moves, but the problem persists, contact support.</p></li>
</ol>

