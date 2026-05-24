# OSPF Testcase Requirements

The lab has 5 FRR containers: r1, r2, r3, r4, r5.

Each router participates in OSPF area 0.

Basic validations:
1. OSPF daemon must be running.
2. Each router must have 2 FULL OSPF neighbors.
3. OSPF routes must be present.
4. Failures must clearly show router name and command output.

Useful commands:
- show ip ospf neighbor
- show ip route ospf
- show running-config
- ip -br addr
