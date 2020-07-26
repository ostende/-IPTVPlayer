# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.libs import ph
import re,urllib,base64

def getinfo():
	info_={}
	info_['name']='Extra-3sk.Com'
	info_['version']='1.1 10/04/2020'
	info_['dev']='RGYSoft'
	info_['cat_id']='201'
	info_['desc']='أفلام و مسلسلات تركية'
	info_['icon']='https://i.ibb.co/qR294FT/extra.png'
	info_['recherche_all']='0'
	#info_['update']='Fix Links extractor'	

	return info_
	
	
class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'extra_3sk.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
		self.MAIN_URL = 'https://watch.extra-3sk.com'
		self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
		self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
		self.getPage = self.cm.getPage
		 
	def showmenu0(self,cItem):
		sts, data = self.getPage(self.MAIN_URL)
		if sts:
			lst_data=re.findall('<li id="menu.*?href="(.*?)".*?>(.*?)<', data, re.S)
			for (url,titre) in lst_data:
				if 'الرئيسية' not in titre:
					if 'ramadan-2020' in url: titre = 'Ramadan 2020 | ' + titre
					self.addDir({'import':cItem['import'],'category' : 'host2','title': titre,'icon':cItem['icon'],'mode':'30','url':url,'sub_mode':'0'})
			self.addDir({'import':cItem['import'],'category' :'search','title': _('Search'),'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})





		#self.addDir({'import':cItem['import'],'category' : 'host2','title':'المسلسلات والافلام التركية'  ,'icon':cItem['icon'],'mode':'30','url':self.MAIN_URL+'/','sub_mode':'0'})
		#self.addDir({'import':cItem['import'],'category' : 'host2','title':'اخر الحلقات'  ,'icon':cItem['icon'],'mode':'30','url':self.MAIN_URL+'/episodes/','sub_mode':'0'})
		#self.addDir({'import':cItem['import'],'category' : 'host2','title':'افلام'         ,'icon':cItem['icon'],'mode':'30','sub_mode':'2'})			
		#self.addDir({'import':cItem['import'],'category' : 'host2','title':'جميع المسلسلات','icon':cItem['icon'],'mode':'30','url':self.MAIN_URL+'/series/','sub_mode':'1'})	
		#self.addDir({'import':cItem['import'],'category' :'search','title': _('Search'),'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})


	def showitms(self,cItem):
		printDBG('citem='+str(cItem))
		sub_mode=cItem.get('sub_mode', '0')	
		page = cItem.get('page', 1)
		url0=cItem.get('url', '')	
		pat = 'class="block(.*?)</a>'
	
		if page>1:
			url0=url0+'/page/'+str(page)+'/'
			url0=url0.replace('//page/','/page/')
		sts, data = self.getPage(url0)
		if sts:
			lst_data=re.findall(pat, data, re.S)
			i=0
			for data0 in lst_data:
				i=i+1
				lst_data0=re.findall('href="(.*?)".*?src="(.*?)".*?alt="(.*?)"', data0, re.S)
				if lst_data0:
					titre = lst_data0[0][2]
					image = lst_data0[0][1]
					url   = lst_data0[0][0]
					desc=''
					desc0,titre = self.uniform_titre(titre)
					image=self.std_url(image)
					self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc0,'icon':image,'mode':'31','good_for_fav':True,'sub_mode':'1','EPG':True})	
			if i>95:
				self.addDir({'import':cItem['import'],'category' : 'host2','title':'Page Suivante','url':cItem['url'],'page':page+1,'mode':'30','sub_mode':sub_mode})

	def showelms(self,cItem):
		url0=cItem.get('url', '')	
		self.addVideo({'import':cItem['import'],'category' : 'host2','title':cItem['title'],'url':cItem['url'],'desc':cItem['desc'],'icon':cItem['icon'],'hst':'tshost','good_for_fav':True,'EPG':True})	
		self.addMarker({'title':tscolor('\c00????00')+'اذا اعجبك العمل نرشح لك','icon':cItem['icon']})	
		pat = 'class="block(.*?)</a>'		
		sts, data = self.getPage(url0)
		if sts:
			lst_data=re.findall(pat, data, re.S)
			for data0 in lst_data:
				lst_data0=re.findall('href="(.*?)".*?src="(.*?)".*?alt="(.*?)"', data0, re.S)
				if lst_data0:
					titre = lst_data0[0][2]
					image = lst_data0[0][1]
					url   = lst_data0[0][0]
					desc=''
					lst_inf0=re.findall('ribbon">(.*?)<', data0, re.S)
					if lst_inf0: desc = tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+self.cleanHtmlStr(lst_inf0[0])+'\n'
					lst_inf0=re.findall('StarLabels">(.*?)</i', data0, re.S)
					if lst_inf0: desc = desc + tscolor('\c00????00')+'Rate: '+tscolor('\c00??????')+self.cleanHtmlStr(lst_inf0[0])				
					desc0,titre = self.uniform_titre(titre)
					desc = desc0+desc
					image=self.std_url(image)
					self.addVideo({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'EPG':True})	

	def SearchResult(self,str_ch,page,extra):
		url = self.MAIN_URL+'/search/'+str_ch
		if page>1:
			url=url+'?order='+str(page*50-50)
		pat = 'class="block(.*?)</a>'
		sts, data = self.getPage(url)
		if sts:
			lst_data=re.findall(pat, data, re.S)
			i=0
			for data0 in lst_data:
				i=i+1
				lst_data0=re.findall('href="(.*?)".*?src="(.*?)".*?alt="(.*?)"', data0, re.S)
				if lst_data0:
					titre = lst_data0[0][2]
					image = lst_data0[0][1]
					url   = lst_data0[0][0]
					desc=''
					image=self.std_url(image)
					if '/selary/' in url:
						self.addDir({'import':extra,'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'30','good_for_fav':True,'sub_mode':'0'})	
					else:
						self.addVideo({'import':extra,'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'EPG':True})	

	def getArticle(self, cItem):
		otherInfo1 = {}
		desc= cItem['desc']	
		sts, data = self.getPage(cItem['url'])
		if sts:
			lst_dat=re.findall("<span>سنة الاصدار : </span>(.*?)</li>", data, re.S)
			if lst_dat: otherInfo1['year'] = ph.clean_html(lst_dat[0])		
			lst_dat=re.findall("<span>البلد : </span>(.*?)</li>", data, re.S)
			if lst_dat: otherInfo1['country'] = ph.clean_html(lst_dat[0])				
			lst_dat=re.findall("<span>الانواع : </span>(.*?)</li>", data, re.S)
			if lst_dat: otherInfo1['genres'] = ph.clean_html(lst_dat[0])			
			lst_dat=re.findall("<span>IMDB</span>(.*?)</a>", data, re.S)
			if lst_dat: otherInfo1['rating'] = ph.clean_html(lst_dat[0])				
			lst_dat=re.findall("<span>قصة العمل</span>(.*?)</div>", data, re.S)
			if lst_dat: desc = ph.clean_html(lst_dat[0])			
			

		icon = cItem.get('icon')
		title = cItem['title']		
		return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]
		
		
	def get_links(self,cItem): 	
		urlTab = []
		baseUrl=cItem['url']
		post_data = {'wtchBtn':''}
		sts, data = self.getPage(baseUrl,post_data=post_data)
		if sts:	
			#printDBG('data='+data)
			_data = re.findall('<li class="server.*?data-q="(.*?)".*?data-num=(.*?)>(.*?)</li>',data, re.S)
			for (q,n,titre) in _data:
				titre = self.cleanHtmlStr(titre)
				titre = titre.replace('سيتم عرضة بعد الانتهاء من معالجة الفيديو','').strip()
				q = q.strip()
				n = n.strip()
				post_data = q+'|'+n
				urlTab.append({'name':titre, 'url':'hst#tshost#'+baseUrl+'|'+post_data, 'need_resolve':1,'type':''})					
		return urlTab	
		

	def getVideos(self,videoUrl):
		urlTab = []
		url=self.MAIN_URL+'/wp-content/themes/Shahid%2B/Ajax/server-single.php'
		referer,q,n=videoUrl.split('|')
		post_data = {'q':q,'i':n,'out':'0'}
		header = {'Host': self.MAIN_URL.replace('https://','').replace('http://',''), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0','Accept': '*/*',\
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',\
		'X-Requested-With': 'XMLHttpRequest','Origin': self.MAIN_URL,'Connection': 'keep-alive','Referer': referer}
		params = dict(self.defaultParams) 
		params['header']=header
		sts, data = self.getPage(url,params,post_data=post_data)
		if sts:
			printDBG('data='+data)
			Liste_els = re.findall('src=["\'](.*?)["\']', data, re.IGNORECASE)		
			if 	Liste_els:
				URL_= Liste_els[0]
				if URL_.startswith('//'): URL_='http:'+URL_
				urlTab.append((URL_,'1'))		
		return urlTab
			
	def start(self,cItem):      
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu0(cItem)
		if mode=='20':
			self.showmenu1(cItem)
		if mode=='30':
			self.showitms(cItem)			
		if mode=='31':
			self.showelms(cItem)			

