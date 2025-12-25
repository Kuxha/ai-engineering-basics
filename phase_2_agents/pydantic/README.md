# Strict Data Modeling with Pydantic

**Goal:** Implement strict schema validation to ensure system reliability when processing non-deterministic inputs.

## The Engineering Concept
In production systems, we cannot trust external inputs (like those from an LLM) to be perfect. We use **Pydantic** to enforce a "Schema-First" design.

### Key Patterns
1.  **Constraining Output (`Literal`):**
    We restrict string fields to a specific set of allowed values (Enums). This prevents invalid states from entering the database.
    
2.  **Enforcing Invariants (`@model_validator`):**
    We encapsulate business rules (e.g., "End time must be after Start time") directly in the data model. This ensures that an invalid object cannot physically exist in memory.

### Usage
Run the script to see how the system automatically catches and rejects invalid data:
```bash
python strict_models.py