Christopher Audette

##Command line argument##

From Command Line, enter values as follows
python Audette_Assignment5.py [text file] [epsilon value]

##Epsilon values tested##

Up until an epsilon value of 93 (with epsilon values as low as .00001), the same path is always returned. (17 loop minimum on value iteration)
At epsilon = ~93, the path returned changes from a path containing 17 nodes to one containing 29. (15 loop minimum on value iteration)
At epsilon ~115, the path changes again. (14 loop minimum)
Again the path changes at epsilon ~128. (10 loop minimum)
At epsilon ~194 the path changes again. (6 loop minimum)
At epsilon value ~296, the path ceases to function (likely because g is greater too often than the utility of neighbor n).  (5 loops and fewer fail to find path)

