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
Normalized = os.path.join(base_dir, "process", "Normalized")


# Export Features
arcpy.conversion.ExportFeatures(in_features=SharedSpace, out_features=Normalized)


#### Normalized

### NM_SharedWidth
output_field_name = "NM_SharedWidth"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]

# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

with arcpy.da.UpdateCursor(Normalized, ["Path1Type", "Path1PedWidth", "Path1CycWidth", "Path2PedWidth", "Path2CycWidth", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)
        
        
    for row in cursor:
        Path1Type = row[cursor.fields.index("Path1Type")]
        Path1PedWidth = row[cursor.fields.index("Path1PedWidth")]
        Path1CycWidth = row[cursor.fields.index("Path1CycWidth")]
        Path2PedWidth = row[cursor.fields.index("Path2PedWidth")]
        Path2CycWidth = row[cursor.fields.index("Path2CycWidth")]
            
        # Determine the relevant path width based on type    
        if Path1Type is None or Path1Type == "NULL":
            NM_SharedWidth = 1
        elif Path1Type == "Pedestrian Only" or Path1Type == "Cycling Only":
            NM_SharedWidth = 1
        elif Path1Type == "Shared Cycling" or Path1Type == "Shared Pedestrian":
            NM_SharedWidth = 0
        else:
            SharedWidth = 1
            

        # Update row with the normalized width
        row[normalized_field_index] = NM_SharedWidth
        cursor.updateRow(row)



        
### NM_CyclWidth
output_field_name = "NM_CyclWidth"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]

# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

with arcpy.da.UpdateCursor(Normalized, ["Path1Type", "Path1PedWidth", "Path1CycWidth", "Path2PedWidth", "Path2CycWidth", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)
        
    cycl_widths = []
        
    for row in cursor:
        Path1Type = row[cursor.fields.index("Path1Type")]
        Path1PedWidth = row[cursor.fields.index("Path1PedWidth")]
        Path1CycWidth = row[cursor.fields.index("Path1CycWidth")]
        Path2PedWidth = row[cursor.fields.index("Path2PedWidth")]
        Path2CycWidth = row[cursor.fields.index("Path2CycWidth")]
            
        # Determine the relevant path width based on type    
        if Path1Type is None or Path1Type == "NULL":
            CyclWidth = 1
        elif Path1Type == "Pedestrian Only":
            CyclWidth = Path1PedWidth
        elif Path1Type == "Cycling Only":
            CyclWidth = Path1CycWidth
        elif Path1Type == "Shared Cycling":
            CyclWidth = Path1CycWidth
        elif Path1Type == "Shared Pedestrian":
            CyclWidth = Path2CycWidth
        else:
            CyclWidth = 1
            
        cycl_widths.append(CyclWidth)
                
        min_CyclWidth = min(cycl_widths) if cycl_widths else 0
        max_CyclWidth = max(cycl_widths) if cycl_widths else 1
        
        # Normalize width (avoid division by zero)
        if CyclWidth is None:
            NM_CyclWidth = 0
        elif min_CyclWidth == max_CyclWidth:
            NM_CyclWidth = 0
        else:
            NM_CyclWidth = (max_CyclWidth - CyclWidth) / (max_CyclWidth - min_CyclWidth)

        # Update row with the normalized width
        row[normalized_field_index] = NM_CyclWidth
        cursor.updateRow(row)
        
        
        
### NM_PedeWidth
output_field_name = "NM_PedeWidth"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]

# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

with arcpy.da.UpdateCursor(Normalized, ["Path1Type", "Path1PedWidth", "Path1CycWidth", "Path2PedWidth", "Path2CycWidth", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)
        
    pede_widths = []
        
    for row in cursor:
        Path1Type = row[cursor.fields.index("Path1Type")]
        Path1PedWidth = row[cursor.fields.index("Path1PedWidth")]
        Path1CycWidth = row[cursor.fields.index("Path1CycWidth")]
        Path2PedWidth = row[cursor.fields.index("Path2PedWidth")]
        Path2CycWidth = row[cursor.fields.index("Path2CycWidth")]
            
        # Determine the relevant path width based on type    
        if Path1Type is None or Path1Type == "NULL":
            PedeWidth = 0
        elif Path1Type == "Pedestrian Only":
            PedeWidth = Path1PedWidth
        elif Path1Type == "Cycling Only":
            PedeWidth = Path1CycWidth
        elif Path1Type == "Shared Cycling":
            PedeWidth = Path2PedWidth
        elif Path1Type == "Shared Pedestrian":
            PedeWidth = Path1PedWidth
        else:
            PedeWidth = 0
            
        pede_widths.append(PedeWidth)
                
        min_PedeWidth = min(pede_widths) if pede_widths else 0
        max_PedeWidth = max(pede_widths) if pede_widths else 1
        
        # Normalize width (avoid division by zero)
        if PedeWidth is None:
            NM_PedeWidth = 0
        elif min_PedeWidth == max_PedeWidth:
            NM_PedeWidth = 0
        else:
            NM_PedeWidth = (max_PedeWidth - PedeWidth) / (max_PedeWidth - min_PedeWidth)

        # Update row with the normalized width
        row[normalized_field_index] = NM_PedeWidth
        cursor.updateRow(row)
        



### NM_Hotspot
output_field_name = "NM_Hotspot"

# Define feature class paths
BusStop = os.path.join(base_dir, "input", "BusStop")
Entrance = os.path.join(base_dir, "input", "Entrance")

POI = os.path.join(base_dir, "process", "POI") 
POI_Buffer = os.path.join(base_dir, "process", "POI_Buffer")
SpatialJoin = os.path.join(base_dir, "process", "SpatialJoin") 

# Merge to POI
arcpy.management.Merge(inputs=[Entrance, BusStop], output=POI)

# Process: Buffer (Buffer) (analysis)
arcpy.analysis.Buffer(POI, POI_Buffer, "15 Meters", "FULL", "ROUND")

# Process: Spatial Join (Spatial Join) 
arcpy.analysis.SpatialJoin(target_features=Normalized, join_features=POI_Buffer, out_feature_class=SpatialJoin, field_mapping=
    "ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,POI_Buffer,ORIG_FID,-1,-1"
    )

# Normalize Counts
arcpy.management.AddField(in_table=SpatialJoin, field_name=output_field_name, field_type="FLOAT")

join_counts = []

with arcpy.da.UpdateCursor(SpatialJoin, ["Join_Count", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)    
    
    for row in cursor:
        Join_Count = row[cursor.fields.index("Join_Count")]
        join_counts.append(Join_Count)
        
        min_count = min(join_counts) if join_counts else 0
        max_count = max(join_counts) if join_counts else 1 
     
        if Join_Count is None:
            NM_Hotspot = 0
        elif min_count == max_count:
            NM_Hotspot = 0
        else:
            NM_Hotspot = (Join_Count - min_count) / (max_count - min_count) 

        row[normalized_field_index] = NM_Hotspot
        cursor.updateRow(row) 

# Process: Join Field (Join Field) (management)
Normalized = arcpy.management.JoinField(in_data=Normalized, in_field="OBJECTID", join_table=SpatialJoin, join_field="OBJECTID", fields=["NM_Hotspot"], fm_option="NOT_USE_FM")[0]



### NM_GroundMk
output_field_name = "NM_GroundMk"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]
 
# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

# Update cursor to normalize width values
with arcpy.da.UpdateCursor(Normalized, ["Path1GroundMarking", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

    for row in cursor:
        Path1GroundMarking = row[cursor.fields.index("Path1GroundMarking")]

        # Determine the relevant path width based on type
        if Path1GroundMarking is None or Path1GroundMarking == "NULL":
            NM_GroundMk = 1
        elif Path1GroundMarking == "Line":
            NM_GroundMk = 0.5
        elif Path1GroundMarking == "Filled Color":
            NM_GroundMk = 0
        else:
            NM_GroundMk = 1


        # Update row with the normalized width
        row[normalized_field_index] = NM_GroundMk
        cursor.updateRow(row)
        
        
        
### NM_Divider
output_field_name = "NM_Divider"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]
  
# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")
        
# Update cursor to normalize width values
with arcpy.da.UpdateCursor(Normalized, ["Divider", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

    for row in cursor:
        Divider = row[cursor.fields.index("Divider")]

        # Determine the relevant path width based on type
        if Divider is None or Divider == "NULL":
            Divider = 1
        elif Path1GroundMarking == "NO":
            Divider = 1
        elif Path1GroundMarking == "YES":
            Divider = 0
        else:
            Divider = 1


        # Update row with the normalized width
        row[normalized_field_index] = Divider
        cursor.updateRow(row)    



### NM_Vege  

output_field_name = "NM_Vege"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]

# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

# Update cursor to normalize width values
with arcpy.da.UpdateCursor(Normalized, ["VergeVege", "BufferVege", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

    for row in cursor:
        VergeVege = row[cursor.fields.index("VergeVege")]
        BufferVege = row[cursor.fields.index("BufferVege")]
        
        if VergeVege is None or VergeVege == "NULL":
            normalized_vv = 0
        elif VergeVege == "Grassland":
            normalized_vv = 0.2
        elif VergeVege == "Clustered Shrub":
            normalized_vv = 0.4
        elif VergeVege == "Small Street Tree":
            normalized_vv = 0.6
        elif VergeVege == "Dense Shrub":
            normalized_vv = 0.8
        elif VergeVege == "Large Shading Tree":
            normalized_vv = 1   
        else:
            normalized_vv = 0
                

        if BufferVege is None or BufferVege == "NULL":
            normalized_bv = 0
        elif BufferVege == "Grassland":
            normalized_bv = 0.2
        elif BufferVege == "Clustered Shrub":
            normalized_bv = 0.4
        elif BufferVege == "Small Street Tree":
            normalized_bv = 0.6
        elif BufferVege == "Dense Shrub":
            normalized_bv = 0.8
        elif BufferVege == "Large Shading Tree":
            normalized_bv = 1   
        else:
            normalized_bv = 0

        NM_Vege= (normalized_bv + normalized_vv)/ 2


        # Update row with the normalized width
        row[normalized_field_index] = NM_Vege
        cursor.updateRow(row)  



### NM_FcAndCnp      
output_field_name = "NM_FcAndCnp"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(Normalized)]
  
# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")
        
# Update cursor to normalize width values
with arcpy.da.UpdateCursor(Normalized, ["VergeFence", "Path1Canopy", "Path2Canopy", "BufferFence", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

    for row in cursor:
        VergeFence = row[cursor.fields.index("VergeFence")]
        Path1Canopy = row[cursor.fields.index("Path1Canopy")]
        Path2Canopy = row[cursor.fields.index("Path2Canopy")]
        BufferFence = row[cursor.fields.index("BufferFence")]
        
        if VergeFence == "YES" or Path1Canopy == "YES" or Path2Canopy == "YES" or BufferFence == "YES":
            NM_FcAndCnp = 1
        else:
            NM_FcAndCnp = 0


        # Update row with the normalized width
        row[normalized_field_index] = NM_FcAndCnp
        cursor.updateRow(row)   




#### Current_CS
try:

    output_field_name = "Current_CS"

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(Normalized)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="FLOAT")

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
    with arcpy.da.UpdateCursor(Normalized, ["NM_SharedWidth", "NM_CyclWidth", "NM_PedeWidth", "NM_Hotspot", "NM_GroundMk", "NM_Divider", "NM_Vege", "NM_FcAndCnp", output_field_name]) as cursor:
        normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
            NM_SharedWidth = row[cursor.fields.index("NM_SharedWidth")]
            NM_CyclWidth = row[cursor.fields.index("NM_CyclWidth")]
            NM_PedeWidth = row[cursor.fields.index("NM_PedeWidth")]
            NM_Hotspot = row[cursor.fields.index("NM_Hotspot")]
            NM_GroundMk = row[cursor.fields.index("NM_GroundMk")]
            NM_Divider = row[cursor.fields.index("NM_Divider")]
            NM_Vege = row[cursor.fields.index("NM_Vege")]

            Current_CS = (
                weight_SharedWidth * NM_SharedWidth +
                weight_CyclWidth * NM_CyclWidth +
                weight_PedeWidth * NM_PedeWidth +
                weight_Hotspot * NM_Hotspot +
                weight_GroundMk * NM_GroundMk +
                weight_Divider * NM_Divider +
                weight_Vege * NM_Vege +
                weight_FcAndCnp * NM_FcAndCnp
            )

            # Update row with the normalized width
            row[normalized_field_index] = Current_CS
            cursor.updateRow(row)

except Exception as e:
    print(f"Error: {e}")    
    
    
    
#### Topo
try:

    output_field_name = "Topo"

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(Normalized)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=Normalized, field_name=output_field_name, field_type="TEXT")


    # Update cursor to normalize width values
    with arcpy.da.UpdateCursor(Normalized, ["VergeFence", "BufferFence", "Path1Canopy", "Path2Canopy", "Path2Type", output_field_name]) as cursor:
        normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
            VergeFence = row[cursor.fields.index("VergeFence")]
            BufferFence = row[cursor.fields.index("BufferFence")]
            Path1Canopy = row[cursor.fields.index("Path1Canopy")]
            Path2Canopy = row[cursor.fields.index("Path2Canopy")]
            Path2Type = row[cursor.fields.index("Path2Type")]

            if VergeFence == "YES" or BufferFence == "YES" or Path1Canopy == "YES" or Path2Canopy == "YES":
                topo = "Topo C"
            elif Path2Type in [None, "", "NULL"]:
                topo = "Topo A"
            else:
                topo = "Topo B"

            # Update row with the normalized width
            row[normalized_field_index] = topo
            cursor.updateRow(row)

except Exception as e:
    print(f"Error: {e}")    
    
    
#### NoPath
# Define feature class path
NoPath = os.path.join(base_dir, "input", "NoPath")
CS_NoPath = os.path.join(base_dir, "process", "CS_NoPath")

# Export Features
arcpy.conversion.ExportFeatures(in_features=NoPath, out_features=CS_NoPath)  
    
    
output_field_name = "NM_Vege"

# Get existing field names
field_names = [field.name for field in arcpy.ListFields(CS_NoPath)]

# Add field if it does not exist
if output_field_name not in field_names:
    arcpy.management.AddField(in_table=CS_NoPath, field_name=output_field_name, field_type="FLOAT")

# Update cursor to normalize width values
with arcpy.da.UpdateCursor(CS_NoPath, ["VergeVege", "BufferVege", output_field_name]) as cursor:
    normalized_field_index = cursor.fields.index(output_field_name)  # Get index of output field

    for row in cursor:
        VergeVege = row[cursor.fields.index("VergeVege")]
        BufferVege = row[cursor.fields.index("BufferVege")]
        
        if VergeVege is None or VergeVege == "NULL":
            normalized_vv = 0
        elif VergeVege == "Grassland":
            normalized_vv = 0.2
        elif VergeVege == "Clustered Shrub":
            normalized_vv = 0.4
        elif VergeVege == "Small Street Tree":
            normalized_vv = 0.6
        elif VergeVege == "Dense Shrub":
            normalized_vv = 0.8
        elif VergeVege == "Large Shading Tree":
            normalized_vv = 1   
        else:
            normalized_vv = 0
                

        if BufferVege is None or BufferVege == "NULL":
            normalized_bv = 0
        elif BufferVege == "Grassland":
            normalized_bv = 0.2
        elif BufferVege == "Clustered Shrub":
            normalized_bv = 0.4
        elif BufferVege == "Small Street Tree":
            normalized_bv = 0.6
        elif BufferVege == "Dense Shrub":
            normalized_bv = 0.8
        elif BufferVege == "Large Shading Tree":
            normalized_bv = 1   
        else:
            normalized_bv = 0

        NM_Vege= (normalized_bv + normalized_vv)/ 2


        # Update row 
        row[normalized_field_index] = NM_Vege
        cursor.updateRow(row)  
        
try:

    output_field_name = "Current_CS"

    # Get existing field names
    field_names = [field.name for field in arcpy.ListFields(CS_NoPath)]

    # Add field if it does not exist
    if output_field_name not in field_names:
        arcpy.management.AddField(in_table=CS_NoPath, field_name=output_field_name, field_type="FLOAT")
        
    # Update cursor to normalize width values
    with arcpy.da.UpdateCursor(CS_NoPath, [output_field_name]) as cursor:
        index = cursor.fields.index(output_field_name)  # Get index of output field

        for row in cursor:
            index = 9999
            
            # Update row 
            row[normalized_field_index] = index
            cursor.updateRow(row)    

except Exception as e:
    print(f"Error: {e}")  
    
    
#### Crossing
# Define feature class path
Crossing = os.path.join(base_dir, "input", "Crossing")
CS_Crossing = os.path.join(base_dir, "process", "CS_Crossing")

# Export Features
arcpy.conversion.ExportFeatures(in_features=Crossing, out_features=CS_Crossing)  


#### Joint
# Define feature class path
Joint = os.path.join(base_dir, "input", "Joint")
CS_Joint = os.path.join(base_dir, "process", "CS_Joint")

# Export Features
arcpy.conversion.ExportFeatures(in_features=Joint, out_features=CS_Joint)  

