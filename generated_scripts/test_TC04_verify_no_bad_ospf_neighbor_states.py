import subprocess


containers = [
    "clab-ringlab-r1",
    "clab-ringlab-r2",
    "clab-ringlab-r3",
    "clab-ringlab-r4",
    "clab-ringlab-r5",
]

BAD_STATES = {"Down", "Init", "ExStart", "Exchange", "Loading"}


def get_ospf_neighbors_states(container):
    try:
        result = subprocess.run(
            ["docker", "exec", container, "vtysh", "-c", "show ip ospf neighbor"],
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.splitlines()
        neighbors_states = []
        # Find header line starting with Neighbor ID
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
            # State is the third column (index 2)
            state = parts[2]
            neighbors_states.append(state)
        return neighbors_states
    except subprocess.CalledProcessError:
        return []


def test_no_bad_ospf_neighbor_states():
    print(
        "Executing TC04 - Verify no OSPF neighbor is in bad states: "
        "Down, Init, ExStart, Exchange, Loading"
    )
    for container in containers:
        states = get_ospf_neighbors_states(container)
        print(f"Router {container} OSPF neighbor states: {states}")
        for state in states:
            for bad_state in BAD_STATES:
                assert not state.startswith(
                    bad_state
                ), f"Router {container} has neighbor in bad state: {state}"
