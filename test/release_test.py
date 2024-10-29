
from gtfs2gmns import GTFS2GMNS

# Input and Output Directories
gtfs_input_dir = './GTFS'
gtfs_output_dir = './GMNS'

# Time and Date Configuration
time_period = "07:00:00_08:00:00"
date_period = []  # Assuming you might add specific dates to this list for testing

# Create an instance of the GTFS2GMNS class
gtfs2gmns_converter = GTFS2GMNS(
    gtfs_input_dir=gtfs_input_dir,
    gtfs_output_dir=gtfs_output_dir,
    time_period=time_period,
    date_period=date_period
)

# Load GTFS data
print("Loading GTFS data...")
gtfs2gmns_converter.load_gtfs()

# Generate GMNS nodes and links
print("Generating GMNS nodes and links...")
nodes, links = gtfs2gmns_converter.gen_gmns_nodes_links()

# Print outputs to verify
print("Nodes DataFrame:")
print(nodes.head())  # Print first few rows of the nodes DataFrame

print("Links DataFrame:")
print(links.head())  # Print first few rows of the links DataFrame

###############################################################################################
# Generate access links if zone.csv is available
print("Generating access links...")
zone_path = './zone.csv'  # Update this path to your actual zone file location
node_path = f"{gtfs_output_dir}/node.csv"  # Assuming nodes are saved as node.csv in the GMNS directory
radius = 500.0  # Define your desired radius for linking zones to nodes
k_closest = 5  # Optional: define the number of closest nodes you want to connect to each zone

# Generate and print access links
access_links = gtfs2gmns_converter.generate_access_link(zone_path, node_path, radius, k_closest)
print("Access Links DataFrame:")
print(access_links.head())

# Save access links to a CSV file
access_links.to_csv(f"{gtfs_output_dir}/access_links.csv", index=False)
print("Access Links saved to access_links.csv.")