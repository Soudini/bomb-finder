import matplotlib.pyplot as plt
import numpy as np

with open("data_temp_threshold", "r") as f:
    file = f.read()
    list_data = file.split(":")
    del list_data[-1]

print(list_data)
T = [10, 100, 1000]
X = [float(data) for data in list_data]
Y1 = [np.exp(-float(data)/T[0]) for data in list_data]
Y2 = [np.exp(-float(data)/T[1]) for data in list_data]
Y3 = [np.exp(-float(data)/T[2]) for data in list_data]

plt.close()
plt.scatter(X,Y1,label="T="+str(T[0]))
plt.scatter(X,Y2,label="T="+str(T[1]))
plt.scatter(X,Y3,label="T="+str(T[2]))
plt.title('Seuil de température entre points du voisinage')
plt.xlabel("E'-E")
plt.ylabel("exp(-(E'-E)/T)")
plt.legend()
plt.savefig("plot_temp_threshold.png")