#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ["preview"],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_compute_address
description:
    - Represents an Address resource.
    - Each virtual machine instance has an ephemeral internal IP address and,
      optionally, an external IP address. To communicate between instances on
      the same network, you can use an instance's internal IP address. To
      communicate with the Internet and instances outside of the same network,
      you must specify the instance's external IP address.
    - Internal IP addresses are ephemeral and only belong to an instance for the
      lifetime of the instance; if the instance is deleted and recreated, the
      instance is assigned a new internal IP address, either by Compute Engine
      or by you. External IP addresses can be either ephemeral or static.
short_description: Creates a GCP Address
version_added: 2.6
author: Google Inc. (@googlecloudplatform)
requirements:
    - python >= 2.6
    - requests >= 2.18.4
    - google-auth >= 1.3.0
options:
    state:
        description:
            - Whether the given object should exist in GCP
        required: true
        choices: ['present', 'absent']
        default: 'present'
    address:
        description:
            - The static external IP address represented by this resource. Only
              IPv4 is supported.
        required: false
    description:
        description:
            - An optional description of this resource.
        required: false
    name:
        description:
            - Name of the resource. The name must be 1-63 characters long, and
              comply with RFC1035. Specifically, the name must be 1-63
              characters long and match the regular expression
              [a-z]([-a-z0-9]*[a-z0-9])? which means the first character must be
              a lowercase letter, and all following characters must be a dash,
              lowercase letter, or digit, except the last character, which
              cannot be a dash.
        required: false
    region:
        description:
            - A reference to Region resource.
        required: true
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name: create a address
  gcp_compute_address:
      name: 'test-address1'
      region: 'us-west1'
      project: testProject
      auth_kind: service_account
      service_account_file: /tmp/auth.pem
      scopes:
        - https://www.googleapis.com/auth/compute
      state: present
'''

RETURN = '''
    address:
        description:
            - The static external IP address represented by this resource. Only
              IPv4 is supported.
        returned: success
        type: str
    creation_timestamp:
        description:
            - Creation timestamp in RFC3339 text format.
        returned: success
        type: str
    description:
        description:
            - An optional description of this resource.
        returned: success
        type: str
    id:
        description:
            - The unique identifier for the resource.
        returned: success
        type: int
    name:
        description:
            - Name of the resource. The name must be 1-63 characters long, and
              comply with RFC1035. Specifically, the name must be 1-63
              characters long and match the regular expression
              [a-z]([-a-z0-9]*[a-z0-9])? which means the first character must be
              a lowercase letter, and all following characters must be a dash,
              lowercase letter, or digit, except the last character, which
              cannot be a dash.
        returned: success
        type: str
    users:
        description:
            - The URLs of the resources that are using this address.
        returned: success
        type: list
    region:
        description:
            - A reference to Region resource.
        returned: success
        type: str
'''

################################################################################
# Imports
################################################################################

from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            address=dict(type='str'),
            description=dict(type='str'),
            name=dict(type='str'),
            region=dict(required=True, type='str')
        )
    )

    state = module.params['state']
    kind = 'compute#address'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                fetch = update(module, self_link(module), kind, fetch)
                changed = True
        else:
            delete(module, self_link(module), kind, fetch)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, kind, fetch):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.put(link, resource_to_request(module)))


def delete(module, link, kind, fetch):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'kind': 'compute#address',
        u'region': module.params.get('region'),
        u'address': module.params.get('address'),
        u'description': module.params.get('description'),
        u'name': module.params.get('name')
    }
    return_vals = {}
    for k, v in request.items():
        if v:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind):
    auth = GcpSession(module, 'compute')
    return return_if_object(module, auth.get(link), kind)


def self_link(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/addresses/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/addresses".format(**module.params)


def return_if_object(module, response, kind):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))
    if result['kind'] != kind:
        module.fail_json(msg="Incorrect result: {kind}".format(**result))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'address': response.get(u'address'),
        u'creationTimestamp': response.get(u'creationTimestamp'),
        u'description': response.get(u'description'),
        u'id': response.get(u'id'),
        u'name': response.get(u'name'),
        u'users': response.get(u'users')
    }


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response, 'compute#operation')
    if op_result is None:
        return None
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']), 'compute#address')


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], 'message')
        time.sleep(1.0)
        if status not in ['PENDING', 'RUNNING', 'DONE']:
            module.fail_json(msg="Invalid result %s" % status)
        op_result = fetch_resource(module, op_uri, 'compute#operation')
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


if __name__ == '__main__':
    main()
