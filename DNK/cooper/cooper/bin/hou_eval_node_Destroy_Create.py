import sys,hou

fr = 1

hou.hipFile.load("/studio/proj/Voskresensky/work/Water_Tower/3d/Water_Tower_sim_v0020.hip", ignore_load_warnings=True)

node=hou.node("/obj/geo_prepare/file6")
print node.name()
node.cook(force=True,frame_range=(1,2))

