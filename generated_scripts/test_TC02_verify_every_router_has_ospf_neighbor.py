import subprocess


containers = [
    "clab-ringlab-r1",
    "clab-ringlab-r2",
    "clab-ringlab-r3",
    "clab-ringlab-r4",
    "clab-ringlab-r5",
]


def get_ospf_neighbors(container):
    try:
        result = subprocess.run(
            ["docker", "exec", container, "vtysh", "-c", "show ip ospf neighbor"],
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.splitlines()
        neighbors = []
        # Skip header lines until we find the header line starting with Neighbor ID
        start_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("Neighbor ID"):
                start_index = i + 1
                break
        for line in lines[start_index:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 7:
                continue
            neighbor_id = parts[0]
            neighbors.append(neighbor_id)
        return neighbors
    except subprocess.CalledProcessError:
        return []


def test_every_router_has_ospf_neighbor():
    print("Executing TC02 - Verify every router has at least one OSPF neighbor")
    for container in containers:
        neighbors = get_ospf_neighbors(container)
        print(f"Router {container} OSPF neighbors discovered: {neighbors}")
        assert len(neighbors) > 0, f"Router {container} has no OSPF neighbors"
