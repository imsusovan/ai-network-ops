# TC01 - Verify all lab containers are running
**Objective:**  
Ensure that all lab containers (clab-ringlab-r1 to clab-ringlab-r5) are up and running.

**Preconditions:**  
- Lab containers are deployed and accessible on the host machine.

**Steps:**  
1. Run `docker inspect <container> --format "{{.State.Running}}"` for each container.  
2. Check the output for each container.

**Expected Result:**  
- All containers return `true` indicating they are running.

---

# TC02 - Verify every router has at least one OSPF neighbor
**Objective:**  
Verify that each router in the lab has discovered at least one OSPF neighbor.

**Preconditions:**  
- OSPF is configured and running on all routers.  
- Lab containers are running.

**Steps:**  
1. Execute `docker exec <container> vtysh -c "show ip ospf neighbor"` on each router container.  
2. Parse the output to identify OSPF neighbors.

**Expected Result:**  
- Each router has at least one OSPF neighbor listed.

---

# TC03 - Verify every discovered OSPF neighbor is in Full state
**Objective:**  
Confirm that all discovered OSPF neighbors are in a Full adjacency state.

**Preconditions:**  
- OSPF neighbors are discovered on each router.  
- Lab containers are running.

**Steps:**  
1. Run `docker exec <container> vtysh -c "show ip ospf neighbor"` on each router.  
2. Parse the neighbor states.  
3. Verify each neighbor state starts with "Full" (e.g., Full, Full/DR, Full/Backup).

**Expected Result:**  
- All OSPF neighbors on every router are in Full adjacency states.

---

# TC04 - Verify no OSPF neighbor is in bad states: Down, Init, ExStart, Exchange, Loading
**Objective:**  
Ensure that no OSPF neighbor is stuck in any of the bad states: Down, Init, ExStart, Exchange, or Loading.

**Preconditions:**  
- OSPF neighbors are discovered on each router.  
- Lab containers are running.

**Steps:**  
1. Execute `docker exec <container> vtysh -c "show ip ospf neighbor"` on each router.  
2. Parse the neighbor states.  
3. Check that no neighbor state matches any of the bad states.

**Expected Result:**  
- No OSPF neighbor is in Down, Init, ExStart, Exchange, or Loading states.

---

# TC05 - Verify OSPF routes are present on every router
**Objective:**  
Verify that OSPF routes are present in the routing table of every router.

**Preconditions:**  
- OSPF is running and neighbors are established.  
- Lab containers are running.

**Steps:**  
1. Run `docker exec <container> vtysh -c "show ip route ospf"` on each router.  
2. Check the output for presence of OSPF routes.

**Expected Result:**  
- Each router has at least one OSPF route in its routing table.
