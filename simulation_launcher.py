import sys
import os
import subprocess
import time


def launch_simulation(XC = 40, YC = 65, M_TNT = 10, PAS = 1):
    folder_name = "CAS_SB_2D_" + str(round(float(PAS)*1e2,3)) + "_cm_" + str(round(float(XC),3)) + "_" + str(round(float(YC),3)) + "_" + str(round(float(M_TNT),3)) + "kg"
    print('launching the simulation with parameters :', XC, YC, M_TNT, PAS)  
    if os.path.exists(os.getcwd() + '/' + folder_name) :
        print('simulation already done, skipping it')
        return folder_name, False
    else:
        subprocess.Popen(['/usr/bin/python', './SouffleBati2D.py', str(XC), str(YC), str(M_TNT), str(PAS), "-host=sklb"], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True )
        # subprocess.Popen(['python', './fake_sim.py', folder_name], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True )
    return folder_name, True

def batch_launch_simulation(sim_list):
    folder_names = []
    print(f'launching {len(sim_list)} simulations')
    wait = 0
    for sim in sim_list:
        folder_name, need_to_wait = launch_simulation(**sim)
        folder_names.append(folder_name)
        wait = max(need_to_wait, wait)
    if wait:
        time.sleep(3)
    print('waiting for the simulations to finish')
    while not(all(['T_OK' in os.listdir(f'./{folder}') for folder in folder_names])):
        time.sleep(.2)
    print('alldone')
    return [f'{os.getcwd()}/{folder}' for folder in folder_names]

if __name__ == '__main__':
    print(batch_launch_simulation([{'XC' : i, 'YC': 65, 'M_TNT' : 8, 'PAS': 0.1} for i in range(30,40)]))
