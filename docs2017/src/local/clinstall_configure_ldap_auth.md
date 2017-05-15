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

# Configuring LDAP authentication


You configure LDAP authentication and authorization in the `ini`
configuration file under the `ldap_auth` section.
{:shortdesc}

See the following configuration information example in the
`local.ini` file in `/opt/cloudant/etc`.

``` sh
[ldap_auth]
use_ssl = false
servers = 10.35.186.185
searcher_dn = cn=Manager,dc=example,dc=com
searcher_password = secretsanta
group_base_dn = dc=example,dc=com
```
{:codeblock}

1.  Configure at least one of the available parameters inside the
    `ldap_auth` section of an `ini` configuration file.

2.  Modify the parameters and their associated default values (in
    parentheses) in the following list.

    >   **Note:** The default values for parameters marked '&raquo;' are only useful for testing. Change the parameter's value to match your environment.

<!-- reset markdown parsing -->

*   &raquo; `group_base_dn` (ou=groups,dc=example,dc=com)

    Defines a directory location to use during a search
    for groups.

*   `group_classes` (posixGroup)

    Defines which `objectClasses` indicate a particular
    entry as a group during search.

*   `group_member_attribute` (memberUid)

    Defines which group attribute maps to user uid.

*   `group_role_attribute` (description)

    Defines which group attribute maps to a particular
    role.

*   `port` (389)

    LDAP server port for decrypted communication.

*   &raquo; `searcher_dn` (uid=ldapsearch,ou=users,dc=example,dc=com)

    Defines the distinguished name (DN) to use while
    `ldap_auth` searches for users and groups.

*   &raquo; `searcher_password` (secret)

    Defines the password for the `searcher_dn` parameter.

*   &raquo; `servers` (127.0.0.1)

    Supports one or more LDAP servers, which default to a
    single host, but might also be a comma-separated
    list.

    >   **Note:** All servers must use the same port, which is a limitation of the underlying `eldap` library.

*   `ssl_port` (636)

    LDAP server port for encrypted communication.

*   `timeout` (5000)

    Milliseconds to wait for a response from an LDAP
    server before an error occurs.

*   `use_ssl` (true)

    If true, use TLS to encrypt traffic to LDAP servers.

*   &raquo; `user_base_dn` (ou=users,dc=example,dc=com)

    Defines a directory location to use during a search
    for users.

*   `user_bind_dns` ([ ])

    Defines one or more base DNs into which the
    authenticating user's user name can be inserted as
    the `user_uid_attribute` and used to bind to it
    directly.

*   `user_classes` (person)

    Defines which `objectClasses` indicate a particular
    entry as a user during search.

*   `user_uid_attribute` (uid)

    Defines which attribute maps to a user name.
