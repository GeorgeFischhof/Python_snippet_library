

"""Manipulate virtual machines on ESX, uses library PyVmomi 6.5
usage example
host, username, password values must be added correctly in function __init__ 



from vmware import ESX

esx = ESX()
vm_name = 'machine_name_in_inventory'
snapshot_name = 'my_snapshot'
esx.vm_revert_to_snapshot(vm_name, snapshot_name)
esx.vm_power_on(vm_name)
esx.vm_power_reboot(vm_name)
esx.vm_power_shutdown(vm_name)
esx.vm_power_off(vm_name)
esx.get_virtual_machine_ip_address(vm_name) # returns the ip address of the first interface
"""

import atexit
import ssl
import time

from pyVim import connect
from pyVmomi import vim


class ESX:

    def __init__(self):

        # monkey patch to disable cert verification as we use sef-signed cert
        ssl._create_default_https_context = ssl._create_unverified_context

        host = 'my.esx.server.com'
        username = 'username'
        password = 'secret'

        service_instance = connect.Connect(host=host, user=username, pwd=password)
        atexit.register(connect.Disconnect, service_instance)
        self.content = service_instance.content

    def _get_virtual_machines(self):
        object_types_to_view = [vim.VirtualMachine]
        recursive = True
        container_view = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, object_types_to_view, recursive)

        virtual_machines = container_view.view
        return virtual_machines

    def _get_virtual_machine(self, virtual_machine_name):
        virtual_machines = self._get_virtual_machines()
        for virtual_machine in virtual_machines:
            if virtual_machine.summary.config.name == virtual_machine_name:
                return virtual_machine

    def get_virtual_machine_ip_address(self, virtual_machine_name):
        vm = self._get_virtual_machine(virtual_machine_name)
        ip_address = vm.summary.guest.ipAddress
        return ip_address

    def vm_power(self, virtual_machine_name, on_off):
        vm = self._get_virtual_machine(virtual_machine_name)
        vm_power_action = {
            'on': vm.PowerOn,
            'off': vm.PowerOff,
        }
        task = vm_power_action[on_off]()

        while task.info.state not in [vim.TaskInfo.State.success,
                                      vim.TaskInfo.State.error]:
            time.sleep(1)

    def vm_power_on(self, virtual_machine_name):
        self.vm_power(virtual_machine_name, 'on')

    def vm_power_off(self, virtual_machine_name):
        self.vm_power(virtual_machine_name, 'off')

    def vm_power_shutdown(self, virtual_machine_name):
        vm = self._get_virtual_machine(virtual_machine_name)
        vm.ShutdownGuest()
        while vm.GuestInfo.GuestState == 'shuttingDown':
            time.sleep(1)

    def vm_power_reboot(self, virtual_machine_name):
        vm = self._get_virtual_machine(virtual_machine_name)
        vm.RebootGuest()
        time.sleep(20)
        # TODO currently the finish wait is not good: reboot returns None
        # TODO uptime can be good to watch: the new uptime is less than the previous

    def vm_revert_to_snapshot(self, virtual_machine_name, snapshot_name):
        vm = self._get_virtual_machine(virtual_machine_name)
        snapshot_tree = vm.snapshot.rootSnapshotList
        for snapshot in snapshot_tree:
            if snapshot.name == snapshot_name:
                snapshot_to_revert = snapshot
                # Returns the last if there are more with the same name
        snapshot_obj = snapshot_to_revert.snapshot
        task = snapshot_obj.RevertToSnapshot_Task()
        while task.info.state not in [vim.TaskInfo.State.success,
                                      vim.TaskInfo.State.error]:
            time.sleep(1)
