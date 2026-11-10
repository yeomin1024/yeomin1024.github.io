"""VERSION v1.0. Artistic food properties, separate from ceramic/plastic tableware."""
import bpy
def apply(asset_name):
    prefix='M_'+asset_name+'_'
    for mat in list(bpy.data.materials):
        if not mat.name.startswith(prefix) or not mat.use_nodes:continue
        bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if bs is None:continue
        if mat.name.endswith('_Liquid'):
            bs.inputs['IOR'].default_value=1.33;bs.inputs['Roughness'].default_value=.08;bs.inputs['Transmission Weight'].default_value=.25
            noise=mat.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=120
            ramp=mat.node_tree.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.04,.04,.04,1);ramp.color_ramp.elements[1].color=(.12,.12,.12,1)
            mat.node_tree.links.new(noise.outputs['Fac'],ramp.inputs[0]);mat.node_tree.links.new(ramp.outputs['Color'],bs.inputs['Roughness'])
    food_keys=('Garnish','Dumpling','GiantDumpling','HalfEgg','Yolk','Noodle','GlassNoodle','Seafood','GrilledPiece','FoldedDough','Lettuce')
    for obj in list(bpy.data.objects):
        if obj.type!='MESH' or not obj.name.startswith('FOOD') or not any(k in obj.name for k in food_keys):continue
        if not obj.name.split('_')[1]==asset_name:continue
        for slot in obj.material_slots:
            src=slot.material
            if src is None:continue
            name=prefix+'Food'+src.name.rsplit('_',1)[-1]
            dst=bpy.data.materials.get(name)
            if dst is None:dst=src.copy();dst.name=name
            slot.material=dst;bs=next(n for n in dst.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            bs.inputs['Subsurface Weight'].default_value=.08 if asset_name=='BangeoSashimi' else .05
            bs.inputs['Subsurface Radius'].default_value=(.008,.004,.002)
            if 'GrilledPiece' in obj.name:bs.inputs['Roughness'].default_value=.16 if name.endswith('BusRed') else .22
