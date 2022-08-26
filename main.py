from PIL import Image, ImageFont, ImageDraw
import sys
import getopt
import json
import random

dir_chr = {}
document = []
fonts = []
backpic = None


def creat_doc_pir(width: int, height: int, fonts, backpic, document):
    back = Image.open(backpic).convert('RGBA')
    count = 0
    n = 0
    i = 0
    lenght = 0
    spacing = fonts[0].getlength('有')
    origindocpir = Image.new('RGBA', back.size)
    docpir = origindocpir.copy()
    d = ImageDraw.Draw(docpir)
    for line in document:
        for c in line:
            if((n+spacing*1.15) > height):
                count += 1
                out = Image.alpha_composite(back, docpir)
                out.save('q%s.png' % count)
                docpir = origindocpir.copy()
                d = ImageDraw.Draw(docpir)
                n=0
            if(c == '\n'):
                i = 0
                n += int(spacing*1.5)
                continue
            if(random.randint(1, 100) < 50):
                pr = fonts[0]
            else:
                pr = fonts[1]
            fllow = spacing*(1+random.randint(-15, 15)/100)
            lenght = pr.getlength(c)
            if((i+lenght) < width):
                d.text((i, int(n+fllow)), c, font=pr,
                       fill='black', align='left')
                # docpir.save('q.png')
                i += lenght
            else:
                i = 0
                n += int(spacing*1.5)
                d.text((i, int(n+fllow)), c, font=pr,
                       fill='black', align='left')
                # docpir.save('q.png')
                i += lenght


def read_arg(data, fonts, backpic, document):
    keylist = set(key for key in data.keys())
    temp = set(('doc', 'backwall', 'font',
               'font_size', 'width', 'height', 'line'))
    if(not keylist == temp):
        if(keylist.issuperset(temp)):
            print("Worring:缺少参数 %s，可能导致错误" % str(temp-keylist))
        else:
            print("Worring:无效参数或拼写错误 %s" % str(keylist-temp))

    fontfile = data['font']
    fontsize = data['font_size']
    fonts = [ImageFont.truetype(fontfile, fontsize), ImageFont.truetype(
        fontfile, int(fontsize-fontsize/10))]
    backpic = data['backwall']
    creat_doc_pir(data['width'], data['height'], fonts, backpic, document)
    pass


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "j:")
    except:
        print("Error")
    # for opt, arg in opts:
    with open('conf.json', 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    with open(data['doc'], 'r', encoding='utf8') as input:
        document = input.readlines()
    read_arg(data, fonts, backpic, document)
