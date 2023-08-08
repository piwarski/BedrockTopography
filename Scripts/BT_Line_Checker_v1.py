
import arcpy, os
from sys import argv
arcpy.env.overwriteOutput = True

#Inputs for Testing
##Choose_Geodatabase_to_Store_Topology="C:\\Users\\10214536\\OneDrive - State of Ohio\\Documents\\Bedrock Topography\\New_BT_Models_WIP\\ModelOutput.gdb"
##Choose_BT_Lines=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\W_Champ_BT_Line_Corrected"
##Choose_Boundary_for_BT_Lines=r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\WesternChampaign_poly'
##Output_Feature_Class_Name_for_BT_Polygons=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Output_BT_Polygons_to_be_used_after_corrections"
##Output_Feature_Class_Name_for_BT_Points_within_Polygons=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Output_BT_Polygons_points_to_be_filled_after_corrections"
##Name_the_Output_Topology_for_Initial_BT = "Output_Topology_for_Just_BT_Lines"
##Name_the_Output_Topology_for_bounded_BT = "Output_Topology_for_BT_Lines_with_Bounds"

#Inputs for Script in Toolbox
Choose_Geodatabase_to_Store_Topology = arcpy.GetParameterAsText(0) #Outputs for feature classes will go here
Choose_BT_Lines = arcpy.GetParameterAsText(1) #Feature class of elevation lines
Choose_Boundary_for_BT_Lines = arcpy.GetParameterAsText(2) #Bounding polygon for model limit
Output_Feature_Class_Name_for_BT_Polygons = arcpy.GetParameterAsText(3) #Bounding polygon is used to clip the BT lines, then it is turned into a line feature class and merged with the BT lines into a separate feature class
Output_Feature_Class_Name_for_BT_Points_within_Polygons = arcpy.GetParameterAsText(4) #Points to have Min and Max Fields added to. 
Name_the_Output_Topology_for_Initial_BT = arcpy.GetParameterAsText(5) #A dataset is created for topology to make sure BT lines do not overlap or intersect. The BT lines are copied there. This dataset is eventually deleted
Name_the_Output_Topology_for_bounded_BT = arcpy.GetParameterAsText(6) #Another dataset is created for topology to make sure new lines to not dangle or self-intersect. This is done with this dataset to make sure that an extra duplicate boundary was not hidden in the dataset, and to make sure lines were properly snapped to eachother/the bounding area.
contourInterval = arcpy.GetParameterAsText(7) #Interval used in cases of estimating contours when they're missing (e.g., top of hills, bottoms of pits, edges of study area)

# Process: Create Feature Dataset (Create Feature Dataset) (management)
TopoChecks1 = arcpy.management.CreateFeatureDataset(out_dataset_path=Choose_Geodatabase_to_Store_Topology, out_name="TopoCheck1_Fix_Initial_BT_Lines", spatial_reference="PROJCS[\"NAD_1983_StatePlane_Ohio_South_FIPS_3402_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",1968500.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-82.5],PARAMETER[\"Standard_Parallel_1\",38.73333333333333],PARAMETER[\"Standard_Parallel_2\",40.03333333333333],PARAMETER[\"Latitude_Of_Origin\",38.0],UNIT[\"Foot_US\",0.3048006096012192]];-119670700 -95612900 3048.00609601219;-100000 10000;-100000 10000;3.28083333333333E-03;0.001;0.001;IsHighPrecision")[0]
print('Create Feature Dataset')
arcpy.AddMessage('Create Feature Dataset')

# Process: Create Topology for BT Lines (Create Topology) (management)
if TopoChecks1:
    Topology_Name_and_Location = arcpy.management.CreateTopology(in_dataset=TopoChecks1, out_name=Name_the_Output_Topology_for_Initial_BT, in_cluster_tolerance=0)
print('Create Topology for BT Lines')
arcpy.AddMessage('Create Topology for BT Lines')

# Process: Copy BT Lines for Topology Dataset (Feature Class To Feature Class) (conversion)
if TopoChecks1:
    BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected = arcpy.conversion.FeatureClassToFeatureClass(in_features=Choose_BT_Lines, out_path=TopoChecks1, out_name="BTLines_Used_For_Bounded_Model_After_Errors_Corrected")
print('Copy BT Lines for Topology Dataset')
arcpy.AddMessage('Copy BT Lines for Topology Dataset')

# Process: Add Feature Class To Topology (Add Feature Class To Topology) (management)
if BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected and TopoChecks1:
    BT_Topology_Rules = arcpy.management.AddFeatureClassToTopology(in_topology=Topology_Name_and_Location, in_featureclass=BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected, xy_rank=1, z_rank=1)
print('Add Feature Class To Topology')
arcpy.AddMessage('Add Feature Class To Topology')

# Process: Add Must Not Overlap Rule (Add Rule To Topology) (management)
if BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected and BT_Topology_Rules and TopoChecks1:
    BT_Line_Overlap = arcpy.management.AddRuleToTopology(in_topology=Topology_Name_and_Location, rule_type="Must Not Overlap (Line)", in_featureclass=BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected, subtype="", in_featureclass2="", subtype2="")
print('Add Must Not Overlap Rule')
arcpy.AddMessage('Add Must Not Overlap Rule')

# Process: Add Must Not Intersect Rule (Add Rule To Topology) (management)
if BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected and BT_Topology_Rules and TopoChecks1:
    BT_Line_Intersect = arcpy.management.AddRuleToTopology(in_topology=Topology_Name_and_Location, rule_type="Must Not Intersect (Line)", in_featureclass=BTLines_Used_For_Next_Bounding_Model_After_Errors_Corrected, subtype="", in_featureclass2="", subtype2="")
print('Add Must Not Intersect Rule')
arcpy.AddMessage('Add Must Not Intersect Rule')

# Process: Create Feature Dataset (2) (Create Feature Dataset) (management)
Topocheck2_fix_BT_within_bounds = arcpy.management.CreateFeatureDataset(out_dataset_path=Choose_Geodatabase_to_Store_Topology, out_name="Topocheck2_fix_BT_within_bounds", spatial_reference="PROJCS[\"NAD_1983_StatePlane_Ohio_South_FIPS_3402_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",1968500.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-82.5],PARAMETER[\"Standard_Parallel_1\",38.73333333333333],PARAMETER[\"Standard_Parallel_2\",40.03333333333333],PARAMETER[\"Latitude_Of_Origin\",38.0],UNIT[\"Foot_US\",0.3048006096012192]];-119670700 -95612900 3048.00609601219;-100000 10000;-100000 10000;3.28083333333333E-03;0.001;0.001;IsHighPrecision")
print('Create Feature Dataset')
arcpy.AddMessage('Create Feature Dataset')

# Process: Create Topology for BT Lines and Boundarys (Create Topology) (management)
Topology_Name_and_Location_2_ = arcpy.management.CreateTopology(in_dataset=Topocheck2_fix_BT_within_bounds, out_name=Name_the_Output_Topology_for_bounded_BT, in_cluster_tolerance=0)
print('Create Topology for BT Lines and Boundarys')
arcpy.AddMessage('Create Topology for BT Lines and Boundarys')

# Process: Feature To Line (Feature To Line) (management)
Boundary_Lines = Choose_Geodatabase_to_Store_Topology + os.sep + "Boundary_Polygon_to_line"
arcpy.management.FeatureToLine(in_features=[Choose_Boundary_for_BT_Lines], out_feature_class=Boundary_Lines, cluster_tolerance="", attributes="ATTRIBUTES")
print('Feature To Line')
arcpy.AddMessage('Feature To Line')

# Process: Clips Lines to Boundary (Clip) (analysis)
Draft_BT_Lines_Clipped = Choose_Geodatabase_to_Store_Topology + os.sep + "BT_Lines_Clipped"
arcpy.analysis.Clip(in_features=Choose_BT_Lines, clip_features=Choose_Boundary_for_BT_Lines, out_feature_class=Draft_BT_Lines_Clipped, cluster_tolerance="")
print('Clips Lines to Boundary')
arcpy.AddMessage('Clips Lines to Boundary')

# Process: Merge (Merge) (management)
BoundaryAndLinesMerge = Choose_Geodatabase_to_Store_Topology + os.sep + "Output_Draft_BTLines_for_eventual_polygon_and_topology"
arcpy.management.Merge(inputs=[Boundary_Lines, Draft_BT_Lines_Clipped], output=BoundaryAndLinesMerge)
print('Merge')
arcpy.AddMessage('Merge')

# Process: Copy BT Lines for Topology Dataset (2) (Feature Class To Feature Class) (conversion)
Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_ = arcpy.conversion.FeatureClassToFeatureClass(in_features=BoundaryAndLinesMerge, out_path=Topocheck2_fix_BT_within_bounds, out_name="BTLines_with_bounding_lines_to_be_used_after_corrections")
print('Copy BT Lines for Topology Dataset')
arcpy.AddMessage('Copy BT Lines for Topology Dataset')

# Process: Add Feature Class To Topology (2) (Add Feature Class To Topology) (management)
if Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_:
    BT_Topology_Rules_2_ = arcpy.management.AddFeatureClassToTopology(in_topology=Topology_Name_and_Location_2_, in_featureclass=Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_, xy_rank=1, z_rank=1)
print('Add Feature Class To Topology')
arcpy.AddMessage('Add Feature Class To Topology')

# Process: Add Must Not Intersect Self Rule (Add Rule To Topology) (management)
if BT_Topology_Rules_2_ and Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_:
    BT_Line_Self_Intersect = arcpy.management.AddRuleToTopology(in_topology=Topology_Name_and_Location_2_, rule_type="Must Not Self-Intersect (Line)", in_featureclass=Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_, subtype="", in_featureclass2="", subtype2="")
print('Add Must Not Intersect Self Rule')
arcpy.AddMessage('Add Must Not Intersect Self Rule')

# Process: Add Must Not Dangle Rule (Add Rule To Topology) (management)
if BT_Topology_Rules_2_ and Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_:
    BT_Line_Dangle = arcpy.management.AddRuleToTopology(in_topology=Topology_Name_and_Location_2_, rule_type="Must Not Have Dangles (Line)", in_featureclass=Name_for_BT_Lines_merged_with_Bounding_Lines_that_could_be_used_for_Polygons_if_desired_After_Corrections_, subtype="", in_featureclass2="", subtype2="")
print('Add Must Not Dangle Rule')
arcpy.AddMessage('Add Must Not Dangle Rule')

# Process: Validate Topology (Validate Topology) (management)
if TopoChecks1:
    Choose_Topology_Name = arcpy.management.ValidateTopology(in_topology=Topology_Name_and_Location, visible_extent="Full_Extent")
print('Validate Topology')
arcpy.AddMessage('Validate Topology')

# Process: Export Topology Errors (Export Topology Errors) (management)
if TopoChecks1:
    Topology_Errors_Points, Topology_Errors_Lines, Topology_Errors_Polygons = arcpy.management.ExportTopologyErrors(in_topology=Choose_Topology_Name, out_path=Choose_Geodatabase_to_Store_Topology, out_basename=Name_the_Output_Topology_for_Initial_BT)
print('Export Topology Errors')
arcpy.AddMessage('Export Topology Errors')

# Process: Validate Topology (2) (Validate Topology) (management)
Choose_Topology_Name_2_ = arcpy.management.ValidateTopology(in_topology=Topology_Name_and_Location_2_, visible_extent="Full_Extent")
print('Validate Topology')
arcpy.AddMessage('Validate Topology')

# Process: Export Topology Errors (2) (Export Topology Errors) (management)
Topology_Errors_Points_2_, Topology_Errors_Lines_2_, Topology_Errors_Polygons_2_ = arcpy.management.ExportTopologyErrors(in_topology=Choose_Topology_Name_2_, out_path=Choose_Geodatabase_to_Store_Topology, out_basename=Name_the_Output_Topology_for_bounded_BT)
print('Export Topology Errors')
arcpy.AddMessage('Export Topology Errors')

# Process: Merge Topology Lines (Merge) (management)
Output_Topology_for_Line_Issues = Choose_Geodatabase_to_Store_Topology + os.sep + "Output_Topology_for_Line_Issues"
if TopoChecks1:    
    arcpy.management.Merge(inputs=[Topology_Errors_Lines, Topology_Errors_Lines_2_], output=Output_Topology_for_Line_Issues)
print('Merge Topology Lines')
arcpy.AddMessage('Merge Topology Lines')

# Process: Merge (3) (Merge) (management)
Output_Topology_for_Point_Issues = Choose_Geodatabase_to_Store_Topology + os.sep + "Output_Topology_for_Point_Issues"
if TopoChecks1:    
    arcpy.management.Merge(inputs=[Topology_Errors_Points, Topology_Errors_Points_2_], output=Output_Topology_for_Point_Issues)
print('Merge again')
arcpy.AddMessage('Merge again')

# Process: Feature To Polygon: Create Polys from BT lines and Bounds (Feature To Polygon) (management)
arcpy.management.FeatureToPolygon(in_features=[BoundaryAndLinesMerge], out_feature_class=Output_Feature_Class_Name_for_BT_Polygons, cluster_tolerance="", attributes="NO_ATTRIBUTES", label_features="")
print('Feature To Polygon')
arcpy.AddMessage('Feature To Output_Feature_Class_Name_for_BT_Polygons')

# Process: Feature To Point (Feature To Point) (management)
arcpy.management.FeatureToPoint(in_features=Output_Feature_Class_Name_for_BT_Polygons, out_feature_class=Output_Feature_Class_Name_for_BT_Points_within_Polygons, point_location="INSIDE")
print('Feature To Point')
arcpy.AddMessage('Feature To Point')

# Process: Add Min and Max Fields (Add Fields (multiple)) (management)
BT_Polygons_points_to_be_filled_after_corrections = arcpy.management.AddFields(in_table=Output_Feature_Class_Name_for_BT_Points_within_Polygons, field_description=[["MIN", "SHORT", "", "", "", ""], ["MAX", "SHORT", "", "", "", ""]], template=[])[0]
print('Add Min and Max Fields')
arcpy.AddMessage('Add Min and Max Fields')

# Convert contours and area boundary to polygons
contourPolygons = r"memory\contourPolygons"
arcpy.management.FeatureToPolygon([Choose_Boundary_for_BT_Lines,Choose_BT_Lines],contourPolygons)
print('Converted contours to Polygons')
arcpy.AddMessage('Converted contours to Polygons')

#Iterate through each of the points, select contour polygon by location, select contours that have boundaries that touch,
#get elevation values from each and put them in a list, and finally use the list for calculating fields for the individual point - then repeat!
arcpy.AddMessage('Calculating Min/Max Values')
with arcpy.da.SearchCursor(Output_Feature_Class_Name_for_BT_Points_within_Polygons,'SHAPE@') as points:
    for pt in points:
        selConPoly = arcpy.management.SelectLayerByLocation(contourPolygons,'INTERSECT',pt)
        selContours = arcpy.management.SelectLayerByLocation(Choose_BT_Lines,'SHARE_A_LINE_SEGMENT_WITH',selConPoly)
        selPt = arcpy.management.SelectLayerByLocation(Output_Feature_Class_Name_for_BT_Points_within_Polygons,'INTERSECT',selConPoly)        
        conRows = arcpy.da.SearchCursor(selContours,'ELEVATION')
        conElevs = []
        for row in conRows:
            if row[0] is not None:
                conElevs.append(row[0])
        if len(conElevs) > 1: #Two bounding contours
            arcpy.management.CalculateFields(selPt,"PYTHON3",[
                ['MIN',min(conElevs)],
                ['MAX',max(conElevs)]])
        elif len(conElevs) == 1: #One bounding contour. Either a pit or top of hill
            #print(conElevs)
            #If a point is located on in either a pit or on top of a hill, need to select the next contour out to figure out which case exists.            
            nearContours = Choose_Geodatabase_to_Store_Topology + os.sep + 'nearContours'
            arcpy.analysis.GenerateNearTable(selPt,Choose_BT_Lines,nearContours,'','NO_LOCATION','NO_ANGLE','ALL',2)
            objCounter = 1
            with arcpy.da.SearchCursor(nearContours,'*') as nearRows:
                for row in nearRows:
                    if objCounter == 2:
                        #print(row) #need near when OBJECTID = 2. This is the second closes contour
                        objId = row[2]
                        closeCont = arcpy.analysis.Select(Choose_BT_Lines,r'memory/secClosCon','"OBJECTID" = ' + str(objId))
                        with arcpy.da.SearchCursor(closeCont,'ELEVATION') as closeRows:
                            for closeRow in closeRows:                                
                                closeElev = closeRow[0]
                                #print(closeElev)
                    objCounter +=1
            if closeElev not in conElevs: #This is the next contour elevation out. If it's smaller, we're on a hill. Larger means we're in a pit.                        
                if closeElev > conElevs[0]: #pit
                    conElevs.append(conElevs[0] - int(contourInterval))
                    #print('pit')
                elif closeElev < conElevs[0]: #hill
                    conElevs.append(conElevs[0] + int(contourInterval))
                    #print('hill')
            #print(conElevs)
            arcpy.management.CalculateFields(selPt,"PYTHON3",[
                ['MIN',min(conElevs)],
                ['MAX',max(conElevs)]])
            
# Process: Delete (Delete) (management)
if TopoChecks1:
    Delete_Succeeded = arcpy.management.Delete(in_data=[Topology_Errors_Polygons, Topology_Errors_Polygons_2_, Topocheck2_fix_BT_within_bounds, Topology_Errors_Lines_2_, Topology_Errors_Points_2_, Topology_Errors_Lines, Topology_Errors_Points, TopoChecks1, nearContours, contourPolygons], data_type="")[0]
print('Delete')
arcpy.AddMessage('Delete')

print('Assigned Min and Max values to BT Points')
arcpy.AddMessage('Assigned Min and Max values to BT Points')

