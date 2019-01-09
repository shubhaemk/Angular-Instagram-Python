import matplotlib.pyplot as plt
import sys


names_array = sys.argv[1].split(',')
likes_array = [int(x) for x in sys.argv[2].split(',')]
plt.bar(names_array,likes_array, tick_label = names_array,width = 0.5)
plt.xlabel('Users')
plt.ylabel('Likes')
plt.title('Top 10 Likers')
plt.xticks(list(float(a) for a in range(0,10)),rotation=40)
plt.gcf().subplots_adjust(bottom=0.35)
plt.savefig("../Resources/Graph.png")
