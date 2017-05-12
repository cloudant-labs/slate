---

copyright:
  years: 2017
lastupdated: "2017-05-12"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-MM-DD -->

# IBM Cloud Identity and Access Management

IBM Cloud Identity and Access Management (IAM) provides a unified approach to managing
user identities,
services,
and access control.
{:shortdesc}

This guide provides a high-level overview of how IAM is used to enable access to Cloudant database services.This

## Users

A human user is identified by their IBMid.

A client application,
is identified by its API key.

A user or application authenticates themselves to the system by 'logging in',
using their IBMid or API key,
and a valid password.
If the authentication succeeds,
a 'token' is returned.

Possession of a valid and current token is necessary to access and use Cloudant services.

## Services

A service that is managed using IAM,
such as Cloudant,
is identified by a ServiceID.

For Cloudant,
the ServiceID is defined internally as part of the process of managing Cloudant access using IAM.
Users and client applications do not need to know the ServiceID,
but it is helpful to know that it exists to help you understand how Cloudant uses IAM.

## Roles and access policy

Each of the capabilities provided by a service such as Cloudant has a set of associated roles and access requirements.
For example,
to create or administer a database,
a tightly-controlled 'administration' role is required,
rather than a more general-purpose 'read only' role.
Similarly,
an administrator with access permission for one database might not have permission to access and administer another database.

Services permit access and enable actions,
based on the roles and accesses defined for each action within the service.
Each time a user or application attempts to perform an action on a database,
a decision is made about whether they are authorized to access the database,
_and_ whether they are authorized to perform that action.