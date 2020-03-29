import cost_function as costf
import import_data as importd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm



# ###################################################
# #Bench Y
# ###################################################
#path_source = "./SOURCE/POST1D/TE"
# CAS = "CAS_Y"
# fig, axs = plt.subplots(3)
# for ax in axs.flat:
#     ax.set(xlabel = 'y',ylabel='cost')

# mass = []
# cost = [[],[],[]]

# for i in range(48,73):
#     path = "./"+CAS+"/CAS_SB_2D_10.0_cm_40_{}_10kg/POST1D/TE".format(i)
#     mass.append(i)
#     c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
#     for k in range (3):
#         cost[k].append(c[k])

# axs[0].plot(mass,cost[0],'b',label='f0')
# axs[0].legend(loc='lower left')

# axs[1].plot(mass,cost[1],'g',label='f1')
# axs[1].legend(loc='lower left')

# axs[2].plot(mass,cost[2],'c',label='f2')
# axs[2].legend(loc='lower left')

# plt.savefig("CAS_Y_BENCH.png")
# plt.clf()


# ###################################################
# #Bench TNT
# ###################################################
#path_source = "./SOURCE/POST1D/TE"
# CAS = "CAS_TNT"
# fig, axs = plt.subplots(3)
# for ax in axs.flat:
#     ax.set(xlabel = 'tnt mass (kg)',ylabel='cost')

# mass = []
# cost = [[],[],[]]

# for i in range(5,16):
#     path = "./"+CAS+"/CAS_SB_2D_10.0_cm_40_65_{}.0kg/POST1D/TE".format(i)
#     mass.append(i)
#     c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
#     for k in range (3):
#         cost[k].append(c[k])

# axs[0].plot(mass,cost[0],'b',label='f0')
# axs[0].legend(loc='lower left')

# axs[1].plot(mass,cost[1],'g',label='f1')
# axs[1].legend(loc='lower left')

# axs[2].plot(mass,cost[2],'c',label='f2')
# axs[2].legend(loc='lower left')

# plt.savefig("CAS_TNT_BENCH.png")
# plt.clf()

###################################################
#Bench XY
###################################################
# path_source = "./SOURCE1/POST1D/TE"
# CAS = "CAS_XY"

# fig = plt.figure(figsize=plt.figaspect(3.))

# X = [i for i in range (35,46)]
# Y = [j for j in range (55,66)]
# XG, YG = np.meshgrid(X, Y)
# cost = [[],[],[]]

# for k in range(3):
#     for i in range(len(XG)):
#         cost[k].append([0 for j in range(len(YG))])

# for i in range(len(XG)):
#     for j in range(len(YG)):
#         path = "./"+CAS+"/CAS_SB_2D_10.0_cm_{}_{}_10.0kg/POST1D/TE".format(XG[i][j],YG[i][j])
#         c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
#         for k in range (3):
#             cost[k][i][j] = c[k]

# ax0 = fig.add_subplot(3,1,1,projection='3d')
# surf = ax0.plot_surface(XG, YG, np.array(cost[0]), cmap=cm.coolwarm,linewidth=0,antialiased=False)
# ax0.set(xlabel = 'x',ylabel='y', zlabel='f0')

# ax1 = fig.add_subplot(3,1,2,projection='3d')
# surf = ax1.plot_surface(XG, YG, np.array(cost[1]), cmap=cm.coolwarm,linewidth=0,antialiased=False)
# ax1.set(xlabel = 'x',ylabel='y', zlabel='f1')

# ax2 = fig.add_subplot(3,1,3,projection='3d')
# surf = ax2.plot_surface(XG, YG, np.array(cost[2]), cmap=cm.coolwarm,linewidth=0,antialiased=False)
# ax2.set(xlabel = 'x',ylabel='y', zlabel='f2')

# plt.savefig("test.png")
#plt.clf()

###################################################
#Bench TNT
###################################################
# path_source = "./SOURCE_75_30_13/POST1D/TE"
# CAS = "CAS_TNT2"
# fig, axs = plt.subplots(3)
# for ax in axs.flat:
#     ax.set(xlabel = 'tnt mass (kg)',ylabel='cost')

# mass = []
# cost = [[],[],[]]

# for i in range(5,21):
#     path = "./"+CAS+"/CAS_SB_2D_10.0_cm_80_27_{}kg/POST1D/TE".format(i)
#     mass.append(i)
#     c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
#     for k in range (3):
#         cost[k].append(c[k])

# axs[0].plot(mass,cost[0],'b',label='f0')
# axs[0].legend(loc='lower left')

# axs[1].plot(mass,cost[1],'g',label='f1')
# axs[1].legend(loc='lower left')

# axs[2].plot(mass,cost[2],'c',label='f2')
# axs[2].legend(loc='lower left')

# plt.savefig("CAS_TNT2_BENCH.png")
# plt.clf()

# ###################################################
# #Bench YM
# ###################################################
path_source = "./SOURCE_50_30_10/POST1D/TE"
CAS = "CAS_YM"
fig, axs = plt.subplots(3)
for ax in axs.flat:
    ax.set(xlabel = 'y',ylabel='cost')

mass = []
cost = [[],[],[]]

for i in range(20,80):
    path = "./"+CAS+"/CAS_SB_2D_10.0_cm_{}.0_30_13kg/POST1D/TE".format(i)
    mass.append(i)
    c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
    for k in range (3):
        cost[k].append(c[k])
    if i>=45 and i<55:
        path = "./"+CAS+"/CAS_SB_2D_10.0_cm_{}_30_13kg/POST1D/TE".format(i+0.5)
        mass.append(i+0.5)
        c = (costf.cost_function0(path_source, path), costf.cost_function1(path_source, path), costf.cost_function2(path_source, path))
        for k in range (3):
            cost[k].append(c[k])

axs[0].plot(mass,cost[0],'b',label='f0')
axs[0].legend(loc='lower left')

axs[1].plot(mass,cost[1],'g',label='f1')
axs[1].legend(loc='lower left')

axs[2].plot(mass,cost[2],'c',label='f2')
axs[2].legend(loc='lower left')

plt.savefig("CAS_YM_BENCH.png")
plt.clf()
