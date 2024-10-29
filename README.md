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



## Main steps in gtfs2gmns code

### *Read GTFS data*

**Step 1.1: Read routes.txt**

- route_id, route_long_name, route_short_name, route_url, route_type

**Step 1.2: Read stop.txt**

- stop_id, stop_lat, stop_lon, direction, location_type, position, stop_code, stop_name, zone_id

**Step 1.3: Read trips.txt**

- trip_id, route_id, service_id, block_id, direction_id, shape_id, trip_type
- and create the directed_route_id by combining route_id and direction_id

**Step 1.4: Read stop_times.txt**

- trip_id, stop_id, arrival_time, deaprture_time, stop_sequence
- create directed_route_stop_id by combining directed_route_id and stop_id through the trip_id

  > Note: the function needs to skip this record if trip_id is not defined, and link the virtual stop id with corresponding physical stop id.
  >
- fetch the geometry of the direction_route_stop_id
- return the arrival_time for every stop

### *Building service network*

**Step 2.1 Create physical nodes**

- physical node is the original stop in standard GTFS

**Step 2.2 Create directed route stop vertexes**

- add route stop vertexes. the node_id of route stop nodes starts from 100001

  > Note: the route stop vertex the programing create nearby the corresponding physical node, to make some offset.
  >
- add entrance link from physical node to route stop node
- add exit link from route stop node to physical node. As they both connect to the physical nodes, the in-station transfer process can be also implemented

**Step 2.3 Create physical arcs**

- add physical links between each physical node pair of each trip

**Step 2.4 Create service arcs**

- add service links between each route stop pair of each trip

## Visualization

You can visualize generated networks using [NeXTA](https://github.com/xzhou99/NeXTA-GMNS) or [QGIS](https://qgis.org/).

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




## Upcoming Features

- [ ] Map matching transit network and auto network.
- [ ] Set the time period and add vdf_fftt and vdf_freq fields in link files.
- [ ] Add Visualization functions
  - [ ] Stops
  - [ ] Routes
  - [ ] ...

