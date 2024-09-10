 # -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 14:27:41 2021

@author: Suranjita
Resources: https://github.com/mne-tools/mne-python/blob/main/mne/channels/layout.py
"""


import pyvista as pv
from pyvista import examples
import numpy as np
import matplotlib.pyplot as plt
import math
# Import the Tkinter library
from tkinter import *
from tkinter import ttk
import logging
import pandas as pd 

#------------------------------------------------List of global variables
Label_sensors=[]
picked_points=np.array([0,0,0])
def Label_selections():
    return Label_sensors
def Picked_point():
    return picked_points


#-----------------------------------------------Util Functions
def import_from_polhemus():
    return

def save_for_mne():
    return

def save_for_FT():
    return
   
def SelectElectrode():
    p = pv.Plotter()
    p.add_mesh_clip_box(mesh, color='white')
    p.show(cpos=[-1, -1, 0.2])
    clipped_mesh=p.box_clipped_meshes  #This is a list.
    return clipped_mesh
    
def FindElectrodeProperties(clipped_mesh):
    temp=str(clipped_mesh[0]).split('\n')    
    tempx=(temp[3].replace('X Bounds:\t', ''))
    tempy=(temp[4].replace('Y Bounds:\t', ''))
    tempz=(temp[5].replace('Z Bounds:\t', ''))
    
    tempx=(tempx).split(', ')
    tempy=(tempy).split(', ')
    tempz=(tempz).split(', ')
    
    tempx[0]=tempx[0].replace(' ','')
    tempy[0]=tempy[0].replace(' ','')
    tempz[0]=tempz[0].replace(' ','')
    
    x_min=float(tempx[0])
    x_max=float(tempx[1])
    y_min=float(tempy[0])
    y_max=float(tempy[1])
    z_min=float(tempz[0])
    z_max=float(tempz[1])
    return x_min, x_max, y_min, y_max, z_min, z_max

def VisualizeGeneralPlots(mesh):  #List of plots   
    curvature_plot_max=mesh.plot_curvature(curv_type='maximum',clim=[-1, 1])
    #mesh.plot(scalars=mesh.curvature('Maximum'))   ---- basically the same thing as previous line, but without using Pyvista plot_curvature
    curvature_plot_min=mesh.plot_curvature(curv_type='minimum',clim=[-1, 1])
    boundary_plot=mesh.plot_boundaries(edge_color='red')
    projected_plot=mesh.project_points_to_plane([0,0,0])
    # for saving grapoh? NOT tested:   save_graphic(filename, title='PyVista Export', raster=True, painter=True
    
def VisualizeSpecificVertices(mesh, indx):
    cpos =mesh.plot(show_edges=True, color=True)
    p = pv.Plotter()
    p.add_mesh(mesh, show_edges=True)
    p.add_mesh(mesh.points[indx], color="red", point_size=10)
    p.show(cpos=cpos)        
    
def ExtractCurvatureArray(curvature, vertices, status):
    #status will extract the curvature by low values or high values
    indx=[]
    count=0
    count1=0
    for i,j in enumerate(curvature):
        if status < 0:
            if j<0:
                indx=np.append(indx, i)
        elif status > 0:
            if j>0:
                indx=np.append(indx, i)
        else:
            if j==0:
                indx=np.append(indx, i)
    indx = indx.astype(int)   
    return indx

def FindAssociatedFaces(IndexOfAVertex):
    return [i for i, face in enumerate(faces) if IndexOfAVertex in face]   #i = index number, face= the three vertice numbers at that index

def FindAssociatedVertices(IndexOfAVertex):
    """Pass the index of the node in question.
    Returns the indices of the vertices connected with that node."""
    cids = FindAssociatedFaces(IndexOfAVertex)
    connected = np.unique(faces[cids].ravel()) 
    return np.delete(connected, np.argwhere(connected == IndexOfAVertex))

def FindFittingSphere(mesh, vertices):        
    Radius=((3*mesh.volume)/(4*3.14))**(1/3)
    x_centre=(min(vertices[:,0])+max(vertices[:,0]))/2
    y_centre=(min(vertices[:,1])+max(vertices[:,1]))/2
    z_centre=(min(vertices[:,2])+max(vertices[:,2]))/2
    sphere=pv.Sphere(radius=Radius, center=(x_centre, y_centre, z_centre), direction=(0, 0, 1), theta_resolution=30, phi_resolution=30, start_theta=0, end_theta=360, start_phi=0, end_phi=180)
    return sphere, Radius, x_centre, y_centre, z_centre

def FindProjectionOnSphere(selection, status, mesh, vertices):
    projection_array_sphere=np.asarray([0,0,0])
    if status==0:
        Radius=((3*mesh.volume)/(4*3.14))**(1/3)
    else:
        Radius=((3*mesh.volume)/(4*3.14))**(1/3) + 50
    x_centre=(min(vertices[:,0])+max(vertices[:,0]))/2
    y_centre=(min(vertices[:,1])+max(vertices[:,1]))/2
    z_centre=(min(vertices[:,2])+max(vertices[:,2]))/2
    for i in selection:
        x=i[0]-x_centre
        y=i[1]-y_centre
        z=i[2]-z_centre
        vector=np.asarray([x,y,z])
        length_vector=np.linalg.norm(vector)
        scaled_vector=(Radius/length_vector)*vector
        final_vector=np.asarray([(scaled_vector[0]+x_centre), (scaled_vector[1]+y_centre), (scaled_vector[2]+z_centre)])
        projection_array_sphere=np.column_stack((projection_array_sphere, final_vector))
    projection_array_sphere= projection_array_sphere.transpose()
    projection_array_sphere=projection_array_sphere.tolist()
    projection_array_sphere.pop(0)

    # projected array plot
    p = pv.Plotter()    
    p.add_mesh(np.asarray(selection), color="red", point_size=10)
    p.add_mesh(np.asarray(projection_array_sphere), color="blue", point_size=10)
    p.show()
    return projection_array_sphere

def FindProjectionOnSphereFromLayoutOnly(vertices):
    projection_array_sphere=np.asarray([0,0,0])
    Radius=1000
    x_centre=(min(vertices[:,0])+max(vertices[:,0]))/2
    y_centre=(min(vertices[:,1])+max(vertices[:,1]))/2
    z_centre=(min(vertices[:,2])+max(vertices[:,2]))/2
    for i in vertices:
        x=i[0]-x_centre
        y=i[1]-y_centre
        z=i[2]-z_centre
        vector=np.asarray([x,y,z])
        length_vector=np.linalg.norm(vector)
        scaled_vector=(Radius/length_vector)*vector
        final_vector=np.asarray([(scaled_vector[0]+x_centre), (scaled_vector[1]+y_centre), (scaled_vector[2]+z_centre)])
        projection_array_sphere=np.column_stack((projection_array_sphere, final_vector))
    projection_array_sphere= projection_array_sphere.transpose()
    projection_array_sphere=projection_array_sphere.tolist()
    projection_array_sphere.pop(0)

    return projection_array_sphere

def FindFiducialPlane(selection):
    p1=selection[0]
    p2=selection[1]
    p3=selection[2]
    #calculate vectors
    v1 = p3 - p1
    v2 = p2 - p1
    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp
    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = np.dot(cp, p3)

def FindGeodesic(vertices, mesh):
    p1=mesh.find_closest_point(vertices[150])
    p2=mesh.find_closest_point(vertices[3000])  
    a = mesh.geodesic(p1,p2)
    p = pv.Plotter()
    p.add_mesh(a, line_width=10, color="red", label="Geodesic Path")
    p.add_mesh(mesh, show_edges=True)
    p.add_legend()
    p.show()


#Link: https://github.com/mne-tools/mne-python/blob/9627d0965ced345fc5339caeb828e4180afacaa6/mne/transforms.py#L707
def _cart_to_sph(cart):
    """Convert Cartesian coordinates to spherical coordinates.
    Parameters
    ----------
    cart_pts : ndarray, shape (n_points, 3)
        Array containing points in Cartesian coordinates (x, y, z)
    Returns
    -------
    sph_pts : ndarray, shape (n_points, 3)
        Array containing points in spherical coordinates (rad, azimuth, polar)
    """
    assert cart.ndim == 2 and cart.shape[1] == 3
    cart = np.atleast_2d(cart)
    out = np.empty((len(cart), 3))
    out[:, 0] = np.sqrt(np.sum(cart * cart, axis=1))
    norm = np.where(out[:, 0] > 0, out[:, 0], 1)  # protect against / 0
    out[:, 1] = np.arctan2(cart[:, 1], cart[:, 0])
    out[:, 2] = np.arccos(cart[:, 2] / norm)
    out = np.nan_to_num(out)
    return out

#link: https://github.com/mne-tools/mne-python/blob/9627d0965ced345fc5339caeb828e4180afacaa6/mne/transforms.py#L1146
def _pol_to_cart(pol):
    """Transform polar coordinates to cartesian."""
    out = np.empty((len(pol), 2))
    if pol.shape[1] == 2:  # phi, theta
        out[:, 0] = pol[:, 0] * np.cos(pol[:, 1])
        out[:, 1] = pol[:, 0] * np.sin(pol[:, 1])
    else:  # radial distance, theta, phi
        d = pol[:, 0] * np.sin(pol[:, 2])
        out[:, 0] = d * np.cos(pol[:, 1])
        out[:, 1] = d * np.sin(pol[:, 1])
    return out


                
def ConvertExceltoArray(df2):
#convertes dataframe type into array
#df2 is the gtec coordinates dataframe inported in AlignGtecCoordinates
    gtec_coordinates=np.array([0,0,0])
    for i in df2:
      row=np.array([])
      row=np.append(row,i[0]*100)
      row=np.append(row,i[1]*100)
      row=np.append(row,i[2]*100)
      gtec_coordinates=np.column_stack((gtec_coordinates, row))
    gtec_coordinates=np.transpose(gtec_coordinates)
    gtec_coordinates=gtec_coordinates.tolist()
    gtec_coordinates.pop(0)
    gtec_coordinates=np.asarray(gtec_coordinates)
    return gtec_coordinates
    
def AlignGtecCoordinates(mesh, vertices): 
    Radius=((3*mesh.volume)/(4*3.14))**(1/3)
    x_centre=(min(vertices[:,0])+max(vertices[:,0]))/2
    y_centre=(min(vertices[:,1])+max(vertices[:,1]))/2
    z_centre=(min(vertices[:,2])+max(vertices[:,2]))/2
    df = pd.read_excel (r'C:\Users\g.tec\Downloads\gtec_coordinates.xls')
    t=df.to_numpy()
    df2=t[:,1:4] #extracting only the vertices
    gtec_coordinates=ConvertExceltoArray(df2)
    
def FindCommonSurface(mesh, sphere):
    select = mesh.select_enclosed_points(sphere)
    inside = select.threshold(0.5)
    outside = select.threshold(0.5, invert=True) 
    dargs = dict(show_edges=True)
    p = pv.Plotter()
    p.add_mesh(outside, color="Crimson", **dargs)
    #p.add_mesh(inside, color="green", **dargs)
    p.add_mesh(sphere, color="mintcream", opacity=0.35, **dargs)
    p.camera_position = cpos
    p.show()
    
def FindNormals(mesh):
    NormalArray=mesh.compute_normals(inplace=True)
    CellNormals=NormalArray.cell_normals()
    FaceNormals=NormalArray.face_normals()   

def ConvertSensorLocTo3DMesh(selection):
    '''
    There is an issue here: the mesh is an unstructured grid and not a surface PolyData
    Hence, although we can find geodesic by converting it to POlyData, its not giving us what we want
    '''
    cloud = pv.PolyData(selection)
    cloud.plot(point_size=15)
    surf = cloud.delaunay_3d()
    surf.plot(show_edges=True)
    p1=surf.find_closest_point(projection_array_sphere[0])
    p2=surf.find_closest_point(projection_array_sphere[1])
    
def UVMap(cloud):
    print()
    
def getMontage():
    print()

def PlotScatter3D(selection, gtec_coordinates):
    temp1=selection.transpose()
    temp2=gtec_coordinates.transpose()
    temp3=np.column_stack((temp1, temp2))
    temp3=temp3.transpose()
    x=temp3[:,0]
    y=temp3[:,1]
    z=temp3[:,2]
    temp2=temp2.transpose()
    x_gteconly=temp2[:,0]
    y_gteconly=temp2[:,1]
    z_gteconly=temp2[:,2]
    from mpl_toolkits import mplot3d
    # Creating figure
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d") 
    # Creating plot
    ax.scatter3D(x, y, z, color = "green")
    ax.scatter3D(x_gteconly,y_gteconly,z_gteconly, color='red')
    plt.title("gtec+einscan")
    # show plot
    plt.show()


'''
x=((selection[0][0]+selection[1][0])/2)
y=((selection[0][1]+selection[1][1])/2)
z=((selection[0][2]+selection[1][2])/2)

pos=np.array([x,y,z])
# Plot-1
p = pv.Plotter()
p.add_mesh(mesh, show_edges=True)
#p.add_mesh(pos, color="red", point_size=50)
p.add_mesh(np.asarray(selection), color="blue", point_size=10)
p.show(cpos=cpos)

#Plot-2
p = pv.Plotter(notebook=False)
p.add_mesh(np.asarray(selection), show_edges=True, color='w')
p.add_mesh(mesh.points, show_edges=True, color='r')
picker = Picker(p, mesh)
p.track_click_position(picker, side='right')
print (len(picker.points))
p.add_text('Right click to select!!')
p.show()
selection2=picker.points
'''

'''
x2=3
y2=4
z2=5
x2,y2,z2=P
theta2=np.arccos(abs(z2)/(x2**2+y2**2+z2**2)**.5)
phi2=np.arctan((y2/x2))
xp=theta2*np.cos((phi2))
yp=theta2*np.sin((phi2))
Plot xp,yp

'''

'''
# Select only the fiducials
p2 = pv.Plotter(notebook=False)
p2.add_mesh(mesh, show_edges=True, color='w')
picker2 = Picker(p2, mesh)
p2.track_click_position(picker2, side='right')

p2.add_text('Right click to select fiducials!!')
p2.show()
selection_fiducials=picker2.points
selection_fiducials=np.asarray(selection_fiducials) 
'''

'''
x=((selection[0][0]+selection[1][0])/2)
y=((selection[0][1]+selection[1][1])/2)
z=((selection[0][2]+selection[1][2])/2)

pos=np.array([x,y,z])
# Plot-1
p = pv.Plotter()
p.add_mesh(mesh, show_edges=True)
#p.add_mesh(pos, color="red", point_size=50)
p.add_mesh(np.asarray(selection), color="blue", point_size=10)
p.show(cpos=cpos)

#Plot-2
p = pv.Plotter(notebook=False)
p.add_mesh(np.asarray(selection), show_edges=True, color='w')
p.add_mesh(mesh.points, show_edges=True, color='r')
picker = Picker(p, mesh)
p.track_click_position(picker, side='right')
print (len(picker.points))
p.add_text('Right click to select!!')
p.show()
selection2=picker.points
'''

'''
x2=3
y2=4
z2=5
x2,y2,z2=P
theta2=np.arccos(abs(z2)/(x2**2+y2**2+z2**2)**.5)
phi2=np.arctan((y2/x2))
xp=theta2*np.cos((phi2))
yp=theta2*np.sin((phi2))
Plot xp,yp

'''
























