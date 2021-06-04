import json
import os
import matplotlib.pyplot as plt
import numpy as np
width = 0.2
dataType = "influence"
fig, ax = plt.subplots()
with os.scandir(path="Stats/") as files:
    for file in files:
        with open(file.path) as file_io:
            data = json.loads(file_io.read())
            data_number = int(len(data) / 2)
            turns = str(file.name).split(".")[0]

            for i in range(1,len(data),2):
                label= data[i-1]
                influence_dic = dict(data[i][dataType])

                x = np.arange(len(influence_dic))
                rec = ax.bar(x + width/2*(i-data_number), list(influence_dic.values()),width, label=label)
                ax.bar_label(rec, fmt="%.2f")

            ax.set_xticks(x)
            ax.set_xticklabels(list(influence_dic.keys()))
            ax.set_title(f"Average {dataType} after {turns} turns")
            ax.set_ylabel(dataType)
            ax.legend()

            fig.tight_layout()
            plt.show()
