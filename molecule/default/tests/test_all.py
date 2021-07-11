#!/usr/bin/env python3

import os, pytest, yaml

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(os.environ["MOLECULE_INVENTORY_FILE"]).get_hosts("all")


def is_centos7(host, port, protocol):

    os_release_file = host.file("/etc/os-release")
    centos = 'ID="centos"'
    version = 'VERSION_ID="7"'

    if os_release_file.contains(centos) and os_release_file.contains(version):
        content = '<port protocol="{}" port="{}"/>'.format(protocol, port)
    else:
        content = '<port port="{}" protocol="{}"/>'.format(port, protocol)

    return content


@pytest.mark.parametrize("pkg", ["firewalld"])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize("svc", ["firewalld"])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


def test_custom_ssh_port_is_set(host):

    file = host.file("/etc/firewalld/services/ssh.xml")

    assert file.exists
    assert file.contains(is_centos7(host, "42749", "tcp"))


@pytest.mark.parametrize("zones", ["custom1", "custom2"])
def test_zones_exist(host, zones):

    file = host.file("/etc/firewalld/zones/{}.xml".format(zones))
    assert file.exists


@pytest.mark.parametrize(
    "port,protocol",
    [
        ("8080", "tcp"),
        ("42749", "tcp"),
        ("1714-1764", "tcp"),
        ("1714-1764", "udp"),
    ],
)
def test_ports_in_zone(host, port, protocol):

    file = host.file("/etc/firewalld/zones/public.xml")

    assert file.contains(is_centos7(host, port, protocol))


@pytest.mark.parametrize("svc", ["dhcp", "dns"])
def test_services_in_zone(host, svc):

    file = host.file("/etc/firewalld/zones/public.xml")
    content = '<service name="{}"/>'.format(svc)

    assert file.contains(content)


def test_services_not_in_zone(host):

    file = host.file("/etc/firewalld/zones/public.xml")
    content = '<service name="dhcpv6-client"/>'

    assert not file.contains(content)


def test_interface_in_zone(host):
    file = host.file("/etc/firewalld/zones/public.xml")
    content = '<interface name="eth0"/>'

    assert file.contains(content)


def test_target_applied(host):
    file = host.file("/etc/firewalld/zones/internal.xml")
    content = '<zone target="ACCEPT">'

    assert file.contains(content)


def test_zone_source(host):
    file = host.file("/etc/firewalld/zones/public.xml")
    content = '<source address="192.168.22.60/24"/>'

    assert file.contains(content)
