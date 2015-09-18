The second heuristic I used was the straight line function; I figured it had to be better than the Manhatten distance because it was admissable, as opposed to the manhatten distance.Theoretically, there would be scenarios where the Manhatten distance heuristic would overestimate the total movement necessary to reach the goal (such as pure diagonal movement).I thought the straight line heuristic would always produce a better solution than the manhatten distance, however I failed to take into account the fact that I wasn't calculating actual distances, but movement from square to square.Thus, my somewhat dumber version of the function sometimes returns a better result, and sometimes returns a worse result, than the manhatten heuristic.

#Equations#

##Manhatten Distance##
Adds number of horizontal moves + number of vertical moves (as if only moving in cardinal directions) and multiplies by 10.  Will obviously underestimate in cases of mountain movement.

##Dumbed Down Straight Line Heuristic##
Square Root(horizontal moves to goal squared + vertical moves to goal squared)*10 = Approximation of Straight Line

World1 Manhatten Path: 14 Nodes visited, Path cost 170, [('0', '7'), ('1', '6'), ('1', '5'), ('1', '4'), ('1', '3'), ('2', '2'), ('3', '2'), ('4', '1'), ('5', '0'), ('5', '1'), ('6', '0'), ('7', '0'), ('8', '0'), ('9', '0')]
World1 Straight Line Path: 14 Nodes visited, Path cost 158, [('0', '7'), ('1', '6'), ('1', '7'), ('2', '7'), ('3', '6'), ('4', '5'), ('3', '5'), ('4', '4'), ('5', '3'), ('6', '3'), ('7', '2'), ('7', '1'), ('8', '0'), ('9', '0')]

World2 Manhatten Path: 15 Nodes visited, Path cost 156, [('0', '7'), ('1', '6'), ('0', '6'), ('0', '5'), ('1', '4'), ('2', '4'), ('3', '4'), ('4', '3'), ('4', '2'), ('4', '1'), ('5', '0'), ('6', '0'), ('7', '0'), ('8', '0'), ('9', '0')]
World2 Straight Line Path: 12 Nodes visited, Path cost 158, [('0', '7'), ('1', '6'), ('1', '7'), ('2', '7'), ('3', '6'), ('3', '5'), ('4', '4'), ('5', '3'), ('6', '3'), ('7', '2'), ('8', '1'), ('9', '0')]

Command Line Argument Should be written as:
python Audette_Assignment3.py [text file] [1 or leave blank for manhatten distance, any other number for straight line]
