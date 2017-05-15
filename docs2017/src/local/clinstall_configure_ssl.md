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

# Configuring SSL

Use these instructions to configure Secure Sockets Layer (SSL)
for your Cloudant&reg; Local installation, especially if you access
the Cloudant database across an untrusted network. If your
network is trusted, configuring SSL/HTTPS is optional. You can
use HTTP requests (that is, port 80) instead.
{:shortdesc}

SSL is a standard security technology for establishing an
encrypted link between a server and a client, such as between a
website and a browser. SSL is used to ensure that sensitive
information is transmitted securely over the internet. SSL uses a
cryptographic system that uses two keys to encrypt data: a public
key that is available to anyone, and a secret key that is known
only to the recipient of the message.