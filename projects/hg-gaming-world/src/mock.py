R="/home/user/Brand-Design-Skill/projects/hg-gaming-world"
L=f"file://{R}/01-logo"; T=f"file://{R}/03-typography"; P=f"file://{R}/04-patterns"
css=f"""
@font-face{{font-family:HGWD;src:url({T}/font/HGWDisplay-ExtraBold.woff2)}}
*{{box-sizing:border-box}} body{{margin:0;background:#1a1a1f;font-family:Inter;color:#F4F4F8;padding:40px;width:1800px}}
.d{{font-family:HGWD}} .mock{{margin-bottom:40px;position:relative;overflow:hidden}}
.volt{{color:#C6FF33}} .btn{{display:inline-block;background:#C6FF33;color:#0A0A10;font-family:HGWD;border-radius:12px}}
"""
def page(body): return f"<html><head><style>{css}</style></head><body>{body}</body></html>"
M=[]
# 1 Billboard at dusk
M.append(f"""<div class=mock data-name=01-billboard style="width:1700px;height:900px;background:linear-gradient(#141432 0%,#2a1c5a 55%,#3b2470 70%,#0b0b14 70.2%,#0b0b14 100%)">
 <div style="position:absolute;left:0;right:0;bottom:0;height:270px;background:linear-gradient(#16161d,#0a0a10)"></div>
 <div style="position:absolute;left:300px;top:700px;width:34px;height:300px;background:#2b2b33"></div><div style="position:absolute;left:1360px;top:700px;width:34px;height:300px;background:#2b2b33"></div>
 <div style="position:absolute;left:160px;top:170px;width:1380px;height:530px;background:#0A0A10;border:14px solid #22222a;box-shadow:0 30px 80px #0008;overflow:hidden">
   <img src="{P}/01-extrude-field-indigo.svg" style="position:absolute;right:-120px;top:-40px;width:900px;opacity:1">
   <div style="position:absolute;left:0;top:0;width:640px;height:100%;background:#0A0A10"></div>
   <img src="{T}/lockups/hgw-stack3-on-dark.svg" style="position:absolute;left:56px;top:56px;height:190px">
   <div class=d style="position:absolute;left:58px;top:300px;font-size:76px;line-height:.98;width:700px">Level up<br>your setup.</div>
   <div class=btn style="position:absolute;left:58px;top:455px;font-size:26px;padding:12px 22px">Buy · Repair · Refuel</div>
 </div>
 <div style="position:absolute;left:160px;top:156px;width:1380px;height:14px;background:linear-gradient(90deg,transparent,#fff3,transparent)"></div></div>""")
# 2 Bus shelter poster
M.append(f"""<div class=mock data-name=02-bus-shelter style="width:820px;height:1150px;background:#202028;padding:40px">
 <div style="position:relative;width:740px;height:1060px;background:#0A0A10;border:16px solid #3a3a44;overflow:hidden">
  <img src="{P}/04-controller-city-indigo.svg" style="position:absolute;bottom:-40px;left:-300px;width:1400px">
  <img src="{L}/hg-primary.svg" style="position:absolute;left:50px;top:60px;width:300px">
  <div class=d style="position:absolute;left:52px;top:330px;font-size:92px;line-height:.95">Repairs<br>in <span class=volt>48h.</span></div>
  <div style="position:absolute;left:54px;top:540px;font-size:22px;color:#cfcfe0;width:520px;line-height:1.45">Controllers, consoles, handhelds. Drop it off, track it live, play again by the weekend.</div>
  <img src="{T}/lockups/hgw-line-white.svg" style="position:absolute;left:54px;bottom:46px;height:48px">
 </div></div>""")
# 3 Website hero
M.append(f"""<div class=mock data-name=03-website style="width:1700px;height:1000px;background:#2a2a33;padding:40px 60px">
 <div style="background:#d9d9e2;height:40px;border-radius:14px 14px 0 0;display:flex;align-items:center;gap:8px;padding:0 16px"><i style="width:12px;height:12px;border-radius:9px;background:#ff5f57"></i><i style="width:12px;height:12px;border-radius:9px;background:#febc2e"></i><i style="width:12px;height:12px;border-radius:9px;background:#28c840"></i><span style="margin-left:20px;background:#fff;color:#555;border-radius:8px;padding:4px 14px;font-size:13px;width:520px">happygamingworld.com</span></div>
 <div style="position:relative;background:#0A0A10;height:880px;overflow:hidden">
  <div style="display:flex;align-items:center;gap:34px;padding:22px 44px;border-bottom:1px solid #24242F"><img src="{T}/lockups/hgw-hg-world-on-dark.svg" style="height:40px"><span style="color:#A3A3B3">Consoles</span><span style="color:#A3A3B3">Accessories</span><span style="color:#A3A3B3">Repairs</span><span style="color:#A3A3B3">Top-ups</span><span style="margin-left:auto;color:#8C83FF">Sign in</span><span class=btn style="font-size:16px;padding:10px 18px">Cart · 2</span></div>
  <img src="{P}/02-w-chain-indigo.svg" style="position:absolute;right:-200px;top:90px;width:1100px">
  <div style="position:absolute;right:0;top:90px;width:900px;height:800px;background:linear-gradient(90deg,#0A0A10 0%,#0A0A1000 40%)"></div>
  <img src="{L}/hg-primary.svg" style="position:absolute;right:170px;top:220px;width:520px">
  <div class=d style="position:absolute;left:44px;top:180px;font-size:110px;line-height:.93">The whole<br>gaming world.</div>
  <div style="position:absolute;left:48px;top:420px;font-size:21px;color:#A3A3B3;width:560px;line-height:1.5">Buy consoles and accessories, book a repair, top up your wallet — all in one place.</div>
  <div style="position:absolute;left:48px;top:510px;display:flex;gap:12px"><span class=btn style="font-size:20px;padding:14px 24px">Shop consoles</span><span style="font-family:HGWD;font-size:20px;padding:14px 24px;border-radius:12px;background:#2E1FF5">Book a repair</span></div>
  <div style="position:absolute;left:44px;right:44px;bottom:40px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px">
   {''.join(f"<div style='background:#15151E;border:1px solid #24242F;border-radius:14px;padding:18px'><div class=d style='font-size:24px'>{a}</div><div style='color:#A3A3B3;font-size:14px;margin-top:6px'>{b}</div></div>" for a,b in [("Buy","Consoles, games, gear"),("Repair","48h turnaround"),("Refuel","Wallet top-ups, +5%"),("Play","Events & tournaments")])}
  </div></div></div>""")
# 4 Phones
def phone(inner, bg="#0A0A10"):
    return f"<div style='width:360px;height:740px;border-radius:52px;background:#111;padding:14px;box-shadow:0 30px 60px #0008'><div style='position:relative;width:100%;height:100%;border-radius:40px;overflow:hidden;background:{bg}'>{inner}</div></div>"
app=f"""<div style='padding:54px 20px 0'><img src='{T}/lockups/hgw-hg-world-on-dark.svg' style='height:30px'></div>
<div style='margin:18px 16px;height:200px;border-radius:20px;overflow:hidden;position:relative;background:#2E1FF5'><img src='{P}/13-dpad-lattice-indigo.svg' style='position:absolute;width:560px;left:-40px;top:-30px'><div class=d style='position:absolute;left:18px;top:22px;font-size:34px;line-height:1'>Weekend<br>drop</div><span class=btn style='position:absolute;left:18px;bottom:18px;font-size:15px;padding:8px 14px'>PS5 Slim −12%</span></div>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 16px'>{''.join(f"<div style='background:#15151E;border-radius:16px;padding:14px;height:96px'><div class=d style='font-size:20px'>{a}</div><div style='color:#A3A3B3;font-size:12px'>{b}</div></div>" for a,b in [("Buy","New & pre-owned"),("Repair","Track your fix"),("Refuel","Top up wallet"),("Play","Events near you")])}</div>"""
story=f"""<img src='{P}/14-hgw-monogram-indigo.svg' style='position:absolute;height:100%;left:-300px'><div style='position:absolute;inset:0;background:linear-gradient(#2E1FF500 40%,#0A0A10 85%)'></div>
<img src='{L}/hg-primary.svg' style='position:absolute;left:24px;top:70px;width:170px'><div class=d style='position:absolute;left:24px;bottom:150px;font-size:52px;line-height:.95'>Top up.<br><span class=volt>+5% bonus.</span></div><span class=btn style='position:absolute;left:24px;right:24px;bottom:56px;text-align:center;font-size:20px;padding:14px'>Swipe up to refuel</span>"""
home=f"""<img src='{P}/06-grip-flow-indigo.svg' style='position:absolute;height:100%;left:-250px'>
<div style='position:absolute;left:14px;right:14px;top:70px;background:#ffffffe6;color:#0A0A10;border-radius:20px;padding:12px;display:flex;gap:10px;align-items:center'><img src='{L}/hg-app-icon.svg' style='width:40px;border-radius:10px'><div><b style='font-size:13px'>HG World</b><div style='font-size:13px'>Your controller is fixed. Pick it up today 🎮</div></div></div>
<div style='position:absolute;left:30px;bottom:120px;display:grid;grid-template-columns:repeat(4,64px);gap:18px'>{''.join("<div style='width:64px;height:64px;border-radius:16px;background:#ffffff33'></div>" for _ in range(7))}<img src='{L}/hg-app-icon.svg' style='width:64px;border-radius:16px'></div>"""
M.append(f"<div class=mock data-name=04-mobile style='width:1300px;height:820px;background:#d9d9e4;display:flex;gap:60px;justify-content:center;align-items:center'>{phone(app)}{phone(story)}{phone(home)}</div>")
# 5 Display banners
M.append(f"""<div class=mock data-name=05-display-banners style="width:1300px;height:620px;background:#E8E8EE;padding:40px;color:#0A0A10">
 <div style="position:relative;width:970px;height:90px;background:#0A0A10;overflow:hidden;border-radius:4px"><img src="{P}/03-speed-lines-void.svg" style="position:absolute;width:970px;top:-200px;opacity:.9"><img src="{L}/hg-primary.svg" style="position:absolute;left:16px;top:8px;height:74px"><div class=d style="position:absolute;left:140px;top:22px;font-size:40px;color:#fff">Repairs in 48h.</div><span class=btn style="position:absolute;right:20px;top:22px;font-size:20px;padding:10px 18px">Book now</span></div>
 <div style="font-size:12px;color:#666;margin:6px 0 24px">Billboard banner 970×90</div>
 <div style="display:flex;gap:40px;align-items:flex-start">
  <div><div style="position:relative;width:300px;height:250px;background:#2E1FF5;overflow:hidden;border-radius:4px"><img src="{P}/10-button-fractal-indigo.svg" style="position:absolute;width:600px;left:90px;top:40px"><img src="{L}/hg-one-colour-white.svg" style="position:absolute;left:18px;top:18px;width:90px"><div class=d style="position:absolute;left:18px;top:110px;font-size:34px;color:#fff;line-height:1">Weekend<br>drop</div><span class=btn style="position:absolute;left:18px;bottom:18px;font-size:16px;padding:9px 14px">Shop −12%</span></div><div style="font-size:12px;color:#666;margin-top:6px">MPU 300×250</div></div>
  <div><div style="position:relative;width:300px;height:600px;background:#0A0A10;overflow:hidden;border-radius:4px"><img src="{P}/04-controller-city-void.svg" style="position:absolute;height:600px;left:-500px"><img src="{L}/hg-primary.svg" style="position:absolute;left:24px;top:28px;width:150px"><div class=d style="position:absolute;left:24px;top:170px;font-size:44px;color:#fff;line-height:.95">The whole gaming world.</div><span class=btn style="position:absolute;left:24px;bottom:28px;font-size:18px;padding:12px 18px">Explore</span></div><div style="font-size:12px;color:#666;margin-top:6px">Half page 300×600</div></div>
  <div><div style="position:relative;width:320px;height:50px;background:#C6FF33;overflow:hidden;border-radius:4px"><img src="{L}/hg-one-colour-black.svg" style="position:absolute;left:8px;top:5px;height:40px"><div class=d style="position:absolute;left:66px;top:12px;font-size:21px;color:#0A0A10">+5% on every top-up</div></div><div style="font-size:12px;color:#666;margin-top:6px">Mobile banner 320×50</div>
   <div style="position:relative;width:320px;height:100px;background:#0A0A10;overflow:hidden;border-radius:4px;margin-top:24px"><img src="{P}/15-ticker-void.svg" style="position:absolute;width:640px;top:-60px"><img src="{T}/lockups/hgw-hg-world-on-dark.svg" style="position:absolute;left:14px;top:30px;height:40px"></div><div style="font-size:12px;color:#666;margin-top:6px">Large mobile 320×100</div></div>
 </div></div>""")
# 6 Packing tape + box (CSS 3D)
tape_unit=f"<span style='display:inline-flex;align-items:center;gap:18px;margin-right:36px'><img src='{L}/hg-one-colour-white.svg' style='height:44px'><span class=d style='font-size:30px;color:#fff'>HAPPY GAMING WORLD</span><span class=d style='font-size:30px;color:#C6FF33'>◆ HANDLE WITH JOY</span></span>"
tape_unit2=f"<span style='display:inline-flex;align-items:center;gap:18px;margin-right:36px'><img src='{L}/hg-one-colour-black.svg' style='height:44px'><span class=d style='font-size:30px;color:#0A0A10'>HGW · BUY · REPAIR · REFUEL · PLAY</span></span>"
M.append(f"""<div class=mock data-name=06-packing-tape style="width:1700px;height:1000px;background:radial-gradient(circle at 40% 30%,#3a3a44,#121216)">
 <div style="position:absolute;left:330px;top:160px;width:900px;height:700px;perspective:1800px">
  <div style="position:absolute;inset:0;transform:rotateX(55deg) rotateZ(-28deg);transform-style:preserve-3d">
   <div style="position:absolute;left:100px;top:40px;width:640px;height:480px;background:linear-gradient(135deg,#c39a6b,#a77c4f);box-shadow:30px 60px 80px #0009"></div>
   <div style="position:absolute;left:100px;top:245px;width:640px;height:70px;background:#2E1FF5;overflow:hidden;white-space:nowrap;padding-top:12px">{tape_unit*3}</div>
   <div style="position:absolute;left:385px;top:40px;width:70px;height:480px;background:#C6FF33;overflow:hidden"></div>
  </div></div>
 <div style="position:absolute;left:60px;top:80px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,#1a1a22 0 28%,#2E1FF5 29% 70%,#2216C4 71%);box-shadow:20px 30px 50px #0009"></div>
 <div style="position:absolute;left:220px;top:300px;width:1500px;height:70px;background:#2E1FF5;transform:rotate(14deg);transform-origin:left;overflow:hidden;white-space:nowrap;padding-top:12px;box-shadow:0 10px 30px #0007">{tape_unit*4}</div>
 <div style="position:absolute;left:100px;top:760px;width:1600px;height:70px;background:#C6FF33;transform:rotate(-6deg);overflow:hidden;white-space:nowrap;padding-top:12px">{tape_unit2*4}</div>
</div>""")
# 7 Shipping box
BW,BH,BD=560,400,380
M.append(f"""<div class=mock data-name=07-shipping-box style="width:1300px;height:900px;background:radial-gradient(circle at 50% 40%,#f2f1ec,#d8d6cf)">
 <div style="position:absolute;left:370px;top:250px;width:{BW}px;height:{BH}px;perspective:2000px">
 <div style="position:absolute;width:{BW}px;height:{BH}px;transform-style:preserve-3d;transform:rotateX(-22deg) rotateY(-34deg)">
  <div style="position:absolute;width:{BW}px;height:{BH}px;background:#0A0A10;transform:translateZ({BD/2}px);overflow:hidden"><img src="{P}/02-w-chain-void.svg" style="position:absolute;width:900px;top:-60px"><img src="{T}/lockups/hgw-stack3-on-dark.svg" style="position:absolute;left:44px;top:130px;height:160px"><div style="position:absolute;left:{BW/2-35}px;top:0;width:70px;height:70px;background:#2E1FF5"></div></div>
  <div style="position:absolute;width:{BD}px;height:{BH}px;left:{(BW-BD)/2}px;background:#15151E;transform:rotateY(90deg) translateZ({BW/2}px);overflow:hidden"><img src="{P}/17-ecosystem-tiles-void.svg" style="position:absolute;width:760px;top:-40px"><div style="position:absolute;left:{BD/2-35}px;top:0;width:70px;height:70px;background:#2216C4"></div></div>
  <div style="position:absolute;width:{BW}px;height:{BD}px;top:{(BH-BD)/2}px;background:#1e1e28;transform:rotateX(90deg) translateZ({BH/2}px)"><div style="position:absolute;left:{BW/2-35}px;top:0;width:70px;height:{BD}px;background:#2E1FF5"></div><img src="{L}/hg-one-colour-white.svg" style="position:absolute;left:40px;top:40px;width:150px;opacity:.9"></div>
 </div></div>
 <div style="position:absolute;left:330px;top:720px;width:700px;height:60px;border-radius:50%;background:#0003;filter:blur(18px)"></div></div>""")
# 8 Shopping bag
M.append(f"""<div class=mock data-name=08-shopping-bag style="width:1300px;height:900px;background:linear-gradient(#ECEBF3,#d6d5e0);display:flex;gap:80px;justify-content:center;align-items:flex-end;padding-bottom:80px">
 {''.join(f'''<div style="position:relative;width:{w}px;height:{h}px;background:{bg};border-radius:6px 6px 10px 10px;box-shadow:24px 30px 50px #0004;overflow:hidden"><img src="{P}/{pat}.svg" style="position:absolute;width:{w*2.4}px;left:-{w*0.4}px;top:{h*0.45}px"><div style="position:absolute;left:0;right:0;top:0;height:{h*0.45}px;background:{bg}"></div><img src="{lock}" style="position:absolute;left:{w*0.12}px;top:{h*0.12}px;width:{w*0.62}px"><div style="position:absolute;left:{w*0.3}px;top:-{w*0.18}px;width:{w*0.4}px;height:{w*0.36}px;border:12px solid #0A0A10;border-radius:50%"></div></div>''' for w,h,bg,pat,lock in [(380,520,"#0A0A10","01-extrude-field-indigo",f"{L}/hg-primary.svg"),(300,420,"#2E1FF5","05-grip-weave-indigo",f"{T}/lockups/hgw-hgw-white.svg"),(240,330,"#C6FF33","13-dpad-lattice-volt",f"{L}/hg-one-colour-black.svg")])}
</div>""")
# 9 Store fascia at night
M.append(f"""<div class=mock data-name=09-store-sign style="width:1700px;height:900px;background:linear-gradient(#0b0b18,#141428 60%,#1b1b24 60%,#0e0e12)">
 <div style="position:absolute;left:120px;top:120px;width:1460px;height:200px;background:#0A0A10;border:10px solid #2a2a33;box-shadow:0 0 120px #2E1FF566;display:flex;align-items:center;padding:0 60px;gap:60px">
  <img src="{T}/lockups/hgw-line-on-dark.svg" style="height:120px;filter:drop-shadow(0 0 18px #5E52FFaa)"><span class=d style="margin-left:auto;font-size:34px;color:#C6FF33;text-shadow:0 0 20px #C6FF3388">OPEN · REPAIRS INSIDE</span></div>
 <div style="position:absolute;left:120px;top:330px;width:1460px;height:420px;background:linear-gradient(#22223a,#111118);border:10px solid #2a2a33;overflow:hidden">
  <img src="{P}/04-controller-city-indigo.svg" style="position:absolute;width:900px;left:-40px;bottom:-120px;opacity:.85">
  <div style="position:absolute;right:120px;top:40px;width:380px;height:380px;background:#0A0A10;border:6px solid #2a2a33;display:flex;align-items:center;justify-content:center"><img src="{L}/hg-primary.svg" style="width:300px;filter:drop-shadow(0 0 30px #2E1FF5)"></div>
  <div style="position:absolute;left:520px;top:0;width:10px;height:100%;background:#2a2a33"></div></div>
 <div style="position:absolute;left:1520px;top:330px;width:140px;height:140px;background:#2E1FF5;border-radius:12px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px #2E1FF5"><img src="{L}/hg-small-one-colour-white.svg" style="width:110px"></div>
</div>""")
# 10 Staff tee
tee="M140 40 L230 10 Q300 60 370 10 L460 40 L560 150 L480 220 L440 180 L440 560 L160 560 L160 180 L120 220 L40 150 Z"
M.append(f"""<div class=mock data-name=10-staff-tee style="width:1300px;height:760px;background:#E8E8EE;display:flex;gap:60px;justify-content:center;align-items:center">
 {''.join(f'''<div style="position:relative;width:600px;height:600px"><svg viewBox="0 0 600 600" width="600" height="600" style="position:absolute;filter:drop-shadow(10px 20px 24px #0003)"><path d="{tee}" fill="{c}"/></svg>{inner}</div>''' for c,inner in [("#0A0A10",f"<img src='{L}/hg-primary.svg' style='position:absolute;left:330px;top:120px;width:80px'>"),("#0A0A10",f"<img src='{T}/lockups/hgw-stack3-on-dark.svg' style='position:absolute;left:180px;top:140px;width:240px'><div class=d style='position:absolute;left:180px;top:330px;font-size:30px;color:#C6FF33'>REPAIR CREW</div>")])}
</div>""")
# 11 Business cards
M.append(f"""<div class=mock data-name=11-business-cards style="width:1300px;height:760px;background:#d8d8e2">
 <div style="position:absolute;left:150px;top:140px;width:560px;height:320px;border-radius:14px;background:#0A0A10;transform:rotate(-8deg);box-shadow:20px 30px 40px #0005;overflow:hidden"><img src="{P}/02-w-chain-void.svg" style="position:absolute;width:800px;top:-60px;opacity:.9"><img src="{T}/lockups/hgw-stack3-on-dark.svg" style="position:absolute;left:44px;top:86px;height:150px"></div>
 <div style="position:absolute;left:600px;top:280px;width:560px;height:320px;border-radius:14px;background:#F4F4F8;transform:rotate(5deg);box-shadow:20px 30px 40px #0004;color:#0A0A10;padding:40px">
  <img src="{L}/hg-primary.svg" style="position:absolute;right:36px;top:36px;width:110px"><div class=d style="font-size:34px;margin-top:60px">Your Name</div><div style="font-size:15px;color:#55556A">Brand & Product</div>
  <div style="position:absolute;left:40px;bottom:36px;font-size:14px;line-height:1.6;color:#0A0A10">hello@happygamingworld.com<br><span style="color:#2E1FF5">happygamingworld.com</span></div><div style="position:absolute;right:0;bottom:0;width:120px;height:120px;background:#C6FF33;border-radius:120px 0 14px 0"></div></div>
</div>""")
# 12 Gift / top-up cards
M.append(f"""<div class=mock data-name=12-gift-cards style="width:1300px;height:720px;background:#121216">
 {''.join(f'''<div style="position:absolute;left:{x}px;top:{y}px;width:480px;height:302px;border-radius:22px;background:{bg};transform:rotate({r}deg);box-shadow:20px 30px 50px #000a;overflow:hidden"><img src="{P}/{pat}.svg" style="position:absolute;width:780px;left:200px;top:-80px"><img src="{logo}" style="position:absolute;left:28px;top:26px;height:{lh}px"><div class=d style="position:absolute;left:28px;bottom:26px;font-size:42px;color:{fg}">{amt}</div><div style="position:absolute;right:28px;bottom:32px;font-size:14px;color:{fg};opacity:.8">{lab}</div></div>''' for x,y,r,bg,pat,logo,lh,fg,amt,lab in [(120,140,-10,"#2E1FF5","14-hgw-monogram-indigo",f"{T}/lockups/hgw-hg-world-white.svg",40,"#fff","₹2,000","GIFT CARD"),(420,220,4,"#0A0A10","16-letter-crops-void",f"{L}/hg-primary.svg",90,"#fff","₹500","TOP-UP"),(720,120,12,"#C6FF33","08-grip-maze-volt",f"{L}/hg-one-colour-black.svg",90,"#0A0A10","+5%","REFUEL")])}
</div>""")
# 13 Repair tag + stickers
stick=lambda src,w,bg,rot,x,y,rad="50%": f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w}px;border-radius:{rad};background:{bg};border:8px solid #fff;transform:rotate({rot}deg);box-shadow:6px 10px 20px #0004;display:flex;align-items:center;justify-content:center'><img src='{src}' style='width:{w*0.68}px'></div>"
M.append(f"""<div class=mock data-name=13-repair-tag-stickers style="width:1300px;height:760px;background:#d8d8e2">
 <div style="position:absolute;left:110px;top:90px;width:330px;height:580px;background:#F4F4F8;border-radius:24px 24px 18px 18px;box-shadow:16px 24px 40px #0004;color:#0A0A10;overflow:hidden;transform:rotate(-4deg)">
  <div style="position:absolute;left:135px;top:24px;width:60px;height:60px;border-radius:50%;background:#d8d8e2"></div>
  <div style="position:absolute;left:0;right:0;top:110px;height:150px;background:#2E1FF5;overflow:hidden"><img src="{P}/09-arrow-flow-indigo.svg" style="width:600px;margin-left:-120px;margin-top:-100px"></div>
  <img src="{L}/hg-primary.svg" style="position:absolute;left:24px;top:132px;width:130px">
  <div class=d style="position:absolute;left:26px;top:290px;font-size:40px">REPAIR #4821</div>
  <div style="position:absolute;left:28px;top:350px;font-size:15px;line-height:1.7;color:#55556A">DualSense controller<br>Stick drift · Left<br>Ready: Fri, 6 pm</div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:90px;background:#C6FF33;display:flex;align-items:center;padding-left:26px" class=d><span style="font-size:26px">FIXED WITH JOY</span></div></div>
 {stick(f"{L}/hg-primary.svg",240,"#0A0A10",8,560,90)}{stick(f"{L}/hg-one-colour-black.svg",200,"#C6FF33",-12,860,120,"36px")}{stick(f"{L}/hg-one-colour-white.svg",180,"#2E1FF5",6,600,420,"40px")}{stick(f"{T}/lockups/hgw-hgw-black.svg",210,"#F4F4F8",-6,880,400)}
</div>""")
# 14 Social posts
posts=[("#0A0A10","03-speed-lines-void","New drop.<br><span class=volt>Friday 8pm.</span>","#fff"),("#2E1FF5","12-halves-indigo","Two halves.<br>One world.","#fff"),("#C6FF33","15-ticker-volt","Buy. Repair.<br>Refuel. Play.","#0A0A10")]
M.append(f"""<div class=mock data-name=14-social-posts style="width:1700px;height:620px;background:#E8E8EE;display:flex;gap:40px;justify-content:center;align-items:center">
 {''.join(f'''<div style="position:relative;width:500px;height:500px;background:{bg};border-radius:18px;overflow:hidden;box-shadow:0 20px 40px #0003"><img src="{P}/{pat}.svg" style="position:absolute;width:900px;left:-200px;top:300px"><div style="position:absolute;left:0;right:0;top:0;height:330px;background:linear-gradient({bg} 80%,{bg}00)"></div><img src="{L}/{'hg-one-colour-black.svg' if bg=='#C6FF33' else 'hg-primary.svg'}" style="position:absolute;left:30px;top:30px;width:100px"><div class=d style="position:absolute;left:30px;top:150px;font-size:56px;line-height:.98;color:{fg}">{t}</div></div>''' for bg,pat,t,fg in posts)}
</div>""")
open("mock.html","w").write(page("".join(M)))
