import csv
from collections import defaultdict

def load_lookup_table(lookup_file):
    """
    Load the lookup table from a CSV file into a dictionary.
    The dictionary maps (dstport, protocol) to a tag.
    """
    lookup = {}  # Initialize an empty dictionary for the lookup table
    try:
        with open(lookup_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row_num, row in enumerate(reader, start=1):
                # Ensure the row has at least 3 columns (dstport, protocol, tag)
                if len(row) < 3:
                    print(f"Skipping row {row_num} in lookup table: insufficient columns")
                    continue
                try:
                    # Extract and convert dstport to an integer, protocol to lowercase
                    dstport = int(row[0])
                    protocol = row[1].strip().lower()
                    tag = row[2].strip()  # Tag doesn't need conversion
                    lookup[(dstport, protocol)] = tag  # Store the (dstport, protocol) -> tag mapping
                except ValueError:
                    print(f"Skipping row {row_num} in lookup table: invalid port or protocol")
                    continue
    except FileNotFoundError:
        print(f"Error: The lookup file '{lookup_file}' was not found.")
    except Exception as e:
        print(f"Error while reading the lookup file: {e}")
    return lookup

def process_flow_log(log_file, lookup):
    """
    Process the flow log file and count how many times each tag and port/protocol combination appears.
    """
    tag_counts = defaultdict(int)  # Dictionary to count occurrences of each tag
    port_protocol_counts = defaultdict(int)  # Dictionary to count occurrences of each port/protocol combination

    # Map protocol codes (e.g., 6 = tcp, 17 = udp) to their string representation
    protocol_map = {
        1: 'icmp',
        6: 'tcp',
        17: 'udp'
    }

    try:
        with open(log_file, mode='r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                parts = line.split()
                # Ensure that the line has at least 14 fields before accessing dstport and protocol
                if len(parts) < 14:
                    print(f"Skipping line {line_num} in flow log: insufficient fields")
                    continue
                try:
                    # Extract dstport and protocol code from the log entry
                    dstport = int(parts[6])  # Destination port is at index 6
                    protocol_code = int(parts[7])  # Protocol code is at index 7
                    protocol = protocol_map.get(protocol_code, 'unknown')  # Convert protocol code to name
                except ValueError:
                    print(f"Skipping line {line_num} in flow log: invalid port or protocol code")
                    continue  # Skip lines with conversion errors

                # Use the lookup table to find the appropriate tag for this port/protocol combination
                tag = lookup.get((dstport, protocol), "Untagged")
                # Increment the tag count and the port/protocol combination count
                tag_counts[tag] += 1
                port_protocol_counts[(dstport, protocol)] += 1
    except FileNotFoundError:
        print(f"Error: The log file '{log_file}' was not found.")
    except Exception as e:
        print(f"Error while processing the log file: {e}")

    return tag_counts, port_protocol_counts

def save_tag_counts(tag_counts, output_file):
    """
    Save the counts of each tag to a CSV file.
    """
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Tag', 'Count'])  # Write header row
            for tag, count in sorted(tag_counts.items()):
                writer.writerow([tag, count])  # Write each tag and its count
    except Exception as e:
        print(f"Error while saving tag counts: {e}")

def save_port_protocol_counts(port_protocol_counts, output_file):
    """
    Save the counts of each port/protocol combination to a CSV file.
    """
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Port', 'Protocol', 'Count'])  # Write header row
            # Write each port/protocol combination and its count
            for (port, protocol), count in sorted(port_protocol_counts.items()):
                writer.writerow([port, protocol, count])
    except Exception as e:
        print(f"Error while saving port/protocol counts: {e}")

def main():
    """
    Main function that coordinates the loading of lookup table, processing of flow log, and saving results.
    """
    flow_log_file = "flow_log.txt"  # Path to the flow log file
    lookup_file = "lookup.csv"  # Path to the lookup table CSV file
    tag_output_file = "tag_counts.csv"  # Path to save the tag counts CSV file
    port_protocol_output_file = "port_protocol_counts.csv"  # Path to save the port/protocol counts CSV file
    
    # Load the lookup table into a dictionary
    lookup = load_lookup_table(lookup_file)
    # If the lookup table is empty, exit the program early
    if not lookup:
        print("No valid entries in the lookup table. Exiting.")
        return
    
    # Process the flow log to get counts of tags and port/protocol combinations
    tag_counts, port_protocol_counts = process_flow_log(flow_log_file, lookup)
    
    # Save the results to CSV files
    save_tag_counts(tag_counts, tag_output_file)
    save_port_protocol_counts(port_protocol_counts, port_protocol_output_file)
    
    print("Processing completed. Output saved.")

if __name__ == "__main__":
    main()

