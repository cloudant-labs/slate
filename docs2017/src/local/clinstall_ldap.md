---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-20"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Authenticating with LDAP

Use these instructions to configure Lightweight Directory Access
Protocol (LDAP) authentication and authorization for Cloudant&reg;
Local.
{:shortdesc}

Cloudant Local has its own security model with a self-contained
authentication and authorization system. The authentication and
authorization system relies on ini files and user databases to
store user data, including user names (uids), passwords, and user
roles for accessing resources in the database. If your
organization uses an LDAP service for access control, you can
delegate authentication and authorization services to LDAP when
you access a Cloudant Local database. The `ldap_auth` configuration
allows you to use LDAP with Cloudant Local.

At a high level, when `ldap_auth` is configured, it replaces the
default basic and cookie authentication and authorization. It
ignores any administrator users who are configured in the `ini`
files and user databases. Instead, `ldap_auth` validates user
credentials by using the configured LDAP service. After you
authenticate your credentials with the LDAP service, `ldap_auth`
determines the user roles. The user roles determine what the user
is authorized to access, based on the LDAP groups where the user
is a member.

>   **Note:** You can use LDAP and the Metrics application together.
    However, the Metrics application requires that specific
    authentication credentials and roles exist in the LDAP database
    so that LDAP and the Metrics application work properly.

The Metrics application stores its authentication credentials in
the `metrics.ini` file. The Metrics application's default
authentication credentials include user name admin and password
pass. You must create a user in your LDAP database that has both
`_admin` and `server_admin` roles and whose credentials match the
credentials set in the `metrics.ini` file. See the [Cloudant Metrics
application](clinstall_config_metrics_app.html).
