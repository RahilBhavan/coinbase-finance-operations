from pathlib import Path
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "work" / "video-deps"))
import imageio_ffmpeg

slides = [
 ("Settlement exception desk", ["Synthetic x402 exact workflow on Base Sepolia", "Decision: retain FIFO for the initial scenario", "65 events | 16 incidents | 0 control failures"]),
 ("Timeout is not failure", ["Settlement request timed out", "Outcome remains unknown", "Reconcile the original attempt", "Never trigger another charge automatically"]),
 ("Late payment, missing delivery", ["Late evidence attaches to the original attempt", "Payment state: observed", "Delivery state: prepared", "Recover the persisted report; do not charge again"]),
 ("Refund reservation control", ["Approval reserves refundable balance", "Unknown submission keeps the reservation", "Completed plus reserved cannot exceed capture", "Concurrent excess request is blocked"]),
 ("Policy comparison", ["FIFO overdue cases: 6", "Deadline-first overdue cases: 6", "Weighted delay improved, primary count did not", "The 15% adoption gate was not met"]),
 ("Recommendation and limits", ["Keep FIFO as the working baseline", "Test a narrow SLA-window hybrid next", "All data and timings are simulated", "No live wallet, payment, Coinbase system, or savings claim"]),
]
font_paths = ["/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/Helvetica.ttc"]
font_path = next(p for p in font_paths if Path(p).exists())
title_font = ImageFont.truetype(font_path, 48); line_font = ImageFont.truetype(font_path, 34); small_font = ImageFont.truetype(font_path, 22)

def frame(title, lines):
    img=Image.new("RGB",(1280,720),(245,249,252)); d=ImageDraw.Draw(img)
    d.rectangle((0,0,1280,106),fill=(21,58,91)); d.text((70,28),title,font=title_font,fill="white")
    for i,line in enumerate(lines): d.text((100,180+i*105),line,font=line_font,fill=(23,33,43))
    d.text((70,670),"SIMULATED DATA - NO ACTIONS EXECUTED",font=small_font,fill=(88,104,116))
    return img

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe(); silent=root/"work"/"demo-silent.mp4"; final=root/"artifacts"/"demo.mp4"
cmd=[ffmpeg,"-y","-f","rawvideo","-pix_fmt","rgb24","-s","1280x720","-r","1","-i","-","-c:v","libx264","-pix_fmt","yuv420p","-t","180",str(silent)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
for second in range(180): p.stdin.write(frame(*slides[min(second//30,5)]).tobytes())
p.stdin.close(); err=p.stderr.read(); code=p.wait()
if code: raise RuntimeError(err.decode(errors="replace"))

audio=root/"work"/"demo-narration.aiff"
subprocess.run(["/usr/bin/say","-r","145","-f",str(root/"work"/"demo-narration.txt"),"-o",str(audio)],check=True)
subprocess.run([ffmpeg,"-y","-i",str(silent),"-i",str(audio),"-filter_complex","[1:a]apad=pad_dur=180[a]","-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-t","180",str(final)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(root/"outputs"/"demo.mp4").write_bytes(final.read_bytes())
