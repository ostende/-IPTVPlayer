# -*- coding: utf-8 -*-

#
#
# @Codermik release, based on @Samsamsam's E2iPlayer public.
# Released with kind permission of Samsamsam.
# All code developed by Samsamsam is the property of the Samsamsam and the E2iPlayer project,  
# all other work is Â© E2iStream Team, aka Codermik.  TSiPlayer is Â© Rgysoft, his group can be
# found here:  https://www.facebook.com/E2TSIPlayer/
#
# https://www.facebook.com/e2iStream/
#
#


###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass, CDisplayListItem, ArticleContent, RetHost, CUrlItem
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import CSelOneLink, printDBG, printExc, MergeDicts
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
import re
import urllib
import time
import random
from Components.config import config, ConfigSelection, ConfigYesNo, getConfigListEntry
###################################################

###################################################
# Config options for HOST
###################################################
config.plugins.iptvplayer.ekstraklasa_defaultformat = ConfigSelection(default = "450", choices = [("0", "bitrate: najgorszy"), ("200", "bitrate: 200p"), ("450", "bitrate: 450p"),("900", "bitrate: 900"),("1800", "bitrate: 1800"), ("9999", "bitrate: najlepszy")])
config.plugins.iptvplayer.ekstraklasa_usedf = ConfigYesNo(default = False)
config.plugins.iptvplayer.ekstraklasa_proxy = ConfigYesNo(default = False)

def GetConfigList():
    optionList = []
    optionList.append( getConfigListEntry( "DomyÅlny format video:", config.plugins.iptvplayer.ekstraklasa_defaultformat ) )
    optionList.append( getConfigListEntry( "UÅ¼ywaj domyÅlnego format video:", config.plugins.iptvplayer.ekstraklasa_usedf ) )
    optionList.append( getConfigListEntry( "Ekstraklasa korzystaj z proxy?", config.plugins.iptvplayer.ekstraklasa_proxy) )
    return optionList
###################################################

def gettytul():
    return 'http://ekstraklasa.tv/'

class Ekstraklasa(CBaseHostClass):

    EORG_MAIN_URL = 'http://ekstraklasa.org/'
    EORG_MAIN_MENU = [ {'name': 'NowoÅci', 'navi': 'nowosci'},
                       {'name': 'Bramki i skrÃ³ty', 'navi': 'galeria-i-wideo'},
                     ]
    
    ETV_MAIN_URL  = 'http://ekstraklasa.tv/'
    ETV_MAIN_MENU = [ {'name': 'Bramki', 'navi': 'bramki'},
                      {'name': 'SkrÃ³ty', 'navi': 'skroty'},
                      {'name': 'Bramka kolejki', 'navi': 'bramka-kolejki'},
                      {'name': 'Magazyn', 'navi': 'magazyny/magazyn-ekstraklasy'},
                    ]
    ETV_CATEGORY  = 'etv_category'
    MAIN_URL = ETV_MAIN_URL
    def __init__(self):
        printDBG("Ekstraklasa.__init__")
        CBaseHostClass.__init__(self, {'proxyURL': config.plugins.iptvplayer.proxyurl.value, 'useProxy': config.plugins.iptvplayer.ekstraklasa_proxy.value})
        self.DEFAULT_ICON_URL = 'http://footballtripper.com/wp-content/themes/ft/flags/Ekstraklasa-flag.png'

    def listsCategories_ETV(self):
        printDBG("Ekstraklasa.listsCategories_ETV")
        
        for item in Ekstraklasa.ETV_MAIN_MENU:
            params = { 'name'     : 'category',
                       'category' : Ekstraklasa.ETV_CATEGORY,
                       'url'      : Ekstraklasa.ETV_MAIN_URL + item['navi'],
                       'title'    : item['name'],
                       'desc'     : 'ekstraklasa.tv',
                       'depth'    : 0,
                       'host'     : 'ekstraklasa.tv'
                     }  
            self.addDir(params)

    def listsCategory_ETV(self, cItem):
        printDBG("Ekstraklasa.listsCategory_ETV")
        page = cItem.get('page', 0)
        url = cItem['url']
        if page > 0: url += str(page)

        ITEM_MARKER = '<div class="listItem'
        sts, data = self.cm.getPage(url)
        if not sts: return
        moreData = ph.find(data, ('<div', '>', 'data-preset'))[1]

        # check if we should check for sub categories
        if 0 == cItem['depth']:
            subMenuData  = ph.find(data, ('<ul', '>', 'subMenu'), '</ul>', flags=0)[1]
            subMenuData  = re.compile('<a[ ]+?href="(http[^">]+?)"[ ]*?>([^<]+?)</a>').findall(subMenuData)
            if 0 < len(subMenuData):
                params = dict(cItem)
                params.update({'title':'Najnowsze', 'depth':1})
                self.addDir(params)
                for item in subMenuData:
                    params = dict(cItem)
                    params.update({'url':item[0], 'title': self.cleanHtmlStr(item[1]), 'depth':1, })
                    self.addDir(params)
                return

        data = self.cm.ph.getDataBeetwenMarkers(data, ITEM_MARKER, '<script')[1]

        data = data.split(ITEM_MARKER)
        del data[0]
        for item in data:
            icon  = ph.search(item, '<img[^>]+?data-original="([^"]+?)"')[0]
            title = ph.find(item, '<h3 class="itemTitle">', '</h3>', flags=0)[1].strip() + ', ' + ph.find(item, '<div class="datePublished">', '</div>', flags=0)[1].strip()
            desc  = self.cleanHtmlStr(ITEM_MARKER + item)
            url   = self.cm.ph.getSearchGroups(item, '<a href="([^"]+?)" title="([^"]+?)"', 2)[0]
            params = {'title':ph.clean_html(title), 'url':url, 'icon':icon, 'desc': desc, 'host':'ekstraklasa.tv'}
            self.addVideo(params)

        if page == 0 and moreData and len(self.currList):
            try:
                url = self.getFullUrl(ph.getattr(moreData, 'data-preset').replace('&amp;', '&'), self.cm.meta['url'])
                page = int(ph.getattr(moreData, 'data-page'))
                if url: self.addDir(MergeDicts(cItem, {'title':_('Next page'), 'url':url, 'page':page}))
            except Exception:
                printExc()
        elif page > 0 and len(self.currList):
            self.addDir(MergeDicts(cItem, {'title':_('Next page'), 'page':page+1}))
        # list items

    def getLinks_ETV(self, url):
        printDBG("Ekstraklasa.getLinks_ETV url[%r]" % url )
        return self.up.getVideoLinkExt(url)

    def getArticleContent(self, cItem):
        printDBG("Ekstraklasa.getArticleContent [%s]" % cItem)
        retTab = []
        itemsList = []

        sts, data = self.cm.getPage(cItem['url'])
        if not sts: return []

        title = cItem['title']
        icon = cItem.get('icon', self.DEFAULT_ICON_URL)
        desc = cItem.get('desc', '')

        data = ph.find(data, ('<script', '>', 'ld+json'), '</script>', flags=0)[1]
        try:
            data = json_loads(data)
            title = ph.clean_html(data['headline'])
            icon = self.getFullIconUrl(data['image']['url'], self.cm.meta['url'])
            desc = ph.clean_html(data['description'])
            itemsList.append((_('Author'), data['author']['name']))
            itemsList.append((_('Published'), data['datePublished'].split('+', 1)[0]))
        except Exception:
            printExc()

        if title: title = cItem['title']
        if icon:  icon = cItem.get('icon', self.DEFAULT_ICON_URL)
        if desc:  desc = cItem.get('desc', '')
        
        return [{'title':self.cleanHtmlStr( title ), 'text': self.cleanHtmlStr( desc ), 'images':[{'title':'', 'url':self.getFullUrl(icon)}], 'other_info':{'custom_items_list':itemsList}}]
    
    def handleService(self, index, refresh = 0, searchPattern = '', searchType = ''):
        printDBG('Ekstraklasa..handleService start')
        
        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        
        name     = self.currItem.get("name", None)
        category = self.currItem.get("category", '')
        printDBG( "Ekstraklasa.handleService: ---------> name[%s], category[%s] " % (name, category) )
        self.currList = []
        
        if None == name:
            self.listsCategories_ETV()
        elif Ekstraklasa.ETV_CATEGORY == category:
            self.listsCategory_ETV(self.currItem)


class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, Ekstraklasa(), False)

    def getLinksForVideo(self, Index = 0, selItem = None):
        listLen = len(self.host.currList)
        if listLen < Index and listLen > 0:
            printDBG( "ERROR getLinksForVideo - current list is to short len: %d, Index: %d" % (listLen, Index) )
            return RetHost(RetHost.ERROR, value = [])
        retlist = []
        if 'ekstraklasa.tv' in self.host.currList[Index].get('host', ''):
            tab = self.host.getLinks_ETV(self.host.currList[Index].get('url', ''))

            def __getLinkQuality( itemLink ):
                return int(itemLink['bitrate'])

            maxRes = int(config.plugins.iptvplayer.ekstraklasa_defaultformat.value) * 1.1
            tab = CSelOneLink(tab, __getLinkQuality, maxRes).getSortedLinks()
            printDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>. tab[%s]" % tab)
            if config.plugins.iptvplayer.ekstraklasa_usedf.value and len(tab):
                tab = [tab[0]]

            for item in tab:
                retlist.append(CUrlItem(item['name'], item['url'], 0))
        elif 'ekstraklasa.org' in self.host.currList[Index].get('host', ''):
            pass
        return RetHost(RetHost.OK, value = retlist)
    # end getLinksForVideo

    def withArticleContent(self, cItem):
        return True if 'video' == cItem.get('type') else False