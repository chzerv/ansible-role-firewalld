# Ansible Role: Firewalld

Ansible role to install and setup [firewalld](https://firewalld.org) on Ubuntu(>20.04), RedHat/CentOS/Fedora and Archlinux systems.

> *Disclaimer*: Debian offers a very outdated version of firewalld, so it is *currently* not supported.

The role provides the ability to:

+ Add/remove *ports* to/from a specific zone.
+ Add/remove *services* to/from a specific zone.
+ Add/remove *ports* to/from specific *services*.
+ Create new zones.
+ Change the default zone.
+ Define default zone targets (ACCEPT, REJECT etc.).
+ Add/remove *interfaces* to/from a zone.
+ Add/remove *sources* to/from a zone.
+ Enable/disable masquarading for a specific zone.
+ Add/remove rich rules.

**Important:** If you are using a port other than 22 to connect to SSH, make sure to set the variable `firewalld_ssh_port` to the port you are using. This way, the port can be added to the allowed ports *before* the `firewalld` service is started, making sure you will not get locked out of the remote system.

# Requirements

None.

# Role Variables

List of variables and their default values. Make sure to also check `defaults/main.yml` for more examples.

```yaml
firewalld_ssh_port: []
```

> If you are using a port other than 22 to connect to SSH, set this variable to the port you are using.

```yaml
firewalld_default_zone: public
```

> The zone to be used as the default one. Defaults to "public".

```yaml
firewalld_add_new_zone: []
```

> Additional zones to be created. Note that either a single zone, or a list of zones can be passed to it. 

```yaml
firewalld_zone_ports: []
```

> Ports you want to add/remove to/from a zone. 

```yaml
firewalld_zone_services: []
```

> Services you want to add/remove to/from a zone. 

```yaml
firewalld_zone_masquerading: []
```

> Zones for which masquerading will be enabled or disabled.

```yaml
firewalld_zone_target: []
```

> Chage a zone's default target. Note that, setting `state: absent` will reset the target to the default value for the zone you have specified.

```yaml
firewalld_zone_interfaces: []
```

> Interfaces to add/remove to/from a zone.

```yaml
firewalld_zone_sources: []
```

> Sources to add/remove to/from a zone.

```yaml
firewalld_service_ports: []
```

> Add/remove a port from a specific service. Mostly used to change the default port of a service, e.g., to change the default SSH port.

```yaml
firewalld_rich_rules: []
```

> Rich rules to add/remove from a zone. 

Dependencies
------------

None.

## Example Playbook

Here is an example playbook that will:

+ Change the SSH port from 22 to 42900.
+ Allow ports 8080/tcp, 1714-1764/tcp and 1714-1764/udp for the `public` zone.
+ In the `public` zone, disable the `dhcpv6-client` service and enable the `dhcp` and `dns` services.
+ Assign interface `enp25s0` to the public zone.

```yaml
---
- hosts: server
  vars_files:
    - vars/main.yml

  roles:
    - { role: chzerv.firewalld }
```

The `vars/main.yml` file:

```yaml
---
firewalld_ssh_port: "42900"

firewalld_state: started
firewalld_enabled_at_boot: true

firewalld_zone_ports:
  - zone: public
    port:
      - 8080/tcp
      - 1714-1764/tcp
      - 1714-1764/udp
    state: enabled

firewalld_zone_services:
  - zone: public
    service:
      - dhcpv6-client
    state: disabled
  - zone: public
    service:
      - dhcp
      - dns
    state: enabled

firewalld_zone_interfaces:
  - zone: public
    interface: 
      - enp25s0
    state: enabled

firewalld_service_ports:
  - service: ssh
    port: 42900/tcp
    state: enabled
  - service: ssh
    port: 22/tcp
    state: disabled
```

## License

MIT / BSD

## Author Information

Chris Zervakis

