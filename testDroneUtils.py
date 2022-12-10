import Drone
import DroneUtils
import NetworkUtils
import Coords

drone1 = Drone.Drone("alpha",8008,"1",Coords.Coords(0, 1, 2))
drone2 = Drone.Drone("beta",8008,"2",Coords.Coords(1000, 1, 2))
drone3 = Drone.Drone("gamma",8008,"3",Coords.Coords(2000, 1, 2))
    

network = [drone1, drone2, drone3]

for drone in network:
    x, y = DroneUtils.localSimGetNeighbors(network, drone)
    print("From "+drone.name+':', end='')
    for X in x:
        print(X.name, end=' ')
    print("")