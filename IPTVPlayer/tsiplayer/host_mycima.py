# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor

import re
import base64,urllib

def getinfo():
	info_={}
	info_['name']='Mycima.Tv'
	info_['version']='1.0 28/07/2019'
	info_['dev']='RGYSoft'
	info_['cat_id']='201'
	info_['desc']='افلام و مسلسلات كرتون'
	info_['icon']='https://i.ibb.co/rv3jmJ6/Sans-titre.png'
	info_['recherche_all']='0'
	return info_


class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'mycima.cookie'})
		self.MAIN_URL = 'https://mycima.me'
				
	def showmenu(self,cItem):
		self.add_menu(cItem,'class="Sidebar"(.*?)</ul','<li.*?href="(.*?)".*?>(.*?)</li','','10',del_=['إستكشف'],search=True)		
	
	def showmenu1(self,cItem):	
		result = self.add_menu(cItem,'CategoryTitle">.*?Tabs">(.*?)</div','<a.*?href="(.*?)".*?>(.*?)</a>','','20',del_=['الكل'])
		self.add_menu(cItem,'SmartSearch">.*?class="Tabs">(.*?)</div','<a.*?href="(.*?)".*?>(.*?)</a>',result[0],'20',Titre='>>>> حدّد اولوية تصفحك <<<<',del_=['افلام جديدة','آخر المسلسلات','آخر العروض'])		
			
	def showitms(self,cItem):
		desc = [('Rate','IMDBRate">(.*?)</div>','','n/a'),('Views','ViewsCounter">.*?M(.*?)<div','','</i>1</div>')]
		url = self.get_url_page(cItem['url'],cItem.get('page',1))
		sts, data = self.getPage(url)
		if sts:
			self.add_menu(cItem,'','BoxItem">.*?title="(.*?)".*?href="(.*?)".*?img="(.*?)"(.*?)</strong>',data,'21',ord=[1,0,2,3],del_=['data.title'],Desc=desc,Next=[1,'20'],u_titre=True,EPG=True)
	
	def showelms(self,cItem):
		url=cItem['url']
		if '/series/' in url:
			url = url.replace('/series/','/episodes/series/')
			pat = 'data-datatax=(.*?)<ul'
			ind = 0
		else:
			pat ='AsideContext"><h2>(.*?)class="AsideContext'
			ind = 1
		sts, data = self.getPage(url)
		if sts:	
			self.add_menu(cItem,pat,'BoxItem">.*?href="(.*?)".*?img="(.*?)".*?title="(.*?)"',data,'video',ord=[0,2,1],ind_0=ind)

	def SearchResult(self,str_ch,page,extra):
		desc = [('Rate','IMDBRate">(.*?)</div>','','n/a'),('Views','ViewsCounter">.*?M(.*?)<div','','</i>1</div>')]
		url = self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
		self.add_menu({'import':extra,'url':url},'','BoxItem">.*?title="(.*?)".*?href="(.*?)".*?img="(.*?)"(.*?)</strong>','','21',ord=[1,0,2,3],del_=['data.title'],Desc=desc,u_titre=True)

	def getArticle(self,cItem):
		Desc = [('Title','<span>الإسم بالعربي</span>(.*?)</li>','',''),('Country/Lang','<span>البلد و اللغة</span>(.*?)</li>','',''),('Time','<span>المدة</span>(.*?)</li>','',''),
		        ('Genre','<span>النوع</span>(.*?)</li>','',''),('Quality','<span>الجودة</span>(.*?)</li>','',''),('Time','<span>مدة الحلقة</span>(.*?)</li>','',''),
				('Category','<span>التصنيف</span>(.*?)</li>','',''),('Story','StoryMovieContent">(.*?)</div>','\n','')]
		desc = self.add_menu(cItem,'','','','desc',Desc=Desc)	
		if desc =='': desc = cItem.get('desc','')
		return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]




	def get_links(self,cItem): 		
		local = [('/mycima.me','MyCima','1'),]
		result = self.add_menu(cItem,'WatchServersList">(.*?)</ul','<li.*?href="(.*?)".*?>(.*?)</li>','','serv',local=local)						
		return result[1]	

	def getVideos(self,videoUrl):
		result = self.add_menu({'url':videoUrl},'sources: \[(.*?)\]','format:.*?["\'](.*?)["\'].*?src:.*?["\'](.*?)["\']','','link4',ord=[1,0])						
		return result[1]	
		
