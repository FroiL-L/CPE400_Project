import Drone
import NetworkUtils

def testGenDijskraVector():
    drone1 = Drone.Drone(1,8008,69)
    drone2 = Drone.Drone(2,8008,69)
    drone3 = Drone.Drone(3,8008,69)
    
    drone1.neighbors = [drone2,drone3]
    drone2.neighbors = [drone1,drone3]
    drone3.neighbors = [drone1,drone2]
    
    drone1.distances = [2,4]
    drone2.distances = [2,3]
    drone3.distances = [4,3]
    
    drones = [drone1, drone2, drone3]
    
    distances = NetworkUtils.genDijskraVector(drones, 1)
    print(distances)
    
testGenDijskraVector()