import numpy
from scipy.cluster.vq import vq
import scipy
import csv



reader = csv.reader(open('MatchOut.csv', 'rb'),delimiter=',')

lista=[]
csv_list=[]
for index,row in enumerate(reader):
    if index>0:
        row2=[int(row[3]), int(row[4])]
        lista.append(row2)
    csv_list.append(row)

features  = numpy.array(lista)

#print features


whitened =features
codes = 100
#centroid, label =scipy.cluster.vq.kmeans2(whitened,codes)
centroid=[]
centx=[-590, -570, -550, -530, -510, -490, -470, -450, -430, -410, -390, -370, -350, -330, -310, -290, -270, -250, -230, -210, -190, -170, -150, -130, -110, -90, -70, -50, -30, -10, 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550, 570, 590]
centy=[-390, -370, -350, -330, -310, -290, -270, -250, -230, -210, -190, -170, -150, -130, -110, -90, -70, -50, -30, -10, 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390]
for i in centx:
    for j in centy:
        centroid.append([i,j])


# computing K-Means with K = 2 (2 clusters)
#centroid,_ = kmeans(features,codes)
# assign each sample to a cluster
label,_ =vq(features,numpy.array(centroid))

archivo = csv.writer(open("MatchOut2cent.csv", "wb"),delimiter=',')
for i in range(len(csv_list)):
    row1=csv_list[i]
    if i>0:
        lab=int(label[i-1])
        cent=centroid[lab]
        row2=[str(lab), str(int(cent[0])),str(int(cent[1]))]
    else:
        row2=['Label','CentX','CentY']

    #print row1, row2
    row3=row1+row2
    archivo.writerow(row3)

