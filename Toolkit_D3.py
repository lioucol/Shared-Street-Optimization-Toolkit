import arcpy
from arcpy.sa import *
import os

# Set working directory
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprx_path = aprx.filePath  
current_file_path = os.path.dirname(aprx_path)
base_dir = os.path.join(current_file_path, "Conflict Score.gdb")

# Create Feature Dataset
if not arcpy.Exists(os.path.join(base_dir, "process")):
    process = arcpy.management.CreateFeatureDataset(base_dir, "process", arcpy.SpatialReference(4326))[0]
if not arcpy.Exists(os.path.join(base_dir, "output")):
    output = arcpy.management.CreateFeatureDataset(base_dir, "output", arcpy.SpatialReference(4326))[0]

##### !!!!!! Set the Code!!!!! ########
Topo_Code = "Topo D"
Solution_Code = "D3"
Cost = 2400
SpaceNeeded = 4

# Define feature class path
CS_NoPath = os.path.join(base_dir, "process", "CS_NoPath")

#### Check the Possibility
try:

    output_field_name = Solution_Code

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(CS_NoPath)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=CS_NoPath, field_name=output_field_name, field_type="FLOAT")


    # Update cursor to normalize width values
    with arcpy.da.UpdateCursor(CS_NoPath, ["VergeWidth", "BufferWidth", output_field_name]) as cursor:
        normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
            VergeWidth = row[cursor.fields.index("VergeWidth")]
            BufferWidth = row[cursor.fields.index("BufferWidth")]

            if SpaceNeeded <= (VergeWidth + BufferWidth) :
                possibility = 1
            else:
                possibility = 0

            # Update row 
            row[normalized_field_index] = possibility
            cursor.updateRow(row)

except Exception as e:
    print(f"Error: {e}")  
    

#### New Conflict Score
try:

    output_field_name = Solution_Code+"_CS"

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(CS_NoPath)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=CS_NoPath, field_name=output_field_name, field_type="FLOAT")

    # Weights
    weight_SharedWidth = 0.25
    weight_CyclWidth = 0.15
    weight_PedeWidth = 0.15
    weight_Hotspot = 0.15
    weight_GroundMk = 0.1
    weight_Divider = 0.1
    weight_Vege = 0.05
    weight_FcAndCnp = 0.05

    # Update cursor to normalize width values
    with arcpy.da.UpdateCursor(CS_NoPath, ["NM_Vege", output_field_name]) as cursor:
        normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
        
            #### !!!!! Attribute Changes !!!!!##### 
            NM_SharedWidth = 0
            NM_CyclWidth = 1/3
            NM_PedeWidth = 1
            NM_Hotspot = 0
            NM_GroundMk = 0
            NM_Divider = 0
            NM_Vege = row[cursor.fields.index("NM_Vege")]
            NM_FcAndCnp = 0

            ##### !!!!!!!!!!!!!!!! ##########

            CS = (
                weight_SharedWidth * NM_SharedWidth +
                weight_CyclWidth * NM_CyclWidth +
                weight_PedeWidth * NM_PedeWidth +
                weight_Hotspot * NM_Hotspot +
                weight_GroundMk * NM_GroundMk +
                weight_Divider * NM_Divider +
                weight_Vege * NM_Vege +
                weight_FcAndCnp * NM_FcAndCnp
            )

            # Update row 
            row[normalized_field_index] = CS
            cursor.updateRow(row)

except Exception as e:
    print(f"Error: {e}")    



#### Cost
try:

    output_field_name = Solution_Code+"_Cost"

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(CS_NoPath)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=CS_NoPath, field_name=output_field_name, field_type="FLOAT")

    # Update cursor to normalize width values
    with arcpy.da.UpdateCursor(CS_NoPath, [output_field_name]) as cursor:
        normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
            
            # Update row 
            row[normalized_field_index] = Cost
            cursor.updateRow(row)

except Exception as e:
    print(f"Error: {e}")           
