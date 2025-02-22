**Ansible Modules for Dell Technologies PowerStore**
=========================================
### Release Notes 3.3.0

>   © 2024 Dell Inc. or its subsidiaries. All rights reserved. Dell,
>   and other trademarks are trademarks of Dell Inc. or its
>   subsidiaries. Other trademarks may be trademarks of their respective
>   owners.

Content
-------
These release notes contain supplemental information about Ansible
Modules for Dell Technologies (Dell) PowerStore.

-   [Revision History](#revision-history)
-   [Product Description](#product-description)
-   [New Features & Enhancements](#new-features--enhancements)
-   [Known Issues](#known-issues)
-   [Limitations](#limitations)
-   [Distribution](#distribution)
-   [Documentation](#documentation)

Revision history
----------------
The table in this section lists the revision history of this document.

Table 1. Revision history

| Revision | Date         | Description                                               |
|----------|--------------|-----------------------------------------------------------|
| 01       | April 2024 | Current release of Ansible Modules for Dell PowerStore 3.3.0 |

Product Description
-------------------
The Ansible modules for Dell PowerStore are used to automate and orchestrate the deployment, configuration, and management of Dell PowerStore storage systems. The capabilities of Ansible modules are managing Volumes, Volume groups, Hosts, Host groups, Protection policies, Replication rules, Replication sessions, NFS exports, SMB shares, NAS server, File interfaces, File DNS, File NIS, SMB servers, NFS servers, service configurations, File systems, File system snapshots, Tree quotas, User quotas, Clusters, Networks, Local users, Roles, Jobs, Certificates, Remote systems, Security Configuration, DNS server, Email notification destinations, NTP server, Remote support contacts, Remote support configuration, SMTP configuration, LDAP accounts, LDAP domain, and obtaining high-level information about a PowerStore system. The options available are list, show, create, delete, and modify.

New features & enhancements
---------------------------
Along with the previous release deliverables, this release supports these features:

- Added support for PowerStore 4.0.0.0
- Added support for PowerStore 3.6.x.x.
- Added support for creating, getting details, modifying and deleting
  a file interface.
- Added support for enabling, getting details, modifying and disabling
  the file DNS.
- Added support for enabling, getting details, modifying and disabling
  the file NIS.
- Added support for enabling, getting details, modifying and disabling
  the SMB server.
- Added support for enabling, getting details, modifying and disabling
  the NFS server.
- Added support for getting details and modifying a service configuration.
- Added support for creating multiple NFS exports with same name
  but different NAS servers
- Info module is enhanced to list file interfaces, file DNS,
  file NIS, SMB servers and NFS servers.

Known issues
------------
Hosts in IPv4/prefix_length format do not get mapped to an NFS export in Foothills Prime version of PowerStore.

Limitations
-----------
- All occurrences of Password and related parameters do not support Idempotency.
- Exchange, reset and add/import of certificates do not support Idempotency.
- Verify connection  and send test alert for remote support module do not support Idempotency.
- Sending test alert through SMTP configuration and Email module does not support Idempotency.
- Verify operation for LDAP domain module does not support Idempotency.

Distribution
----------------
The software package is available for download from the [Ansible Modules
for PowerStore GitHub](https://github.com/dell/ansible-powerstore/tree/3.3.0) page.

Documentation
-------------
The documentation is available on [Ansible Modules for PowerStore GitHub](https://github.com/dell/ansible-powerstore/tree/3.3.0/docs)
page. It includes these:
- README
- Release Notes (this document)
