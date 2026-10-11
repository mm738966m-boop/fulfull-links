import os, sys, time
from pathlib import Path
env = Path.home()/"Desktop/ユメカネnote自動化/.env"
for line in env.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k,v=line.split("=",1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
from google import genai
from google.genai import types
client=genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
MODEL="nano-banana-pro-preview"
OUT=Path("."); REF=Path.home()/"Desktop/fulfull-seo/drafts/ai-shindan/img/mascot_base.png"
STYLE=("Illustration style: gentle children's-picture-book watercolor with fine ink line art, soft paper texture, pure white background (#FFFFFF), limited palette of teal (#0E7C86), deep teal (#0A5A62), warm gold (#D9A441) and soft grey. No text, no letters, no numbers anywhere in the image. Not anime, not 3D, not glossy, no glow. Calm, warm, trustworthy, slightly humorous. ")
CHAR="Same small teal robot mascot as the reference image (keep its exact design: round body, dot eyes, gentle smile, gold-tipped antenna, holding a small gold abacus). "
def gen(name,prompt,aspect):
    parts=[STYLE+CHAR+prompt, types.Part.from_bytes(data=REF.read_bytes(), mime_type="image/png")]
    for a in range(3):
        try:
            r=client.models.generate_content(model=MODEL, contents=parts, config=types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=aspect)))
            for p in r.candidates[0].content.parts:
                if getattr(p,"inline_data",None) and p.inline_data.data:
                    (OUT/f"{name}.png").write_bytes(p.inline_data.data); print("ok",name,len(p.inline_data.data),flush=True); return
            print("no image",name,flush=True)
        except Exception as e: print("retry",name,a,repr(e)[:160],flush=True); time.sleep(5)
gen("note_hero","Scene: a Japanese woman in her 50s and her mother in her 80s sit at a small kitchen table with two cups of tea, leaning in and talking warmly, the daughter gently holding a single sheet of paper. The mascot sits on the table edge holding a tiny pencil, listening. Wide composition with white space on the left for a headline.","16:9")
gen("note_boxes","Scene: three simple wooden boxes in a row on a table, small to large from left to right, a hand placing a coin into the middle one; the mascot stands beside the boxes pointing at them with its abacus. Clean, airy, lots of white.","16:9")
gen("note_done","Scene: a smartphone on a table with a small paper airplane flying up and out of it toward the upper right, a few gold confetti pieces in the air, the mascot jumping happily with both arms up beside the phone. Celebration, light and joyful.","4:3")
gen("ai_hero","Scene: a cozy small office. A Japanese man in his 30s in a navy jacket sits at a wooden desk, smiling, speaking on the phone and holding a handwritten thank-you card. Around him three copies of the mascot are busy: one carries an envelope, one puts a gold circle sticker on a wall calendar, one types on a small laptop. Wide composition with white space on the left.","16:9")
gen("ai_lanes","Scene: a simple two-lane path drawn on paper, left lane with the mascot walking carrying papers, right lane with a person walking carrying a cup of tea, both lanes meeting at a small door at the end. Minimal, diagram-like, airy.","16:9")
gen("ai_result","Scene: the mascot opening a small shop door from inside and inviting the viewer in with one arm, a warm light from the doorway, a tiny welcome mat. Centered, square.","1:1")
print("DONE",flush=True)
