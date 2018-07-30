import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import *

f = open("../raw-data/footballData.txt","r").read().split("PLAYERSPLIT")

categories = ["player","season","height", "weight","position"]

processing = []

for player in f[1:-1]:
    stats = player.split("\n")
    stats.pop(0)
    stats.pop(-1)
    processing.append(stats)

df = pd.DataFrame(processing)
df.columns = categories

x = list(df.height.unique())
y = list(df.weight.unique())

heights = ["5-1","5-2","5-3","5-4","5-5","5-6","5-7","5-8","5-9","5-10","5-11","6-0","6-1","6-2","6-3","6-4","6-5","6-6","6-7","6-8","6-9","6-10"]
heights = heights[::-1]
weights = sorted(y, reverse=True)

def listicle(max, min, divisor):
    final_list = []
    length = int((max - min) / divisor)
    starting_point = min
    for item in list(range(length)):
        final_list.append(list(range(starting_point, (starting_point + divisor))))
        starting_point += divisor
    return final_list

new_weights = listicle(380,100,10)
new_weights = sorted(new_weights,reverse=False)
seasons = []

y_labels = list(range(100,380,20))
y_labels = sorted(y_labels)

y_labels_final = []

for label in y_labels:
    new_label = str(label) + "lbs"
    y_labels_final.append(new_label)

x_labels = heights[1::2]

x_labels_final = []

for label in x_labels:
    new_label = str(label).split("-")
    new_label = str(new_label[0]) + "'" + str(new_label[1]) + '"'
    x_labels_final.append(new_label)

for season in df["season"]:
    if season not in seasons:
        seasons.append(season)

seasons = sorted(seasons)
n = 0
for season in seasons:
    season_data = df.loc[df["season"]==season]
    all_heights = []
    all_weights = []
    for entry in season_data["height"]:
        all_heights.append(entry)
    for entry in season_data["weight"]:
        all_weights.append(entry)
    array = np.zeros((22,28))
    for entry in list(range(len(all_heights))):
        current_height = all_heights[entry]
        current_weight = int(str(all_weights[entry]).replace("lb",""))
        y_index = heights.index(current_height)
        for bin in new_weights:
            if current_weight in bin:
                x_index = new_weights.index(bin)
        array[y_index,x_index] += 1
    maximum_value = np.max(array)
    sum_values = np.sum(array)
    array = np.true_divide(array,sum_values)
    array = np.multiply(array,100)
    fig, ax = plt.subplots(figsize=(15.5,12.25))
    im = ax.imshow(array,cmap="Blues",vmin=0,vmax=3.25)
    plt.yticks(np.arange(1,len(heights),2),fontsize=11)
    plt.xticks(np.arange(0, len(new_weights), 2),fontsize=11)
    cbar = plt.colorbar(im, fraction=0.026, pad = 0.04, ticks=[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3])
    cbar.ax.set_yticklabels(["  0%","0.25%"," 0.5%","0.75%","  1%","1.25%"," 1.5%","1.75%","  2%","2.25%"," 2.5%","2.75%","  3%"])
    ax.set_yticklabels(x_labels_final)
    ax.set_xticklabels(y_labels_final)
    fig.tight_layout()
    plt.savefig("graph_{0}.jpg".format(n))
    plt.close('all')
    n+=1

base_text = "graph_"

y = []

for x in list(range(0,96)):
    y.append(base_text + str(x) + ".jpg")

clip = ImageSequenceClip(y, fps=6)

clip.write_videofile('footballHeatmap.mp4')
clip.write_gif('footballHeatmap.gif')
