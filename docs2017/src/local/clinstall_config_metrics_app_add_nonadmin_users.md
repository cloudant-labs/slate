---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-13"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Adding non-administrator users

Administrators can create accounts with limited,
non-administrator, permissions. To do so, an administrator
creates users who access the Metrics application without
administrator permissions. To add a user, an administrator
updates the metrics database security document.
{:shortdesc}

<ol>
<li>Create a user for the Metrics application.
<p>The new user in this example is `metuser3`.</p>
<p>`curl -X PUT http://localhost/_users/org.couchdb.user:metuser3 -H "Accept: application/json" -H "Content-Type: application/json" -d '{"name": "metuser3", "password": "metpass3", "type": "user", "roles":[]}' -u admin`</p>
</li>
<li>Get the list of current Metrics application users from the
    metrics security document.
<p>`curl -X GET http://localhost/metrics/_security -u admin`</p>
<p>**Note:** When you add a user for the first time, this list might be empty.</p></li>
<li>Add or append a new user to the `members:names` list in the
    metrics `_security` document.
<p>**Note:** The `_security` document is overwritten. If you want to keep existing users, you must add them, and the new users, to the list.</p>
<ol type=a>
<li>Run the following command to add a user to the original
        security document when the `members:names` list is empty.
<p>`curl -X PUT http://localhost/metrics/_security -Hcontent-type:application/json -d '{"admins":{"names":[],"roles":[]},"members":{"names":["metuser3"],"roles":[]}}' -u admin`</p>
</li>
<li>Run the following command to add a user to the original
        security document when the `members:names` list is not
        empty and contains existing users, for example, `metuser1`
        and `metuser2`.
<p>`curl -X PUT http://localhost/metrics/_security -Hcontent-type:application/json -d '{"admins":{"names":[],"roles":[]},"members":{"names":["metuser1","metuser2","metuser3"],"roles":[]}}' -u admin`</p>
        </li>
</ol>
</li>
<li>The new user can log in to the Metrics application and view
    metrics with their new ID, `metuser3`.</li>
</ol>

