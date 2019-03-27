##Author: Jake Olbrich
##Date: November 5th, 2018
##Version: 2.7.8
##Description: Compute the Lee-Sallee Metric from fire perimeter shapefiles

import arcpy, os
from arcpy.sa import *

path="C:/Users/jolbrich/Desktop/Fire/FARSITE_Famine_Redeye/FARSITE_LCP"  #Specify what folder you want
os.chdir(path) #Sets path to the directory you'll be using

#check extensions
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        # Raise a custom exception
        #
        raise LicenseError
except LicenseError:
        print "spatial Analyst license is unavailable"  
except:
        print arcpy.GetMessages(2)
finally:
    # Check in the 3D Analyst extension
    #
    arcpy.CheckInExtension("Spatial")
    
arcpy.env.overwriteOutput = True



#Actual Fire perimeters
Redeye = os.path.join(path, "Redeye_Perim_w_Lakes.shp")
Famine = os.path.join(path, "Famine_Perim_w_Lakes.shp")
spat_ref= arcpy.Describe(Redeye).spatialReference

#file
new_file = open(os.path.join(path, "LeeSallee_info.txt"),"w")
new_file.write("Fire_name, Actual_Fire, SIM_FIRE, Int_Fire, Union_Fire \n")

for root, directories, files in os.walk(path):
        for d in directories:
                print(d)
                if d.startswith("Sim_"):
                        arcpy.env.workspace = os.path.join(path,d)
                        print(d)
                        for root, directories, files in os.walk(d):
                                        for f in files:
                                                if f.endswith('.shp'):
                                                        if f.startswith('RE_'):
                                                                p = os.path.join(os.path.join(path,root),f)
                                                                new_file.write(f)
                                                                new_file.write(", 7248915.47482, ")
                                                                arcpy.AddField_management(p, "Uniform", "Integer")
                                                                arcpy.RepairGeometry_management(p)
                                                                print(f)
                                                                dis = arcpy.Dissolve_management(p, str('dis_' + f), 'Uniform')
                                                                arcpy.AddField_management(dis, "Shape_area", "DOUBLE") 
                                                                exp = "!SHAPE.AREA@SQUAREMETERS!"
                                                                arcpy.CalculateField_management(dis, "Shape_area", exp, "PYTHON_9.3")
                                                                arcpy.RepairGeometry_management(dis)
                                                                for row in arcpy.SearchCursor(dis):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                clip = arcpy.Clip_analysis(dis, Redeye, str('clip_' + f))
                                                                arcpy.CalculateField_management(clip, "Shape_area", exp, "PYTHON_9.3")
                                                                for row in arcpy.SearchCursor(clip):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                mrg = arcpy.Merge_management([dis, Redeye], str('mrg_' + f))
                                                                dis2 = arcpy.Dissolve_management(mrg, str('dis2_' + f), 'Uniform')
                                                                arcpy.AddField_management(dis2, "Shape_area", "DOUBLE")
                                                                exp2 = "!SHAPE.AREA@SQUAREMETERS!"
                                                                arcpy.CalculateField_management(dis2, "Shape_area", exp2, "PYTHON_9.3")
                                                                for row in arcpy.SearchCursor(dis2):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                new_file.write("\n")
                                                        elif f.startswith('FAM_'):
                                                                p = os.path.join(os.path.join(path,root),f)
                                                                new_file.write(f)
                                                                new_file.write(", 16360346.051562, ")
                                                                arcpy.AddField_management(p, "Uniform", "Integer")
                                                                arcpy.RepairGeometry_management(p)
                                                                dis = arcpy.Dissolve_management(p, str('dis_' + f), 'Uniform')
                                                                print(f)
                                                                arcpy.AddField_management(dis, "Shape_area", "DOUBLE") 
                                                                exp = "!SHAPE.AREA@SQUAREMETERS!"
                                                                arcpy.CalculateField_management(dis, "Shape_area", exp, "PYTHON_9.3")
                                                                arcpy.RepairGeometry_management(dis)
                                                                for row in arcpy.SearchCursor(dis):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                clip = arcpy.Clip_analysis(dis, Famine, str('clip_' + f))
                                                                arcpy.CalculateField_management(clip, "Shape_area", exp, "PYTHON_9.3")
                                                                for row in arcpy.SearchCursor(clip):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                mrg = arcpy.Merge_management([dis, Famine], str('mrg_' + f))
                                                                dis2 = arcpy.Dissolve_management(mrg, str('dis2_' + f), 'Uniform')
                                                                arcpy.AddField_management(dis2, "Shape_area", "DOUBLE")
                                                                exp2 = "!SHAPE.AREA@SQUAREMETERS!"
                                                                arcpy.CalculateField_management(dis2, "Shape_area", exp2, "PYTHON_9.3")
                                                                for row in arcpy.SearchCursor(dis2):
                                                                        new_file.write(str(row.getValue("Shape_area")))
                                                                        new_file.write(", ")
                                                                new_file.write("\n")


new_file.close()

