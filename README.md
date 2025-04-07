# Dual EPR-NMR variable magnetic field cryogenic system
programming structure:

% For modularity and scalability, each component of the cryogenic magnet system will have a separate library as follow:

**project**
- components/  
  - __init__.py
  - AWT.py
  - VDIsynth.py
  - windfreak.py
  - cryomagnet.py
  - component4.py
-  SourceFiles/ %All source files regarding the controlling of the individual components
- controller.py   % This program will handle the communication between components and logs for troubleshooting 
- Pulseprogram.py % Experiment program, handling the pulse program execution and read out
- requirements.txt  % The libraries from the companies providing each components
- config.yaml     % Store setting for flexibility 



This document presents a plan for the development of a python library to control the EPR bridge of our Cryogenic system. The aims of this infrastructure are 

To make it flexible but not too much to avoid making the programming and use unnecessarily complicated. 
That the files associated with experiments reflect the spectrometer configuration (physical connections) 
That it can easily be imbedded in a GUI later 
An EPR experiment is associated with three files 

Spectrometer configuration: defines what devices is the bridge composed of and how they are connected 
Pulse program: defines the sequence of event 
Parameters: define the parameters that are necessary to run the sequence (eg: delays, pulse powers, pulse lengths) 
Classes to be constructed 

spectro=configClass(configPath): the input is the path where the configuration is saved. When an instance is created, the following tasks are realized 
Read the configuration file, create structures (eg: spectro.channel(0), spectro.devices.synth(0), …) to store the device and channel information, converting the values into the appropriate types 
Define the frequency range for each channel, which is inherited from the frequency ranges of the corresponding synthesizer and AMC  
Load the UCA, frequency, power tables of the AMC, if any. 
Set up the communication with the FTCI and serial connections 
Other methods 
spectro.checkConnection(arg): if arg is empty, check all connections. Otherwise, arg must contain a list of names of devices for which the connection is to be checked. Print result to console 
spectro.close(arg): if arg is empty, close all connections. Otherwise, arg must contain a list of names of devices where the connection is to be closed. 
spectro.reconnect(arg): arg must contain a list of names of devices where the connection is to be reestablished. 
sequence=sequenceClass(sequencePath,parameterPath): the input is the path where the pulse sequence is saved. When an instance is created, the following tasks are realized 
Read the sequence and parameter files and create a table of events. The types of events are defined below (delay, CW pulse, square pulse, shaped pulsed, delay, trigger, read signal) 
Check that parameters are within range (eg: frequencies defined for each channel, sampling rate of AWT) 
Other methods 
sequence.time(): Computes the time the sequence will take 
sequence.run(): Load sequence to devices () and run the sequence 
sequence.abort(): stop the sequence that is running by interrupting the AWT 
 

Example of Spectrometer configuration 

This configuration has 2 channels for ELDOR experiments, using 2 synth, 2 AMCs, and QO with 1 crosspolar and 1 copolar beam (with respect to the detector). This configuration is similar to the 7 T static, except that only one channel has a phase control (via AWG). The second channel can only be used as CW (or CW with frequency sweeping). 

Document setting up the configuration of the EPR spectrometer. 
The CHANNELS section reflects the physical connections between the devices, which are defied in the second section. 
 
2-channel configuration for ELDOR with 1 pulsed channel copolar with detection and 1 CW channel crosspolar with detection 
________________________________ 
## CHANNELS 
 
#1 - Pulsed, copolar 
Synthesizer		VDIS217 
AMC			AMC629-16 
MixI			AO1@TaborAWT 
MixQ			AO2@TaborAWT 
UCA			DO1@ArduinoUCA 
Switch			DO1@TaborAWT 
Max pulse		5u 
Max duty cycle		0.005 
 
#2 - CW, cross polar 
Synthesizer		VDIS218 
AMC			Tx233 
UCA			DO2@ArduinoUCA 
Switch			DO2@TaborAWT	 
________________________________ 
## DEVICES 
 
# VDIS217 
FTCI address		VDIS217 
Min freq			8 
Max freq			18 
 
# VDIS218 
FTCI address		VDIS218 
Min freq			8 
Max freq			18 
 
# AMC629-16 
Multiplication factor	16 
Min freq			190 
Max freq			196 
Power-UCA table		<path to data> 
 
# AMC629-8 
Multiplication factor	16 
Min freq			95 
Max freq			98 
Power-UCA table		<path to data> 
 
# Tx233-16 
Multiplication factor	16 
Min freq			185 
Max freq			198 
Power-UCA table		<path to data> 
 
# TaborAWT 
FTCI address		<address> 
AWG bandwidth		2.5 
Digitizer bandwidth	2.5 
Memory			XXX 
 
# ArduinoUCA 
Serial address		COMXXX 
 

Example of Pulse program 

This pulse sequence is an example of ELDOR experiment using the configuration above 

# Variable declaration 
tpump 	:	pump length 
tprobe 	:	probe pulse length 
Ppump	:	pump power 
Pprobe	:	probe power 
tclean	:	cleaning delay 
techo	:	echo time 
taqstart	:	start of acquisition time (can be negative) 
aqlength	:	acquisition length 
sr	:	sampling rate 
N	:	number of scans	 
 
# Phases 
ph0 = 0 0 1 1 2 2 3 3 
ph1 = 0 1 0 1 0 1 0 1 
phd = 0 0 0 0 1 1 1 1 
 
# Events 
1	cwPulse(2,tpump,Ppump) 
delay(tclean) 
squarepulse(1,tprobe,Pprobe,ph0) 
delay(techo) 
squarepulse(1,tprobe,Pprobe,ph1) 
delay(techo) 
detect(taq,aqlength,sr,phd) 
loop to 1 times ns 
