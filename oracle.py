import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

NORM=1.5; LAYER=0.87; USABLE=0.5

def size_plan(weight,rating):
    if not pos(weight): return {"error":"the vehicle weight must be above zero"}
    if not pos(rating): return {"error":"the box rating must be above zero"}
    needed=weight*NORM
    margin=rating/needed*100
    if margin>=100: verdict="the box covers the norm"
    elif margin>=80: verdict="the box runs under the norm"
    else: verdict="the box is badly undersized"
    return {"needed":r1(needed),"margin":r1(margin),"verdict":verdict}

def render_size(r,weight,rating):
    return ("At "+jsnum(weight)+" pounds of rig, the one-and-a-half norm wants a winch rated for "+jsnum(r["needed"])
            +" pounds; the "+jsnum(rating)+"-pound box sits at "+jsnum(r["margin"])+"% of that, and "+r["verdict"]+".")

def layer_plan(rating,layers):
    if not pos(rating): return {"error":"the box rating must be above zero"}
    if not num(layers) or layers<1 or layers!=int(layers): return {"error":"the layer count must be a whole number, 1 or more"}
    return {"honest":r1(rating*LAYER**(layers-1))}

def render_layer(r,rating,layers):
    word=" layer up" if layers==1 else " layers up"
    return ("The "+jsnum(rating)+"-pound rating is the first-layer pull; wrapped "+jsnum(layers)
            +word+" the drum, the honest pull is about "+jsnum(r["honest"])+" pounds.")

def draw_plan(pull,rating,full_amps,battery_ah):
    if not pos(pull): return {"error":"the pull must be above zero"}
    if not pos(rating): return {"error":"the box rating must be above zero"}
    if pull>rating: return {"error":"the pull cannot beat the first-layer rating"}
    if not pos(full_amps): return {"error":"the full-load amps must be above zero"}
    if not pos(battery_ah): return {"error":"the battery amp-hours must be above zero"}
    amps=full_amps*pull/rating
    minutes=battery_ah*USABLE/amps*60
    if minutes<2: verdict="the battery fades before the pull ends"
    elif minutes<=5: verdict="one short pull per battery, then a charge"
    else: verdict="the battery outlasts the line speed"
    return {"amps":r1(amps),"minutes":r1(minutes),"verdict":verdict}

def render_draw(r,pull,rating,full_amps,battery_ah):
    return ("Pulling "+jsnum(pull)+" pounds on the "+jsnum(rating)+"-pound winch draws about "+jsnum(r["amps"])
            +" amps; the "+jsnum(battery_ah)+" amp-hour battery gives about "+jsnum(r["minutes"])
            +" honest minutes, and "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="size": r=size_plan(*args); fn=render_size
    elif tool=="layer": r=layer_plan(*args); fn=render_layer
    else: r=draw_plan(*args); fn=render_draw
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(5000,9500),(3500,4500),(6000,8000),(4500,6000),(5500,8000),(7000,9500)]:
    add("size",a)
for a in [(9500,1),(9500,2),(9500,3),(9500,4),(8000,3),(12000,5)]:
    add("layer",a)
for a in [(6000,9500,430,70),(9500,9500,430,70),(3000,9500,430,70),(8000,9500,430,50),(5000,8000,400,80),(7000,12000,460,100)]:
    add("draw",a)
add("size",[0,9500]); add("size",[5000,0])
add("layer",[0,3]); add("layer",[9500,0]); add("layer",[9500,2.5]); add("layer",[9500,"deep"])
add("draw",[0,9500,430,70]); add("draw",[9900,9500,430,70]); add("draw",[6000,9500,0,70]); add("draw",[6000,9500,430,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
