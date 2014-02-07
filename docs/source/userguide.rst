.. highlight:: bash


User guide
==========

Installation
------------

::

  - git clone -b master https://github.com/jpcw/mr.bobby.git
  - cd mr.bobby
  - python setup.py install
  - cd ../
  - git clone -b master https://github.com/jpcw/bobbyplugins.jpcw.git
  - cd bobbyplugins.jpcw
  - python setup.py install
  - cd ../bobbytemplates.thd/
  - python setup.py install

Running tests or develop

::
 
  - python setup.py develop
  - easy_install . bobbytemplates.thd[test]
  - make test -k

Usage
-----


carp_iface template
____________________

::

    jpcw$ mrbobby -O output_dir bobbytemplates.thd:carp_iface
    Welcome to mr.bobby interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.

    --> cidr ip: 192.168.1.1/25

    --> vhid: 42

    --> slave advskew: 100

    --> description: Default gateway for family home lan

    --> password: secret

    --> physical device card name: em0

    --> vlan id (1 to 4094,  0 -> no vlan carpdev) [42]:

    --> master hostname: charybde

    --> slave hostname: scylla

    --> carp_group hostname: ha

    Generated file structure at /Users/jpcw/devel/releases/working/output_dir

.. note:: Notice that by default vlan id is same as vhid, of course you could put any valable vlan id (1 to 4094), the template will create a hostname.vlanid attach to the physical device, and your carpdev will be vlanid. if you don't want attach your carp device to a vlan, just input 0 to the vlan question.
    

::
    
    jpcw$ tree output_dir/
    output_dir/
    ├── charybde
    │   └── etc
    │       ├── hostname.carp42
    │       └── hostname.vlan42
    └── scylla
        └── etc
            ├── hostname.carp42
            └── hostname.vlan42

ok lookup to generated files ::
     
    jpcw$ cat output_dir/charybde/etc/hostname.carp42
    inet 192.168.1.1 255.255.255.128 192.168.1.127 vhid 42 carpdev vlan42 pass secret group ha description "Default gateway for family home lan"
    # subnet : 192.168.1.0/25

    jpcw$ cat output_dir/charybde/etc/hostname.vlan42
    vlandev em0

    jpcw$ cat output_dir/scylla/etc/hostname.carp42
    inet 192.168.1.1 255.255.255.128 192.168.1.127 vhid 42 carpdev vlan42 advskew 100 pass secret group ha description "Default gateway for family home lan"
    # subnet : 192.168.1.0/25

    jpcw$ cat output_dir/scylla/etc/hostname.vlan42
    vlandev em0

Specifying defaults
*******************

Sometimes you might want to override defaults for a template. Given ``me.ini``:

.. code-block:: ini

    [defaults]
    advskew = 100
    vhid = 117
    description = 
    password = secret
    physdev = em0
    master = charybde
    slave = scylla
    carp_group = ha


do::

  $ mrbobby -O output_dir --config carp_iface.ini bobbytemplates.thd:carp_iface

``mrbobby`` will as you questions but default values will be also taken from config file.

mrbobby Documentation
*********************
more infos on mrbobby http://mrbobby.readthedocs.org/

