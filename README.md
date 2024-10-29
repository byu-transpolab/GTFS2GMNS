## GTFS2GMNS

The open-source Python package, gtfs2gmns, is released to facilitate researchers and planners to construct the multi-modal transit networks easily from generic [General Transit Feed Specification (GTFS)](https://gtfs.org/) to the network modeling format in [General Modeling Network Specification (GMNS)](https://github.com/zephyr-data-specs/GMNS). The converted physical and service networks in GMNS format are more convenient for network modeling tasks such as transit network routing, traffic flow assignment, simulation, and service network optimization.

### *Input and Output*

**Input**: Static GTFS data
**Output**: Transit service network with GMNS format (node.csv and link.csv).
Users can customize:
1. the path of input GTFS data and output GMNS files
2. `time_period`, such as 12:00 to 13:00.
3. `date_period`, such as 10/29/2024.


## Getting Started

### *Download GTFS Data*

On TransitFeed [homepage](https://transitfeeds.com/), users can browse and download official GTFS  feeds from around the world. Make sure that the following files are present, so that we can proceed.

* stop.txt
* route.txt
* trip.txt
* stop_times.txt
* agency.txt

GTFS2GMNS can handle the transit data from several agencies. Users need to configure different sub-files in the same directory. Under the `test/GTFS` folder, a subfolder `BART` with its own GTFS data is set up.

### *Install gtfs2gmns package*

Before you install gtfs2gmns, please ensure you have installed Python 3.9 or higher on your system.

Please open your terminal (or command prompt) and run the following command:

```python
pip install gtfs2gmns
```

This command will download and install gtfs2gmns along with any necessary dependencies.

_Optional_: Installing in a virtual environment 

If you prefer to keep your Python environment isolated for specific projects, you can install gtfs2gmns in a virtual environment.

1. Create a virtual environment (replace env_name with your preferred name):

python -m venv env_name

2. Activate the virtual environment:
On Windows: .\env_name\Scripts\activate
On macOS/Linux: source env_name/bin/activate

3. Install gtfs2gmns within the virtual environment:
pip install gtfs2gmns

4. To exit the virtual environment, simply type:
deactivate

### *Step 3: Run test code*

```python
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
```

## Main steps in gtfs2gmns code

### *1. Read GTFS data*

**1.1 Read routes.txt**

- route_id, route_long_name, route_short_name, route_url, route_type

**1.2 Read stop.txt**

- stop_id, stop_lat, stop_lon, direction, location_type, position, stop_code, stop_name, zone_id

**1.3 Read trips.txt**

- trip_id, route_id, service_id, block_id, direction_id, shape_id, trip_type
- and create the directed_route_id by combining route_id and direction_id

**1.4 Read stop_times.txt**

- trip_id, stop_id, arrival_time, deaprture_time, stop_sequence
- create directed_route_stop_id by combining directed_route_id and stop_id through the trip_id

  > Note: the function needs to skip this record if trip_id is not defined, and link the virtual stop id with corresponding physical stop id.
  >
- fetch the geometry of the direction_route_stop_id
- return the arrival_time for every stop

### *2. Building service network*

**2.1 Create physical nodes**

- physical node is the original stop in standard GTFS

**2.2 Create directed route stop vertexes**

- add route stop vertexes. the node_id of route stop nodes starts from 100001

  > Note: the route stop vertex the programing create nearby the corresponding physical node, to make some offset.
  >
- add entrance link from physical node to route stop node
- add exit link from route stop node to physical node. As they both connect to the physical nodes, the in-station transfer process can be also implemented

**2.3 Create physical arcs**

- add physical links between each physical node pair of each trip

**2.4 Create service arcs**

- add service links between each route stop pair of each trip

### Functions and Attributes


| func_type     | func_name                    | Python example | Input | Output    | Remark                                                        |
| :------------ | :--------------------------- | :------------- | ----- | --------- | ------------------------------------------------------------- |
| read-show     | agency                       | `gg.agency`    | NA    | DataFrame | This attribute load and return agency data from source folder |
|               | calendar                     | `gg.calendar`  |       |           |                                                               |
|               | calendar_dates               |                |       |           |                                                               |
|               | fare_attributes              |                |       |           |                                                               |
|               | fare_rules                   |                |       |           |                                                               |
|               | feed_info                    |                |       |           |                                                               |
|               | frequencies                  |                |       |           |                                                               |
|               | routes                       |                |       |           |                                                               |
|               | shapes                       |                |       |           |                                                               |
|               | stops                        |                |       |           |                                                               |
|               | stop_times                   |                |       |           |                                                               |
|               | trips                        |                |       |           |                                                               |
|               | transfers                    |                |       |           |                                                               |
|               | timepoints                   |                |       |           |                                                               |
|               | timepoint_times              |                |       |           |                                                               |
|               | trip_routes                  |                |       |           |                                                               |
|               | stops_freq                   |                |       |           |                                                               |
|               | routes_freq                  |                |       |           |                                                               |
|               | rute_segments                |                |       |           |                                                               |
|               | route_segment_speed          |                |       |           |                                                               |
|               | vis_stops_freq               |                |       |           |                                                               |
| analysis      | vis_routes_fres              |                |       |           |                                                               |
|               | vis_route_segment_speed      |                |       |           |                                                               |
|               | vis_route_segment_runtime    |                |       |           |                                                               |
|               | vis_route_stop_speed_heatmap |                |       |           |                                                               |
|               | vis_spacetime_trajectory     |                |       |           |                                                               |
|               | equity_alanysis              |                |       |           |                                                               |
|               | accessibility_analysis       |                |       |           |                                                               |
|               | load_gtfs                    |                |       |           |                                                               |
|               | gen_gmns_node_link           |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
| visualization |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |
|               |                              |                |       |           |                                                               |



## Visualization

You can visualize generated networks using [NeXTA](https://github.com/xzhou99/NeXTA-GMNS) or [QGIS](https://qgis.org/).

## Upcoming Features

- [ ] Map matching transit network and auto network.
- [ ] Set the time period and add vdf_fftt and vdf_freq fields in link files.
- [ ] Add Visualization functions
  - [ ] Stops
  - [ ] Routes
  - [ ] ...

