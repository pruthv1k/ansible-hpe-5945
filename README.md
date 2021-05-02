# Introduction

This project contains playbooks that can are used to automate HP Comware 5945 switch.  

The playbook utilize ansible-hpe-cw7 modules which rely on NETCONF to communicate with the device for making configuration changes and getting operational data back such as LLDP neighbors, OS, serial number, uptime, and active interfaces on the device.

## Prepare Switch for Ansible

### Create User Account
If a user account already exists on the switch that can be used to login via SSH and make changes, there is no need to create a new account.

If there isn't an account already created, here is an example of how to create one:

```
#
local-user hp
 password simple hp123
 service-type ssh http https
 authorization-attribute user-role network-admin
#
line vty 0 15
 authentication-mode scheme
 user-role network-admin

```

### Enable SSH

```
ssh server enable
ssh user hp service-type all authentication-type password
```

### Enable NETCONF

```
netconf ssh server enable
```

### Enable SCP

This step is only required when using specific Ansible modules that copy files from the local Ansible control host to the HP switch.  Three of these modules include: `comware_install_config`, `comware_install_os`, and `comware_file_copy`.

```
scp server enable
```


## Prepare Controller

While in a terminal session on your Linux machine, execute the following commands:

```
$ sudo apt-get install python-pip
$ sudo pip install markupsafe
$ sudo pip install ansible
$ yum install gcc libffi-devel python-devel OpenSSL-devel
$ yum install -y python3-setuptools
$ pip3 install --upgrade pip
$ pip3 install pycrypto
$ pip3 install py3hpecw7
```

## Verify Library is Installed Correctly

Enter a new terminal session and source the following env.

```
$ source hpep3/bin/activate
```

Run the following code

```
$python ~/ansible-hpe-5945/hpepytest.py
```

## Install HP Ansible Modules

First go back to your home directory.
```
$ cd
```

Perform a clone of this project.

```
$ git clone https://github.com/cpranava/ansible-hpe-5945
$ cp library/modules/network/comware/ /usr/share/ansible/plugins/modules/
```

## Automation Usecases

### Ansible Introduction & Example Playbook 1

Open the file called `hp-vlans.yml`.  This is a playbook that is automating VLAN provisioning across HP switches.

The following is the contents of the file `hp-vlans.yml`

```
---

  - name: VLAN Automation with Ansible on HP Com7 Devices
    hosts: switches 
    gather_facts: no
    connection: local
    vars_files:
      - vars-hp-vlans.yml 
    tasks:
      - name: ensure VLAN {{ item }} exists
        comware_vlan: 
          vlanid: "{{ item }}"
          name: "VLAN_{{ item }}" 
          descr: LOCALSEGMENT 
          username: "{{ username }}" 
          password: "{{ password }}"
          hostname: "{{ inventory_hostname }}"
          state: present
        with_items:
          - "{{ vlan_list }}"
```
The following is the contents of the file `hp-vlans.yml`
```
---
 vlan_list:
   - 10
   - 20
```

The following is the contents of the file `hosts`
```
[all:vars]
username=priya
password=123456789
ansible_python_interpreter=/usr/bin/python3
[switches]
hp1

```


While in the current directory where the `hp-vlans.yml` is located, execute the following command:

```
$ ansible-playbook -i hosts hp-vlans.yml 
```

You will then see the following output:

```
PLAY [VLAN Automation with Ansible on HP Com7 Devices] ***********************************

TASK [ensure VLAN {{ item }} exists] *****************************************************
changed: [hp1] => (item=10)
changed: [hp1] => (item=20)
[WARNING]: The value "10" (type int) was converted to "'10'" (type string). If this does
not look like what you expect, quote the entire value to ensure it does not change.
[WARNING]: The value "123456789" (type int) was converted to "'123456789'" (type string).
If this does not look like what you expect, quote the entire value to ensure it does not
change.
[WARNING]: Module did not set no_log for password
[WARNING]: The value "20" (type int) was converted to "'20'" (type string). If this does
not look like what you expect, quote the entire value to ensure it does not change.

PLAY RECAP *******************************************************************************
hp1                        : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

To verify, while in the current directory where the `hpepytest.py` is located, execute the following command:

```
$ python hpepytest.py
```

You will then see the following output:
```
device.open()
<ncclient.manager.Manager object at 0x7f9cdb63a0b8>
{'vlanid': '10', 'name': 'VLAN_10', 'descr': 'LOCALSEGMENT'}
11 VLAN does not exist
12 VLAN does not exist
13 VLAN does not exist
14 VLAN does not exist
15 VLAN does not exist
16 VLAN does not exist
17 VLAN does not exist
18 VLAN does not exist
19 VLAN does not exist
{'vlanid': '20', 'name': 'VLAN_20', 'descr': 'LOCALSEGMENT'}
```


### Example Playbook 2


This playbook is the `hp-interface-vlan-config.yml` file.

```
---
 - name: VLAN Automation with Ansible on HP Com7 Devices
   hosts: switches 
   gather_facts: no
   connection: local
   vars_files:
      - vars-hp-interface-vlan-config.yml 
   tasks:
     - name: Configure {{ vlans }} as vlans on {{ interface_name }}
       comware_switchport: 
         name: "{{ interface_name }}"
         link_type: trunk
         permitted_vlans: "{{ vlans }}"
         username: "{{ username }}" 
         password: "{{ password }}" 
         hostname: "{{ inventory_hostname }}"
```

The following is the contents of the file `vars-hp-interface-vlan-config.yml`
```
---
  interface_name: FortyGigE1/0/2 
  vlans: "1-3,5,8-10" 
```

The following is the contents of the file `hosts`
```
[all:vars]
username=priya
password=123456789
ansible_python_interpreter=/usr/bin/python3
[switches]
hp1

```


While in the current directory where the `hp-interface-vlan-config.yml` is located, execute the following command:

```
$ ansible-playbook -i hosts hp-interface-vlan-config.yml
```

You will then see the following output:

<To-be-added>


### Example Playbook 3

This playbook is the `hp-create-user.yml` file.

```
---
 - name: VLAN Automation with Ansible on HP Com7 Devices
   hosts: switches 
   gather_facts: no
   connection: local
   vars_files:
      - vars-hp-create-user.yml 
   tasks:
     - name: Create {{ new_user }} with privileges {{ new_role_name }}
       comware_command:
         type: config
         command:
           - local-user {{ new_user }}
           - password simple {{ new_password }}
           - service-type ssh http https
           - authorization-attribute user-role {{ new_role_name }}
         username: "{{ username }}" 
         password: "{{ password }}" 
         hostname: "{{ inventory_hostname }}"
```
The following is the contents of the file `vars-hp-create-user.yml`
```
---
 new_user: ansible_test_user
 new_password: r3dh4t1!
 new_role_name: network-admin
```

The following is the contents of the file `hosts`
```
[all:vars]
username=priya
password=123456789
ansible_python_interpreter=/usr/bin/python3
[switches]
hp1

```
While in the current directory where the `hp-create-user.yml` is located, execute the following command:

```
$ ansible-playbook -i hosts hp-interface-vlan-config.yml
```

To verify, execute the following command:
```
ssh ssh -p 22 ansible_test_user@192.168.10.2
```

Enter the pasword mentioned in the vars file to get the following output:
```
******************************************************************************
* Copyright (c) 2010-2019 Hewlett Packard Enterprise Development LP          *
* Without the owner's prior written consent,                                 *
* no decompiling or reverse-engineering shall be allowed.                    *
******************************************************************************

<HPE>
```


# Requirements

* Comware 7 switch that supports NETCONF over SSH (not SOAP)
* Modules require the pyhpecw7 library as described above
* Devices require NETCONF to be enabled
* All testing was performed on HP 5945 switches

