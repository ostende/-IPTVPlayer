# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import base64
import re,urllib

from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'UpToStream'
        self.__sFileName = self.__sDisplayName
        self.oPremiumHandler = None

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uptostream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return self.__sUrl.split('/')[-1]

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('iframe/', '')
        self.__sUrl = self.__sUrl.replace('http:', 'https:')

    def checkSubtitle(self, sHtmlContent):
        oParser = cParser()

        # On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
        # if not re.search("<h1 class='file-title'>[^<>]+(?:TRUEFRENCH|FRENCH)[^<>]*</h1>", sHtmlContent, re.IGNORECASE):
        if "<track type='vtt'" in sHtmlContent:

            sPattern = '<track type=[\'"].+?[\'"] kind=[\'"]subtitles[\'"] src=[\'"]([^\'"]+).vtt[\'"] srclang=[\'"].+?[\'"] label=[\'"]([^\'"]+)[\'"]>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                Files = []
                for aEntry in aResult[1]:
                    url = aEntry[0]
                    label = aEntry[1]
                    url = url + '.srt'

                    if not url.startswith('http'):
                        url = 'http:' + url
                    if 'Forc' not in label:
                        Files.append(url)
                return Files

        return False

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self, premium=False):

        api_call = False
        SubTitle = ''

        # compte gratuit ou payant
        token = ''
        if premium:
            if self.oPremiumHandler.Authentificate():
                sHtmlContent = self.oPremiumHandler.GetHtml(self.__sUrl)
                sPattern = "window\.token = '([^']+)';"
                token = re.search(sPattern,sHtmlContent, re.DOTALL)
                if token:
                    token = token.group(1)

                SubTitle = self.checkSubtitle(sHtmlContent)

        if token:
            sUrl2 = "https://uptostream.com/api/streaming/source/get?token={}&file_code={}".format(token, self.__getIdFromUrl())
            sHtml = self.oPremiumHandler.GetHtml(sUrl2)
        else:
            # pas de compte
            sUrl2 = "https://uptostream.com/api/streaming/source/get?token=null&file_code={}".format(self.__getIdFromUrl())

            oRequest = cRequestHandler(sUrl2)
            sHtml = oRequest.request()

        qua, url_list = decodeur1(sHtml)
        
        if qua and url_list:
            i=0
            url = ''
            for x1 in qua:
                if url!='': url=url+'||'
                url = url+url_list[i]+'|tag:'+x1
                i=i+1
            return True, url
        return False, False


def decodeur1(Html):
    from ast import literal_eval
    # search list64 and his var name.
    vl = re.search('var *(_\w+) *= *(\[[^;]+\]);', Html, re.DOTALL)
    if vl:
        var_name = vl.group(1)
        list_b64 = vl.group(2)
        # reduce html
        start = Html.find(list_b64)
        Html = Html[start:]

        list_b64 = literal_eval(list_b64)

        # search ref number to re-order the b64list and the var name.
        nrvr = re.search(var_name + ',(0x\w+)\)*; *var *([^=]+) *=', Html, re.DOTALL)
        if nrvr:
            number_ref = int(nrvr.group(1),16)
            var_ref = nrvr.group(2)

            i = 0
            while i < number_ref:
                list_b64.append(list_b64.pop(0))
                i += 1

            # search for group
            test2 = re.findall("(?:;|;}\(\)\);)sources(.+?)};", Html, re.DOTALL)
            if test2:
                url = ''
                movieID = ''
                qua_list = []

                for page in test2:
                    tableau = {}
                    data = page.find("={")
                    if data != -1:
                        Html = page[data:]
                        if Html:
                            i = 0
                            vname = ''
                            for i in xrange(len(Html)):
                                fisrt_r = re.match("([^']+)':", Html, re.DOTALL)
                                if fisrt_r:
                                    vname = fisrt_r.group(1)
                                    tableau[vname] = 'null'

                                    index = len(fisrt_r.group()[:-1])
                                    Html = Html[index:]

                                whats = re.match("[:+]'([^']+)'", Html, re.DOTALL)
                                if whats:
                                    if vname:
                                        ln = tableau[vname]
                                        if not ln == 'null':
                                            tableau[vname] = tableau[vname] + whats.group(1)
                                        else:
                                            tableau[vname] = whats.group(1)

                                    index = len(whats.group(0))
                                    Html = Html[index:]

                                else:
                                    whats = re.match("\+*" + var_ref + "\(\'([^']+)\' *, *\'([^']+)\'\)", Html, re.DOTALL)
                                    if whats:
                                        if vname:
                                            ln = tableau[vname]
                                            if not ln == 'null':
                                                tableau[vname] = tableau[vname] + decoder(list_b64[int(whats.group(1), 16)], whats.group(2))

                                            else:
                                                tableau[vname] = decoder(list_b64[int(whats.group(1), 16)], whats.group(2))

                                        index = len(whats.group(0))
                                        Html = Html[index:]

                                if not whats:
                                    Html = Html[1:]

                        if tableau:
                            langFre = True  # langue par défaut si pas précisée
                            qual = ''
                            for i, j in tableau.items():
                                if j.startswith('http') and j.endswith('com'):  # url
                                    url = tableau[i] if not tableau[i] in url else url
                                    continue

                                if len(i) == 5 and len(j) >= 10 and j.isalnum() and not 'video' in j:
                                    movieID = j if not j in movieID else movieID
                                    continue

                                if len(test2) > 1:  # s'il y a plusieurs flux
                                    if j == 'eng':  # on ne gere pas plusieurs langues car on sait pas l'associer à la bonne qualité
                                        langFre = False

                                if j == '360' or j == '480' or j == '720' or j == '1080':
                                    qual = j

                            if langFre and qual and qual not in qua_list:
                                qua_list.append(qual)

                qua_list.sort()
                url_list = []
                for qual in qua_list:
                    url_list.append("{}/{}/{}/0/video.mp4".format(url, movieID, qual))

                return qua_list, url_list


def decoder(data, fn):
    data = base64.b64decode(data)

    secretKey = {}
    url = ''
    temp = ''
    tempData = ''

    for i in xrange(len(data)):
        tempData += ("%" + format(ord(data[i]), '02x'))

    data =  urllib.unquote(tempData)

    x = 0
    while x < 256:
        secretKey[x] = x
        x += 1

    y = 0
    x = 0
    while x < 256:
        y = (y + secretKey[x] + ord(fn[x % len(fn)])) % 256

        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp
        x += 1

    x = 0
    y = 0
    i = 0
    while i < len(data.decode('utf-8')):

        x = (x + 1) % 256
        y = (y + secretKey[x]) % 256

        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp

        url += (chr(ord(data.decode('utf-8')[i]) ^ secretKey[(secretKey[x] + secretKey[y]) % 256]))

        i += 1

    return url
