# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost
from Components.config import config


import re


def getinfo():
	info_={}
	name = 'Aflam06'
	hst = tshost(name)	
	if hst=='': hst = 'https://aflam06.net'
	info_['host']= hst
	info_['name']=name	
	info_['version']='1.0.01 05/07/2020'
	info_['dev']='OPESBOY'
	info_['cat_id']='201'
	info_['desc']='أفلام, مسلسلات و انمي عربية و اجنبية'
	info_['icon']='http://aflam06.net/wp-content/uploads/2017/12/1aa8a166848.png'
	info_['recherche_all']='1'
	#info_['update']='New Host'
	return info_
	
	
class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'aflam06.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
		self.MAIN_URL = getinfo()['host']
		self.HTTP_HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.AJAX_HEADER = dict(self.HTTP_HEADER)
		self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
		self.defaultParams = {'header':self.HTTP_HEADER, 'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}

	def getPage(self, baseUrl, addParams = {}, post_data = None):
		baseUrl=self.std_url(baseUrl)
		if addParams == {}: addParams = dict(self.defaultParams)
		addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
		return self.cm.getPageCFProtection(baseUrl, addParams, post_data)
		
	def aflam06_plus_extract(self,code,id):	
		URL=self.MAIN_URL+'/wp-content/themes/YourColor/servers/server.php?q='+code+'&i='+id
		URL_=''
		sts, data = self.getPage(URL)
		if sts:
			_data2 = re.findall('(<iframe|<IFRAME).*?(src|SRC)=(.*?) ',data, re.S)
			if _data2:
				URL_=_data2[0][2]
				URL_=URL_.replace('"','')
				URL_=URL_.replace("'",'')
				if URL_.startswith('//'):
					URL_='http:'+URL_
		return URL_

		 
	def showmenu0(self,cItem):
		hst='host2'
		img_=cItem['icon']
		aflam06_TAB=[ {'category':hst,'title': 'الأفلام'    ,'mode':'20'  ,'sub_mode':'film'},
					  {'category':hst,'title': 'المسلسلات'   ,'mode':'20'  ,'sub_mode':'serie'},
					  #{'category':hst,'title': 'Other'    ,'mode':'20'  ,'sub_mode':'other'},
					  {'category':hst,'title': tscolor('\c0000????') + 'حسب التصنيف'   ,'mode':'20' ,'sub_mode':'filter'},						  
					  {'category':'search'  ,'title':tscolor('\c00????30') + _('Search'),'search_item':True,'page':1,'hst':'tshost'},
					]
		self.listsTab(aflam06_TAB, {'icon':img_,'import':cItem['import']})




	def showmenu1(self,cItem):
		gnr2=cItem['sub_mode']			 
		url=self.MAIN_URL
		img=cItem['icon']
	
		if gnr2=='filter':
			
			
			
			
			aflam06_filter=[{'category':'host2', 'title': 'اثارة'       , 'url':self.MAIN_URL+'/genre/%d8%a7%d8%ab%d8%a7%d8%b1%d8%a9/', 'desc':'', 'icon':img, 'mode':'30', 'page':1},
							 {'category':'host2', 'title': 'رعب'      , 'url':self.MAIN_URL+'/genre/%d8%b1%d8%b9%d8%a8/'   , 'desc':'', 'icon':img, 'mode':'30', 'page':0},						  
							 {'category':'host2', 'title': 'اكشن', 'url':self.MAIN_URL+'/genre/أكشن/'                                 , 'desc':'', 'icon':img, 'mode':'30', 'page':1},						  
							 {'category':'host2', 'title': 'كوميدي', 'url':self.MAIN_URL+'/genre/%d9%83%d9%88%d9%85%d9%8a%d8%af%d9%8a/'                                   , 'desc':'', 'icon':img, 'mode':'30', 'page':1},	 
							 {'category':'host2', 'title': 'جريمة', 'url':self.MAIN_URL+'/genre/%d8%ac%d8%b1%d9%8a%d9%85%d8%a9/'                                   , 'desc':'', 'icon':img, 'mode':'30', 'page':1},	 
							 {'category':'host2', 'title': 'دراما', 'url':self.MAIN_URL+'/genre/%d8%af%d8%b1%d8%a7%d9%85%d8%a7/'                                   , 'desc':'', 'icon':img, 'mode':'30', 'page':1},	 
							 {'category':'host2', 'title': 'مغامرة', 'url':self.MAIN_URL+'/genre/%d9%85%d8%ba%d8%a7%d9%85%d8%b1%d8%a9/'                                   , 'desc':'', 'icon':img, 'mode':'30', 'page':1},	 
							 
							]
			self.listsTab(aflam06_filter, {'name':'categories','import':cItem['import']})
		else:
			sts, data = self.getPage(url)
			if sts:
				lst_data = re.findall('<i class="fa fa-bars">(.*?)</ul>',data, re.S)
				if lst_data:
					i=0
					if gnr2=='film':
						i1=1
						i2=5	
					elif gnr2=='serie':
						i1=6
						i2=11				
					lst_data1 = re.findall('<li.*?href="(.*?)">(.*?)<',lst_data[1], re.S)
					for (url1,titre1) in lst_data1:
						if ((i+1>i1 and i-1<i2) or (i==0 and gnr2=='serie')):
							if 'Show' in titre1: titre1='برامج و عروض'
							self.addDir({'import':cItem['import'],'category' :'host2', 'url':url1, 'title':titre1, 'desc':titre1, 'icon':img, 'mode':'30', 'page':1})
						i=i+1 	
				
	def showitms(self,cItem):
		page=cItem.get('page',1)
		url0=cItem['url']
		url=url0
		if page!=0:
			if url0.endswith('.php'): 
				url=url0+'/?page='+str(page)+'/'
			else:
				url=url0+'page/'+str(page)+'/'
		#sts, data = self.cm.getPage(url)	
		sts, data = self.getPage(url)	
		if sts:		
			lst_data=re.findall('class="block">.*?href="(.*?)".*?src="(.*?)".*?<p>(.*?)<.*?class="title">(.*?)<', data, re.S)
			for (url1,image,desc,titre) in lst_data:
				image=self.std_url(image)
				desc0,titre = self.uniform_titre(titre)
				
				self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url1, 'desc':desc0,'title':titre, 'icon':image, 'mode':'31','EPG':True,'hst':'tshost'} )							
			if page!=0:
				self.addDir({'import':cItem['import'],'category':'host2', 'url':url0, 'title':tscolor('\c0090??20')+_('Next page'), 'page':page+1, 'desc':'Page Suivante', 'icon':cItem['icon'], 'mode':'30'})	
						
	def SearchResult(self,str_ch,page,extra):
		url_=self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
		sts, data = self.getPage(url_)
		if sts:
			cat_data=re.findall('class="block">.*?href="(.*?)".*?src="(.*?)".*?<p>(.*?)<.*?class="title">(.*?)<', data, re.S)
			for (url1,image,desc,name_eng) in cat_data:
				image=self.std_url(image)
				desc=ph.clean_html(desc)
				desc0,name_eng = self.uniform_titre(name_eng)
				if desc.strip()!='':
					desc = tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+desc
				desc=desc0+desc
				#name_eng=name_eng.replace('مشاهدة وتحميل مباشر','')
				params = {'import':extra,'good_for_fav':True,'category' :'video','url': url1, 'desc':desc,'title':name_eng,'icon':image,'mode':'31','EPG':True,'hst':'tshost'} 
				self.addVideo(params)		
		
	def get_links(self,cItem): 	
		urlTab = []	
		URL=cItem['url']+'?view=1'				
		sts, data = self.getPage(URL)
		if sts:
			code_data = re.findall("data: 'q=(.*?)&", data, re.S)
			if code_data:
				code=code_data[0]
				server_data = re.findall('data-server="(.*?)">(.*?)</li>', data, re.S)	
				for (id,name) in server_data:
					name = self.cleanHtmlStr(name)
					name = name.replace('سيرفر','Server')
					if config.plugins.iptvplayer.ts_dsn.value:
						URL_=self.aflam06_plus_extract(code,id)
						urlTab.append({'name':self.up.getDomain(URL_), 'url':URL_, 'need_resolve':1})
					else:
						urlTab.append({'name':name, 'url':'hst#tshost#'+code+'|'+id, 'need_resolve':1})
				if urlTab == []:
					for i in range(1,14):
						URL_=self.aflam06_plus_extract(code,str(i))
						if URL_!='':
							urlTab.append({'name':self.up.getDomain(URL_), 'url':URL_, 'need_resolve':1})				
		return urlTab
		 
	def getVideos(self,videoUrl):
		urlTab = []	
		code,id=videoUrl.split('|')
		urlTab.append((self.aflam06_plus_extract(code,id),'1'))
		return urlTab
				
	def getArticle(self, cItem):
		printDBG("aflam06Com.getArticleContent [%s]" % cItem)
		otherInfo = {}
		desc = cItem.get('desc', '')
		title = cItem['title']
		icon = cItem.get('icon', '')
		return [{'title':self.cleanHtmlStr( title ), 'text': self.cleanHtmlStr( desc ), 'images':[{'title':'', 'url':self.getFullUrl(icon)}], 'other_info':otherInfo}]

	
	def start(self,cItem):      
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu0(cItem)
		if mode=='20':
			self.showmenu1(cItem)
		if mode=='30':
			self.showitms(cItem)			
		if mode=='31':
			self.showelems(cItem)
