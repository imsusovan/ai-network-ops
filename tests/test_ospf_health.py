from utils.command_runner import run_docker_command
import yaml


def load_topology():
    with open("topology.yaml") as f:
        return yaml.safe_load(f)


def count_full_neighbors(output):
    return sum(1 for line in output.splitlines() if "Full/" in line)


def test_ospf_neighbors_up_and_count():
    topo = load_topology()

    for node, data in topo["nodes"].items():
        container = data["container"]

        rc, out, err = run_docker_command(container, ["vtysh", "-c", "show ip ospf neighbor"])

        assert rc == 0, f"{node}: command failed\n{err}"

        full_count = count_full_neighbors(out)

        # For your ring topology each router should have 2 neighbors
        assert full_count == 2, f"{node}: expected 2 FULL neighbors, got {full_count}\n\n{out}"
