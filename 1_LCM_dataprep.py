# Import system modules
import os, arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

PAbound = "Pennsylvania_boundary"
PAbuffer = "Pennsylvania_buffer10km"
NLCD = r"S:\Data\External\Landuse_Landcover\USGS_NLCD\2019NLCD\nlcd_2019_land_cover_l48_20210604.img"

rail_tiger = "input_RailsTiger_Clip"
rail_PennDOT = "input_PennDOT_rails"
roads_tiger = "input_RoadsTiger_Clip"
roads_PennDOT = "input_PennDOT_stateRds"

oilgas = "OilGasLocations_ConventionalUnconventional2023_03"

outFolder = r"S:\Projects\PA_NHP\iMap_PrioritizationTool\Workspace\Christopher_Tracey\LCM\_data\input"

# Set environment settings
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("USA_Contiguous_Albers_Equal_Area_Conic_USGS_version")
arcpy.env.extent = "1271073.94854837 2044788.12728329 1371748.5188338 2100559.31182636" #"1658750.98934339 2138147.93162499 1762664.41198543 2180582.86907212"
arcpy.env.snapRaster = NLCD
env.workspace = r"S:\Projects\PA_NHP\iMap_PrioritizationTool\Workspace\Christopher_Tracey\LCM\PA_LCM _dataprep\PA_LCM _dataprep.gdb"

# # work
# print("Extracting NLCD to project boundary")
# outExtractByMask = ExtractByMask(NLCD, PAbuffer)
#  
# # get developed land
# print("Extracting Medium and High Intensity Developed Land")
# out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (23, 24)")
# out_raster.save("ext_nlcd23_24")
# print("- Creating Distance Raster for Medium and High Intensity Developed Land")
# with arcpy.EnvManager(mask=PAbuffer):
#     out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd23_24", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
#     out_distance_accumulation_raster.save(os.path.join(outFolder, "Dist_nlcd23_24.tif"))
# arcpy.management.Delete("ext_nlcd23_24")
# 
#  # get low developed land
# print("Extracting med developed land")
# out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (22)")
# out_raster.save("ext_nlcd22")
# print("- Creating Distance Raster for Low Intensity Developed land")
# with arcpy.EnvManager(mask=PAbuffer):
#     out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd22", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
#     out_distance_accumulation_raster.save(os.path.join(outFolder, "Dist_nlcd22.tif"))
# arcpy.management.Delete("ext_nlcd22")
#  
# # get high intensity ag land
# print("Extracting high intensity ag land")
# out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (82)")
# out_raster.save("ext_nlcd82")
# print("- Creating Distance Raster for high intensity ag land")
# with arcpy.EnvManager(mask=PAbuffer):
#     out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd82", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
#     out_distance_accumulation_raster.save(os.path.join(outFolder, "Dist_nlcd82.tif"))
# arcpy.management.Delete("ext_nlcd82")
# 
# # get Pasture land
# print("Extracting Pasture and")
# out_raster = arcpy.sa.ExtractByAttributes(outExtractByMask, "Value IN (81)")
# out_raster.save("ext_nlcd81")
# print("- Creating Distance Raster for Pasture land")
# with arcpy.EnvManager(mask=PAbuffer):
#     out_distance_accumulation_raster = arcpy.sa.DistanceAccumulation("ext_nlcd81", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
#     out_distance_accumulation_raster.save(os.path.join(outFolder, "Dist_nlcd81.tif"))
# arcpy.management.Delete("ext_nlcd81")
# 
# # railroads
print("working on the railroads, I've been")
arcpy.analysis.Erase(rail_tiger, PAbound, "rail_tiger_erase")
arcpy.management.Merge(["rail_tiger_erase",rail_PennDOT], "rail_merge")
print("- Creating Distance Raster for Railroads")
out_distance_accumulation_raster1 = arcpy.sa.DistanceAccumulation("rail_merge", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
out_distance_accumulation_raster1.save(os.path.join(outFolder, "Dist_railroad.tif")) #  oName+ ".tif") 
arcpy.management.Delete("rail_tiger_erase")
arcpy.management.Delete("rail_merge")

#output_raster = arcpy.ia.RasterCalculator('(1/(1+ Exp(("Dist_railroad.tif"/100) - 2.5)*2)*300)')
theDivide = Divide(os.path.join(outFolder, "Dist_railroad.tif"), 100)
theDivMinus = Minus(theDivide, 0.5)
theTimes = Times(theDivMinus,10)
theExp = Exp(theTimes)
thePlus = Plus(theExp, 1)
theDivide2 = Divide(1,thePlus)
theTimes2 = Times(theDivide2,500)
theTimes2.save(os.path.join(outFolder, "Wgt_railroad.tif"))

# roads
print("working on the roads")
print("- starting with interstates")
arcpy.analysis.Erase(roads_tiger, PAbound, "roads_tiger_erase")
a = arcpy.management.SelectLayerByAttribute("roads_tiger_erase", "NEW_SELECTION", """"RTTYP" = 'I'""")
arcpy.management.CopyFeatures(a, "roads_tiger_erase_interstates")
arcpy.management.Delete("roads_tiger_erase")
b = arcpy.management.SelectLayerByAttribute(roads_PennDOT, "NEW_SELECTION", """"INTERST_NE" = 'Y'""")
arcpy.management.CopyFeatures(b, "roads_PennDOT_interstates")
arcpy.management.Merge(["roads_tiger_erase_interstates","roads_PennDOT_interstates"], "roads_interstates_merge")
print("- Creating Distance Raster for Interstates")
out_distance_accumulation_raster2 = arcpy.sa.DistanceAccumulation("roads_interstates_merge", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
out_distance_accumulation_raster2.save(os.path.join(outFolder, "Dist_Interstates.tif")) #  oName+ ".tif")
arcpy.management.Delete("roads_tiger_erase") 
arcpy.management.Delete("roads_tiger_erase_interstates")
arcpy.management.Delete("roads_PennDOT_interstates")

#output_raster = arcpy.ia.RasterCalculator('(1/(1+ Exp(("Dist_Interstates.tif"/100) - 2.5)*2)*300)')
theDivide = Divide(os.path.join(outFolder, "Dist_Interstates.tif"), 100)
theDivMinus = Minus(theDivide, 5)
theTimes = Times(theDivMinus,5)
theExp = Exp(theTimes)
thePlus = Plus(theExp, 1)
theDivide2 = Divide(1,thePlus)
theTimes2 = Times(theDivide2,300)
theTimes2.save(os.path.join(outFolder, "Wgt_Interstates.tif"))

# 
print("- moving on to other roads")
arcpy.analysis.Erase(roads_tiger, PAbound, "roads_tiger_erase")
a = arcpy.management.SelectLayerByAttribute("roads_tiger_erase", "NEW_SELECTION", """"RTTYP" <> 'I'""")
arcpy.management.CopyFeatures(a, "roads_tiger_erase_stateroads")
arcpy.management.Delete("roads_tiger_erase")
b = arcpy.management.SelectLayerByAttribute(roads_PennDOT, "NEW_SELECTION", """"INTERST_NE" <> 'Y'""")
arcpy.management.CopyFeatures(b, "roads_PennDOT_stateroads")
arcpy.management.Merge(["roads_tiger_erase_stateroads","roads_PennDOT_stateroads"], "roads_stateroads_merge")
print("- Creating Distance Raster for stateroads")
out_distance_accumulation_raster2 = arcpy.sa.DistanceAccumulation("roads_stateroads_merge", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
out_distance_accumulation_raster2.save(os.path.join(outFolder, "Dist_stateroads.tif")) #  oName+ ".tif")
arcpy.management.Delete("roads_tiger_erase") 
arcpy.management.Delete("roads_tiger_erase_stateroads")
arcpy.management.Delete("roads_PennDOT_stateroads")

#output_raster = arcpy.ia.RasterCalculator('(1/(1+ Exp(("Dist_stateroads.tif"/100) - 2.5)*2)*300)')
theDivide = Divide(os.path.join(outFolder, "Dist_stateroads.tif"), 100)
theDivMinus = Minus(theDivide, 1)
theTimes = Times(theDivMinus,5)
theExp = Exp(theTimes)
thePlus = Plus(theExp, 1)
theDivide2 = Divide(1,thePlus)
theTimes2 = Times(theDivide2,300)
theTimes2.save(os.path.join(outFolder, "Wgt_stateroads.tif"))

# ## STILL NEED TO DO SOMETHING WITH LOCAL ROADS

print("- moving on to oil and gas")
a = arcpy.management.SelectLayerByAttribute(oilgas, "NEW_SELECTION", """"WELL_STATU" = 'Active' And "UNCONVENTI" = 'Y'""")
arcpy.management.CopyFeatures(a, "oilgas_unconventional")
arcpy.analysis.PairwiseBuffer("oilgas_unconventional", "oilgas_unconventional_buffer", "100 Meters")
print("- Creating Distance Raster for unconventional oil gas")
out_distance_accumulation_raster3 = arcpy.sa.DistanceAccumulation("oilgas_unconventional_buffer", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
out_distance_accumulation_raster3.save(os.path.join(outFolder, "Dist_oilgas_unconventional.tif")) #  oName+ ".tif")

#output_raster = arcpy.ia.RasterCalculator('(1/(1+ Exp(("Dist_oilgas.tif"/100) - 2.5)*2)*300)')
theDivide = Divide(os.path.join(outFolder, "Dist_oilgas_unconventional.tif"), 100)
theDivMinus = Minus(theDivide, 2.5)
theTimes = Times(theDivMinus,2)
theExp = Exp(theTimes)
thePlus = Plus(theExp, 1)
theDivide2 = Divide(1,thePlus)
theTimes2 = Times(theDivide2,300)
theTimes2.save(os.path.join(outFolder, "Wgt_oilgas_unconventional.tif"))

#output_raster.save(os.path.join(outFolder, "Wgt_oilgas_unconventional.tif"))

b = arcpy.management.SelectLayerByAttribute(oilgas, "NEW_SELECTION", """"WELL_STATU" = 'Active' And "UNCONVENTI" = 'N'""")
arcpy.management.CopyFeatures(b, "oilgas_conventional")
arcpy.analysis.PairwiseBuffer("oilgas_conventional", "oilgas_conventional_buffer", "50 Meters")
print("- Creating Distance Raster for conventional oil gas")
out_distance_accumulation_raster3 = arcpy.sa.DistanceAccumulation("oilgas_conventional_buffer", None, None, None, None, "BINARY 1 -30 30", None, "BINARY 1 45", None, None, None, None, None, None, '', "PLANAR")
out_distance_accumulation_raster3.save(os.path.join(outFolder, "Dist_oilgas_conventional.tif")) #  oName+ ".tif")

#output_raster = arcpy.ia.RasterCalculator('(1/(1+ Exp(("Dist_oilgas_conventional.tif"/100) - 0.5)*2)*100)')
theDivide = Divide(os.path.join(outFolder, "Dist_oilgas_conventional.tif"), 100)
theDivMinus = Minus(theDivide, 0.5)
theTimes = Times(theDivMinus,2)
theExp = Exp(theTimes)
thePlus = Plus(theExp, 1)
theDivide2 = Divide(1,thePlus)
theTimes2 = Times(theDivide2,100)
theTimes2.save(os.path.join(outFolder, "Wgt_oilgas_conventional.tif"))

# sum all the rasters
#arcpy.management.MosaicToNewRaster(os.path.join(outFolder, "Wgt_oilgas_conventional.tif");os.path.join(outFolder, "Wgt_oilgas_unconventional.tif");os.path.join(outFolder, "Wgt_stateroads.tif"), r"S:\Projects\PA_NHP\iMap_PrioritizationTool\Workspace\Christopher_Tracey\LCM\PA_LCM _dataprep", "testsum.tif", 'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-96.0],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["Latitude_Of_Origin",23.0],UNIT["Meter",1.0]]', "32_BIT_FLOAT", None, 1, "SUM", "FIRST")
