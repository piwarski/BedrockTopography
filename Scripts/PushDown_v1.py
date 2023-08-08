
import arcpy
from sys import argv
from arcpy.ddd import *
from arcpy.sa import *
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Inputs for Testing
#waterWells = r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\BT_Model_Base_Data.gdb\WW_Seclection_Champ_BR_ELEV_Calcd"
#pushdownWells = r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Drift_Wells_for_Pushdown"
#driftWells = r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Drift_Wells"
#driftWellsExtract = r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\Extract_Drift_W1"
#prepushdownBTRaster = r"C:\Users\10214536\OneDrive - State of Ohio\Documents\Bedrock Topography\New_BT_Models_WIP\ModelOutput.gdb\TopoToR_W_Ch1"

#Inputs for Script in Toolbox
waterWells = arcpy.GetParameterAsText(0) #input
prepushdownBTRaster = arcpy.GetParameterAsText(1) #input
pushdownWells = arcpy.GetParameterAsText(2) #output

# Process: Extract Values to Points (Extract Values to Points) (sa)
driftWellsExtract = r'memory/driftWellsExtract'
arcpy.sa.ExtractValuesToPoints(waterWells, prepushdownBTRaster, driftWellsExtract, interpolate_values="NONE", add_attributes="VALUE_ONLY")
print('Values Extracted to Points')
arcpy.AddMessage('Values Extracted to Points')

# Process: Add Field (Add Field) (management)
arcpy.management.AddField(driftWellsExtract, field_name="Pushdown_BR_ELEV", field_type="FLOAT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
print('Add Field Pushdown_BR_ELEV')
arcpy.AddMessage('Add Field Pushdown_BR_ELEV')

# Process: Calculate Field (Calculate Field) (management) Pushdown_BR_ELEV = "!OH_DEM! - !TOTAL_DEPTH!"
expression="!OH_DEM! - !TOTAL_DEPTH!"
arcpy.management.CalculateField(driftWellsExtract, "Pushdown_BR_ELEV", expression, expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
print('Calculate Field 1')
arcpy.AddMessage('Calculate Field 1')

# Process: Add Fields (multiple) (Add Fields (multiple)) (management)
arcpy.management.AddFields(driftWellsExtract, field_description=[["Pushdown_minus_Raster", "FLOAT", "", "", "", ""], ["Use_for_pushdown", "TEXT", "", "255", "", ""]], template=[])
print('Add Fields Pushdown_minus_Raster & Use_for_pushdown')
arcpy.AddMessage('Add Fields Pushdown_minus_Raster & Use_for_pushdown')

# Process: Calculate Field (2) (Calculate Field) (management) Pushdown_minus_Raster = "!Pushdown_BR_ELEV! - !Raster_BR_ELEV!"
expression="!Pushdown_BR_ELEV! - !RASTERVALU!" #Previously "!Pushdown_BR_ELEV! - !Raster_BR_ELEV!"
arcpy.management.CalculateField(driftWellsExtract, "Pushdown_minus_Raster", expression, expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Calculate Field 2')
arcpy.AddMessage('Calculate Field 2')

# Process: Calculate Field (3) (Calculate Field) (management)
arcpy.management.CalculateField(driftWellsExtract, "Use_for_pushdown", expression="classify(!Pushdown_minus_Raster!)", expression_type="PYTHON3", code_block=
"""def classify(push):
        if (push <= 0):
            return 'Yes'
        elif (push > 0):
            return 'No'
""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
print('Calculate Field 3')
arcpy.AddMessage('Calculate Field 3')

# Process: Select (Select) (analysis)
arcpy.analysis.Select(driftWellsExtract, pushdownWells, where_clause="Use_for_pushdown = 'Yes'")
print('Select Use_for_pushdown = Yes')
arcpy.AddMessage('Select Use_for_pushdown = Yes')

# Process: Calculate Field (4) (Calculate Field) (management)
arcpy.management.CalculateField(pushdownWells, "Pushdown_BR_ELEV_minus_1", expression="!Pushdown_BR_ELEV! - 1", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
print('Calculate Field 4')
arcpy.AddMessage('Calculate Field 4')

# Process: Delete (Delete) (management)
Delete_Succeeded = arcpy.management.Delete(driftWellsExtract)
arcpy.AddMessage('Deleted Temporary Point File with Extracted Data')
