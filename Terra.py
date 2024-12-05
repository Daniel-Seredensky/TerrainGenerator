import numpy as np
import plotly.graph_objects as go
import os
import math
import random
from scipy.spatial import Delaunay
import trimesh
import pymeshlab
import pyvista as pv

def isInSphere(x,y):
    if ((25-x)**2 + (25-y)**2) <= 25**2:
      return True
    return False

class Terra:

  def __init__(self):
    self.light = [10,10,40]
    self.x_data = None
    self.y_data = None
    self.All_data = {}

    self.mainLineSpace = self.my_linspace(0,50,.5)
    
    self.generate_terrain()

    self.create_moon()

    self.generate_trees()

    self.generateBottom()

    self.objectColors = {"rock":[75,75,75,255],
                         "ground":[0,100,0,255],
                         "water":[137, 207, 240,255],
                         "moon":[130,130,130,255],
                         "bark":[139,69,19,255],
                         "leaf":[0,128,0,255],
                         }
    self.objectTextures = {"ground":[0,100,0,255],
                         "water":[137, 207, 240,255],
                         "moon":[130,130,130,200],
                         "bark":[139,69,19,255],
                         "leaf":[0,128,0,255],
                         "rock":[75,75,75,255]
                         }

  def my_linspace(self,start,stop,step):
    data = []
    cur = start
    if start<stop:
      while cur<=stop:
        data.append(round(cur,2))
        cur+=step
    else:
      while cur>=stop:
        data.append(round(cur,2))
        cur-=step
    return data
  
  def getSeperateData(self):
    ground_data = [list(key) for key,val in self.terrain_data.items() if val == "ground"]
    water_data = [list(key) for key,val in self.terrain_data.items() if val == "water" ]
    moon_data = [list(key) for key,val in self.terrain_data.items() if val == "moon" ]
    rock_data = [list(key) for key,val in self.terrain_data.items() if val == "rock" ]
    bark_data = []
    leaf_data = []
    bark_data = []
    leaf_data = []
    for tree in self.Trees:
      bark_data.append([list(key) for key,val in tree.items() if val == "bark" ])
      leaf_data.append([list(key) for key,val in tree.items() if val == "leaf" ])
    return rock_data,ground_data,water_data,moon_data,bark_data,leaf_data
  
  def generate_terrain(self):
    size = 35
    x_WaveLengths = np.random.rand(size)*(1/3.5)
    x_coef = np.random.rand(size)-.2
    y_coef = np.random.rand(size)-.2
    y_WaveLengths = np.random.rand(size)*(1/3.5)
    orderx = np.random.rand(size)
    ordery = np.random.rand(size)
    self.x_data = self.mainLineSpace
    self.y_data = self.mainLineSpace
    self.terrain_data = {}

    def x_func(x):
      sum = 0
      index = -1
      for waveL,coef,order in zip(x_WaveLengths,x_coef,orderx):
        if order>.5:
          sum += coef*math.sin(waveL*x)
        else:
          sum+= coef*math.cos(waveL*x)
        index*=-1
      return sum 

    def y_func(y):
      sum = 0
      index = -1
      for waveL,coef,order in zip(y_WaveLengths,y_coef,ordery):
        if order>.5:
          sum += coef*math.cos(waveL*y)
        else:
          sum += coef*math.sin(waveL*y)
        index*=-1
      return sum

    for x in self.x_data:
      for y in self.y_data:
        z = x_func(x)+y_func(y)
        if isInSphere(x,y):
          if z > 2:
            self.terrain_data[(x,y,z)] = "ground"
            self.All_data[(x,y)] = [[z,"ground"]]
          else:
            self.terrain_data[(x,y,0)] = "ground"
            self.terrain_data[(x,y,2)] = "water"
            self.All_data[(x,y)] = [[2,"water"]]

  def create_tree(self,origin_x,origin_y,origin_z):
    tree_data = {}
    coef = np.random.rand() + .4
    r = .25
    #bark generation
    for theta in self.my_linspace(0,6.28,.4):
        for z in self.my_linspace(0,3,.2):
            x = r*math.cos(theta) + origin_x
            y = r*math.sin(theta) + origin_y
            tree_data[tuple((x,y,z+origin_z))] = "bark"
            try:
                self.All_data[(x,y)].append([origin_z+z,"bark"])
            except:
                self.All_data[(x,y)] = [[origin_z+z,"bark"]]
    for z in self.my_linspace(2,4,.2):
        for theta in self.my_linspace(0,6.28,.4):
            x = coef*(z-4)*math.cos(theta) + origin_x
            y = coef*(z-4)*math.sin(theta) + origin_y
            tree_data[tuple((x,y,z+origin_z))] = "leaf"
            try:
                self.All_data[(x,y)].append([z+origin_z,"leaf"])
            except:
                self.All_data[(x,y)] = [[z+origin_z,"leaf"]]
    return tree_data

  def generate_trees(self):
    self.Trees = []
    data = [key for key,val in self.terrain_data.items() if val == "ground" and key[2]!=0]
    for i in range(15):
      x,y,z = random.choice(data)
      self.Trees.append(self.create_tree(x,y,z))

  def create_moon(self):
    r = 1.5
    theta_vals = phi_vals = self.my_linspace(0,6.28,.4)
    for theta in theta_vals:
      for phi in phi_vals:
        x = r*math.sin(theta)*math.cos(phi) + self.light[0]

        y = r*math.sin(theta)*math.sin(phi) + self.light[1]

        z = r*math.cos(theta) + self.light[2]
        
        self.terrain_data[(x,y,z)] = "moon"
        try:
          self.All_data[(x,y)].append([z,"moon"])
        except:
          self.All_data[(x,y)] = [[z,"moon"]]

  def generateBottom(self,radius=25):
    # Generate random spherical coordinates
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "ground" or val == "water"])
    x_data,y_data = terrain[:,0],terrain[:,1]

    for x,y in zip(x_data,y_data):
      value_under_sqrt = (25**2) - (x-25)**2 - (y-25)**2
      if value_under_sqrt >= 0:
          z = (value_under_sqrt**(1/2)) * (-1/2)
          minValue = math.floor(min([arr[0] for arr in self.All_data[(x,y)] if arr[1] == "ground" or arr[1] == "water" ]))
          while (z < minValue):
            self.All_data[(x,y)].append([z,"rock"])
            self.terrain_data[(x,y,z)] = "rock"
            z+=.75

  def triMeshTerrain (self):
    """
    Triangulate the terrain based on the heightmap in terra.All_data.
    This function uses Delaunay triangulation on the (x, y) coordinates of the terrain.
    
    Parameters:
    - terra: A Terra object containing the terrain data in terra.All_data.
    
    Returns:
    - vertices: A list of vertices (x, y, z) of the terrain.
    - triangles: A list of indices defining the triangles in the mesh.
    """
    scene = trimesh.Scene()

    # Extract (x, y) coordinates and corresponding heights (z)
    for datum,Type in zip(self.getSeperateData(),self.objectColors.keys()):
      if Type != "bark" and Type != "leaf":
        if Type != "rock":
          points = []
          heights = []
          for x,y,z in datum:
            points.append([x, y])
            heights.append(z)
          points = np.array(points)
          heights = np.array(heights)
            # Perform Delaunay triangulation on the (x, y) coordinates
          tri = Delaunay(points)
          
          # Extract the vertices and triangles for the mesh
          vertices = np.column_stack((points, heights))  # Combine x, y, z into a single array of vertices
          triangles = tri.simplices  # Indices of the vertices forming triangles
          color = self.objectColors[Type]
          mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
        else:
          point_cloud = pv.PolyData(datum)

          # Step 3: Use the Delaunay 3D filter with surface extraction to preserve concavity
          # This tries to triangulate the point cloud and then extract a surface that retains concave features
          delaunay_mesh = point_cloud.delaunay_3d(alpha=0.5)  # Alpha can help manage concave details

          # Step 4: Extract surface from the volume
          surface = delaunay_mesh.extract_surface()

          # Step 5: Convert to vertices and faces for Trimesh
          vertices = surface.points
          faces_flat = surface.faces
          faces = []

          i = 0
          while i < len(faces_flat):
              num_points = faces_flat[i]
              if num_points == 3:
                  faces.append(faces_flat[i + 1:i + 4])
              i += num_points + 1

          faces = np.array(faces)
          mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        # Export to STL format
        mesh.export('temp.obj', file_type='obj')

        # Load using STL format
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh('temp.obj')
        ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetfacenum=5000)
        ms.save_current_mesh('temp_decimated.obj')

        # Load back the decimated mesh
        decimated_mesh = trimesh.load_mesh('temp_decimated.obj')
        # Assign vertex colors to the decimated mesh
        color = np.array(self.objectColors[Type])  # Ensure color is an array, e.g., [R, G, B, A]
        vertex_colors = np.tile(color, (len(decimated_mesh.vertices), 1))
        decimated_mesh.visual.vertex_colors = vertex_colors

        # Add the decimated and colored mesh to the scene
        scene.add_geometry(decimated_mesh)
        os.remove('temp.obj')
        os.remove('temp_decimated.obj')

      else:
        for obj in datum:
          points = []
          heights = []
          for x,y,z in obj:
            points.append([x, y])
            heights.append(z)

          points = np.array(points)
          heights = np.array(heights)

          # Extract the vertices and triangles for the mesh
          vertices = np.column_stack((points, heights))  # Combine x, y, z into a single array of vertices
          mesh = trimesh.Trimesh(vertices=vertices, vertex_colors=[self.objectColors[Type]] * len(vertices))
          mesh = mesh.convex_hull
          color = self.objectColors[Type]
          vertex_colors = np.tile(color, (len(mesh.vertices), 1))
          mesh.visual.vertex_colors = vertex_colors
          scene.add_geometry(mesh)


    scene.export('terrain.glb',file_type = 'glb')
    scene.show()

  def plot(self):
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "ground" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,mode = "markers")])
    fig.update_traces(marker=dict(color="darkgreen",opacity=1,size = 1))
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "water" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="blue",opacity=1,size = 1)))
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "moon" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="gray",opacity=1,size = 1)))
    terrain = np.array([list(key) for key,val in self.terrain_data.items() if val == "rock" ])
    x,y,z = terrain[:,0],terrain[:,1],terrain[:,2]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="darkgray",opacity=1,size = 1)))
    for tree in self.Trees:
      bark_data = np.array([list(key) for key,val in tree.items() if val == "bark" ])
      x,y,z = bark_data[:,0],bark_data[:,1],bark_data[:,2]
      fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="brown",opacity=1,size = 1)))
      leaf_data = np.array([list(key) for key,val in tree.items() if val == "leaf" ])
      x,y,z = leaf_data[:,0],leaf_data[:,1],leaf_data[:,2]
      fig.add_trace(go.Scatter3d(x=x, y=y, z=z,marker=dict(color="green",opacity=1,size = 1)))
    fig.show()

