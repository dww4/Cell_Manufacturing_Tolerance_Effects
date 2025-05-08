# Anode Thickness Tolerance Effects on Fast Charging

############################### Description ###############################

Uses a DFN cell model with lithium plating to understand the effects of anode thickness manufacturing tolerances on fast-charging performance. Runs the model with N samples (N=10 by default) at each tolerance level and outputs i) average capacity lost to plating ii) average amount of charge in 10 minutes and iii) % of cells with lithium plating. 

############################### Dependencies ###############################

0. PyBamm Installation (pip install pybamm)

1. Manufacturing-Tolerance.py

############################### Executing Program ###############################

1. Run Simulation:
	a. Run: python Manufacturing-Tolerance.py

	b. Should Output:
		i. Plot of voltage profile for all cells at each tolerance level
		ii. Performance csv file that contains outputs i-iii at each tolerance level

############################### Help ###############################

*Ignore flags that are outputted - the model is working*

Ask DJ (dejuante1503@gmail.com) 
