#!/usr/bin/env python3

import os, pytest, yaml

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(os.environ["MOLECULE_INVENTORY_FILE"]).get_hosts("all")


@pytest.mark.parametrize("pkg", ["firewalld"])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize("svc", ["firewalld"])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


def test_ssh_port_is_set(host):
    stream = host.file("/tmp/ansible_vars.yml").content
    ansible_vars = yaml.full_load(stream)

    file = host.file("/etc/firewalld/services/ssh.xml")
    ssh_port = ansible_vars["firewalld_ssh_port"]
    content = '<port port="{}" protocol="tcp"/>'.format(ssh_port)

    assert file.exists
    assert file.contains(content)
