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

# Defining LDAP groups and roles

The method for defining groups and roles varies based on your
LDAP server. However, before Cloudant&reg; Local and LDAP function
together, you must define groups for each Cloudant role.
{:shortdesc}

Each role defines the tasks that a user can do. Some of
the available roles are defined in the following list.

*   `_reader`

    Read from a database.

*   `_writer`

    Update a database.

After the groups are defined, you must determine the users that
can perform the tasks in each role.
