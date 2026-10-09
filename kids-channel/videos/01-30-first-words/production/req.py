import json,sys
m=json.load(open('manifest.json'))
names=json.load(open('image_index.json'))
P=["480ac865-4527-4761-8bd5-0123e9973c0a","01bba7bc-a999-4142-b9ec-bde17d8cdadf"]
out=[]
for i in map(int,sys.argv[1:]):
    n=names[i]; k=n[2:]
    p=m["poppy_frames"][k] if n.startswith("P_") else m["object_frames"][k]
    refs=P if n.startswith("P_") else P[:1]
    out.append({"index":i,"params":{"model":"gpt_image_2_5","aspect_ratio":"16:9","quality":"high","resolution":"1k","use_unlim":False,"medias":[{"value":r,"role":"image_references"} for r in refs],"prompt":p}})
print(json.dumps(out))
