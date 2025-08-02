# Bridging Imperative Process Models and Process Data Queries—Translation and Relaxation


This repository provides a Python command-line tool for interactively manipulating a matrix representation of activities and their relationships. The tool supports a variety of relaxation and transformation operations on the activity matrix, can generate declarative constraints.

## Getting Started

### Prerequisites

- Python 3.x
- pandas
- pm4py

### Installation

Install the required Python packages:

```bash
pip install pandas pm4py
```

### Usage

1. **Run the main script with a txt file:**

    ```bash
    python driver.py <path_to_txt_file>
    ```
    ```example
    python .\driver.py .\data\BPIC19-Matrix.txt
    ```

2. Relaxation operations for BPIC19 Model
- **Turn Exclusive (#) into Direct Relationship (→)** RIR, RIR
- **Turn Direct (→) into Indirect Relationship (≺)** RIR, RIR
- **Turn Exclusive (#) into Direct Relationship (→)** RGR, RGR
- **Turn Direct (→) into Indirect Relationship (≺)** RGR, RGR
- **Remove All Relationships Between Two Activities** CP, CQ
- **Remove All Relationships Between Two Activities** ROC, CQ
- **Remove All Relationships Between Two Activities** CPOI, CP
- **Remove All Relationships Between Two Activities** CPOI, CQ
- **Remove All Relationships Between Two Activities** CPOI, ROC
- **Remove All Relationships Between Two Activities** CPRI, CP
- **Remove All Relationships Between Two Activities** CPRI, CQ

