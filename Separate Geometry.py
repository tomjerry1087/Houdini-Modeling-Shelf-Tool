# 1. Set view to /obj level
# 2. Select geometry to separate
# 3. Click this shelf tool

# It will hide original object, and create geometry node for each separated part.
# You can then stash those geometries if you no longer need to modify them

import toolutils
scene_viewer=toolutils.sceneViewer()
selected_objects=list(scene_viewer.selectObjects(
	prompt=toolutils.selectionPrompt(hou.objNodeTypeCategory()),
	allow_multisel=True,
	allowed_types=("geo",)))
if len(selected_objects)==0:
	raise hou.Error("Nothing was selected.")
for _obj in selected_objects:
	_obj.setDisplayFlag(False)
	dis_sop=_obj.displayNode()
	conn_sop=dis_sop.createOutputNode('connectivity','connectivity',run_init_scripts=False)
	conn_sop.parm('attribname').set('class')
	part_sop=conn_sop.createOutputNode('partition','partition',run_init_scripts=False)
	part_sop.parm('rule').set('`@class`')
	part_sop.setDisplayFlag(True)
	part_sop.setRenderFlag(True)
	groups=part_sop.geometry().primGroups()
	for group in groups:
		new_obj=_obj.createOutputNode('geo',group.name(),run_init_scripts=False)
		merge=new_obj.createNode('object_merge')
		merge.parm('objpath1').set(part_sop.path())
		merge.parm('group1').set(group.name())
