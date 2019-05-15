#################################
#
# James Remer
# VirtualBox Automation
# Date Created: 4/5/19
# Late Updated: 4/29/19
#
# Description: VirtualMachine Class
#
#################################
class VirtualMachine:

    def __init__(self, name, memorySize, vramSize, osType, netAdapter, state, machineID):

        self.name = name
        self.memorySize = memorySize
        self.vramSize = vramSize
        self.osType = osType
        self.netAdapter = netAdapter
        self.state = state
        self.machineID = machineID



