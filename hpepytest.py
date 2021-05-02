from pyhpecw7.comware import HPCOM7
from pyhpecw7.features.vlan import Vlan
args = dict(host='192.168.10.2', username='priya', password='123456789', port=830, ssh_config=None)
device = HPCOM7(**args)
print('device.open()')
print(device.open())
vlan = Vlan(device, 10)
for i in range(10,21):
    vlan = Vlan(device, str(i))
    if vlan.get_config() == {}:
        print(str(i)+' VLAN does not exist')
    else:
        print(vlan.get_config()) 

