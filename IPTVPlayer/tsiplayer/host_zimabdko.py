# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor
from Components.config import config
import re
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
import base64
from binascii import unhexlify
from hashlib import md5
from Plugins.Extensions.IPTVPlayer.libs.crypto.cipher.aes_cbc import AES_CBC
import urllib

def getinfo():
	info_={}
	info_['name']='Zimabdko.Com'
	info_['version']='1.1 20/10/2019'
	info_['dev']='RGYSoft'
	info_['cat_id']='202'
	info_['desc']='انمي + دراما اسياوية'
	info_['icon']='https://www.zimabdko.com/wp-content/themes/zimabdk/images/logo.png'
	info_['recherche_all']='0'
	info_['update']='Bugs Fix'
	return info_

def cryptoJS_AES_decrypt(encrypted, password, salt):
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    bs = 16
    key, iv = derive_key_and_iv(password, salt, 32, 16)
    cipher = AES_CBC(key=key, keySize=32)
    return cipher.decrypt(encrypted, iv)
	
	
class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'zimabdko.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
		self.MAIN_URL = 'https://www.zimabdko.com'
		self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
		#self.getPage = self.cm.getPage
		self.cacheLinks = {}


	def getPage(self,baseUrl, addParams = {}, post_data = None):
		i=0
		while True:
			printDBG('counttttt'+str(i))
			if addParams == {}: addParams = dict(self.defaultParams)
			origBaseUrl = baseUrl
			baseUrl = self.cm.iriToUri(baseUrl)
			addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
			sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
			printDBG(str(sts))
			if sts:
				break
			else:
				i=i+1
				if i>2: break
		return sts, data

		
	def showmenu0(self,cItem):
		hst='host2'
		img_=cItem['icon']
		cat_TAB = [
					{'category':hst,'title': 'أفلام الأنيمي'    ,'mode':'30','url':self.MAIN_URL+'/anime/'},
					{'category':hst,'title': 'الأنميات'        ,'mode':'30','url':self.MAIN_URL+'/series/'},
					{'category':hst,'title': 'آخر الحلقات'    ,'mode':'30','url':self.MAIN_URL+'/episodes/'},					
					{'category':hst,'title': 'الدراما الأسيوية','mode':'30','url':self.MAIN_URL+'/asian-movies/'},					
					{'category':'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
					]
		self.listsTab(cat_TAB, {'import':cItem['import'],'icon':img_})						
		
	def showitms(self,cItem):
		url1=cItem['url']
		page=cItem.get('page',1)
		if page>0:
			sts, data = self.getPage(url1+'page/'+str(page)+'/')
		else:
			sts, data = self.getPage(url1)
		if sts:
			if 'class="movies-servers' not in data:
				films_list = re.findall('class="one-poster.*?href="(.*?)".*?src="(.*?)".*?<h2>(.*?)</h2>.*?hover-poster.*?>(.*?)</div>', data, re.S)		
				i=0
				for (url,image,titre,desc_) in films_list:
					desc=''
					i=i+1
					inf_list = re.findall('<span.*?>(.*?)</span>', desc_, re.S)		
					for elm in inf_list:
						if ph.clean_html(elm) !='':
							if 'fa-star' in elm:
								desc=desc+'Rating: '+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'
							elif 'fa-eye' in elm:
								desc=desc+'View: '+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'
							else:
								desc=desc+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'			
					#if not url.startswith('http'): url =  self.MAIN_URL+url
					self.addDir({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','url': url,'title':ph.clean_html(titre),'desc':desc,'icon':image,'hst':'tshost','mode':'30','page':-1,'EPG':True})	
				if (i>17) and (page >0):
					self.addDir({'import':cItem['import'],'title':'Next Page','page':page+1,'category' : 'host2','url':url1,'icon':cItem['icon'],'mode':'30'} )									
			else:
				self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','url': url1,'title':cItem['title'],'desc':cItem['desc'],'icon':cItem['icon'],'hst':'tshost'})	
					
	
	def SearchResult(self,str_ch,page,extra):
		url_=self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
		sts, data = self.getPage(url_)
		if sts:
			films_list = re.findall('class="one-poster.*?href="(.*?)".*?src="(.*?)".*?<h2>(.*?)</h2>.*?hover-poster(.*?)</div>', data, re.S)		
			for (url,image,titre,desc_) in films_list:
				desc=''
				inf_list = re.findall('<span.*?>(.*?)</span>', desc_, re.S)		
				for elm in inf_list:
					if 'fa-star' in elm:
						desc=desc+'Rating: '+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'
					elif 'fa-eye' in elm:
						desc=desc+'View: '+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'
					else:
						desc=desc+tscolor('\c00????00')+ph.clean_html(elm)+tscolor('\c00??????')+'\\n'			

				self.addDir({'import':extra,'good_for_fav':True,'category' : 'host2','url': url,'title':titre,'desc':desc,'icon':image,'hst':'tshost','EPG':True,'mode':'30','page':-1})	

		
	def get_links(self,cItem):
		urlTab = []	
		URL=cItem['url']
		if config.plugins.iptvplayer.ts_dsn.value:
			urlTab = self.cacheLinks.get(URL, [])
		if urlTab == []:
			sts, data = self.getPage(URL)
			if sts:
				Liste_els = re.findall('class="movies-servers.*?<ul(.*?)</ul>', data, re.S)
				if Liste_els:		
					Liste_els_2 =  re.findall('data-serv="(.*?)".*?post="(.*?)">(.*?)</li>', Liste_els[0], re.S)
					for (code1,code2,srv) in Liste_els_2:
						if not config.plugins.iptvplayer.ts_dsn.value:
							urlTab.append({'name':'Server: '+ph.clean_html(srv), 'url':'hst#tshost#'+code2+'|'+code1, 'need_resolve':1})		
						else:
							urlTab0=self.getVideos(code2+'|'+code1)
							for elm in urlTab0:
								local =''
								printDBG('elm='+str(elm))
								url_ = elm[0]
								type_ = elm[1]
								name_ = gethostname(url_)
								if 'drive.google' in name_.lower(): name_= 'Google.Com'
								if 'zimabdko.' in url_:
									local='local'
									name_ = 'zimabdko.com'
								if type_ == '1':		
									urlTab.append({'name':'|Server: '+ph.clean_html(srv)+'| '+name_, 'url':url_, 'need_resolve':1,'type':local})	
			if config.plugins.iptvplayer.ts_dsn.value:
				self.cacheLinks[str(cItem['url'])] = urlTab
		return urlTab


	def getVideos(self,videoUrl):
		urlTab = []	
		code2,code1=videoUrl.split('|')
		url=self.MAIN_URL+'/wp-admin/admin-ajax.php?action=codecanal_ajax_request&post='+code2+'&serv='+code1
		sts, data = self.getPage(url)
		if sts:
			Liste_els = re.findall('src.*?["\'](.*?)["\']', data, re.S)
			if Liste_els:
				URL_ = Liste_els[0]
				if URL_.startswith('//'): URL_ = 'http:'+URL_
				if False:#'zimabdko.' in URL_:
					sts, data = self.getPage(URL_)
					if sts:
						lst_data = re.findall('data-en=.*?[\'"](.*?)[\'"].*?data-p=.*?[\'"](.*?)[\'"]', data, re.S)	
						if lst_data:
							code = urllib.unquote(lst_data[0][0])
							code = json_loads(code.strip())
							b = lst_data[0][1]
							printDBG('code= '+str(code)+' | pass= '+b)
							ciphertext = base64.b64decode(code['ct'])
							iv = unhexlify(code['iv'])
							salt = unhexlify(code['s'])
							decrypted = cryptoJS_AES_decrypt(ciphertext, b, salt)
							printDBG('decrypted= '+decrypted)
							URL = decrypted.replace('\/','/').replace('"','')
							sts, data = self.getPage(URL)
							if sts:	
								printDBG('data= '+data)
								lst_data = re.findall('file":"(.*?)"', data, re.S)	
								if lst_data:
									urlTab.append((lst_data[0],'3')) 
				else:
					urlTab.append((URL_,'1'))
		return urlTab		
	def getArticle(self, cItem):
		printDBG("cima4u.getVideoLinks [%s]" % cItem) 
		otherInfo1 = {}
		desc= cItem['desc']	
		sts, data = self.getPage(cItem['url'])
		if sts:
			lst_dat=re.findall('class="head-s-meta-first(.*?)</div>', data, re.S)
			if lst_dat:
				lst_dat2=re.findall('<span>(.*?)<span>(.*?)</span>', lst_dat[0], re.S)
				for (x1,x2) in lst_dat2:
					if 'تقييم'  in x1: otherInfo1['imdb_rating'] = ph.clean_html(x2)
					if 'الدولة'  in x1: otherInfo1['country'] = ph.clean_html(x2)			
					if 'حالة'  in x1: otherInfo1['status'] = ph.clean_html(x2)					
					if 'اللغة'  in x1: otherInfo1['language'] = ph.clean_html(x2)
					if 'سنة' in x1: otherInfo1['year'] = ph.clean_html(x2)					
					if 'مدة'  in x1: otherInfo1['duration'] = ph.clean_html(x2)				


			lst_dat=re.findall('class="head-s-meta-last(.*?)</div>', data, re.S)
			if lst_dat:
				lst_dat2=re.findall('<span(.*?)<a.*?>(.*?)</span>', lst_dat[0], re.S)
				for (x1,x2) in lst_dat2:
					if 'الجودة'  in x1: otherInfo1['quality'] = ph.clean_html(x2)
					if 'الفئة' in x1: otherInfo1['age_limit'] = ph.clean_html(x2)			
					if 'السنة'  in x1: otherInfo1['year'] = ph.clean_html(x2)					
				
					
			lst_dat=re.findall('class="head-s-meta-ctas.*?>(.*?)</div>', data, re.S)
			if lst_dat:		
				otherInfo1['genres'] = ph.clean_html(lst_dat[0])				
										
			lst_dat=re.findall('class="head-s-story.*?>(.*?)</div>', data, re.S)
			if lst_dat:		
				desc=ph.clean_html(lst_dat[0])

		icon = cItem.get('icon')
		title = cItem['title']		
		return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]

	
	def start(self,cItem):      
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu0(cItem)
		if mode=='30':
			self.showitms(cItem)			
			
