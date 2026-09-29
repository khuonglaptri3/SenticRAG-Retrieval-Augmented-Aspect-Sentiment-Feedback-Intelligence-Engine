### Sumarize ab the rag,chatbot,agent architecture 






| Memory type | Good store |
|---|---|
| **Short-term / working** | In-context window, lightweight cache |
| **Semantic facts** | Knowledge graph (entities + relationships) |
| **Episodic events** | Temporal graph with validity windows |
| **Unstructured text** | Vector store (still useful for fuzzy lookup) |
| **Procedural rules** | Prompt + code |

| **Memory Type** | **Role** | **Storage** | **Example** |
|---|---|---|---|
| Working memory | Immediate context for the current step | In the prompt | Current tool output the agent is evaluating |
| Episodic memory | Record of past interactions and outcomes | External store | A previous customer conversation the agent recalls |
| Semantic memory | Facts and knowledge the agent reasons over | Vector store | Product documentation retrieved at query time |
| Procedural memory | Instructions and patterns that define behavior | System prompt or config | Step-by-step playbook for handling refund requests |

### GenAI and  Agent architecture. 
- Input and gateway layer (Multimodal Parses, Semantic Router, PII Anonymizer, Rate Limiter ) 
- Core Reasoning And Orchestration (Foundation Model LLM/SLM), Planning Engine, Cyclic State Machine, Reflection Loop
- Hierarchical Memory Module : Working Context (Core Memory), Message Buffer, Recall Storage, Archival Vector Memory, Contect window. 
- Knowledge & Retrieval Layer: Advanced RAG (Hybrid Search, Cross-Encoder Reranker), GraphRAG (Knowledge Graph)
- Tools & Action Protocols : Function Calling, Model Context Protocol (MCP Host/Client/Server), MicroVM Sandboxes 
- Output & Guardrails Layer: Hallucination Verifier, Pydantic Schema Validator, Output Filter
- Observability & Operations : Distributed Tracing, Token/Cost Accounting, Drift Monitoring, Automated Evaluation