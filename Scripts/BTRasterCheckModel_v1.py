
import arcpy, os
from sys import argv
from arcpy.ddd import *
from arcpy.sa import *
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Inputs for Testing
##WW_Seclection_Champ_BR_ELEV_Calcd = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\WW_Seclection_Champ_BR_ELEV_Calcd'
##Tromino_Field__ExportFeature = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\Tromino_Field__ExportFeature'
##OGWells_Statew_ExportFeature = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\OGWells_Statew_ExportFeature'
##Borings_ExportFeatures = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\Borings_ExportFeatures'
##BoreHoleLocati_ExportFeature = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\BoreHoleLocati_ExportFeature'
##Choose_BT_Polygon_Output_from_Line_Checker_Model= r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Output_BT_Polygons_to_be_used_after_corrections'
##Name_Output_BT_Contour_Surface_Raster= r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\TopoToR_W_Ch1'
##Output_cell_size="50"
##Select_corrected_BT_Contour_Lines_with_ELEVATION_field=r"'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\W_Champ_BT_Line_Corrected' ELEVATION Contour"##special
##Name_for_Output_of_BT_Points_Tested_by_model= r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\BT_Points_Test'

#Inputs for Script in Toolbox
WW_Seclection_Champ_BR_ELEV_Calcd = arcpy.GetParameterAsText(0)
Tromino_Field__ExportFeature = arcpy.GetParameterAsText(1)
OGWells_Statew_ExportFeature = arcpy.GetParameterAsText(2)
Borings_ExportFeatures = arcpy.GetParameterAsText(3)
BoreHoleLocati_ExportFeature = arcpy.GetParameterAsText(4)
Choose_BT_Polygon_Output_from_Line_Checker_Model = arcpy.GetParameterAsText(5)
Name_Output_BT_Contour_Surface_Raster = arcpy.GetParameterAsText(6)
Output_cell_size = arcpy.GetParameterAsText(7)
Select_corrected_BT_Contour_Lines_with_ELEVATION_field = r"'" + arcpy.GetParameterAsText(8)+ "' ELEVATION Contour"
arcpy.AddMessage(Select_corrected_BT_Contour_Lines_with_ELEVATION_field)
Name_for_Output_of_BT_Points_Tested_by_model = arcpy.GetParameterAsText(9)

#Create List of Inputs for Merge
Select_All_Bedrock_Control_Point_Feature_Classes_with_BR_ELEV = list(filter(None, [WW_Seclection_Champ_BR_ELEV_Calcd,Tromino_Field__ExportFeature,OGWells_Statew_ExportFeature,Borings_ExportFeatures,BoreHoleLocati_ExportFeature]))

# Process: Merge (Merge) (management)
Name_for_Merged_Bedrock_Control_Point_Dataset = r'memory\BT_Pts_Merge'
arcpy.management.Merge(inputs=Select_All_Bedrock_Control_Point_Feature_Classes_with_BR_ELEV, output=Name_for_Merged_Bedrock_Control_Point_Dataset)
print('Merge completed')
arcpy.AddMessage('Merge completed')

#Copy polygon output from line checker model to memory, otherwise it disappears?!?!?
BT_Polygon_copy = Choose_BT_Polygon_Output_from_Line_Checker_Model + '_rastChkCopy'
arcpy.management.Copy(Choose_BT_Polygon_Output_from_Line_Checker_Model,BT_Polygon_copy)

# Process: Select Layer By Location (Select Layer By Location) (management)
temp_selection_Merged_BT_Points_Within_Boundary = arcpy.management.SelectLayerByLocation(in_layer=[Name_for_Merged_Bedrock_Control_Point_Dataset], overlap_type="WITHIN", select_features=BT_Polygon_copy, search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
print('Select Layer By Location completed')
arcpy.AddMessage('Select Layer By Location completed')

# Process: Topo to Raster (Topo to Raster) (3d)
Output_stream_polyline_features = ""
Output_remaining_sink_point_features = ""
Output_diagnostic_file = ""
Output_parameter_file = ""
Output_residual_point_features = ""
Output_stream_and_cliff_error_point_features = ""
Output_contour_error_point_features = ""
arcpy.ddd.TopoToRaster(Select_corrected_BT_Contour_Lines_with_ELEVATION_field, Name_Output_BT_Contour_Surface_Raster, Output_cell_size, BT_Polygon_copy, 20, None, None, "ENFORCE", "CONTOUR", 20, None, 1, 0, 2.5, 100, Output_stream_polyline_features, Output_remaining_sink_point_features, Output_diagnostic_file, Output_parameter_file, None, Output_residual_point_features, Output_stream_and_cliff_error_point_features, Output_contour_error_point_features)
print('Topo to Raster completed')
arcpy.AddMessage('Topo to Raster completed')

# Process: Export Features (Export Features) (conversion)
Merged_BT_Point_Export = r'memory\Merged_BT_Point_Export'
arcpy.conversion.ExportFeatures(in_features=temp_selection_Merged_BT_Points_Within_Boundary, out_features=Merged_BT_Point_Export)
print('Export Features completed')
arcpy.AddMessage('Export Features completed')

# Process: Extract Values to Points (Extract Values to Points) (sa)
Merged_Extracted_BT_Points = r'memory\Merged_Extracted_BT_Points'
arcpy.sa.ExtractValuesToPoints(Merged_BT_Point_Export, Name_Output_BT_Contour_Surface_Raster, Merged_Extracted_BT_Points) #This will fail the second time it's run
print('Extract Values to Points completed')
arcpy.AddMessage('Extract Values to Points completed')

# Process: Calculate Field (Calculate Field) (management)
Merged_Extracted_BT_Points_Calc = arcpy.management.CalculateField(in_table=Merged_Extracted_BT_Points, field="RASTER_Cell_Test_10ft_tolerance", expression="in_tolerance(!BR_ELEV!, !RASTERVALU!, 10)", expression_type="PYTHON3", code_block=
"""def in_tolerance(elev, raster_value, tolerance):
        if (elev >= (raster_value - tolerance) and elev <= (raster_value + tolerance)):
            return 'Pass'
        elif (elev < (raster_value - tolerance) or elev > (raster_value + tolerance)):
            return 'Fail'""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Calculate Field')
arcpy.AddMessage('Calculate Field')

# Process: Calculate Field to get matching ID field (Calculate Field) (management)
Output_BT_Polys = arcpy.management.CalculateField(in_table=BT_Polygon_copy, field="OBJECTID_1", expression="!OBJECTID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Calculate Field to get matching ID field done')
arcpy.AddMessage('Calculate Field to get matching ID field done')

# Process: Zonal Statistics as Table (Zonal Statistics as Table) (sa)
ZonalStatistic_Max_Min = r'memory\ZonalStatistic_Max_Min'
arcpy.sa.ZonalStatisticsAsTable(in_zone_data=BT_Polygon_copy, zone_field="OBJECTID", in_value_raster=Name_Output_BT_Contour_Surface_Raster, out_table=ZonalStatistic_Max_Min, ignore_nodata="DATA", statistics_type="MIN_MAX", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
#.save(Zonal_Statistics_as_Table)
print('Zonal Statistics as Table done')
arcpy.AddMessage('Zonal Statistics as Table done')

# Process: Join Field (Join Field) (management)
Output_BT_Polys_2_ = arcpy.management.JoinField(in_data=Output_BT_Polys, in_field="OBJECTID", join_table=ZonalStatistic_Max_Min, join_field="OBJECTID_1", fields=["MIN", "MAX"], fm_option="NOT_USE_FM", field_mapping="")[0]
print('Join Field complete')
arcpy.AddMessage('Join Field complete')

# Process: Export Features (2) (Export Features) (conversion)
Output_BT_Poly_Joined_Stats_export = r'memory\Output_BT_Poly_Joined_Stats_export'
arcpy.conversion.ExportFeatures(in_features=Output_BT_Polys_2_, out_features=Output_BT_Poly_Joined_Stats_export, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,Output_BT_Polys,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,Output_BT_Polys,Shape_Area,-1,-1;OBJECTID_1 \"OBJECTID_1\" true true false 512 Text 0 0,First,#,Output_BT_Polys,OBJECTID_1,0,512;MIN \"MIN\" true true false 8 Double 0 0,First,#,Output_BT_Polys,MIN,-1,-1;MAX \"MAX\" true true false 8 Double 0 0,First,#,Output_BT_Polys,MAX,-1,-1", sort_field=[])
print('Features exported')
arcpy.AddMessage('Features exported')

# Process: Spatial Join (Spatial Join) (analysis)
arcpy.analysis.SpatialJoin(target_features=Merged_Extracted_BT_Points_Calc, join_features=Output_BT_Poly_Joined_Stats_export, out_feature_class=Name_for_Output_of_BT_Points_Tested_by_model)
print('Spatial join done')
arcpy.AddMessage('Spatial join done')

# Process: Calculate Field (2) (Calculate Field) (management)
Name_for_Output_of_BT_Points_Tested_by_model = arcpy.management.CalculateField(in_table=Name_for_Output_of_BT_Points_Tested_by_model, field="RASTER_Contour_Range_test", expression="classify(!BR_ELEV!, !MIN!, !MAX!)", expression_type="PYTHON3", code_block=
"""def classify(elev, min, max):
        if (elev >= min and elev <= max):
            return 'Pass'
        elif (elev < min or elev > max):
            return 'Fail'""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Calculate field for RASTER_Contour_Range_test')
arcpy.AddMessage('Calculate field for RASTER_Contour_Range_test')

# Process: Delete (Delete) (management)
Delete_Succeeded = arcpy.management.Delete(in_data=[ZonalStatistic_Max_Min, Name_for_Merged_Bedrock_Control_Point_Dataset, Merged_BT_Point_Export, Output_BT_Polys_2_, BT_Polygon_copy], data_type="")[0]
print('Deleted Zonal Statistics')
arcpy.AddMessage('Deleted Zonal Statistics')
