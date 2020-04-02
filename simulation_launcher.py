import sys
import os
import subprocess
import time


def launch_simulation(XC = 40, YC = 65, M_TNT = 10, PAS = 1):
    folder_name = "CAS_SB_2D_" + str(float(PAS)*1e2) + "_cm_" + str(float(XC)) + "_" + str(float(YC)) + "_" + str(float(M_TNT)) + "kg"
    if os.path.exists(os.getcwd() + '/' + folder_name):
        print('simulation already done, skipping it')
        return folder_name
    else:
        subprocess.Popen(['python', './SouffleBati2D.py', str(XC), str(YC), str(M_TNT), str(PAS)], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True )
        # subprocess.Popen(['python', './fake_sim.py', folder_name], stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True )
    return folder_name

def batch_launch_simulation(sim_list):
    folder_names = []
    for sim in sim_list:
        folder_names.append(launch_simulation(**sim))
    time.sleep(1)
    while not(all(['T_OK' in os.listdir(f'./{folder}') for folder in folder_names])):
        time.sleep(.2)
    print('alldone')
    return [f'{os.getcwd()}/{folder}' for folder in folder_names]

if __name__ == '__main__':
    print(batch_launch_simulation([{'XC' : i, 'YC': 65, 'M_TNT' : 8, 'PAS': 0.1} for i in range(30,40)]))