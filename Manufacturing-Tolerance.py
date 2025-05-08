#Import Libraries
import pybamm
import matplotlib.pyplot as plt
import numpy as np
import csv

#Define Input Parameters
mu = float(input("Avearge electrode thickness [µm]? (ex: 85.2) \n"))*1e-6
c_rate = float(input("C rate? (ex: 0.5, 1, ...) \n"))
ntol = int(input("Number of tolerances to investigate? (ex:3) \n"))
tol = []
for n in range(0,ntol):
    tol.append(float(input(f"Tolerance {n+1} [%]? (ex: 1) \n"))*0.01)
tol = np.array(tol)

N = 50   #Number of samples

#Define DFN model with reversible lithium plating
options = {"lithium plating":"reversible"}
model = pybamm.lithium_ion.DFN(options)

#Define CC-CV Experiment
experiment = pybamm.Experiment([
    "Discharge at 1C until 2.6V",
    "Hold at 2.6V for 10 minutes",
    f"Charge at {c_rate}C for 10 minutes",
])

#Define Parameter Set
pv = pybamm.ParameterValues("OKane2022")

#Define Arrays
cap_plated = []
cap_plated_avg = []
cap_plated_STD = []
cap_sigma = []
capSTD_sigma = []
Q10_Ah_l = []
Q10_Ah_avg = []
Q10_Ah_STD = []
perc_plated = []
for t in tol:
    sigma = t*mu   #Thickness tolerance
    l_anode = np.random.normal(mu, sigma, N)
    count = 0
    for l in l_anode:

        #Define Anode Thickness
        pv['Negative electrode thickness [m]'] = l

        #Run Simulation
        sim = pybamm.Simulation(model,experiment=experiment,parameter_values=pv)
        sim.solve(solver=pybamm.CasadiSolver(mode="safe", dt_max=0.2))

        #Store Time, Voltage, and Loss of Capacity
        time_sim = sim.solution["Time [min]"].data
        Voltage = sim.solution["Voltage [V]"].data
        capacity_plating = sim.solution['Loss of capacity to negative lithium plating [A.h]'].data
        cap_plated.append(np.max(capacity_plating))

        #Count Number of Plated Cells
        min_anode_potential = np.min(sim.solution["Negative electrode lithium plating reaction overpotential [V]"].data)
        if min_anode_potential<0: count+=1

        #Calculate Amount of Charge in 10 minutes
        I = sim.solution["Current [A]"].data          #store current data
        t0 = time_sim[np.where(I < 0)[0][0]]     #index first charging point
        charging_mask = (I < 0) & (time_sim <= t0 + 600) #define 10 minute charging range
        Q10 = np.trapz(-I[charging_mask], time_sim[charging_mask])   #coulomb count for 10 minute charging range
        Q10_Ah = Q10 / 3600     #convert to Ah
        Q10_Ah_l.append(Q10_Ah)  #store

        #Plot Voltage Profile
        plt.title(f"Tolerance Level: {t*100}%")
        plt.plot(time_sim,Voltage)
        plt.xlabel("Time [min]")
        plt.ylabel("Voltage [V]")


    plt.show()
    cap_plated_avg.append(np.mean(cap_plated))
    cap_plated_STD.append(np.std(cap_plated))
    Q10_Ah_avg.append(np.mean(Q10_Ah_l))
    Q10_Ah_STD.append(np.std(Q10_Ah_l))
    perc_plated.append(count/N)

#Output Results
base = f"Performance_C_rate{c_rate}"
for t in tol:
    base+=f"_tol{t}%"
with open(base+".csv",mode='w') as file:
        file_writer = csv.writer(file,delimiter=',')
        y = ["Tolerance Level (%)", "Average Capacity Lost to Plating (Ah)", "Average Amount of Charge in 10 Minutes (Ah)","Percent of Cells Plated (%)"]
        file_writer.writerow(y)
        for i in range(0,len(tol)):
            x = [tol[i]*100,cap_plated_avg[i],Q10_Ah_avg[i],perc_plated[i]*100]
            file_writer.writerow(x)
