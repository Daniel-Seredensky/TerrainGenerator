import numpy  as np
import trimesh 
import math
import random

def createRectangle(topRight, bottomLeft, startHeight, height,step = .5):
    """
    Create coordinates of the surface of a rectangular prism.

    Parameters:
    topRight (tuple): Coordinates of the top-right corner (x, y).
    bottomLeft (tuple): Coordinates of the bottom-left corner (x, y).
    height (float): Height of the rectangular prism (z-axis).

    Returns:
    list: Coordinates of the surface points of the rectangular prism.
    """
    x_min, y_min = min(bottomLeft[0], topRight[0]), min(bottomLeft[1], topRight[1])
    x_max, y_max = max(bottomLeft[0], topRight[0]), max(bottomLeft[1], topRight[1])
    rc = []

    # Create points for the bottom face
    bottom_face = []
    for x in np.arange(x_min, x_max + step, step):
        for y in np.arange(y_min, y_max + step, step):
            bottom_face.append([x, y, startHeight])

    # Create points for the top face
    top_face = []
    for x in np.arange(x_min, x_max + step, step):
        for y in np.arange(y_min, y_max + step, step):
            top_face.append([x, y, startHeight+height])

    # Create points for the sides
    side1,side2,side3,side4 = [],[],[],[]
    for x in np.arange(x_min, x_max + step, step):
        for z in np.arange(startHeight, startHeight + height + step, step):
            side1.append([x, y_min, z])  # Side 1 (y = y_min)
            side2.append([x, y_max, z])  # Side 2 (y = y_max)
    for y in np.arange(y_min, y_max + step, step):
        for z in np.arange(startHeight, startHeight +  height + step, step):
            side3.append([x_min, y, z])  # Side 3 (x = x_min)
            side4.append([x_max, y, z])  # Side 4 (x = x_max)
    
    # Combine all points
    rc.append(bottom_face)
    rc.append(top_face)
    rc.append(side1)
    rc.append(side2)
    rc.append(side3)
    rc.append(side4)

    return rc


def generate_spheroid(x_center, y_center, z_center, x_coeff, y_coeff, z_coeff, num_points=100):
    phi = np.linspace(0, np.pi, num_points)
    theta = np.linspace(0, 2 * np.pi, num_points)
    phi, theta = np.meshgrid(phi, theta)

    x = x_center + x_coeff * np.sin(phi) * np.cos(theta)
    y = y_center + y_coeff * np.sin(phi) * np.sin(theta)
    z = z_center + z_coeff * np.cos(phi)

    return np.column_stack((x.flatten(), y.flatten(), z.flatten()))


class  otherShapes:
  class Boat:
    def __init__(self,x=0,y=0,z=0):
      self.x = x
      self.y = y
      self.z = z
      self.scene = trimesh.Scene()
      self.createBoat()
      self.scene.export('boat.glb',file_type = 'glb')
      self.scene.show()


    def createBoat(self):
      x,y,z = self.x, self.y, self.z
      boat_cords = []
      
      #create bottom
      bottom = []
      for x in np.arange(0,5.5,.5):
        for y in np.arange(0,3.5,.5):
          bottom.append([x,y,0])
      boat_cords.append(bottom)

      #create sides
      side1,side2,side3,side4 = [],[],[],[]

      for x in np.arange(0,5.5,.5):
        for z in np.arange(0,2,.5):
          side1.append([x,0,z])
      boat_cords.append(side1)
      for x in np.arange(0,5.5,.5):
        for z in np.arange(0,2,.5):
          side2.append([x,3,z])
      boat_cords.append(side2)
      for y in np.arange(0,3.5,.5):
        for z in np.arange(0,2,.5):
          side3.append([0,y,z])
      boat_cords.append(side3)
      for y in np.arange(0,3.5,.5):
        for z in np.arange(0,2,.5):
          side4.append([5,y,z])
      boat_cords.append(side4)
      
      for obj in boat_cords:
        points,heights = [],[]
        for x,y,z in obj:
          points.append([x,y])
          heights.append(z)
        newObj = np.column_stack((points,heights))
        newObj = trimesh.Trimesh(vertices = newObj)
        newObj = newObj.convex_hull
        self.scene.add_geometry(newObj)

      #createPrisms
      prisms = []
      prism1 = createRectangle((5.5,-.5),(-.5,.5),1.5,.5)
      prisms.append(prism1)
      prism2 = createRectangle((5.5,2.5),(-.5,3.5),1.5,.5)
      prisms.append(prism2)
      prism3 = createRectangle((.5,3.5),(-.5,-.5),1.5,.5)
      prisms.append(prism3)
      prism4 = createRectangle((5.5,3.5),(4.5,-.5),1.5,.5)
      prisms.append(prism4)


      for prism in prisms:
        for obj in prism:
          points,heights = [],[]
          for x,y,z in obj:
            points.append([x,y])
            heights.append(z)
          newObj = np.column_stack((points,heights))
          newObj = trimesh.Trimesh(vertices = newObj)
          newObj = newObj.convex_hull
          self.scene.add_geometry(newObj)



  class Board:
    def __init__(self):
      self.scene = trimesh.Scene()
      self.createBoard()
      self.scene.export('board.glb',file_type = 'glb')
      self.scene.show()



    def createBoard(self):
       stand1 = createRectangle((0,0),(.5,.5),0,1)
       stand2 = createRectangle((2,0),(2.5,.5),0,1)
       board = createRectangle((-.5,-.5),(3,.5),1,3)
       board_cords = []
       board_cords.append(stand1)
       board_cords.append(stand2)
       board_cords.append(board)
       for thing in board_cords:
          for obj in thing:
            points,heights = [],[]
            for x,y,z in obj:
              points.append([x,y])
              heights.append(z)
            newObj = np.column_stack((points,heights))
            newObj = trimesh.Trimesh(vertices = newObj)
            newObj = newObj.convex_hull
            self.scene.add_geometry(newObj)



  class newTrees:
    def __init__(self):
      for i in range(15):
        self.treeCords = []
        self.scene = trimesh.Scene()
        self.createBark()
        self.createLeaves()
        self.createTree()
        self.scene.export(f'trees/tree{i}.glb',file_type = 'glb')


    def createBark(self):
      bark_data = []
      #bark generation
      for theta in np.arange(0,6.32,.5):
        for z in np.arange(0,4.1,.4):
          r = .8
          if z <=.4:
             r-=z
          else:
             r-=.4
          x = r*math.cos(theta)
          y = r*math.sin(theta)
          bark_data.append([x,y,z])
      self.treeCords.append(bark_data)
    

    def createLeaves(self):
        xCoef = 2 + np.random.rand() * .5
        yCoef = 2 + np.random.rand() * .5
        zCoef = 1.5 + np.random.rand() * .25
        coefs = [xCoef,yCoef,zCoef]
        #leaves generation
        # Create the main spheroid
        mainSpheroid = generate_spheroid(*[0,0,6.5], *coefs, 25)
        # Select random points on the main spheroid to generate smaller spheroids
        index = 0 
        for pos in mainSpheroid:
          if not index%5==0:
             index+=1
             continue
          index+=1
          # Create smaller spheroid centered at leaf_center
          leaf_x_coeff = np.random.rand() * .4 + 1
          leaf_y_coeff = np.random.rand() * .4 + 1
          leaf_z_coeff = np.random.rand() * .4 + 1
          subSpheroid = generate_spheroid(*pos, leaf_x_coeff, leaf_y_coeff, leaf_z_coeff, num_points=10)
          self.treeCords.append(subSpheroid)  

    def createTree(self):
      for obj in self.treeCords:
        points,heights = [],[]
        for x,y,z in obj:
          points.append([x,y])
          heights.append(z)
        newObj = np.column_stack((points,heights))
        newObj = trimesh.Trimesh(vertices = newObj)
        newObj = newObj.convex_hull
        self.scene.add_geometry(newObj)
  


#boat = BoatAndBoard.Boat()
#board = BoatAndBoard.Board()
#tree = otherShapes.newTrees()

