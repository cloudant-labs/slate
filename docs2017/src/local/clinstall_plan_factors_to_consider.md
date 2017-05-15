---

copyright:
  years: 2015, 2017
lastupdated: "2017-02-08"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# Factors to consider

Like most applications, Cloudant&reg; Local consists of two parts:
the application and the data it manages. After installation, the
application does not change often, but the data will change and
grow over time. Therefore, it is helpful to plan your
installation carefully before you install the product.
{:shortdesc}

In particular, consider the following aspects.

*  Any organizational policies that you might have regarding the
   installation of software and data. For example, you might have
   a policy against installing databases on the root partition of
   a system.
*  Current and expected storage requirements. For example, while
   the target system might have enough storage space for the
   initial installation, subsequent use and data growth might
   exceed the available space.
*  Simplification of maintenance and backup. For example, by
   keeping the application software and data locations separate,
   it is often easier to run backup and maintenance tasks.

If you install Cloudant Local on a dedicated system, you will
have more control over where data is stored and how future
capacity is assured. If you install Cloudant Local on an existing
or shared system, it is important to consider your installation
plan. In the future, you might not have full control over
available space and future storage space.

When you consider these factors in your plan, you are better able
to identify installation locations and any storage partition
requirements.
