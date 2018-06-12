import requests
import re
import demjson
import os
import math
import time

#pn是页数的关键字

head={
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/66.0.3359.181Safari/537.36"
}
#字典
dic={'w': 'a', 'k': 'b', 'v': 'c', '1': 'd','j': 'e', 'u': 'f', '2': 'g', 'i': 'h','t': 'i', '3': 'j', 'h': 'k', 's': 'l',
     '4': 'm', 'g': 'n', '5': 'o', 'r': 'p','q': 'q', '6': 'r', 'f': 's', 'p': 't','7': 'u', 'e': 'v', 'o': 'w', '8': '1',
     'd': '2', 'n': '3', '9': '4', 'c': '5','m': '6', '0': '7', 'b': '8', 'l': '9','a': '0'}


#解析出图片源链接地址
def getUrl(objUrl):
    conten=''
    objUrl=objUrl.replace('_z2C$q',':').replace('_z&e3B','.').replace('AzdH3F','/')
    for each in objUrl:
        if dic.get(each):
            conten=conten+dic.get(each)
        else:
            conten=conten+each

    print(conten)
    return conten

#获取页面并返回r.text
def getPage(url,parms):
    r=requests.get(url,headers=head,params=parms)
    r.raise_for_status()
    r.encoding='UTF-8'
    print('获得页面成功')
    print(r.encoding,r.apparent_encoding)
    return r.text

#解析json获取相应数据
def filterJson(js):
    UrlList=[]
    pageTitle=[]
    tyepeList=[]

    imageList=demjson.decode(js)
    #获取图片总数

    all_pageNum =imageList.get('displayNum')
    for each in imageList.get('data')[:-1]:
        UrlList.append(each.get('objURL'))
        pageTitle.append(each.get('di'))
        tyepeList.append(each.get('type'))
        #UrlList.append(getUrl(each.get('objURL')))
    return UrlList,pageTitle,tyepeList,all_pageNum
    print(Pname)

def saveImage(url,name,type,dirname):
    Rootdir='{}'.format(dirname)
    comp='{}\{}.{}'.format(Rootdir,name.replace('/','').replace('.',''),type)
    try:
        if not os.path.exists(Rootdir):
            os.mkdir(Rootdir)
            print('文件夹创建成功')
        if not os.path.exists(comp):
            r=requests.get(url,headers=head,timeout=5)
            r.raise_for_status()
            print(r.status_code)
            #print(comp)
            with open(comp,'wb') as F:
                F.write(r.content)
                F.close()
                print('图片保存至{}'.format(comp))
        else:
            print('图片已存在')
    except:
        print('获取图片写入失败')





if __name__ =='__main__':
    word=input('输入你要搜索的图片关键字:')
    pnn=0
    parm = {
        "1527826015581": "",
        "adpicid": "",
        "cl": "2",
        "ct": "201326592",
        "face": "0",
        "fp": "result",
        "fr": "",
        "gsm": "3c",
        "height": "",
        "ic": "0",
        "ie": "utf-8",
        "ipn": "rj",
        "is": "",
        "istype": "2",
        "lm": "-1",
        "nc": "1",
        "oe": "utf-8",
        "pn": pnn,
        "qc": "",
        "queryWord": word,
        "rn": 30,
        "s": "",
        "se": "",
        "st": "-1",
        "tab": "",
        "width": "",
        "word": word,
        "z": "",
        "tn": "resultjson_com"
    }
    url = 'https://image.baidu.com/search/acjson'
    #getUrl(url)
    List, Pname, Imgtype, num = filterJson(getPage(url, parm))




    print('图片总数为：{}预测共计{}页'.format(num,math.ceil(int(num)/ 30)))
    print(len(Pname))
    pageN = 0
    #while True:
    for p in range(math.ceil(int(num)/ 30)):

        print('当前页数为{}'.format(p+1))
        pnn = p * 30

        print(pageN)
        parm.update({'pn':p*30})

        List, Pname, Imgtype, num = filterJson(getPage(url,parm))
        for i in range(len(Pname)):
                #print(each)
            True_url=getUrl(List[i])
            print('图片名称：',Pname[i],Imgtype[i])
            saveImage(True_url,Pname[i],Imgtype[i],word)
            time.sleep(0.5)
            # pageNum = pageN+1 * 30suzu
            # parm.setdefault('pn', pageNum)
        print('第{}页图片获取完成，进行下一页。'.format(i))
        #pageN=pageN+1
        #print(pageN)
    print('END')
