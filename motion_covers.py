"""Compose one short cinemagraph for each case header, in the cover's own coordinates."""
from pathlib import Path
from math import cos, pi, sin

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import distance_transform_edt, map_coordinates

ASSETS = Path(__file__).parent / 'dist/assets'
FRAMES = 40
DURATION = 80
FILES = {
    'cad-hero-rect.jpeg': (620, 470),
    'reg-hero-rect.jpeg': (700, 391),
    'kom-hero-rect.jpeg': (700, 382),
    'claro-hero.webp': (666, 470),
    'essana-hero.webp': (700, 467),
    'essana-web-cover.webp': (700, 354),
}

def smooth(x):
    v = min(1., max(0., x))
    return v * v * (3 - 2 * v)

def action(t, begin, reached, leave, end):
    return smooth((t - begin)/(reached-begin)) * (1 - smooth((t-leave)/(end-leave)))

def layer_mask(size, points):
    mask = Image.new('L', size)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask

def masked_joint(image, points, pivot, feather):
    """Keep the pivot fixed; move the limb as one piece, with falloff outside its silhouette."""
    mask = layer_mask(image.size, points)
    distances = distance_transform_edt(np.array(mask) == 0)
    weight = np.exp(-.5 * (distances/feather)**2)
    ys, xs = np.indices(weight.shape)
    px, py = pivot
    rgb = np.asarray(image)
    def pose(angle):
        if abs(angle)<.00001:
            return image.copy()
        a = angle * weight
        xx = px+(xs-px)*np.cos(a)+(ys-py)*np.sin(a)
        yy = py-(xs-px)*np.sin(a)+(ys-py)*np.cos(a)
        active = distances < 4*feather
        coords = np.stack([yy[active],xx[active]])
        pixels = rgb.copy()
        for c in range(3):
            pixels[:,:,c][active] = map_coordinates(rgb[:,:,c],coords,order=1,mode='nearest')
        return Image.fromarray(pixels)
    return pose

def scanning(image):
    outline = [(119,320),(151,315),(200,300),(222,291),(251,280),(273,273),
               (286,273),(294,277),(320,277),(355,283),(357,291),(352,300),
               (341,305),(318,305),(310,300),(295,307),(279,322),(269,334),
               (255,335),(229,329),(212,337),(157,363),(146,372),(124,380),
               (111,375),(107,350)]
    pose = masked_joint(image,outline,(123,348),7)
    def frame(t):
        approach = action(t,.01,.37,.56,.87)
        # Aiming happens at the elbow. The item and opposite hand stay still.
        angle = .045*approach-.012*action(t,.75,.9,.90,1)
        result = pose(angle)
        beam = action(t,.32,.38,.48,.55)
        if beam:
            dx,dy = 354-123,294-348
            start = (123+dx*cos(angle)-dy*sin(angle),348+dx*sin(angle)+dy*cos(angle))
            light = Image.new('RGBA', image.size)
            draw = ImageDraw.Draw(light)
            draw.polygon((start,(384,312),(386,315)),fill=(255,42,32,int(48*beam)))
            draw.line((379,313,402,307), fill=(255,77,59,int(210*beam)),width=1)
            result = Image.alpha_composite(result.convert('RGBA'),light).convert('RGB')
        return result
    return frame

def pointer(draw,x,y,scale=1):
    points=[(0,0),(0,10),(3,7),(6,11),(8,10),(5,6),(9,6)]
    draw.polygon([(x+a*scale,y+b*scale) for a,b in points], fill='white',outline='#262634')

def typing(image):
    pose = masked_joint(image, [(149,390),(157,345),(175,311),(187,295),(202,294),
                              (206,300),(219,294),(229,297),(234,304),(244,303),(257,319),
                              (247,335),(225,360),(211,390)],(169,389),6)
    def frame(t):
        press = action(t,.14,.28,.29,.42) + .8*action(t,.49,.59,.6,.74)
        result = pose(.024*press)
        active = action(t,.01,.12,.79,.98)
        if active:
            overlay = Image.new('RGBA',image.size)
            d = ImageDraw.Draw(overlay)
            select = action(t,.48,.53,.74,.82)
            if select:
                d.rounded_rectangle((176,238,195,246),radius=1,outline=(150,213,255,int(170*select)),width=1)
            progress=smooth((t-.07)/.40)
            pointer(d,200-14*progress,251-10*progress,.76)
            result=Image.blend(result,Image.alpha_composite(result.convert('RGBA'),overlay).convert('RGB'),active)
        return result
    return frame

def chart(image):
    # Animate actual columns, retaining the laptop perspective and dashboard axes.
    bars=[(328,247,336,260),(341,254,349,260),(354,251,362,258),
          (366,237,375,257),(379,236,388,255),(391,232,400,254),(403,228,413,253)]
    def frame(t):
        result=image.copy()
        for i,(x,y,r,b) in enumerate(bars):
            u=action(t,.01+i*.018,.28+i*.018,.32+i*.018,.79+i*.02)
            if u<=0: continue
            band=image.crop((x,y,r,b))
            # Extract only blue/gray ink, so grid lines behind the bars remain aligned.
            a=np.asarray(band,dtype=float)
            color=np.max(a,axis=2)-np.min(a,axis=2)
            ink=(color>17)&(a[:,:,0]<175)
            if i==0: ink|=(a[:,:,0]<165)&(a[:,:,0]>70)
            alpha=Image.fromarray(np.uint8(ink)*255)
            # Sample an empty column inside the same plot to clear the entire old bar.
            src=image.crop((322,y-1,323,b)).resize((r-x+2,b-y+1))
            result.paste(src,(x-1,y-1))
            h=max(2,round((b-y)*(1-.57*u)))
            result.paste(band.resize((r-x,h),Image.Resampling.LANCZOS),(x,b-h),
                         alpha.resize((r-x,h),Image.Resampling.LANCZOS))
        return result
    return frame

def offer_carousel(image):
    # Pull the horizontal offer strip a short distance and let it settle back.
    region=(146,205,535,390)
    strip=image.crop(region)
    offer=Image.open(ASSETS/'claro-home-after.webp').convert('RGB')
    # Use an actual Claro campaign graphic from the same project for the next slide.
    next_card=offer.crop((23,2023,568,2320))
    extended=Image.new('RGB',(strip.width*2,strip.height),strip.getpixel((0,0)))
    extended.paste(strip,(0,0))
    extended.paste(next_card.resize((362,172),Image.Resampling.LANCZOS),(strip.width+4,7))
    def frame(t):
        offset=round(65*action(t,.03,.42,.47,.9))
        if not offset:return image.copy()
        result=image.copy()
        result.paste(extended.crop((offset,0,offset+strip.width,strip.height)),region[:2])
        return result
    return frame

def projection(dest,src):
    a=[];b=[]
    for (x,y),(u,v) in zip(dest,src):
        a.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
        b.extend([u,v])
    return np.linalg.solve(a,b)

def book_cover(image):
    # Left edge is the bound spine. Only the upper cover lifts off the page block.
    corners=[(199,128),(536,82),(599,271),(235,326)]
    original_mask=layer_mask(image.size,corners)
    inside=Image.new('RGB',image.size,'#e9e4f1')
    for k in range(3):
        ImageDraw.Draw(inside).line((539+k,84,596+k,272),fill='#c7c1cf')
    base=Image.composite(inside,image,original_mask)
    def frame(t):
        amount=action(t,.01,.44,.5,.98)
        if not amount:return image.copy()
        dest=[corners[0],(536-5*amount,82-13*amount),(599-5*amount,271-16*amount),corners[3]]
        mask=layer_mask(image.size,dest)
        cast=mask.filter(ImageFilter.GaussianBlur(3))
        shadow=Image.blend(base,Image.new('RGB',image.size,'#42334f'),.17*amount)
        result=Image.composite(shadow,base,Image.composite(cast,Image.new('L',image.size),original_mask))
        cover=image.transform(image.size,Image.Transform.PERSPECTIVE,projection(dest,corners),Image.Resampling.BICUBIC)
        result.paste(cover,(0,0),mask.filter(ImageFilter.GaussianBlur(.35)))
        return result
    return frame

def registration(image):
    # The miniature desktop has an actual sign-up button; open the project's registration design.
    dialog=Image.open(ASSETS/'essana-web-registration.webp').convert('RGB')
    dialog=dialog.resize((205,121),Image.Resampling.LANCZOS)
    def frame(t):
        result=image.copy()
        appear=action(t,.41,.54,.72,.87)
        if appear:
            x,y=437,82
            result.paste(Image.blend(image.crop((x,y,x+205,y+121)),dialog,appear),(x,y))
        visible=action(t,.02,.12,.79,.95)
        if visible:
            over=result.copy()
            p=smooth((t-.07)/.33)
            pointer(ImageDraw.Draw(over),541+47*p,126-38*p,.63)
            result=Image.blend(result,over,visible)
        return result
    return frame

RENDERERS=[scanning,typing,chart,offer_carousel,book_cover,registration]
def main():
    for (filename,size),renderer in zip(FILES.items(),RENDERERS):
        image=Image.open(ASSETS/filename).convert('RGB').resize(size,Image.Resampling.LANCZOS)
        make_frame=renderer(image)
        frames=[make_frame(i/(FRAMES-1)) for i in range(FRAMES)]
        path=ASSETS/(Path(filename).stem+'-motion.webp')
        frames[0].save(path,save_all=True,append_images=frames[1:],duration=DURATION,
                       loop=1,quality=86,method=3)
        print(path.name, path.stat().st_size,flush=True)
if __name__=='__main__':
    main()
