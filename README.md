Here are in-depth summaries of all five papers covering objectives, methods, key contributions, limitations, and how they relate to SFC placement and resource allocation in 5G/Beyond-5G (B5G) networks.


---

Paper 1: CNSM 2019 – Cost-Aware SFC Placement (Optimization-Based Approach)

Title: Orchestrating End-to-End Slices in 5G Networks

Objective

Optimize VNF placement to minimize bandwidth usage, deployment cost, and VNF migrations.

Ensure QoS constraints while embedding SFCs across RAN, Transport, and Core domains.


Methodology

Uses Mixed Integer Linear Programming (MILP) to determine the optimal placement of VNFs.

Three MILP models:

1. MILP-Bwt → Minimizes bandwidth consumption.


2. MILP-Cost → Minimizes the total cost of deploying VNFs.


3. MILP-Mig → Minimizes VNF migrations.



Heuristic-based method (Heu-Mig) for real-time optimization.


Key Contributions

✅ Introduced cost-efficient slicing strategies for end-to-end network slicing.
✅ Considered different trade-offs (bandwidth vs. cost vs. migration frequency).
✅ Implemented heuristics to improve computational efficiency.

Limitations

❌ Centralized approach → Not scalable for large networks.
❌ Computationally expensive → MILP models do not work in real-time.
❌ Does not support multi-domain orchestration.

Relation to ECAP

ECAP improves on CNSM 2019 by making placement decisions dynamically across multiple domains and integrating constraints like latency, reliability, and multi-generation network support (2G–6G).



---

Paper 2: NetSoft 2019 – Latency-Aware SFC Placement (Heuristic-Based Approach)

Title: Latency-Aware Service Function Chain Placement in 5G Mobile Networks

Objective

Minimize end-to-end (E2E) latency while placing SFCs across Distributed Units (DUs), Centralized Units (CUs), and Core Networks (5GC).

Ensure QoS for low-latency applications (e.g., AR/VR, autonomous driving).


Methodology

Uses Integer Linear Programming (ILP) to find optimal placement (but only feasible for small networks).

Proposes a heuristic approach to make real-time placement decisions:

1. Constraint-Aware Shortest Path First (CSPF) → Finds paths that meet latency requirements.


2. Resource Collector → Selects paths that satisfy resource constraints (CPU, bandwidth).




Key Contributions

✅ First work to explicitly model hierarchical SFC placement in 5G networks.
✅ Latency-aware approach ensures real-time service requirements.
✅ Heuristic-based placement is faster than traditional ILP models.

Limitations

❌ Heuristic methods do not guarantee optimal solutions.
❌ Not adaptable to dynamic traffic changes in real-time.
❌ No multi-domain orchestration → Assumes a single-provider environment.

Relation to ECAP

ECAP extends CSPF + Resource Allocation mechanisms but integrates them into a dynamic, constraint-aware orchestration for 2G–6G networks.



---

Paper 3: SCHE2MA – Scalable, Energy-Aware SFC Placement (Reinforcement Learning-Based Approach)

Title: SCHE2MA: Scalable, Energy-Aware, Multi-Domain Orchestration for Beyond-5G URLLC Services

Objective

Enable scalable, energy-efficient, multi-domain orchestration for Beyond-5G URLLC services.

Distribute placement decisions across multiple domains (Edge, Regional, Core).


Methodology

Uses Multi-Agent Reinforcement Learning (MARL) where each domain has an independent RL agent.

Auction-Based Migration Mechanism:

1. If a domain is overloaded, it auctions VNFs to other domains.


2. Other domains bid for these VNFs based on resource availability.




Key Contributions

✅ Introduces a multi-domain orchestration model for scalable SFC placement.
✅ Optimizes both latency and energy consumption dynamically.
✅ Auction mechanism ensures load balancing between domains.

Limitations

❌ RL-based methods require long training times.
❌ Auction-based migration introduces additional latency overhead.
❌ Fails to generalize well to unseen network conditions.

Relation to ECAP

ECAP improves SCHE2MA by removing RL training delays and avoiding auction overhead through constraint-aware plug-ins that make real-time SFC placement decisions.



---

Paper 4: TMC 2020 – Latency & Mobility-Aware SFC Placement

Title: Latency and Mobility-Aware Service Function Chain Placement for 5G Networks

Objective

Minimize latency while considering user mobility in SFC placement.

Reduce QoS degradation caused by frequent handovers and VNF migrations.


Methodology

Uses MILP-based models to reduce inter-CU handovers and optimize placement for mobile users.

Heuristic approach for large-scale networks to quickly adjust SFC placement based on mobility patterns.


Key Contributions

✅ First work to explicitly model mobility in SFC placement.
✅ Reduces unnecessary VNF migrations due to user mobility.
✅ Balances latency constraints with network resource allocation.

Limitations

❌ Does not support multi-generation networks.
❌ Still relies on MILP, which is computationally expensive.
❌ Assumes a predefined mobility model, limiting adaptability.

Relation to ECAP

ECAP extends mobility-aware placement by incorporating dynamic resource allocation for 2G–6G networks.



---

Paper 5: GCN-Based VNF Placement (AI-Driven Approach)

Title: Virtual Network Function Placement Based on Differentiated Weight Graph Convolutional Neural Network and Maximal Weight Matching

Objective

Use AI (Graph Convolutional Networks + Maximal Weight Matching) for SFC placement.

Make instant, data-driven placement decisions without retraining.


Methodology

Represents the network as a graph  and applies a Graph Convolutional Network (GCN).

Uses Maximal Weight Matching (MWM) to allocate VNFs efficiently.


Key Contributions

✅ First AI-driven model for real-time VNF placement.
✅ Instant decision-making without retraining.
✅ Outperforms RL-based models (SCHE2MA) in adaptability and speed.

Limitations

❌ Requires large datasets for training.
❌ Does not explicitly model energy efficiency.

Relation to ECAP

ECAP integrates AI-based learning with constraint-aware resource allocation to support multi-generation traffic dynamically.



---

Final Comparison of All Approaches

Would you like a diagram summarizing these approaches visually?

