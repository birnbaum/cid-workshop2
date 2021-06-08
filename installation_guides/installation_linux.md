# Installation Guide for Linux

This guide describes the steps needed in order to install and configure Eclipse MOSAIC on Debian (i.e. Ubuntu) distributions. It is based on the official guide found in the webpage [https://www.eclipse.org/mosaic/docs/getting_started/].

## Requirements

Essentially, MOSAIC requires two additional software, [Java](https://adoptopenjdk.net/?variant=openjdk16&jvmVariant=hotspot) and [SUMO](https://sumo.dlr.de/docs/Downloads.php#linux_binaries).

### Installing Java

If you have been using your computer for some time, you might already have Java installed. Type in the following terminal command to check: `java --version`

Output should look something similar to this:

```shell
openjdk 16.0.1 2021-04-20
OpenJDK Runtime Environment AdoptOpenJDK-16.0.1+9 (build 16.0.1+9)
OpenJDK 64-Bit Server VM AdoptOpenJDK-16.0.1+9 (build 16.0.1+9, mixed mode, sharing)
```

Else, if you get an error message or something similar, you need to install Java, based on the official [guide](https://adoptopenjdk.net/installation.html?variant=openjdk16&jvmVariant=hotspot#x64_linux-jdk):

1. Download the latest release: [AdoptOpenJDK](https://github.com/AdoptOpenJDK/openjdk16-binaries/releases/download/jdk-16.0.1%2B9/OpenJDK16U-jdk_x64_linux_hotspot_16.0.1_9.tar.gz)
2. Create a new directory in your home-folder called **adoptopenjdk**
   1. Use either file explorer or terminal
3. Locate the downloaded tarball using terminal
   1. If you are using a file explorer, you can right-click and select *"Open in Terminal"*.
   2. Otherwise, open the terminal and change directory to the download folder.
4. Copy-paste/move the tarball to **adoptopenjdk** and open a terminal in this folder ala Step 3.
5. Extract the tarball using `tar xzf OpenJDK16U-jdk_x64_linux_hotspot_16.0.1_9.tar.gz` or type `tar xzf Open` and click **Tab**. The terminal should autofill the rest.
6. The tarball should extract the following folder: **jdk-16.0.1+9**.
7. Open a new terminal and type in the following commands: First `cd` and then `gedit .bashrc`.
8. Insert the following line at the end: `export PATH=/home/USERNAME/adoptopenjdk/jdk-16.0.1+9/bin:$PATH`, save and exit.
   1. You can get your USERNAME using the command `whoami` in a terminal. 
9. Open a new terminal and type `java --version`. It should now be installed.

### Installing SUMO

In the terminal, type in the following commands:

```shell
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

After installation, check using `sumo --version`.

### Installing Eclipse MOSAIC

1. Download Eclipse MOSAIC 21 from [https://www.dcaiti.tu-berlin.de/research/simulation/download/]
2. Extract it in a folder and open a terminal in that folder
3. Type `chmod +x mosaic.sh`. This will make the shell script executable.
4. In the same terminal, type `./mosaic.sh -s Barnim -v`. This should run the Barnim simulation and open the web visualizer.
5. In the terminal window you should see an output similar to this:

```shell
2021-06-08 11:10:13,981 INFO  ROOT - Running Eclipse MOSAIC 21.0 on Java JRE v16.0.1 (AdoptOpenJDK)
2021-06-08 11:10:14,271 INFO  FederationManagement - Start federation with id 'Barnim'
2021-06-08 11:10:14,271 INFO  FederationManagement - Add ambassador/federate with id 'application'
2021-06-08 11:10:14,272 INFO  FederationManagement - Add ambassador/federate with id 'environment'
2021-06-08 11:10:14,273 INFO  FederationManagement - Add ambassador/federate with id 'mapping'
2021-06-08 11:10:14,273 INFO  FederationManagement - Add ambassador/federate with id 'sns'
2021-06-08 11:10:14,273 INFO  FederationManagement - Add ambassador/federate with id 'sumo'
2021-06-08 11:10:14,273 INFO  FederationManagement - Deploying federate 'sumo' locally in ./tmp/sumo
2021-06-08 11:10:14,298 INFO  FederationManagement - Starting federate 'sumo' locally in ./tmp/sumo
2021-06-08 11:10:14,298 INFO  FederationManagement - Add ambassador/federate with id 'output'
11:10:18 - Simulating: 59000000000ns (59.0s / 1000.0s) - 5.9% (RTF:0.00, ETC:unknown)           
11:10:18 - Simulating: 93000000000ns (93.0s / 1000.0s) - 9.3% (RTF:0.00, ETC:unknown)                   
11:10:19 - Simulating: 124000000000ns (124.0s / 1000.0s) - 12.4% (RTF:0.00, ETC:unknown)                
11:10:19 - Simulating: 146000000000ns (146.0s / 1000.0s) - 14.6% (RTF:0.00, ETC:unknown)                
11:10:20 - Simulating: 175000000000ns (175.0s / 1000.0s) - 17.5% (RTF:0.00, ETC:unknown)                
11:10:20 - Simulating: 195000000000ns (195.0s / 1000.0s) - 19.5% (RTF:37.26, ETC:21.7s)                 
11:10:21 - Simulating: 221000000000ns (221.0s / 1000.0s) - 22.1% (RTF:37.26, ETC:21.7s)                 
11:10:21 - Simulating: 250000000000ns (250.0s / 1000.0s) - 25.0% (RTF:37.26, ETC:21.7s)                 
11:10:22 - Simulating: 273000000000ns (273.0s / 1000.0s) - 27.3% (RTF:37.26, ETC:21.7s)                 
11:10:23 - Simulating: 302000000000ns (302.0s / 1000.0s) - 30.2% (RTF:37.26, ETC:21.7s)                 
11:10:23 - Simulating: 344000000000ns (344.0s / 1000.0s) - 34.4% (RTF:37.26, ETC:21.7s)                 
11:10:24 - Simulating: 385000000000ns (385.0s / 1000.0s) - 38.5% (RTF:37.26, ETC:21.7s)                 
11:10:24 - Simulating: 451000000000ns (451.0s / 1000.0s) - 45.1% (RTF:37.26, ETC:21.7s)                 
11:10:25 - Simulating: 555000000000ns (555.0s / 1000.0s) - 55.5% (RTF:37.26, ETC:21.7s)                 
11:10:25 - Simulating: 1000000000000ns (1000.0s) - 100.0%
11:10:25 - Duration: 00h 00m 10.008s (RTF: 99.00)
11:10:25 - Simulation finished: 101
```

**Congrats!** If you need help with problem or need troubleshooting, please feel free to contact me: [ongun.turkcuoglu@campus.tu-berlin.de]
