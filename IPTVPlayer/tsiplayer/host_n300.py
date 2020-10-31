# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor
from Components.config import config

import re



def getinfo():
	info_={}
	info_['name']='N300.Me'
	info_['version']='1.3 11/07/2020'
	info_['dev']='RGYSoft'
	info_['cat_id']='201'
	info_['desc']='افلام و مسلسلات عربية واجنبية'
	info_['icon']='http://www.n300.me/IMGCenter/IMGSystem/LOGO/LOGO_N300_me_200px.png'
	info_['recherche_all']='0'
	#info_['update']='Bugs Fix'
	return info_
	
	
class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'n300.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36'
		self.MAIN_URL = 'http://www.n300.me'
		self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
		self.getPage = self.cm.getPage
		 
	def showmenu0(self,cItem):
		hst='host2'
		img=cItem['icon']			
		CAT_TAB=[	{'category':hst,'title': 'الأفلام'               ,'mode':'20' ,'icon':img ,'sub_mode':0},
					{'category':hst,'title': 'المسلسلات و البرامج'  ,'mode':'20' ,'icon':img ,'sub_mode':1},
					]
		self.listsTab(CAT_TAB, {'import':cItem['import'],'name':hst})			

	def showmenu1(self,cItem):
		hst='host2'
		img=cItem['icon']
		gnr2=cItem['sub_mode']	
		if gnr2==0:
			CAT_TAB=[ {'category':hst,'title':'افلام اجنبية','desc': 'افلام اجنبية مدبلجة / مترجمة'      ,'url':self.MAIN_URL+'/Mobile/Category/CatMovies/OtherMovies' ,'mode':'30' ,'icon':img ,'sub_mode':0},
					  {'category':hst,'title':'افلام عربية' ,'desc':'افلام عربية سورية , مصرية , خليجية' ,'url':self.MAIN_URL+'/Mobile/Category/CatMovies/ArabicMovies','mode':'30' ,'icon':img ,'sub_mode':0},
					  {'category':hst,'title':'افلام تركية' ,'desc':'افلام تركية مترجمة / مدبلجة'        ,'url':self.MAIN_URL+'/Mobile/Category/CatMovies/TurkeyMovies','mode':'30' ,'icon':img ,'sub_mode':0},
					  {'category':hst,'title':'افلام هندية' ,'desc':'افلام هندية مترجمة / مدبلجة'        ,'url':self.MAIN_URL+'/Mobile/Category/CatMovies/IndianMovies','mode':'30' ,'icon':img ,'sub_mode':0},
						]
			self.listsTab(CAT_TAB, {'import':cItem['import'],'name':hst})			
		elif gnr2==1:
			CAT_TAB=[ {'category':hst,'title':'مسلسلات رمضان 2020','desc':'مسلسلات رمضان 2020'                    ,'url':self.MAIN_URL+'/phone/Category/subCat/Ramadan2020' ,'mode':'30' ,'icon':img ,'sub_mode':1},
					  {'category':hst,'title':'مسلسلات تركية'     ,'desc':'مسلسلات تركية مدبلجة / مترجمة'         ,'url':self.MAIN_URL+'/phone/Category/subCat/TurkeySeries','mode':'30' ,'icon':img ,'sub_mode':1},
					  {'category':hst,'title':'مسلسلات عربية'     ,'desc':'مسلسلات عربية سورية , مصرية , خليجية'  ,'url':self.MAIN_URL+'/phone/Category/subCat/ArabicSeries','mode':'30' ,'icon':img ,'sub_mode':1},
					  {'category':hst,'title':'مسلسلات هندية'     ,'desc':'مسلسلات هندية اجنبية'                  ,'url':self.MAIN_URL+'/phone/Category/subCat/OtherSeries' ,'mode':'30' ,'icon':img ,'sub_mode':1},
					  {'category':hst,'title':'برامج تلفزيون'    ,'desc':'برامج تلفزيون'                        ,'url':self.MAIN_URL+'/phone/Category/subCat/TvProgram'   ,'mode':'30' ,'icon':img ,'sub_mode':1},
						]
			self.listsTab(CAT_TAB, {'import':cItem['import'],'name':hst})			
			
	
	def showitms(self,cItem):
		printDBG('citem='+str(cItem))
		url=cItem['url']  
		hst='host2'
		img=cItem['icon']
		gnr2=cItem['sub_mode']	
		if gnr2==0:
			sts, data = self.cm.getPage(url,self.defaultParams)
			if sts:
				lst_data=re.findall('<table id="Content(.*?)</form>', data, re.S)
				if 	lst_data:
					lst_data2=re.findall('<a href="(.*?)".*?src="(.*?)".*?<h1.*?>(.*?)</h1>.*?<h2.*?>(.*?)</h2>.*?<span.*?>(.*?)</span>', lst_data[0], re.S)
					for (url1,image,name,desc1,desc2) in lst_data2:
						image=image.replace('../../../',self.MAIN_URL+'/')
						url1=url1.replace('../',self.MAIN_URL+'/Mobile/Category/')
						name = 'I '+name +' I '+tscolor('\c00????00')+'('+ desc1+')'
						if not image.startswith('http'): image = self.MAIN_URL + image
						if not url1.startswith('http'): url1 = self.MAIN_URL + url1
						self.addVideo({'import':cItem['import'],'good_for_fav':True, 'hst':'tshost', 'category':'host2', 'url':url1, 'title':name, 'desc':desc2, 'icon':image} )	
		elif gnr2==1:
			sts, data = self.cm.getPage(url,self.defaultParams)
			if sts:
				lst_data=re.findall('<table id="Content(.*?)</form>', data, re.S)
				if 	lst_data:
					lst_data2=re.findall('<a href=\'(.*?)&.*?src="(.*?)".*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)</span>', lst_data[0], re.S)
					for (url1,image,name,desc1,desc2) in lst_data2:
						image=image.replace('../../../',self.MAIN_URL+'/')
						url1=url1.replace('../',self.MAIN_URL+'/Mobile/Category/')
						name = 'I '+name +' I '+tscolor('\c00????00')+'('+ desc2+')'
						if not image.startswith('http'): image = self.MAIN_URL + image
						if not url1.startswith('http'): url1 = self.MAIN_URL + url1
						self.addDir({'import':cItem['import'],'good_for_fav':True, 'category':'host2', 'url':url1, 'title':name, 'desc':desc1, 'icon':image, 'mode':'30','sub_mode':2} )	
		elif gnr2==2:	 
			sts, data = self.cm.getPage(url,self.defaultParams)
			if sts:
				#printDBG('data='+data)
				lst_data=re.findall('<table id="Content(.*?)</form>', data, re.S)
				if 	lst_data:
					lst_data2=re.findall('href="(.*?)".*?>(.*?)</a>', lst_data[0], re.S)
					for (url1,name) in lst_data2:
						url1 = self.MAIN_URL+'/phone/Category/moslsl/'+url1
						name = name.replace('<br />',' - ')
						self.addVideo({'import':cItem['import'],'good_for_fav':True, 'hst':'tshost', 'category':'host2', 'url':url1, 'title':ph.clean_html(name), 'desc':'', 'icon':cItem['icon']} )	

		
	def get_links(self,cItem): 	
		urlTab = []	
		URL=cItem['url']
		sts, data0 = self.cm.getPage(URL,self.defaultParams)
		if sts:
			Liste_els0 = re.findall('class="ChooseServer">(.*?)</table>', data0, re.S)
			if Liste_els0:
				Tab_urls=[]
				Liste_els1 = re.findall('<input id="(.*?)".*?\(\'(.*?)\'.*?value="(.*?)"', Liste_els0[0], re.S)
				for (x1,url,titre) in Liste_els1:
					if url not in Tab_urls:
						videoUrl = url
						Tab_urls.append(url)
						nr=1 
						local=''
						#if 'سرفر' in titre:
						titre = titre.replace('سيرفر','Server')
						titre = titre.replace('الموقع','Local')
						if url.startswith('//'): url ='https:'+url
						if '.mp4' in url:
							url=url.replace('../../../',self.MAIN_URL+'/')
							url=url.replace('http://www.n300.net:8080/','https://ssl.n300.me:8080/')
							if 'videoURL=' in url: url = url.split('videoURL=',1)[-1]
							titre = '|'+titre+'| N300'
							nr=0
							local='local'
							meta = {'Referer':videoUrl}
							url = strwithmeta(url, meta)
							if '?videoURL=' in url:
								sts, data0 = self.cm.getPage(url,self.defaultParams)
								if sts:
									Liste_els1 = re.findall('file:.*?["\'](.*?)["\']', data0, re.S)
									if Liste_els1:
										url=Liste_els1[0]
						else:
							titre = '|'+titre+'| '+gethostname(url)
						urlTab.append({'name':titre, 'url':url, 'need_resolve':nr,'type':local})			
		return urlTab
	
	def start(self,cItem):      
		mode=cItem.get('mode', None) 
		if mode=='00':
			self.showmenu0(cItem)
		if mode=='20':
			self.showmenu1(cItem)
		if mode=='30':
			self.showitms(cItem)			
