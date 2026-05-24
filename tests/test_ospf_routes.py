from utils.command_runner import run_docker_command
import yaml


def load_topology():
    with open("topology.yaml") as f:
        return yaml.safe_load(f)


def count_ospf_routes(output):
    return sum(1 for line in output.splitlines() if line.strip().startswith("O"))


def test_ospf_routes_present():
    topo = load_topology()

    for node, data in topo["nodes"].items():
        container = data["container"]

        rc, out, err = run_docker_command(container, ["vtysh", "-c", "show ip route ospf"])

        assert rc == 0, f"{node}: command failed\n{err}"

        route_count = count_ospf_routes(out)

        assert route_count > 0, f"{node}: no OSPF routes found\n\n{out}"
