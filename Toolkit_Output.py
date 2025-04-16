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

# Define feature class path
SharedSpace = os.path.join(base_dir, "input", "SharedSpace")
NoPath = os.path.join(base_dir, "input", "NoPath")
Crossing = os.path.join(base_dir, "input", "Crossing")
Joint = os.path.join(base_dir, "input", "Joint")

Normalized = os.path.join(base_dir, "process", "Normalized")
CS_NoPath = os.path.join(base_dir, "process", "CS_NoPath")
CS_Crossing = os.path.join(base_dir, "process", "CS_Crossing")
CS_Joint = os.path.join(base_dir, "process", "CS_Joint")

SharedSpace_Score = os.path.join(base_dir, "output", "SharedSpace_Score")
NoPath_Score = os.path.join(base_dir, "output", "NoPath_Score")
Crossing_Score = os.path.join(base_dir, "output", "Crossing_Score")
Joint_Score = os.path.join(base_dir, "output", "Joint_Score")


### SharedSpace_Score
try:
    in_table = Normalized 

    fields_to_add = [
        ("D1", "FLOAT"),
        ("D1_CS", "FLOAT"),
        ("D1_Cost", "FLOAT"),
        ("D2", "FLOAT"),
        ("D2_CS", "FLOAT"),
        ("D2_Cost", "FLOAT"),
        ("D3", "FLOAT"),
        ("D3_CS", "FLOAT"),
        ("D3_Cost", "FLOAT"),
        
    ]
    for field_name, field_type in fields_to_add:
        if field_name not in [f.name for f in arcpy.ListFields(in_table)]:
            arcpy.management.AddField(in_table, field_name, field_type)

except Exception as e:
    print(f"Error: {e}")  


try:

    input_table=Normalized
    output_table=SharedSpace_Score

    fields_to_export = [
        "Current_CS", "Topo", 
        "A1", "A1_CS", "A1_Cost", 
        "A2", "A2_CS", "A2_Cost",
        "A3", "A3_CS", "A3_Cost",
        "A4", "A4_CS", "A4_Cost",
        "B1", "B1_CS", "B1_Cost",
        "B2", "B2_CS", "B2_Cost",
        "B3", "B3_CS", "B3_Cost",
        "C1", "C1_CS", "C1_Cost",
        "D1", "D1_CS", "D1_Cost",
        "D2", "D2_CS", "D2_Cost",
        "D3", "D3_CS", "D3_Cost"
    ]

    field_mappings = arcpy.FieldMappings()

    for field in fields_to_export:
        field_map = arcpy.FieldMap()
        field_map.addInputField(input_table, field)
        field_mappings.addFieldMap(field_map)

    arcpy.conversion.ExportFeatures(input_table, output_table, field_mapping=field_mappings)

except Exception as e:
    print(f"Error: {e}") 



### NoPath_Score   
try:
    in_table = CS_NoPath 

    fields_to_add = [
        ("Topo", "TEXT"),
        ("A1", "FLOAT"),
        ("A1_CS", "FLOAT"),
        ("A1_Cost", "FLOAT"),
        ("A2", "FLOAT"),
        ("A2_CS", "FLOAT"),
        ("A2_Cost", "FLOAT"),
        ("A3", "FLOAT"),
        ("A3_CS", "FLOAT"),
        ("A3_Cost", "FLOAT"),
        ("A4", "FLOAT"),
        ("A4_CS", "FLOAT"),
        ("A4_Cost", "FLOAT"),
        ("B1", "FLOAT"),
        ("B1_CS", "FLOAT"),
        ("B1_Cost", "FLOAT"),
        ("B2", "FLOAT"),
        ("B2_CS", "FLOAT"),
        ("B2_Cost", "FLOAT"),
        ("B3", "FLOAT"),
        ("B3_CS", "FLOAT"),
        ("B3_Cost", "FLOAT"),
        ("C1", "FLOAT"),
        ("C1_CS", "FLOAT"),
        ("C1_Cost", "FLOAT"),
        
    ]
    for field_name, field_type in fields_to_add:
        if field_name not in [f.name for f in arcpy.ListFields(in_table)]:
            arcpy.management.AddField(in_table, field_name, field_type)
            
    with arcpy.da.UpdateCursor(in_table, ["Topo"]) as cursor:
        field_index = cursor.fields.index("Topo")  # Get index of output field
    
        for row in cursor:
            topo= "Topo D"
            
            row[field_index] = topo
            cursor.updateRow(row)


except Exception as e:
    print(f"Error: {e}")   
    
    
    
try:

    input_table=CS_NoPath
    output_table=NoPath_Score

    fields_to_export = [
        "Current_CS", "Topo", 
        "A1", "A1_CS", "A1_Cost", 
        "A2", "A2_CS", "A2_Cost",
        "A3", "A3_CS", "A3_Cost",
        "A4", "A4_CS", "A4_Cost",
        "B1", "B1_CS", "B1_Cost",
        "B2", "B2_CS", "B2_Cost",
        "B3", "B3_CS", "B3_Cost",
        "C1", "C1_CS", "C1_Cost",
        "D1", "D1_CS", "D1_Cost",
        "D2", "D2_CS", "D2_Cost",
        "D3", "D3_CS", "D3_Cost"
    ]

    field_mappings = arcpy.FieldMappings()

    for field in fields_to_export:
        field_map = arcpy.FieldMap()
        field_map.addInputField(input_table, field)
        field_mappings.addFieldMap(field_map)

    arcpy.conversion.ExportFeatures(input_table, output_table, field_mapping=field_mappings)

except Exception as e:
    print(f"Error: {e}") 
    
    
    
### Crossing_Score
try:
    in_table = CS_Crossing

    fields_to_add = [
        ("Current_CS", "FLOAT"),
        ("Topo", "TEXT"),
        ("A1", "FLOAT"),
        ("A1_CS", "FLOAT"),
        ("A1_Cost", "FLOAT"),
        ("A2", "FLOAT"),
        ("A2_CS", "FLOAT"),
        ("A2_Cost", "FLOAT"),
        ("A3", "FLOAT"),
        ("A3_CS", "FLOAT"),
        ("A3_Cost", "FLOAT"),
        ("A4", "FLOAT"),
        ("A4_CS", "FLOAT"),
        ("A4_Cost", "FLOAT"),
        ("B1", "FLOAT"),
        ("B1_CS", "FLOAT"),
        ("B1_Cost", "FLOAT"),
        ("B2", "FLOAT"),
        ("B2_CS", "FLOAT"),
        ("B2_Cost", "FLOAT"),
        ("B3", "FLOAT"),
        ("B3_CS", "FLOAT"),
        ("B3_Cost", "FLOAT"),
        ("C1", "FLOAT"),
        ("C1_CS", "FLOAT"),
        ("C1_Cost", "FLOAT"),
        ("D1", "FLOAT"),
        ("D1_CS", "FLOAT"),
        ("D1_Cost", "FLOAT"),
        ("D2", "FLOAT"),
        ("D2_CS", "FLOAT"),
        ("D2_Cost", "FLOAT"),
        ("D3", "FLOAT"),
        ("D3_CS", "FLOAT"),
        ("D3_Cost", "FLOAT"),
        
    ]
    for field_name, field_type in fields_to_add:
        if field_name not in [f.name for f in arcpy.ListFields(in_table)]:
            arcpy.management.AddField(in_table, field_name, field_type)
            
    with arcpy.da.UpdateCursor(in_table, ["Current_CS"]) as cursor:
        field_index = cursor.fields.index("Current_CS")  # Get index of output field
    
        for row in cursor:
            SCORE= 1
            
            row[field_index] = SCORE
            cursor.updateRow(row)


except Exception as e:
    print(f"Error: {e}")   
    
try:

    input_table=CS_Crossing
    output_table=Crossing_Score

    fields_to_export = [
        "Current_CS", "Topo", 
        "A1", "A1_CS", "A1_Cost", 
        "A2", "A2_CS", "A2_Cost",
        "A3", "A3_CS", "A3_Cost",
        "A4", "A4_CS", "A4_Cost",
        "B1", "B1_CS", "B1_Cost",
        "B2", "B2_CS", "B2_Cost",
        "B3", "B3_CS", "B3_Cost",
        "C1", "C1_CS", "C1_Cost",
        "D1", "D1_CS", "D1_Cost",
        "D2", "D2_CS", "D2_Cost",
        "D3", "D3_CS", "D3_Cost"
    ]

    field_mappings = arcpy.FieldMappings()

    for field in fields_to_export:
        field_map = arcpy.FieldMap()
        field_map.addInputField(input_table, field)
        field_mappings.addFieldMap(field_map)

    arcpy.conversion.ExportFeatures(input_table, output_table, field_mapping=field_mappings)

except Exception as e:
    print(f"Error: {e}") 
    
    
    
    
### Joint_Score
try:
    in_table = CS_Joint

    fields_to_add = [
        ("Current_CS", "FLOAT"),
        ("Topo", "TEXT"),
        ("A1", "FLOAT"),
        ("A1_CS", "FLOAT"),
        ("A1_Cost", "FLOAT"),
        ("A2", "FLOAT"),
        ("A2_CS", "FLOAT"),
        ("A2_Cost", "FLOAT"),
        ("A3", "FLOAT"),
        ("A3_CS", "FLOAT"),
        ("A3_Cost", "FLOAT"),
        ("A4", "FLOAT"),
        ("A4_CS", "FLOAT"),
        ("A4_Cost", "FLOAT"),
        ("B1", "FLOAT"),
        ("B1_CS", "FLOAT"),
        ("B1_Cost", "FLOAT"),
        ("B2", "FLOAT"),
        ("B2_CS", "FLOAT"),
        ("B2_Cost", "FLOAT"),
        ("B3", "FLOAT"),
        ("B3_CS", "FLOAT"),
        ("B3_Cost", "FLOAT"),
        ("C1", "FLOAT"),
        ("C1_CS", "FLOAT"),
        ("C1_Cost", "FLOAT"),
        ("D1", "FLOAT"),
        ("D1_CS", "FLOAT"),
        ("D1_Cost", "FLOAT"),
        ("D2", "FLOAT"),
        ("D2_CS", "FLOAT"),
        ("D2_Cost", "FLOAT"),
        ("D3", "FLOAT"),
        ("D3_CS", "FLOAT"),
        ("D3_Cost", "FLOAT"),
        
    ]
    for field_name, field_type in fields_to_add:
        if field_name not in [f.name for f in arcpy.ListFields(in_table)]:
            arcpy.management.AddField(in_table, field_name, field_type)
            
    with arcpy.da.UpdateCursor(in_table, ["Current_CS"]) as cursor:
        field_index = cursor.fields.index("Current_CS")  # Get index of output field
    
        for row in cursor:
            SCORE= 1
            
            row[field_index] = SCORE
            cursor.updateRow(row)


except Exception as e:
    print(f"Error: {e}")   
    
try:

    input_table=CS_Joint
    output_table=Joint_Score

    fields_to_export = [
        "Current_CS", "Topo", 
        "A1", "A1_CS", "A1_Cost", 
        "A2", "A2_CS", "A2_Cost",
        "A3", "A3_CS", "A3_Cost",
        "A4", "A4_CS", "A4_Cost",
        "B1", "B1_CS", "B1_Cost",
        "B2", "B2_CS", "B2_Cost",
        "B3", "B3_CS", "B3_Cost",
        "C1", "C1_CS", "C1_Cost",
        "D1", "D1_CS", "D1_Cost",
        "D2", "D2_CS", "D2_Cost",
        "D3", "D3_CS", "D3_Cost"
    ]

    field_mappings = arcpy.FieldMappings()

    for field in fields_to_export:
        field_map = arcpy.FieldMap()
        field_map.addInputField(input_table, field)
        field_mappings.addFieldMap(field_map)

    arcpy.conversion.ExportFeatures(input_table, output_table, field_mapping=field_mappings)

except Exception as e:
    print(f"Error: {e}") 
 
