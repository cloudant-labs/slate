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

# Optimizing LDAP Authentication and Authorization


The `ldap_auth` function uses two different modes of operation that
depend on whether the `user_bind_dns` parameter is defined. Both
modes return a list of roles that are associated with a user upon
successful authentication.
{:shortdesc}

By default, `ldap_auth` opens a connection to an LDAP server and
binds the connection handle with the `searcher` DN and password. It
then uses that connection to search for a user record with the
authenticating user name. If a matching user DN is found, it
opens a second connection to the server and attempts to bind that
connection by using the user name and password credentials. If
the bind is successful, it closes the connection and uses the
original "`searcher`" bound connection to search for groups that
contain the `group_member_attribute` parameter that matches the
user's user name. Those groups have a `group_role_attribute`
parameter that indicates the actual roles for the user.

If you know in advance that all your users' DNs can be
constructed by inserting their user names into the following
pattern, `$uid_attribute=$username,$user_bind_dn` (for example,
`uid=jay,ou=users,dc=example,dc=com`), you can configure multiple
`user_bind_dns` parameters. The `ldap_auth` function does not use the
`searcher` DN or `user_base_dn`. Instead, `ldap_auth` binds directly to
the constructed user DNs. If the bind is successful, the bound
connection is used again to make the same group search as
described earlier. This technique can eliminate extra network
round trips.
