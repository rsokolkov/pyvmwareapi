# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2012 VMware, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Management class for Storage-related functions (attach, detach, etc).
"""

import logging
import vim_util
import vm_util

LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler())


class VMwareVolumeOps(object):
    """
    Management class for Volume-related tasks
    """

    def __init__(self, session, cluster_name=None):
        self._session = session
        if not cluster_name:
            self._cluster = None
        else:
            self._cluster = vm_util.get_cluster_ref_from_name(
                                        self._session, cluster_name)

    def attach_disk_to_vm(self, vm_ref, instance_name,
                          adapter_type, disk_type, vmdk_path=None,
                          disk_size=None, linked_clone=False,
                          controller_key=None, unit_number=None,
                          device_name=None):
        """
        Attach disk to VM by reconfiguration.
        """
        client_factory = self._session._get_vim().client.factory
        vmdk_attach_config_spec = vm_util.get_vmdk_attach_config_spec(
                                    client_factory, adapter_type, disk_type,
                                    vmdk_path, disk_size, linked_clone,
                                    controller_key, unit_number, device_name)

        reconfig_task = self._session._call_method(
                                        self._session._get_vim(),
                                        "ReconfigVM_Task", vm_ref,
                                        spec=vmdk_attach_config_spec)
        self._session._wait_for_task(instance_name, reconfig_task)
