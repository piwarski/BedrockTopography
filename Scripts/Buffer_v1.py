import arcpy, os
from sys import argv
arcpy.env.overwriteOutput = True

#Inputs for Testing
##geoDB = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb'
##waterWells = geoDB + os.sep + 'WW_Seclection_Champ_BR_ELEV_Calcd'
##tromino_pts = geoDB + os.sep + 'Tromino_Field__ExportFeature'
##oil_and_gas_wells = geoDB + os.sep + 'OGWells_Statew_ExportFeature'
##testBoreholes = geoDB + os.sep + 'BoreHoleLocati_ExportFeature'
##geotechnicalBorings = geoDB + os.sep + 'Borings_ExportFeatures'

#Inputs for Script in Toolbox
waterWells = arcpy.GetParameterAsText(0) #Water wells
tromino_pts = arcpy.GetParameterAsText(1) #Tromino points
oil_and_gas_wells = arcpy.GetParameterAsText(2) #Oil and gas wells
testBoreholes = arcpy.GetParameterAsText(3) #Test boreholes
geotechnicalBorings = arcpy.GetParameterAsText(4) #Geotechnical borings

#Buffer Output Location
#Name_and_Location_of_Buffer_output = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\bufferOutput'
Name_and_Location_of_Buffer_output = arcpy.GetParameterAsText(5)

#Distance Parameter Input
#Distance_value_or_field_="0.5 Miles"
Distance_value_or_field_ = arcpy.GetParameterAsText(6)

#Potential other point to be added in the future
Other_Points = arcpy.GetParameterAsText(7)

#print('Merging layers')
arcpy.AddMessage('Merging layers')

# Process: Merge (Merge) (management)
Select_All_Bedrock_Control_Point_Feature_Classes = list(filter(None, [waterWells,tromino_pts,oil_and_gas_wells,testBoreholes,geotechnicalBorings,Other_Points]))
arcpy.AddMessage(Select_All_Bedrock_Control_Point_Feature_Classes)

arcpy.management.Merge(inputs=Select_All_Bedrock_Control_Point_Feature_Classes, output=r"memory\tempBuffers", field_mappings="", add_source="ADD_SOURCE_INFO")

#print('Merging layers complete. Starting pairwise buffer now.')
arcpy.AddMessage('Merging layers complete. Starting pairwise buffer now.')

# Process: Pairwise Buffer (Pairwise Buffer) (analysis)
arcpy.analysis.PairwiseBuffer(in_features=r"memory\tempBuffers", out_feature_class=Name_and_Location_of_Buffer_output, buffer_distance_or_field=Distance_value_or_field_, dissolve_option="NONE", dissolve_field=[], method="PLANAR", max_deviation="0 DecimalDegrees")

#print('Pairwise buffer complete. Deleting temporary merged data.')
arcpy.management.Delete(r"memory\tempBuffers")
arcpy.AddMessage('Pairwise buffer complete. Deleted temporary merged data.')

