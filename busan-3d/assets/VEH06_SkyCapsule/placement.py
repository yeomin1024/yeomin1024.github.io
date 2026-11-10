"""Deterministic module placement. VERSION v1.0; all numeric layout choices are artistic settings."""
import bpy, json, random
from pathlib import Path
SEED=20261110
def place(module_id, count=4, spacing=5.0, seed=SEED):
    if count<1 or spacing<=0: raise ValueError("positive count and spacing required")
    data=json.loads((Path(__file__).parent/'modules.json').read_text())
    names=data['modules'][module_id]
    prefix=data['prefix']
    source=[bpy.data.objects[prefix+n+'_L0'] for n in names]
    from mathutils import Vector, Matrix
    import math
    points=[o.matrix_world@Vector(p) for o in source for p in o.bound_box]
    lo=Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    pivot=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
    col=bpy.data.collections.new(prefix+module_id+'Placed');bpy.context.scene.collection.children.link(col)
    rng=random.Random(seed)
    history=[]
    for i in range(count):
        variation=rng.choices(range(6),weights=[20,15,20,15,10,20])[0]
        if len(history)>=2 and history[-1]==history[-2]==variation: variation=(variation+1)%6
        history.append(variation)
        house=module_id.startswith(('House','Shop'))
        angle=rng.choice([0,90,180,270]) if house else 0
        step=max(spacing,max(hi.x-lo.x,hi.y-lo.y)+.5) if house else spacing
        for src in source:
            dst=src.copy();dst.data=src.data;dst.parent=None
            dst.matrix_world=src.matrix_world.copy();dst.location-=pivot
            dst.matrix_world=Matrix.Rotation(math.radians(angle),4,'Z')@dst.matrix_world
            dst.location.y+=i*step;dst['variation_id']=variation;dst['seed']=seed
            if house and 'Wall' in src.name:
                colors=['#F4A6A0','#F7D57A','#8FC9B9','#9DB7E0','#C3B1E1','#F2EFE6']
                color=colors[variation];rgb=[int(color[j:j+2],16)/255 for j in (1,3,5)]
                rgba=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1.,)
                for slot in dst.material_slots:
                    original=slot.material;mat=bpy.data.materials.get(original.name+'Variant'+str(variation))
                    if mat is None:
                        mat=original.copy();mat.name=original.name+'Variant'+str(variation);mat.diffuse_color=rgba
                        if mat.use_nodes:
                            bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
                            if bs:bs.inputs['Base Color'].default_value=rgba
                    slot.link='OBJECT';slot.material=mat
            col.objects.link(dst)
    return col
