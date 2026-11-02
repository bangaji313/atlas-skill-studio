"""Offline install check; generated fixtures only, no provider calls."""
import json, subprocess, sys
from pathlib import Path
runtime=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(runtime))
from tools.tool_registry import registry
root=runtime/'projects'/'atlas-install-smoke'
root.mkdir(parents=True,exist_ok=True)
names=registry.discover()
assert len(names)>=100,names
report={'tool_count':len(names),'steps':[]}
def run(command):
 p=subprocess.run(command,capture_output=True,text=True,check=True)
 return p.stdout
def call(name,params):
 tool=registry.get(name)
 assert tool is not None,name
 result=tool.execute(params)
 assert result.success,(name,result.error)
 report['steps'].append({'tool':name,'artifacts':result.artifacts,'data':result.data})
 return result
clip=root/'synthetic.mp4'
run(['ffmpeg','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=24:duration=4','-f','lavfi','-i','sine=frequency=440:duration=4','-c:v','libx264','-pix_fmt','yuv420p','-g','24','-c:a','aac','-shortest',str(clip)])
call('video_trimmer',{'operation':'cut','input_path':str(clip),'output_path':str(root/'cut.mp4'),'start_seconds':0,'end_seconds':2,'codec':'libx264'})
call('audio_mixer',{'operation':'extract','input_path':str(clip),'output_path':str(root/'tone.wav')})
call('audio_mixer',{'operation':'mix','tracks':[{'path':str(root/'tone.wav'),'role':'music','volume':0.4,'fade_in_seconds':0.2,'fade_out_seconds':0.2}], 'output_path':str(root/'mix.wav'),'normalize':True})
call('video_compose',{'operation':'compose','edit_decisions':{'render_runtime':'ffmpeg','cuts':[{'source':str(root/'cut.mp4'),'in_seconds':0,'out_seconds':2},{'source':str(root/'cut.mp4'),'in_seconds':0,'out_seconds':2}],'metadata':{'compose_target':{'width':640,'height':360,'fps':24}}},'audio_path':str(root/'mix.wav'),'output_path':str(root/'composed.mp4')})
call('color_grade',{'input_path':str(root/'composed.mp4'),'profile':'cinematic_warm','output_path':str(root/'graded.mp4')})
call('subtitle_gen',{'segments':[{'start':0,'end':4,'text':'OpenMontage offline install check'}],'format':'srt','output_path':str(root/'captions.srt')})
call('video_compose',{'operation':'burn_subtitles','input_path':str(root/'graded.mp4'),'subtitle_path':str(root/'captions.srt'),'output_path':str(root/'final.mp4')})
call('frame_sampler',{'input_path':str(root/'final.mp4'),'strategy':'timestamps','timestamps':[0.5,1.5,2.5,3.5],'output_dir':str(root/'frames')})
call('audio_probe',{'input_path':str(root/'final.mp4')})
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(root/'final.mp4')]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (video['width'],video['height'])==(640,360),video
assert any(s['codec_type']=='audio' for s in probe['streams'])
assert 3.8<float(probe['format']['duration'])<4.3,probe['format']
from PIL import Image,ImageStat
frames=list((root/'frames').glob('*.jpg'))
assert len(frames)==4,frames
assert all(sum(ImageStat.Stat(Image.open(p).convert('RGB')).var)>100 for p in frames)
report.update({'passed':True,'output':str(root/'final.mp4'),'probe':probe,'frames':[str(p) for p in frames]})
(root/'result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
