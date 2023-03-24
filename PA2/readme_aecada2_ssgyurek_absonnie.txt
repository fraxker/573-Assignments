Our code utilizes the ns-3 simulator to build a dumbell topology network. This network will utilize both TCP Cubic and DCTCP. It will then show the average throughputs, standard deviations, and average flow times. We tested using python version 3.10.2, gcc version 11.3.0, and Ubuntu 22.04.

The first thing you need to run on linux command line is: sudo pip3 install cppyy==2.4.1

The above command will provide necessary C++ and python bindings.

In order to execute our code clone the following gitlab:
https://gitlab.com/nsnam/ns-3-dev/-/tree/master/

On a linux command line run: git clone https://gitlab.com/nsnam/ns-3-dev.git

The next step will be to go into the ns-dev folder by doing: cd ns-3-dev

The next part you will have to do is : ./ns3 configure --enable-python-bindings --build-profile=optimized --enable-examples --enable-tests

The above statement may take several minutes to run, but it makes sure the simulator gets configured properly with necessary files.

The last step is to type in: ./ns3 build

This will build and will take quite a long time.

After the build has finished you may need to export the path for python bindings: export PYTHONPATH=$PYTHONPATH:/mnt/c/Users/PC/573-Assignments/PA2/ns-3-dev/build/binding\python\ns

The following lines in the above path will need to be changed to your own path: c/Users/PC/573-Assignments/PA2/


Next you will change directory to where tcp_aecada2_ssgyurek_absonnie.py file is located. 

Then you will type in python3 tcp_aecada2_ssgyurek_absonnie.py and it will execute the simulation and return with a csv file.

The csv file will contain the throughput and average flow completion time for each experiment. 


The value of end time in the code will be 5 seconds and max bytes will be set to 50000000. In our code we only import the ns simulator, csv, and statistics. 
