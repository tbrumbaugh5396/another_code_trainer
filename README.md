```mermaid
graph TD
    %% --- LAYER 1: DATA INGESTION & FEATURE EXTRACTION ---
    subgraph Ingestion_Layer [1. Problem Analysis & Property Extraction]
        P_Raw[Problem Description]         --> P_Analytic{Extraction Engine}
        P_Raw                              --> Equal Descriptions{Equal Descriptions}
        P_Analytic                         --> P_Goal[Goal Properties]
        P_Analytic                         --> P_Cap[Capabilities/Affordances]
        P_Analytic                         --> P_Con[Constraints/Requirements]
        
        P_Con                              --> Req_Type{Requirement Type}
        Req_Type                           --> Req_Exp[Explicit: Time/Space/Input]
        Req_Type                           --> Req_Imp[Implicit: Edge Cases/Logic]
    end

    %% --- LAYER 2: THE INTERMEDIATE LOGIC GATE ---
    subgraph Logic_Gate [2. Constraint Filter & Pruning]
        P_Cap & Req_Exp & Req_Imp          --> CF_Gate{Constraint Filter}
        
        %% Component Learning (System)
        Sys_Learn[[System Learning Layer]] -.->|Refines Regex/NLP| P_Analytic
        Sys_Learn                          -.->|Tunes Mapping| CF_Gate
    end

    %% --- LAYER 3: CONCEPTUAL TAXONOMY (The Tree) ---
    subgraph Concept_Hierarchy [3. Concept & DSA Hierarchy]
        C_Root((Root Strategy))            --> C_General[General: e.g. Sorting]
        C_General                          --> C_Pattern[Pattern: e.g. Divide & Conquer]
        C_Pattern                          --> C_DSA[Specific DSA: e.g. Merge Sort]
        
        CF_Gate                            -->|Prunes| C_General
        CF_Gate                            -->|Activates| C_DSA
        
        C_DSA                              --- C_Nec[Necessary Conditions]
        C_Nec                              -.->|Back-Validation| CF_Gate
    end

    %% --- LAYER 4: SOLUTION OUTCOMES ---
    subgraph Solution_Outcomes [4. Truth Implementation]
        C_DSA                              --> T_Sol[Truth Solutions]
        T_Sol                              --> S_Meta[Metadata: Styles, Best-in-Class]
        T_Sol                              --> S_Trade[Tradeoff Area: Time vs Space]
        T_Sol                              --> S_Rel[Related/Equal Solutions]
    end

    %% --- LAYER 5: THE USER LEARNING LAYER (The Performance Tracker) ---
    subgraph User_Learning [5. Performance & Diagnostic Layer]
        User_Input[User Prediction Path]   --> Compare{Logic Gap Analyzer}
        T_Sol                              --> Compare
        
        Compare                            -->|Extraction Error| D_Pattern[Pattern Blindness]
        Compare                            -->|Filtering Error| D_Logic[Concept Misalignment]
        Compare                            -->|Implementation Error| D_Skill[Syntax/Paradigm Gap]
        
        D_Pattern & D_Logic & D_Skill      --> Heatmap[User Weakness Heatmap]
        Heatmap                            --> Recommendation[Targeted Concept Drills]
    end

    %% Styling
    style CF_Gate fill:#f39c12,stroke:#d35400,stroke-width:2px,color:#fff
    style Sys_Learn fill:#9b59b6,stroke:#8e44ad,color:#fff
    style Compare fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style Heatmap fill:#2ecc71,stroke:#27ae60,color:#fff
```
