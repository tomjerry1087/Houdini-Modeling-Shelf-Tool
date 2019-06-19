# 1. Set display flag of the sop node to stash
# 2. Set view to /obj level
# 3. Select geometry to stash
# 4. Click this shelf tool

# It will automatically create a "stash" SOP to store current displaying geometry

import toolutils
scene_viewer=toolutils.sceneViewer()
selected_objects=list(scene_viewer.selectObjects(
	prompt=toolutils.selectionPrompt(hou.objNodeTypeCategory()),
	allow_multisel=True,
	allowed_types=("geo",)))
if len(selected_objects)==0:
	raise hou.Error("Nothing was selected.")
def delNodes(_nodes):
	for _n in _nodes:
		_n_inputs=_n.inputs()
		delNodes(_n_inputs)
		_n.destroy()
for _obj in selected_objects:
	dis_sop=_obj.displayNode()
	stash_node=_obj.createNode("stash")
	stash_node.setPosition(dis_sop.position())
	this_output_conns=dis_sop.outputConnections()
	this_output=dis_sop.outputs()
	for _output in this_output:
		curr_inputs=_output.inputs()
		for _i,_inp in enumerate(curr_inputs):
			if _inp==dis_sop:
				_output.setInput(_i,stash_node)
	stash_node.setInput(0,dis_sop)
	stash_node.parm('stashinput').pressButton()
	stash_inputs=stash_node.inputs()
	delNodes(stash_inputs)