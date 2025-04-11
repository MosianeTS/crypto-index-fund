```mermaid
flowchart TD
    A[Scheduler Triggers] --> B[Fetch Current Asset Prices]
    B --> C[Log Scheduler Start]
    C --> D[Get All Active Funds]
    D --> E{Any Active Funds?}
    E -- No --> F[Log No Funds to Check]
    F --> Z[End Process]
    E -- Yes --> G[For Each Fund]
    G --> H[Calculate Current Fund Value]
    H --> I[Calculate Current Asset Percentages]
    I --> J{Any Asset Outside\nThreshold?}
    J -- No --> K[Update Last Checked Time]
    K --> N{More Funds?}
    J -- Yes --> L[Execute Rebalancing Algorithm]
    L --> M[Record Rebalance Transactions]
    M --> N
    N -- Yes --> G
    N -- No --> O[Log Scheduler Completion]
    O --> Z

    subgraph "Rebalancing Algorithm"
    L1[Calculate New Target Allocations]
    L2[Apply Asset Cap]
    L3[Calculate Required Trades]
    L4[Execute Trades]
    L5[Update Fund Asset Records]
    L1 --> L2 --> L3 --> L4 --> L5
    end
