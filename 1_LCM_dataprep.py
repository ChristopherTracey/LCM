# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

# Set environment settings
arcpy.env.overwriteOutput = True
env.workspace = r"S:\Projects\PA_NHP\iMap_PrioritizationTool\Workspace\Christopher_Tracey\LCM\PA_LCM _dataprep\PA_LCM _dataprep.gdb"

PAbuffer = "Pennsylvania_buffer10km"
NLCD = r"S:\Data\External\Landuse_Landcover\USGS_NLCD\2019NLCD\nlcd_2019_land_cover_l48_20210604.img"

print("Extracting NLCD to project boundary")

outExtractByMask = ExtractByMask(NLCD, PAbuffer)

# get developed land
print("Extracting Medium and High Intensity Developed Land")
out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (23, 24)")
out_raster.save("ext_nlcd23_24")
print("Creating Distance Raster for Medium and High Intensity Developed Land")
with arcpy.EnvManager(snapRaster="ext_nlcd23_24", mask=PAbuffer):
    out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd23_24", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
    out_distance_accumulation_raster.save(r"Dist_nlcd23_24")

# get med developed land
print("Extracting  med developed  land")
out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (22)")
out_raster.save("ext_nlcd22")
print("Creating Distance Raster for med developed land")
with arcpy.EnvManager(snapRaster="ext_nlcd22", mask=PAbuffer):
    out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd22", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
    out_distance_accumulation_raster.save(r"Dist_nlcd22")

# get high intensity ag land
print("Extracting high intensity ag land")
out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (82)")
out_raster.save("ext_nlcd82")
print("Creating Distance Raster for high intensity ag land")
with arcpy.EnvManager(snapRaster="ext_nlcd23_24", mask=PAbuffer):
    out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd82", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
    out_distance_accumulation_raster.save(r"Dist_nlcd82")

