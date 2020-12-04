# ![Picture of shortest path](https://i.imgur.com/cF4ejvv.png "")<br />

IOT project for semster 8 in software engineering.
For this project the overall goal is to further understand how the WiFi mesh network (supported by the IEEE 802.11s standard) operates. For this and furthermore, a set of bulletpoints have been made: 
- This project aims to characterize WiFi mesh networking based on off-the-shelf network components from Meshmerize.
- The project defines a set of performance metrics and conduct experiments to characterize the performance.
- A comparison between different ad hoc routing schemes is included in the project a preferable backed with quantitative investigation if the time allows.


# Current repo
#### Dynamically_plot_edges 

In this folder running `python3 ./main` without fetching live data, will result in the following images. The program tries to depict how the mesh network always chooses the shortest path.<br />
<img src="https://i.imgur.com/cgwZ9oH.png" width="350">
<img src="https://i.imgur.com/xsKUtps.png" width="350">

#### Dynamically_plot_nodes

In this folder running `python3 ./main` without fetching live data, will resul in the following image. The program tries to depict how nodes will have a greater distance on how strong their TX & RX rates are.<br />

<img src="https://i.imgur.com/F7nQ5GQ.png" width="350">

_The plotting has been done possible why the use of the python library https://networkx.org/_

## Prereqs for running ##

- pip install tabulate
- pip install networkx
- pip install pandas
- pip install matplotlib
- pip install paramiko
- pip install sympy
