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

# Setting up `ldap_auth` to work with Cloudant Local

Cloudant&reg; Local LDAP authentication, `ldap_auth`, implements basic
and cookie-based authentication handlers to obtain the roles that
are associated with a particular user. Using `ldap_auth` with basic
authentication requires no client-side changes.
{:shortdesc}

A properly configured database automatically attempts to
authenticate with LDAP by using the supplied credentials.

1.  For cookie authentication, `POST` credentials to the `_session`
    endpoint to obtain an `AuthSession` cookie, which contains a
    signed hash of its contents: name, time issued, and authorized
    roles. Subsequent requests that use that cookie automatically
    use the roles in the cookie until it expires.

2.  Modify the following configuration parameters in the
    `[couch_httpd_auth]` section.

<!-- reset markdown parser -->

*   `secret`

    The shared secret that is used to sign the
    `AuthSession` cookie that is created when the cluster
    is provisioned.

*   `timeout` (600)

    Seconds until the `AuthSession` cookie expires.
    The default is 600 seconds.
