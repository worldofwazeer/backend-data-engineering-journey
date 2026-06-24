# 03 - API Requests Engine

## 🎯 Strategic Objective
This module constructs production-ready client wrappers to query external REST APIs safely. It emphasizes network stability patterns—enforcing execution limits, catching socket timeouts, and isolating failures to prevent downstream data application crashes.

## 🛠️ Concepts Demonstrated
* **Defensive Timeout Allocation:** Forcing request constraints globally to eliminate hung connections.
* **Cascading Network Catch Hierarchies:** Separating client-side routing exceptions (4xx) from server drops (5xx) and transient connection loss.
* **Encapsulated Client Implementations:** Wrapping requests inside type-hinted extraction components for higher modularity.