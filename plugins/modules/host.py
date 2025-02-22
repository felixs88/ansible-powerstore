#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies
# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: host
version_added: '1.0.0'
short_description: Manage host on PowerStore storage system
description:
- Managing host on PowerStore storage system includes create host with a
  set of initiators, add/remove initiators from host, rename host and
  delete host.
author:
- Manisha Agrawal (@agrawm3) <ansible.team@dell.com>
extends_documentation_fragment:
  - dellemc.powerstore.powerstore
options:
  host_name:
    description:
    - The host name. This value must contain 128 or fewer printable Unicode
      characters.
    - Creation of an empty host is not allowed.
    - Required when creating a host.
    - Use either I(host_id) or I(host_name) for modify and delete tasks.
    type: str
  host_id:
    description:
    - The 36 character long host id automatically generated when a host is
      created.
    - Use either I(host_id) or I(host_name) for modify and delete tasks.
    - The I(host_id) cannot be used while creating host, as it is generated by
      the array after creation of host.
    type: str
  os_type:
      description:
      - Operating system of the host.
      - Required when creating a host.
      - OS type cannot be modified for a given host.
      choices: ['Windows', 'Linux', 'ESXi', 'AIX', 'HP-UX', 'Solaris']
      type: str
  initiators:
      description:
      - List of Initiator WWN or IQN or NQN to be added or removed from the
        host.
      - Subordinate initiators in a host can only be of one type, either FC or
        iSCSI.
      - Required when creating a host.
      - It is mutually exclusive with I(detailed_initiators).
      type: list
      elements: str
  detailed_initiators:
      description:
      - Initiator properties.
      - It is mutually exclusive with I(initiators).
      type: list
      elements: dict
      suboptions:
        port_name:
          description:
          - Name of port type.
          - The I(port_name) is mandatory key.
          type: str
          required: true
        port_type:
          description:
          - Protocol type of the host initiator.
          type: str
          choices: ['iSCSI', 'FC', 'NVMe']
        chap_single_username:
          description:
          - Username for single CHAP authentication.
          - CHAP username is required when the cluster CHAP mode is mutual
            authentication.
          - Minimum length is 1 and maximum length is 64 characters.
          type: str
        chap_single_password:
          description:
          - Password for single CHAP authentication.
          - CHAP password is required when the cluster CHAP mode is mutual
            authentication.
          - Minimum length is 12 and maximum length is 64 characters.
          type: str
        chap_mutual_username:
          description:
          - Username for mutual CHAP authentication.
          - CHAP username is required when the cluster CHAP mode is mutual
            authentication.
          - Minimum length is 1 and maximum length is 64 characters.
          type: str
        chap_mutual_password:
          description:
          - Password for mutual CHAP authentication.
          - CHAP password is required when the cluster CHAP mode is mutual
            authentication.
          - Minimum length is 12 and maximum length is 64 characters.
          type: str
  state:
    description:
    - Define whether the host should exist or not.
    - Value C(present) - indicates that the host should exist in system.
    - Value C(absent) - indicates that the host should not exist in system.
    required: true
    choices: ['absent', 'present']
    type: str
  initiator_state:
    description:
    - Define whether the initiators should be present or absent in host.
    - Value C(present-in-host) - indicates that the initiators should exist on
      host.
    - Value C(absent-in-host) - indicates that the initiators should not exist on
      host.
    - Required when creating a host with initiators or adding/removing
      initiators to/from existing host.
    choices: ['present-in-host', 'absent-in-host']
    type: str
  new_name:
    description:
    - The new name of host for renaming function. This value must contain 128
      or fewer printable Unicode characters.
    - Cannot be specified when creating a host.
    type: str
  host_connectivity:
    description:
    - Connectivity type for host.
    - If any of metro connectivity options specified, a metro host must
      exists in both cluster provide connectivity to a metro volume from both
      cluster.
    choices: ['Local_Only', 'Metro_Optimize_Both', 'Metro_Optimize_Local',
              'Metro_Optimize_Remote']
    type: str

notes:
- Only completely and correctly configured iSCSI initiators can be associated
  with a host.
- The parameters I(initiators) and I(detailed_initiators) are mutually exclusive.
- For mutual CHAP authentication, single CHAP credentials are mandatory.
- Support of C(NVMe) type of initiators is for PowerStore 2.0 and beyond.
- The I(host_connectivity) is supported only in PowerStore 3.0.0.0 and above.
- The I(check_mode) is not supported.
'''
EXAMPLES = r'''
- name: Create host with FC initiator
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_name: "ansible-test-host-1"
    os_type: 'Windows'
    host_connectivity: "Metro_Optimize_Local"
    initiators:
      - 21:00:00:24:ff:31:e9:fc
    state: 'present'
    initiator_state: 'present-in-host'

- name: Create host with iSCSI initiator and its details
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_name: "ansible-test-host-2"
    os_type: 'Windows'
    detailed_initiators:
      - port_name: 'iqn.1998-01.com.vmware:lgc198248-5b06fb37'
        port_type: 'iSCSI'
        chap_single_username: 'chapuserSingle'
        chap_single_password: 'chappasswd12345'
      - port_name: 'iqn.1998-01.com.vmware:imn198248-5b06fb37'
        port_type: 'iSCSI'
        chap_mutual_username: 'chapuserMutual'
        chap_mutual_password: 'chappasswd12345'
    state: 'present'
    initiator_state: 'present-in-host'

- name: Get host details by id
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_id: "5c1e869b-ed8a-4845-abae-b102bc249d41"
    state: 'present'

- name: Add initiators to host by name
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_name: "ansible-test-host-1"
    initiators:
      - 21:00:00:24:ff:31:e9:ee
    initiator_state: 'present-in-host'
    state: 'present'

- name: Add initiators to host by id
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_id: "5c1e869b-ed8a-4845-abae-b102bc249d41"
    detailed_initiators:
      - port_name: 'iqn.1998-01.com.vmware:imn198248-5b06fb37'
        port_type: 'iSCSI'
        chap_mutual_username: 'chapuserMutual'
        chap_mutual_password: 'chappasswd12345'
    initiator_state: 'present-in-host'
    state: 'present'

- name: Remove initiators from by id
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_id: "8c1e869b-fe8a-4845-hiae-h802bc249d41"
    initiators:
      - 21:00:00:24:ff:31:e9:ee
    initiator_state: 'absent-in-host'
    state: 'present'

- name: Modify host by name
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_name: "ansible-test-host-1"
    new_name: "ansible-test-host-1-new"
    host_connectivity: "Metro_Optimize_Remote"
    state: 'present'

- name: Delete host
  dellemc.powerstore.host:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    host_name: "ansible-test-host-1-new"
    state: 'absent'
'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

host_details:
    description: Details of the host.
    returned: When host exists
    type: complex
    contains:
        id:
            description: The system generated ID given to the host.
            type: str
        name:
            description: Name of the host.
            type: str
        description:
            description: Description about the host.
            type: str
        host_group_id:
            description: The host group ID of host.
            type: str
        os_type:
            description: The os type of the host.
            type: str
        host_initiators:
            description: The initiator details of this host.
            type: complex
            contains:
                port_name:
                    description: Name of the port.
                    type: str
                port_type:
                    description: The type of the port.
                    type: str
                chap_single_username:
                    description: Username for single CHAP authentication.
                    type: str
                chap_mutual_username:
                    description: Username for mutual CHAP authentication.
                    type: str
                active_sessions:
                    description: List of active login sessions between an
                                 initiator and a target port.
                    type: list
        type:
            description: Type of the host.
            type: str
        mapped_hosts:
            description: This is the inverse of the resource type
                         I(host_volume_mapping) association.
            type: complex
            contains:
                id:
                    description: Unique identifier of a mapping between
                                 a host and a volume.
                    type: str
                logical_unit_number:
                    description: Logical unit number for the host volume
                                 access.
                    type: int
                host_group:
                    description: Details about a host group to which host is
                                 mapped.
                    type: dict
                    contains:
                        id:
                            description: ID of the host group.
                            type: str
                        name:
                            description: Name of the host group.
                            type: str
                volume:
                    description: Details about a volume which has mapping with
                                 the host.
                    type: dict
                    contains:
                        id:
                            description: ID of the volume.
                            type: str
                        name:
                            description: Name of the volume.
                            type: str
        host_connectivity:
            description: Connectivity type for host. It was added in 3.0.0.0.
            type: str
    sample: {
        "description": null,
        "host_group_id": null,
        "host_initiators": [
            {
                "active_sessions": [],
                "chap_mutual_username": "",
                "chap_single_username": "",
                "port_name": "iqn.1998-01.com.vmware:losat106-0eab2afe",
                "port_type": "iSCSI"
            }
        ],
        "id": "4d56e60-fc10-4f51-a698-84a664562f0d",
        "mapped_hosts": [],
        "name": "sample_host",
        "os_type": "ESXi",
        "host_connectivity": "Local_Only",
        "os_type_l10n": "ESXi"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerstore.plugins.module_utils.storage.dell\
    import utils
import logging

LOG = utils.get_logger('host', log_devel=logging.INFO)

py4ps_sdk = utils.has_pyu4ps_sdk()
HAS_PY4PS = py4ps_sdk['HAS_Py4PS']
IMPORT_ERROR = py4ps_sdk['Error_message']

py4ps_version = utils.py4ps_version_check()
IS_SUPPORTED_PY4PS_VERSION = py4ps_version['supported_version']
VERSION_ERROR = py4ps_version['unsupported_version_message']

# Application type
APPLICATION_TYPE = 'Ansible/3.3.0'

# DO NOT CHANGE BELOW PORT_TYPES SEQUENCE AS ITS USED IN SCRIPT USING INDEX
PORT_TYPES = ["iSCSI", "FC", "NVMe"]


class PowerStoreHost(object):
    '''Class with host(initiator group) operations'''

    def __init__(self):
        # Define all parameters required by this module
        self.module_params = utils.get_powerstore_management_host_parameters()
        self.module_params.update(get_powerstore_host_parameters())
        mutually_exclusive = [['host_name', 'host_id'],
                              ['initiators', 'detailed_initiators']]
        required_one_of = [['host_name', 'host_id']]
        # Initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of
        )

        LOG.info(
            'HAS_PY4PS = %s , IMPORT_ERROR = %s', HAS_PY4PS, IMPORT_ERROR)
        if HAS_PY4PS is False:
            self.module.fail_json(msg=IMPORT_ERROR)
        LOG.info(
            'IS_SUPPORTED_PY4PS_VERSION = %s , VERSION_ERROR = %s',
            IS_SUPPORTED_PY4PS_VERSION, VERSION_ERROR)
        if IS_SUPPORTED_PY4PS_VERSION is False:
            self.module.fail_json(msg=VERSION_ERROR)

        # result is a dictionary that contains changed status and host details
        self.result = {"changed": False, "host_details": {}}

        self.conn = utils.get_powerstore_connection(
            self.module.params, application_type=APPLICATION_TYPE)
        LOG.info(
            'Got Python library connection instance for provisioning on'
            ' PowerStore %s', self.conn)

    def get_host(self, host_id):
        '''
        Get details of a given host, given host ID
        '''
        try:
            LOG.info('Getting host %s details', host_id)
            host_from_get = self.conn.provisioning.get_host_details(host_id)
            if host_from_get:
                return host_from_get
            return None
        except Exception as e:
            error_msg = 'Unable to get details of host with ID: {0}' \
                        ' -- error: {1}'.format(host_id, str(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))

    def get_host_id_by_name(self, host_name):
        try:
            host_info = self.conn.provisioning.get_host_by_name(host_name)
            if host_info:
                if len(host_info) > 1:
                    error_msg = 'Multiple hosts by the same name found'
                    LOG.error(error_msg)
                    self.module.fail_json(msg=error_msg)
                return host_info[0]['id']
        except Exception as e:
            msg = 'Get Host {0} Details for powerstore array failed with ' \
                  'error: {1}'.format(host_name, str(e))
            if isinstance(e, utils.PowerStoreException) and \
                    e.err_code == utils.PowerStoreException.HTTP_ERR \
                    and e.status_code == "404":
                LOG.info(msg)
                return None
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def create_host(self, host_name):
        '''
        Create host with given initiators
        '''
        try:
            initiators = self.module.params['initiators']
            detailed_initiators = self.module.params['detailed_initiators']
            host_connectivity = self.module.params['host_connectivity']

            os_type = self.module.params['os_type']
            if os_type is None:
                error_msg = "Create host {0} failed as os_type is not " \
                            "specified".format(host_name)
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)

            if initiators:
                list_of_initiators = []
                initiator_type = []
                for initiator in initiators:
                    current_initiator = {}
                    current_initiator['port_name'] = initiator
                    if initiator.startswith('iqn'):
                        current_initiator['port_type'] = PORT_TYPES[0]  # iSCSI
                        initiator_type.append(PORT_TYPES[0])
                    elif initiator.startswith('nqn'):
                        current_initiator['port_type'] = PORT_TYPES[2]  # NVMe
                        initiator_type.append(PORT_TYPES[2])
                    else:
                        current_initiator['port_type'] = PORT_TYPES[1]  # FC
                        initiator_type.append(PORT_TYPES[1])
                    list_of_initiators.append(current_initiator)

                if 'iSCSI' in initiator_type and 'FC' in initiator_type \
                        and 'NVMe' in initiator_type:
                    error_msg = ('Invalid initiators. Cannot add IQN, WWN and'
                                 ' NQN as part of host. Connect either fiber '
                                 'channel or iSCSI or NVMe.'
                                 )
                    LOG.error(error_msg)
                    self.module.fail_json(msg=error_msg)

                LOG.info("Creating host %s with initiators %s", host_name,
                         list_of_initiators)
                resp = self.conn.provisioning.create_host(
                    name=host_name, os_type=os_type,
                    initiators=list_of_initiators,
                    host_connectivity=host_connectivity)
            else:
                for initiator in detailed_initiators:
                    if initiator['port_type'] is None:
                        if initiator['port_name'].startswith('iqn'):
                            initiator['port_type'] = PORT_TYPES[0]  # iSCSI
                        elif initiator['port_name'].startswith('nqn'):
                            initiator['port_type'] = PORT_TYPES[2]  # NVMe
                        else:
                            initiator['port_type'] = PORT_TYPES[1]  # FC

                LOG.info("Creating host %s with initiators %s", host_name,
                         detailed_initiators)
                resp = self.conn.provisioning.create_host(
                    name=host_name, os_type=os_type,
                    initiators=detailed_initiators,
                    host_connectivity=host_connectivity)
            LOG.info("The response is %s", resp)
            return True

        except Exception as e:
            error_msg = 'Create host {0} failed with error {1}'.format(
                host_name, str(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))
        return None

    def _get_add_initiators(self, existing, requested):
        all_inits = existing + requested
        add_inits = list(set(all_inits) - set(existing))
        return add_inits

    def _get_remove_initiators(self, existing, requested):
        rem_inits = list(set(existing).intersection(set(requested)))
        return rem_inits

    def add_host_initiators(self, host):
        initiators = self.module.params['initiators']
        detailed_initiators = self.module.params['detailed_initiators']
        add_list = None

        try:
            existing_inits = []
            if 'host_initiators' in host:
                current_initiators = host['host_initiators']
                if current_initiators:
                    for initiator in current_initiators:
                        existing_inits.append(initiator['port_name'])

            if initiators \
               and (set(initiators).issubset(set(existing_inits))):
                LOG.info('Initiators are already present in host %s',
                         host['name'])
                return False

            initiator_list = []
            if detailed_initiators is not None:
                initiator_list = [p_name['port_name'] for p_name in
                                  detailed_initiators]

            if detailed_initiators and \
                    (set(initiator_list).issubset(set(existing_inits))):
                LOG.info('Initiators are already present in host %s',
                         host['name'])
                return False

            if detailed_initiators:
                initiators = []
                for initiator in detailed_initiators:
                    initiators.append(initiator['port_name'])

            add_list = self._get_add_initiators(existing_inits, initiators)
            add_list_with_type = []
            for init in add_list:
                # when detailed_initiators param is used to add new initiators
                if detailed_initiators:
                    for detailed_init in detailed_initiators:
                        if init == detailed_init['port_name']:
                            current_initiator = {}
                            current_initiator['port_name'] = init
                            # iSCSI
                            if init.startswith('iqn'):
                                current_initiator['port_type'] = PORT_TYPES[0]
                                current_initiator['chap_single_username'] \
                                    = detailed_init['chap_single_username']
                                current_initiator['chap_single_password'] \
                                    = detailed_init['chap_single_password']
                                current_initiator['chap_mutual_username'] \
                                    = detailed_init['chap_mutual_username']
                                current_initiator['chap_mutual_password'] \
                                    = detailed_init['chap_mutual_password']
                            # NVMe
                            elif init.startswith('nqn'):
                                current_initiator['port_type'] = PORT_TYPES[2]
                            # FC
                            else:
                                current_initiator['port_type'] = PORT_TYPES[1]
                            add_list_with_type.append(current_initiator)
                # when initiators param is used to add new initiators
                else:
                    current_initiator = {}
                    current_initiator['port_name'] = init
                    # iSCSI
                    if init.startswith('iqn'):
                        current_initiator['port_type'] = PORT_TYPES[0]
                    # NVMe
                    elif init.startswith('nqn'):
                        current_initiator['port_type'] = PORT_TYPES[2]
                    # FC
                    else:
                        current_initiator['port_type'] = PORT_TYPES[1]
                    add_list_with_type.append(current_initiator)

            if len(add_list_with_type) > 0:

                LOG.info('Adding initiators %s to host %s',
                         add_list_with_type, host['name'])
                resp = self.conn.provisioning.modify_host(
                    host['id'], add_initiators=add_list_with_type)
                LOG.info('Response from add initiator function %s', resp)
                return True
            else:
                LOG.info('No initiators to add to host %s', host['name'])
                return False
        except Exception as e:
            error_msg = ("Adding initiators {0} to host {1} failed with error"
                         " {2}".format(add_list, host['name'], str(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))

    def remove_host_initiators(self, host):
        initiators = self.module.params['initiators']
        detailed_initiators = self.module.params['detailed_initiators']
        remove_list = None
        try:

            existing_inits = []
            current_initiators = host['host_initiators']

            if current_initiators:
                for initiator in current_initiators:
                    existing_inits.append(initiator['port_name'])

            if len(existing_inits) == 0:
                LOG.info('No initiators are present in host %s', host['name'])
                return False

            if detailed_initiators:
                initiators = []
                for initiator in detailed_initiators:
                    initiators.append(initiator['port_name'])

            remove_list = self._get_remove_initiators(existing_inits,
                                                      initiators)

            if len(remove_list) > 0:

                LOG.info('Removing initiators %s from host %s', remove_list,
                         host['name'])
                resp = self.conn.provisioning.modify_host(
                    host['id'], remove_initiators=remove_list)
                LOG.info('Response from remove initiator function %s', resp)
                return True
            else:
                LOG.info('No initiators to remove from host %s', host['name'])
                return False
        except Exception as e:
            error_msg = (("Removing initiators {0} from host {1} failed"
                          "with error {2}").format(
                remove_list, host['name'], str(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))

    def update_host(self, host, new_name=None, host_connectivity=None):
        try:
            self.conn.provisioning.modify_host(
                host['id'], name=new_name, host_connectivity=host_connectivity)
            return True
        except Exception as e:
            error_msg = 'Renaming of host {0} failed with error {1}'.format(
                host['name'], str(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))

    def delete_host(self, host):
        '''
        Delete host from system
        '''
        try:
            self.conn.provisioning.delete_host(host['id'])
            return True
        except Exception as e:
            error_msg = ('Delete host {0} failed with error {1}'.format(
                host['name'], str(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg, **utils.failure_codes(e))

    def validate_initiators(self, detailed_initiators):
        for initiator in detailed_initiators:
            if (initiator['chap_single_username']
                    or initiator['chap_mutual_username']):
                if initiator['port_type'] == PORT_TYPES[1]:  # FC
                    error_msg = "CHAP authentication is not supported " \
                                "for FC initiator type."
                    LOG.error(error_msg)
                    self.module.fail_json(msg=error_msg)
                elif initiator['port_type'] == PORT_TYPES[2]:  # NVMe
                    error_msg = "CHAP authentication is not supported " \
                                "for NVMe initiator type."
                    LOG.error(error_msg)
                    self.module.fail_json(msg=error_msg)

    def _create_result_dict(self, changed, host_id):
        self.result['changed'] = changed
        if self.module.params['state'] == 'absent':
            self.result['host_details'] = dict()
        else:
            self.result['host_details'] = self.get_host(host_id)

    def perform_module_operation(self):
        '''
        Perform different actions on host based on user parameter
        chosen in playbook
        '''
        state = self.module.params['state']
        initiator_state = self.module.params['initiator_state']
        host_name = self.module.params['host_name']
        host_id = self.module.params['host_id']
        initiators = self.module.params['initiators']
        detailed_initiators = self.module.params['detailed_initiators']
        new_name = self.module.params['new_name']
        os_type = self.module.params['os_type']
        host_connectivity = self.module.params['host_connectivity']

        if host_name:
            host_id = self.get_host_id_by_name(host_name)
        if host_id:
            host = self.get_host(host_id)
            host_name = host['name']
        else:
            host = None
        changed = False

        if initiator_state and ((initiators is None or not len(initiators))
                                and (detailed_initiators is None
                                     or not len(detailed_initiators))):
            error_msg = "initiators or detailed_initiators are " \
                        "mandatory along with initiator_state. Please " \
                        "provide a valid value."
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
        if (initiators or detailed_initiators) and initiator_state is None:
            error_msg = "initiator_state is mandatory along with " \
                        "initiators or detailed_initiators. Please " \
                        "provide a valid value."
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

        # validate detailed initiators dict
        if detailed_initiators and initiator_state is not None:
            self.validate_initiators(detailed_initiators)

        if state == 'present' and not host and host_name:
            if self.module.params['new_name']:
                error_msg = "Operation on host failed as new_name is given " \
                            "for a host that doesnt exist."
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)

            if initiator_state != "present-in-host":
                error_msg = "Incorrect initiator_state specified for Create" \
                            " host functionality"
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
            LOG.info('Creating host %s', host_name)
            changed = self.create_host(host_name)
            if changed:
                host_id = self.get_host_id_by_name(host_name)

        if host and os_type and os_type != host["os_type"]:
            error_msg = "os_type cannot be modified for an already existing" \
                        " host."
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

        if (state == 'present' and host
                and initiator_state == 'present-in-host'
                and (initiators or detailed_initiators)):
            LOG.info('Adding initiators to host %s', host_id)
            changed = (self.add_host_initiators(host) or changed)

        if (state == 'present' and host
                and initiator_state == 'absent-in-host'
                and (initiators or detailed_initiators)):
            LOG.info('Removing initiators from host %s', host_id)
            changed = (self.remove_host_initiators(host) or changed)

        if state == 'present' and host and (new_name or host_connectivity):
            modify_flag = is_modify_required(host, new_name, host_connectivity)
            if modify_flag:
                changed = self.update_host(host=host, new_name=new_name,
                                           host_connectivity=host_connectivity)

        if state == 'absent' and host:
            LOG.info('Delete host %s ', host['name'])
            changed = self.delete_host(host) or changed

        self._create_result_dict(changed, host_id)
        # Update the module's final state
        LOG.info('changed %s', changed)
        self.module.exit_json(**self.result)


def is_modify_required(host, new_name, host_connectivity):
    """ Check whether modification for host is required or not."""

    modify_flag = False
    if new_name is not None and host['name'] != new_name:
        modify_flag = True
    if host_connectivity is not None and \
            host['host_connectivity'] != host_connectivity:
        modify_flag = True
    return modify_flag


def get_powerstore_host_parameters():
    """This method provides the parameters required for the ansible host
       module on PowerStore"""
    return dict(
        host_name=dict(required=False, type='str'),
        host_id=dict(required=False, type='str'),
        initiators=dict(required=False, type='list', elements='str'),
        detailed_initiators=dict(
            type='list', required=False, elements='dict',
            options=dict(port_name=dict(type='str', required=True),
                         port_type=dict(type='str', required=False,
                                        choices=PORT_TYPES),
                         chap_single_username=dict(type='str',
                                                   required=False),
                         chap_single_password=dict(type='str',
                                                   required=False,
                                                   no_log=True),
                         chap_mutual_username=dict(type='str',
                                                   required=False),
                         chap_mutual_password=dict(type='str',
                                                   required=False,
                                                   no_log=True))
        ),
        state=dict(required=True, choices=['present', 'absent'],
                   type='str'),
        initiator_state=dict(required=False, choices=['absent-in-host',
                                                      'present-in-host'],
                             type='str'),
        new_name=dict(required=False, type='str'),
        os_type=dict(
            required=False, type='str',
            choices=['Windows', 'Linux', 'ESXi', 'AIX', 'HP-UX', 'Solaris']),
        host_connectivity=dict(
            required=False, type='str',
            choices=['Local_Only', 'Metro_Optimize_Both',
                     'Metro_Optimize_Local', 'Metro_Optimize_Remote'])
    )


def main():
    ''' Create PowerStore host object and perform action on it
        based on user input from playbook'''
    obj = PowerStoreHost()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
