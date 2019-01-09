import pandas as pd
import matplotlib.pyplot as plt
import sys

followPrivateCount = int(sys.argv[1])
followCount = int(sys.argv[2])
followingPrivateCount = int(sys.argv[3])
followingCount = int(sys.argv[4])

follow1Percentage = round((followPrivateCount/followCount)*100,2)
follow2Percentage = round(((followCount - followPrivateCount )/followCount)*100,2)
following1Percentage = round((followingPrivateCount/followingCount)*100,2)
following2Percentage = round(((followingCount - followingPrivateCount )/followingCount)*100,2)

df1 = pd.DataFrame({'Followers':[followPrivateCount,followCount]},index=['Private Account : '+str(follow1Percentage),'Public Account : '+str(follow2Percentage)])
df2 = pd.DataFrame({'Following':[followingPrivateCount,followingCount]},index=['Private Account : '+str(following1Percentage),'Public Account : '+str(following2Percentage)])
plot1 = df1.plot.pie(y='Followers', figsize=(5, 5),labeldistance=0.9,radius=0.8)
plt.savefig("../Resources/FollowersPrivate.png")
plot2 = df2.plot.pie(y='Following', figsize=(5, 5),labeldistance=0.9,radius=0.8)
plt.savefig("../Resources/FollowingPrivate.png")
