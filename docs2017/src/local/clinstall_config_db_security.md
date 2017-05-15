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

# Configuring database-level security

If global read and write access is unacceptable, and user- and
role-based authorization to individual databases is required, do
the following steps.
{:shortdesc}

1.  Create a `_users` database.

2.  Create a document in the `_users` database for each
    non-administrator account that requires access to your
    databases.

3.  For each database that you create, add a `_security` document
    that identifies who is allowed to access that database as a
    member or reader.

    For more information about the syntax that is used in that
    document and the API call, see
    [http://docs.couchdb.org/en/stable/api/database/security.html#put--db-_security ![External link icon](images/launch-glyph.svg "External link icon")](http://docs.couchdb.org/en/stable/api/database/security.html#put--db-_security){:new_window}.

4.  Validate the security settings on each database.

    ``` sh
    curl -u username:password https://hostname.customer.com/dbname
    ```
    {:codeblock}

    Replace the following variables in this command.

    *   Replace `hostname.customer.com` with the host name of the
        configured cluster load balancer.
    *   Replace `dbname` with the name of the database.
    *   To test anonymous access, omit the `-u` flag.
    *   Replace `username:password` with the user ID and password for
        any non-administrator account that you create.
