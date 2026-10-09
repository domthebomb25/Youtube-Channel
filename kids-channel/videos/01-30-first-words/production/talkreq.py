import json,sys,subprocess,math
m=json.load(open('manifest.json')); names=json.load(open('image_index.json')); jobs=json.load(open('img_jobs.json'))
vj=json.load(open('voice_job_ids.json')); L={l["id"]:l["text"] for l in json.load(open('../voice-lines.json'))}
extra=json.load(open('voice_extra.json')) if __import__('os').path.exists('voice_extra.json') else {}
def dur(i): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'../voice-lines/line-{i:03d}.mp3']))
out=[]
for s in sys.argv[1:]:
    i=int(s); frame="P_"+m["talk_frame"][str(i)]; img=jobs[str(names.index(frame))]
    aud=extra.get(str(i)) or vj[str(i)]
    d=min(15,max(5,math.ceil(dur(i)*1.08+0.3)))
    t=L[i]
    p=("Recreate the reference image exactly as the opening frame: the same animated preschool teacher, same pose, same item, same playroom. "
       "She talks directly to the camera, lip-syncing exactly to the provided voice audio, with clear, exaggerated, easy-to-read mouth shapes for a toddler speech lesson: "
       "lips press fully together on every m, b and p sound, mouth opens wide on 'ah' and rounds on 'oo'. Warm, playful, encouraging expressions and small natural gestures with the item. "
       "She keeps eye contact with the lens. Locked-off steady camera: no zoom, no push-in, no camera movement. Smooth stylized 3D animation, consistent face, hair, headband, apron and hands, five fingers. "
       f"She says: \"{t}\"")
    out.append({"index":i,"params":{"model":"minimax_h3_max","aspect_ratio":"16:9","duration":d,"resolution":"768p","use_unlim":False,"declined_preset_id":"24bae836-2c4a-48e0-89b6-49fcc0b21612","medias":[{"value":img,"role":"image_references"},{"value":aud,"role":"audio_references"}],"prompt":p}})
print(json.dumps(out)); print(sum(o["params"]["duration"] for o in out)*2.5, file=sys.stderr)
