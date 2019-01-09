import pandas as pd
import matplotlib.pyplot as plt
import sys

followUsers = sys.argv[1].split(',')
followingUsers = sys.argv[2].split(',')
count = int(sys.argv[3])

followingLength = len(followingUsers)
followLength = len(followUsers)

follow1Percentage = round((count/followLength)*100,2)
follow2Percentage = round(((followLength - count )/followLength)*100,2)
following1Percentage = round((count/followingLength)*100,2)
following2Percentage = round(((followingLength - count )/followingLength)*100,2)

df1 = pd.DataFrame({'Followers':[count,followLength]},index=['People you follow back : '+str(follow1Percentage),'People whom you do not follow back : '+str(follow2Percentage)])
df2 = pd.DataFrame({'Following':[count,followingLength]},index=['People who follow you back : '+str(following1Percentage),'People who do not follow back : '+str(following2Percentage)])
plot1 = df1.plot.pie(y='Followers', figsize=(5, 5),labeldistance=0.9,radius=0.8)
plt.savefig("../Resources/Followers.png")
plot2 = df2.plot.pie(y='Following', figsize=(5, 5),labeldistance=0.9,radius=0.8)
plt.savefig("../Resources/Following.png")
