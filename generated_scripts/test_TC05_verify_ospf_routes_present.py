import subprocess


containers = [
    "clab-ringlab-r1",
    "clab-ringlab-r2",
    "clab-ringlab-r3",
    "clab-ringlab-r4",
    "clab-ringlab-r5",
]


def get_ospf_routes(container):
    try:
        result = subprocess.run(
            ["docker", "exec", container, "vtysh", "-c", "show ip route ospf"],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError:
        return ""


def test_ospf_routes_present():
    print("Executing TC05 - Verify OSPF routes are present on every router")
    for container in containers:
        output = get_ospf_routes(container)
        print(f"Router {container} OSPF routes output:\n{output}\n")
        # Check if output contains any route lines (skip header lines)
        # A typical OSPF route line starts with 'O' or 'O IA' or similar
        route_lines = [line for line in output.splitlines() if line.strip().startswith("O")]
        assert len(route_lines) > 0, f"Router {container} has no OSPF routes in routing table"
