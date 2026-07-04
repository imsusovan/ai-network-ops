---

# 📘 Project: AI-Network-Ops

AI-driven insights for network operations — combining routing data (BGP/OSPF) with large language models for anomaly detection, policy automation, and intelligent troubleshooting.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen)
![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🔍 Overview
This proof-of-concept explores how **AI can enhance Border Gateway Protocol (BGP)** and OSPF operations. By integrating LLM-driven analysis with routing data, the project demonstrates potential applications such as anomaly detection, automated policy suggestions, and intelligent troubleshooting.

---
🏗️ Architecture
https://copilot.microsoft.com/th/id/BCO.767b4425-3e03-4d4f-b506-a69dbb2be4a0.png

+-------------------+
|   Data Sources    |  <-- BGP/OSPF routing data, configs
+-------------------+
          |
          v
+-------------------+
|   RAG Pipeline    |  <-- Retrieval-Augmented Generation
+-------------------+
          |
          v
+-------------------+
|   LLM Runner      |  <-- AI-driven analysis & suggestions
+-------------------+
          |
          v
+-------------------+
|   Reports/Tests   |  <-- OSPF test reports, CI/CD outputs
+-------------------+

![AI-Network-Ops Architecture](architecture.png)



Key Components
llm_runner.py → Core AI execution logic

rag/ → Retrieval-Augmented Generation modules

scripts/ → Utility scripts for automation

tests/ → Unit & integration test cases

jenkins/ → CI/CD pipelines for static analysis

sonar-project.properties → SonarQube integration

Features
AI-driven insights for BGP/OSPF routing

Automated test reports (ospf_test_report.txt)

Jenkins pipelines for static analysis

SonarQube integration for code quality

Modular design for extensibility

Testing
Run all tests:

pytest tests/

Integration test example:
python tests/integration/ospf_test.py

Sample output:
================== test session starts ==================
collected 12 items

tests/test_utils.py .....
tests/test_rag.py .....
tests/test_llm_runner.py ...

================== 12 passed in 2.34s ==================

Roadmap
Expand unit test coverage

Add real-world BGP datasets

Enhance logging & error handling

Publish demo notebooks with sample outputs





## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/imsusovan/ai-network-ops.git
cd ai-network-ops

# Install dependencies
pip install -r requirements.txt

# Run the AI-Network-Ops integration
python llm_runner.py --config config.yaml
