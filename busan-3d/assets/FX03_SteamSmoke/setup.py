# VERSION: v1.0 — 2026-11-10
"""FX settings library. All artistic values are settings; no physical asset export."""
import bpy, math
ASSET_ID='FX03'
ASSET_NAME='SteamSmoke'
SPEC_VERSION='v1.0'
PREFIX=ASSET_ID+'_'+ASSET_NAME
PRESETS={
 'morning':dict(world='#A9D6F0',strength=.55,sun=2.0,elevation=25,azimuth=110,exposure=0.),
 'noon':dict(world='#A9D6F0',strength=.8,sun=3.,elevation=60,azimuth=180,exposure=0.),
 'sunset':dict(world='#F28C5B',strength=.28,sun=1.1,elevation=6,azimuth=250,exposure=-.3),
 'night':dict(world='#121A33',strength=.08,sun=.12,elevation=30,azimuth=40,exposure=-.5),
}
def rgba(h):
 c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)+(1.,)
def apply_preset(name='noon'):
 p=PRESETS[name];scene=bpy.context.scene
 world=bpy.data.worlds.get(PREFIX+'World') or bpy.data.worlds.new(PREFIX+'World');world.use_nodes=True;scene.world=world
 bg=world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=rgba(p['world']);bg.inputs['Strength'].default_value=p['strength']
 lamp=bpy.data.objects.get(PREFIX+'Sun')
 if lamp is None:
  data=bpy.data.lights.new(PREFIX+'Sun','SUN');lamp=bpy.data.objects.new(PREFIX+'Sun',data);scene.collection.objects.link(lamp)
 lamp.data.energy=p['sun'];lamp.data.angle=math.radians(5)
 lamp.rotation_euler=(math.radians(90-p['elevation']),0,math.radians(p['azimuth']))
 scene.view_settings.exposure=p['exposure'];scene.render.fps=24
 return p
def material():
 m=bpy.data.materials.get('M_'+ASSET_NAME+'_Effect') or bpy.data.materials.new('M_'+ASSET_NAME+'_Effect');m.use_nodes=True
 nodes=m.node_tree.nodes;nodes.clear();links=m.node_tree.links
 out=nodes.new('ShaderNodeOutputMaterial');out.location=(650,0)
 if ASSET_ID=='FX01':
  tex=nodes.new('ShaderNodeTexCoord');tex.location=(-750,0)
  mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='ADD';mapping.location=(-560,0)
  links.new(tex.outputs['Object'],mapping.inputs[0]);mapping.inputs[1].driver_add('default_value',1).driver.expression='-frame/24*0.12'
  wave=nodes.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=1.8;wave.inputs['Distortion'].default_value=2.;wave.location=(-350,80)
  noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.5;noise.location=(-350,-150)
  links.new(mapping.outputs[0],wave.inputs['Vector']);links.new(mapping.outputs[0],noise.inputs['Vector'])
  ramp=nodes.new('ShaderNodeValToRGB');ramp.location=(-100,100);ramp.color_ramp.elements[0].color=rgba('#0E4C77');ramp.color_ramp.elements[1].color=rgba('#3FA7B5');links.new(noise.outputs['Fac'],ramp.inputs[0])
  bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.04;bump.location=(100,-120);links.new(wave.outputs['Fac'],bump.inputs['Height'])
  bs=nodes.new('ShaderNodeBsdfPrincipled');bs.location=(350,80);bs.inputs['Roughness'].default_value=.22;bs.inputs['IOR'].default_value=1.33;bs.inputs['Transmission Weight'].default_value=.15
  links.new(ramp.outputs['Color'],bs.inputs['Base Color']);links.new(bump.outputs['Normal'],bs.inputs['Normal']);links.new(bs.outputs[0],out.inputs['Surface'])
 elif ASSET_ID=='FX03':
  tex=nodes.new('ShaderNodeTexCoord');tex.location=(-700,0)
  vector=nodes.new('ShaderNodeVectorMath');vector.operation='ADD';vector.location=(-500,0);links.new(tex.outputs['Object'],vector.inputs[0]);vector.inputs[1].driver_add('default_value',2).driver.expression='-frame/24*0.08'
  noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=12;noise.location=(-300,0);links.new(vector.outputs[0],noise.inputs['Vector'])
  ramp=nodes.new('ShaderNodeValToRGB');ramp.location=(-100,0);ramp.color_ramp.elements[0].position=.4;ramp.color_ramp.elements[0].color=(0,0,0,1);ramp.color_ramp.elements[1].position=.7;ramp.color_ramp.elements[1].color=(.08,.08,.08,1);links.new(noise.outputs['Fac'],ramp.inputs[0])
  volume=nodes.new('ShaderNodeVolumePrincipled');volume.location=(300,0);volume.inputs['Color'].default_value=rgba('#F2EFE6');volume.inputs['Anisotropy'].default_value=.2;links.new(ramp.outputs['Color'],volume.inputs['Density']);links.new(volume.outputs[0],out.inputs['Volume'])
 else:
  bs=nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=rgba('#F2EFE6');links.new(bs.outputs[0],out.inputs['Surface'])
 return m
def setup():
 scene=bpy.context.scene;scene.render.fps=24
 material();apply_preset('noon' if ASSET_ID!='FX03' else 'morning')
 if ASSET_ID=='FX04':
  scene.use_nodes=True;n=scene.node_tree.nodes;n.clear();ln=scene.node_tree.links
  layer=n.new('CompositorNodeRLayers');image=n.new('CompositorNodeImage');alpha=n.new('CompositorNodeAlphaOver');out=n.new('CompositorNodeComposite')
  image.label='Insert rendered cards.svg as transparent PNG';alpha.inputs[0].default_value=1.
  ln.new(layer.outputs['Image'],alpha.inputs[1]);ln.new(image.outputs['Image'],alpha.inputs[2]);ln.new(alpha.outputs[0],out.inputs[0])
  layer.location=(-300,100);image.location=(-300,-100);alpha.location=(0,100);out.location=(250,100)
 return PREFIX
if __name__=='__main__':setup()
