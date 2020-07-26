#-*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.util import cUtil
import json

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Tune'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'tune'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):#correction ancienne url >> embed depreciated
        sPattern = '(?:play/|video/|embed\?videoid=|vid=)([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        url_list = []
        qua = []
        sId = self.__getIdFromUrl(self.__sUrl)

        sUrl = 'https://api.tune.pk/v3/videos/' + sId

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('X-KEY', '777750fea4d3bd585bf47dc1873619fc')
        oRequest.addHeaderEntry('X-REQ-APP', 'web') #pour les mp4
        oRequest.addHeaderEntry('Referer', self.__sUrl) #au cas ou
        sHtmlContent1 = oRequest.request()

        if (sHtmlContent1):
            sHtmlContent = cUtil().removeHtmlTags(sHtmlContent1)
            sHtmlContent = cUtil().unescape(sHtmlContent1)
            content = json.loads(sHtmlContent)

            content = content["data"]["videos"]["files"]

            if content:
                for x in content:
                    if 'Auto' in str(content[x]['label']):
                        continue
                    url2 = str(content[x]['file']).replace('index', str(content[x]['label']))

                    url_list.append(url2)
                    qua.append(repr(content[x]['label']))
					
                if qua and url_list:
                    i=0
                    url = ''
                    for x1 in qua:
                        if url!='': url=url+'||'
                        url = url+url_list[i]+'|tag:'+x1
                        i=i+1
                    return True, url

            return False, False
