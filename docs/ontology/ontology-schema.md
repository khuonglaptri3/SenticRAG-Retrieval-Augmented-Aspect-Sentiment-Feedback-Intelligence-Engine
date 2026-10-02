# SenticRAG Knowledge Graph Ontology Schema (Neo4j)

Formal specification of entity nodes and directed relationships powering **Operational GraphRAG** in SenticRAG:

```text
(Product) -[:HAS_VERSION]-> (ProductVersion)
(Review) -[:MENTIONS_ASPECT]-> (Aspect)
(Review) -[:EXHIBITS_SYMPTOM]-> (Symptom)
(Symptom) -[:CAUSED_BY]-> (RootCause)
(RootCause) -[:AFFECTS]-> (ProductVersion)
(RootCause) -[:RESOLVED_BY]-> (Resolution)
(Resolution) -[:GOVERNED_BY]-> (Policy)
(Resolution) -[:EXECUTED_AT]-> (ServiceCenter)
```

---

## 1. Core Node Types & Properties

| Node Label | Key Properties | Semantic Description |
| :--- | :--- | :--- |
| `Product` | `id`, `name`, `category`, `lifecycle_status` | Master product line (e.g. `SmartPhone-X`). |
| `ProductVersion` | `version_id`, `release_date`, `hardware_rev`, `firmware_rev` | Specific hardware batch or firmware build (e.g. `v1.2.0`). |
| `Aspect` | `aspect_name`, `taxonomy_version` | Component or feature category (e.g. `battery`, `display`, `delivery`). |
| `Symptom` | `symptom_id`, `description`, `severity` | Manifest defect behavior reported by users (e.g. `overheating_during_charge`). |
| `RootCause` | `cause_id`, `summary`, `status`, `confirmed_at` | Validated engineering defect (e.g. `power_management_loop_overflow`). Status: *emerging*, *investigating*, *confirmed*, *mitigated*. |
| `Policy` | `policy_id`, `title`, `version`, `effective_date`, `rules` | Official corporate warranty, return, or refund regulations. |
| `Resolution` | `resolution_id`, `action_type`, `instructions_markdown` | Standard operating procedure (e.g. `firmware_rollback_to_v1.1`, `battery_replacement`). |
| `ServiceCenter` | `center_id`, `name`, `region`, `address`, `contact_phone` | Physical authorized repair station for customer routing. |

---

## 2. Core Graph Traversal Pattern (Cypher Example)

To resolve an incoming defect ticket with verified policy grounding:

```cypher
MATCH (p:Product {id: $product_id})-[:HAS_VERSION]->(v:ProductVersion {version_id: $version})
MATCH (v)<-[:AFFECTS]-(rc:RootCause)-[:RESOLVED_BY]->(res:Resolution)-[:GOVERNED_BY]->(pol:Policy)
WHERE rc.status IN ['confirmed', 'mitigated']
RETURN rc.summary AS root_cause,
       res.instructions_markdown AS resolution_steps,
       pol.policy_id AS policy_reference,
       pol.version AS policy_version
LIMIT 1;
```
