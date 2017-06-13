## Back up your data

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the 'Back up your data' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/backup.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

To protect your business from data loss and corruption,
you should backup your data.

Two important principles help you avoid downtime and lost revenue:

-	Backup all your data regularly.
-	Check the integrity of the backups.

You can back up your data in Cloudant by using [replication](replication.html) to make a copy of your database.

But if your database is big,
or you need backups for multiple points in time,
having a complete copy of your database for each of the requirements can quickly result in significant disk usage.

An alternative is to use the IBM Cloudant Incremental Backup feature.
Incremental backups are a good solution for storing only the documents that have changed since the last backup.

<aside class="warning" role="complementary" aria-label="betaforenterprise">Daily incremental backup for Enterprise customers is currently a Beta capability.
It is not enabled by default.</aside>

You can see more information about Incremental Backups in the topic [Back up your data](backup-guide.html).