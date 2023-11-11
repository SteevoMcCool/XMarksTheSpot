from math import floor, sin
import os 

levels = [
    {
        "name": "Level1",
        "size": (100,60),
        "charSpeed": {
            "right":1,
            "up":1,
            "left": 1,
            "down": 1,
        },
        "startPoint": (15,15),
        "xPosX": lambda pX,pY: 80,
        "xPosY": lambda pX,pY: floor(60/100 * pX), 
        "enemies": [
            
        ]
    },
    {
        "name": "Level2",
        "size": (100,60),
        "charSpeed": {
            "right":1,
            "up":1,
            "left": 1,
            "down": 1,
        },
        "startPoint": (15,15),
        "xPosX": lambda pX,pY: floor(100 * (pX/100 + pY/60)/2),
        "xPosY": lambda pX,pY: floor(30+ 30* sin(6.283*(pX + pY)/160)), 
        "enemies": [
            
        ]
    },
    {
        "name": "Level3",
        "size": (100,60),
        "charSpeed": {
            "right":1,
            "up":1,
            "left": 1,
            "down": 1,
        },
        "startPoint": (0,8),
        "xPosX": lambda pX,pY: floor(min(99,pY * (2/3) + max(pX-5,0))),
        "xPosY": lambda pX,pY: floor((((pX-50)**2 )/50 * (2/5) + max(pY-20,0))/2) , 
        "enemies": [
            {
                "xPos": lambda pX,pY: floor((95/52)*(pY-8) + 5),
                "yPos": lambda pX,pY: floor((52/95)*(pX-5) + 8)
            }
        ]
    },
]
def getxPos(lv,x,y):
    return (levels[lv]["xPosX"](x,y), levels[lv]["xPosY"](x,y) )

def toName(pX,pY):
    pX,pY = (str(pX),str(pY))
    while (len(pX) <3):
        pX = '0' + pX
    while (len(pY) <3):
        pY = '0' + pY
    return (pX+pY) + ".html"


memo = {}
def solve(level=0,):
    lv = levels[level]
    ret = []
    bad = []
    enem = []
    xR = range(0,lv["size"][0])
    yR = range(0, lv["size"][1])
    for X in xR:
        for Y in yR:
            XX, XY = getxPos(level,X,Y)
            if (XX == X) and (XY == Y):
                ret+= [(XX,XY)]
            if (not XX in xR) or (not XY in yR):
                bad += [([X,XX],[Y,XY])]
            if len(list(filter(lambda e: abs(e["xPos"](X,Y)-X<=1) and abs(e["yPos"](X,Y)-Y<=1),lv["enemies"]))):
                enem+= [(X,Y)]
    return (ret, enem)

def expressSolutions(level):
    (g,b) = solve(level)
    return (list(filter(lambda p: not p in b, g)), list(filter(lambda p:  p in b, g)))

def generateLevel(level):
    lv = levels[level]
    xR = range(0,lv["size"][0])
    sX = len(xR)
    yR = range(0, lv["size"][1])
    sY = len(yR)
    up = lv['charSpeed']['up']
    down = lv['charSpeed']['down']
    left = lv['charSpeed']['left']
    right = lv["charSpeed"]['right']
    dir = lv['name']
    if not os.path.isdir(dir):
        os.makedirs(dir)
    pixelWidth = 800//1.25
    pixelHeight = 480//1.25
    for X in xR:
        pixelX = int(pixelWidth * (X/sX))
        for Y in yR:
            pixelY = int(pixelHeight * (Y/sY))
            xx, xy = getxPos(level,X,Y)
            Xpixel = [ int(pixelWidth * (xx/sX))  ,  int(pixelHeight * (xy/sY))  ]
            Xsource = "../X.png"
            line = ""
            if (xx==X and xy == Y):
                Xsource= "../t.png"
                nextlevelhref = "../home.html"
                if (level + 1) < len(levels):
                    nL = levels[level+1]
                    spName= toName(nL['startPoint'][0],nL['startPoint'][1])
                    nextlevelhref= "../" + nL["name"] + "/" + spName
                line = f"<h3>Solved: ({xx},{xy}). <a href={nextlevelhref}>Next Level?</a></h3>"
            innerHTML = \
            f"""
                    <html><head></head>
                    <body style="background-color: rgb(0,100,175)">
                        <div style="display:flex">
                            <div>
                                <p>Walk</p>
                                &emsp;&nbsp;
                                <a href="{toName(   (X) %sX         ,  (Y- up) %sY      )}"><img src="../u.png" height="20"></a>
                                <br>
                                <a href="{toName(   (X- left) %sX   ,  (Y) %sY          )}"><img src="../l.png" height="20"></a>
                                <a href="{toName(   (X) %sX         ,  (Y+ down) %sY    )}"><img src="../d.png" height="20"></a>
                                <a href="{toName(   (X+right) %sX   ,  (Y) %sY          )}"><img src="../r.png" height="20"></a>
                            </div> 
                            <div style="margin:0px 100px">
                                <p>Jump</p>
                                &emsp;&nbsp;
                                <a href="{toName(   (X) %sX         ,  (Y- up*10) %sY      )}"><img src="../u.png" height="20"></a>
                                <br>
                                <a href="{toName(   (X- left*10) %sX   ,  (Y) %sY          )}"><img src="../l.png" height="20"></a>
                                <a href="{toName(   (X) %sX         ,  (Y+ down*10) %sY    )}"><img src="../d.png" height="20"></a>
                                <a href="{toName(   (X+right*10) %sX   ,  (Y) %sY          )}"><img src="../r.png" height="20"></a>
                            </div> 
                            {line}
                            <a href="../home.html">Home</a>
                        </div>
                        <div style="position:relative;top:0px;border:1px solid black; width:{pixelWidth + 20};height:{pixelHeight + 50}">
                            <img src="{Xsource}" height="50" width="20" style="position:absolute;top:{Xpixel[1]}px;left:{Xpixel[0]}px">
                            {"".join(map(lambda enemy: f"<img src='../b.jpg' height='50' width='20' style='position:absolute;top:{int(pixelHeight * (enemy['yPos'](X,Y)/sY))}px;left:{int(pixelWidth * (enemy['xPos'](X,Y)/sX))}px'>",lv["enemies"]))}
                            <img src="../e.png" height="50" width="20" style="position:absolute;top:{pixelY}px;left:{pixelX}px">
                        </div>
                    </body>
                    </html>
            """
            if len(list(filter(lambda e: abs(e["xPos"](X,Y)-X<=1) and abs(e["yPos"](X,Y)-Y<=1),lv["enemies"]))):
                    innerHTML = f'''
                    <html><head></head>
                    <body style="background-color: rgb(175,0,0)">
                        <h1>You died! <a href={toName(lv['startPoint'][0],lv['startPoint'][1])}>Try again</a></h1>
                        <div style="position:relative;top:0px;border:1px solid black; width:{pixelWidth + 20};height:{pixelHeight + 50}">
                            <img src="{Xsource}" height="50" width="20" style="position:absolute;top:{Xpixel[1]}px;left:{Xpixel[0]}px">
                            {"".join(map(lambda enemy: f"<img src='../b.jpg' height='50' width='20' style='position:absolute;top:{int(pixelHeight * (enemy['yPos'](X,Y)/sY))}px;left:{int(pixelWidth * (enemy['xPos'](X,Y)/sX))}px'>",lv["enemies"]))}
                            <img src="../e.png" height="50" width="20" style="position:absolute;top:{pixelY}px;left:{pixelX}px">
                        </div>
                    </body>
                    </html>
                    '''
            html = open(dir+"/"+toName(X,Y),"w")
            html.write(innerHTML)
            html.close()
        print(dir + ":column " + str(X) + " created!")
    print("\n"+dir + " created Successfully! Hooray!\n")


def generateAllLevels(len=len(levels)-1,string=""):
    if len < 0:
        innerhtml = f"""
                    <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>XMarksTheSpot</title>
            </head>
            <body style="background-color: green;">
                <h1>X Marks The Spot</h1>
                <p>A game coded soley in html! No "style" tags (only some inline styles). NO JS or TS AT ALL! ALL HTML! enjoy :) </p>
                <ul>
                    {string}
                </ul>
            </body>
            </html>
        """
        html = open("home.html","w")
        html.write(innerhtml)
        html.close()
        print("\nHome file updated!\n\nGAME COMPILED SUCCESSFULLY!!!!! :)))))\n")
        return ""
    generateLevel(len)
    nL = levels[len]
    spName= toName(nL['startPoint'][0],nL['startPoint'][1])
    string = f"""<li><a href='./{nL["name"] + "/" + spName}'>{nL['name']}</a></li>""" + string
    generateAllLevels(len-1,string)





generateAllLevels()
print(
expressSolutions(2)
)