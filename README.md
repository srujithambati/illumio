# Illumio - Flow Log Parser

This Python script processes a file containing flow log data and applies tags to each row based on a lookup table. The lookup table defines a combination of destination port and protocol that maps to a specific tag. The script outputs two CSV files: one for the counts of tags applied and another for the counts of port/protocol combinations.

# How It Works

The script:

- Loads a lookup table from a CSV file, mapping destination ports and protocols to tags.
- Processes a flow log file, extracting destination ports and protocols.
- Matches each flow log entry to the lookup table, applies the corresponding tag, and counts the occurrences.
- Saves the results to two output CSV files: one with tag counts and another with port/protocol combination counts.

# Assumptions

Here are the key assumptions made when writing this solution:

1. **Flow Log Format**:
   - The flow log file follows Amazon VPC flow log version 2 format.
   - Each flow log entry has at least 14 fields.
   - The destination port is located at the 6th index (zero-based indexing).
   - The protocol code is located at the 7th index.

2. **Lookup Table Format**:
   - The lookup table is a CSV file with exactly three columns: `dstport`, `protocol`, and `tag`.
   - The lookup table uses case-insensitive matching for protocol names (e.g., `TCP` and `tcp` are treated as the same).

3. **Protocols**:
   - The program supports common protocol codes:
     - 1 = `icmp`
     - 6 = `tcp`
     - 17 = `udp`
   - Any other protocol code is treated as `'unknown'`.

4. **Unmatched Entries**:
   - If a flow log entry’s combination of destination port and protocol doesn’t exist in the lookup table, it will be tagged as `"Untagged"`.

5. **Duplicate Entries in Lookup Table**:
   - If multiple entries in the lookup table have the same `(dstport, protocol)` combination, the last entry read will override the previous ones.

6. **Overwriting Output Files**:
   - By default, running the script multiple times **overwrites** the previous output files (`tag_counts.csv` and `port_protocol_counts.csv`).

# Getting Started

### **Prerequisites**

- **Python 3.8 or above** must be installed on your machine.
- You'll need two input files:
  - **Flow log file** (e.g., `flow_log.txt`)
  - **Lookup table** (e.g., `lookup.csv`)

### **Installation**

1. Clone the repository using the following command:
    - git clone https://github.com/srujithambati/illumio.git
2. Navigate to the directory where the repository was cloned:
   - cd illumio
3. Ensure you have the necessary Python version installed. You can check your Python version with:
   - python --version

4. Prepare the required input files (`flow_log.txt` and `lookup.csv`), placing them in the same directory as the script.

### **Running the Script**

1. Prepare the two input files:
- **Flow Log File**: A file containing flow log data (`flow_log.txt`).
- **Lookup Table**: A CSV file with three columns: `dstport`, `protocol`, and `tag` (`lookup.csv`).

2. Run the script from your terminal:
   - python parseFile.py

### **Output Files**

Once the script completes, two CSV files will be created:

- **tag_counts.csv**: This file contains the counts of each tag applied to the flow log entries.
- **port_protocol_counts.csv**: This file contains the counts of unique destination port and protocol combinations.

# Tests Performed

### **Test Cases Covered**:

1. **Basic Flow Log Parsing**:
- A flow log that follows the expected format and matches entries in the lookup table.

2. **Invalid or Missing Fields in Flow Log**:
- Flow log entries with fewer than 14 fields were correctly skipped without crashing.

3. **Bad Lookup Table**:
- Rows in the lookup table with missing or invalid fields were correctly skipped.

4. **Case Insensitivity for Protocol Names**:
- Protocol names were tested in both upper and lower case to ensure case-insensitive matching (`tcp` vs. `TCP`).

5. **Duplicate Port/Protocol Entries**:
- Tested the lookup table with duplicate entries for the same port/protocol combination to ensure that the last entry is applied.

6. **Unmatched Entries**:
- Flow log entries with ports or protocols not present in the lookup table were correctly tagged as `"Untagged"`.


### **Test Results**:
All test cases passed, and the program handled invalid input gracefully without crashing.


