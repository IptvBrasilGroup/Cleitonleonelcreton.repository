#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################################################################################################
#                                     BIBLIOTECAS A IMPORTAR E DEFINICÕES                                  #
############################################################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,xmltosrt,os,sys,urlparse,base64
import mechanize, cookielib
from mechanize import Browser
import urlresolver
import jsunpack
from resources.lib.libraries import client
from bs4 import BeautifulSoup
try:
    import json
except:
    import simplejson as json
h = HTMLParser.HTMLParser()

versao = '0.0.8'
addon_id = 'plugin.video.armagedompirata'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
fav = addonfolder + '/fav'
favseries = addonfolder + '/favseries'
favanimes = addonfolder + '/favanimes'
url_base = 'http://www.armagedomfilmes.biz/'
url_base2 = 'http://s19.postimg.org/'
url_base3 = 'https://docs.google.com/uc?export=download&id='
addonname = 'Armagedom Pirata'
line1 = "Lista de Favoritos limpa com sucesso"
line2 = "Favorito adicionado com sucesso"
line3 = "Favorito removido com sucesso"
icon = addonfolder + '/icon.png'
time = 2
username = urllib.quote(selfAddon.getSetting('username'))
password = selfAddon.getSetting('password')
server = base64.b64decode('aHR0cDovL2dvZmxpeC45Ni5sdC8=')

############################################################################################################
#                                                  MENUS                                                   #
############################################################################################################

def login(url, New=False):
        import mechanize
        import cookielib

        br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
	if not New:
	    cj.load(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies__Armagedom_pirata"), ignore_discard=False, ignore_expires=False)
        br.set_handle_equiv(True)
        br.set_handle_gzip(False)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        if New:
	    br.open(server)
	    br.select_form(nr=0)
	    br.form['username'] = username
	    br.form['password'] = password
	    br.submit()
	    cj.save(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies_Armagedom_pirata"))
        br.open(url)
        return br.response().read()

def menu():
    try:
        principal = login(server + 'pagina_privada.php', True)
        addDir("[B]Gêneros[/B]",url_base3+'0B4KWNSgTIdibVURvSGRRaWVBanc',2,url_base2+'5oj20tqw3/G_neros.png')
        addDir("[B]Lançamentos[/B]",url_base+'?cat=3236',3,url_base2+'mqbw2x5r7/Lan_amentos.png')	
        addDir("[B]Séries[/B]",url_base+'?cat=21',7,url_base2+'ygptkayjn/S_ries.png')
        addDir("[B]Animes[/B]",url_base+'?cat=36',12,url_base2+'oxg4qub1f/Animes.png')
        addDir("[B]Bluray[/B]",url_base+'?cat=5529',32,url_base2+'5gvf4bfxf/Bluray.png')
        addDir("[B]Coleções de Filmes[/B]",url_base+'?cat=4509',5,url_base2+'mio96eusj/Cole_es_de_Filmes.png')	
        addDir("[B]Favoritos[/B]",'-',22,url_base2+'rilped0f7/Favoritos.png')
        addDir("[B]Configurações[/B]",'-',33,url_base2+'kulxnoiub/config.png')	
        setViewMenu()
    except:
        addLink("Apenas para usuários cadastrados no site [COLOR blue]http://goflix.96.lt[/COLOR]","-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
        addLink("Caso já tenha login/senha, insira nas configurações do addon.","-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
        while xbmc.Player().isPlaying():
            time.sleep(1)		
	
def todas_categorias(url):	
	html = gethtml(url)
	soup = html.find("div",{"class":"bi-cat"})
	categorias = soup.findAll("li")
	for categoria in categorias:
		titulo = categoria.a.text
		url = categoria.a["href"]
		img = categoria.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,3,url_base2+img)
		setViewMenu()	
	
def listar_filmes(url):
    print url
    addDir("[B][COLOR red]PESQUISAR FILMES[/B][/COLOR]",'-',11,url_base2+'hzc0kwcwz/Pesquisar_Filmes.png')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    filmes = soup("div",{"class":"bic-miniatura"})
    for filme in filmes:
        titulo = filme.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = filme.a["href"]
        img = filme.img["src"]
        addDirf("[B]"+titulo.encode('utf-8')+"[/B]",url,4,img,False)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],3,url_base2+'597s7t4yr/Pr_xima_P_gina.png')		
        setViewFilmes()
		
def listar_filmes_bluray(url):
    print url
    addDir("[B][COLOR red]PESQUISAR FILMES[/B][/COLOR]",'-',11,url_base2+'hzc0kwcwz/Pesquisar_Filmes.png')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    filmes = soup("div",{"class":"bic-miniatura"})
    for filme in filmes:
        titulo = filme.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = filme.a["href"]
        img = filme.img["src"]
        addDirfb("[B]"+titulo.encode('utf-8')+"[/B]",url,4,img,False)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],3,url_base2+'597s7t4yr/Pr_xima_P_gina.png')		
        setViewFilmes()

def listar_filmes_colecoes(url):
    print url
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    filmes = soup("div",{"class":"bic-miniatura"})
    for filme in filmes:
        titulo = filme.a.text.replace('Assistir ','').replace('&#8211;',"-")
        url = filme.a["href"]
        img = filme.img["src"]
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,6,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],5,url_base2+'597s7t4yr/Pr_xima_P_gina.png')
        setViewFilmes()	


def listar_filmes_colecoes2(url):
    print url
    codigo_fonte = abrir_url(url)
    match = re.compile('<a title="(.+?)" href="(.+?)"><img src="(.+?)" alt=".+?" /></a>').findall(codigo_fonte)
    for titulo, url, img in match:	
	    addDircf(titulo.replace('Assistir ',''),url,4,img,False)
            setViewFilmes()
		
def listar_series(url):
    print url
    addDir("[B][COLOR red]PESQUISAR SÉRIES[/B][/COLOR]",'-',10,url_base2+'wl31959pf/Pesquisar_S_ries.png')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    series = soup("div",{"class":"bic-miniatura"})
    total = len(series)
    for serie in series:
        titulo = serie.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = serie.a["href"]
        img = serie.img["src"]
        addDirts("[B]"+titulo.encode('utf-8')+"[/B]",url,8,img,True,total)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],7,url_base2+'597s7t4yr/Pr_xima_P_gina.png')		
        setViewFilmes()

def listar_temporadas_series(url):
	print url
	html = gethtml(url)
	soup = html.find("ul",{"class":"bp-series"})
	temporadas = soup("li")
	total = len(temporadas)
	i=1
	print total
	while i <= total:
		temporada = soup("li",{"class":"serie"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,9,img,True,total)
			except:
				pass
		i=i+1
		setViewFilmes() 

def listar_episodios_series(name,url,iconimage):
	print url
	codigo = name.replace(' temporada','')
	html = gethtml(url)
	soup = html.find("li",{"class":"serie"+codigo+"-code"})
	episodios = soup("a")
	
	print episodios[0]
	
	a = []
	
	for episodio in episodios:
		try:
			xml = BeautifulSoup(abrir_url(episodio["href"]+'/feed'))
			title = xml.title.string.encode('utf-8').replace('Comentários sobre: Assistir ','')
			try:
				if "html" in os.path.basename(episodio["href"]):
					temp = [episodio["href"],title]
					a.append(temp)
			except:
				pass
		except:
			pass

	total = len(a)
	for url2, titulo, in a:
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','').replace('Comentários sobre: Asistir ','')
		addDir(titulo,url2,4,iconimage,False,total)
        setViewFilmes()

def listar_animes(url):
    print url
    addDir("[B][COLOR red]PESQUISAR ANIMES[/B][/COLOR]",'-',15,url_base2+'jic03m8v7/Pesquisar_Animes.png')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    animes = soup("div",{"class":"bic-miniatura"})
    for anime in animes:
        titulo = anime.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = anime.a["href"]
        img = anime.img["src"]
        addDirta("[B]"+titulo.encode('utf-8')+"[/B]",url,13,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],12,url_base2+'597s7t4yr/Pr_xima_P_gina.png')		
        setViewFilmes() 

def listar_temporadas_animes(name,url,iconimage):
	print url
	html = gethtml(url)
	soup = html.find("ul",{"class":"bp-series"})
	temporadas = soup("li")
	total = len(temporadas)
	i=1
	print total
	while i <= total:
		temporada = soup("li",{"class":"serie"+str(i)+"-code"})
		for temp in temporada:
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,14,iconimage,True,total)
			except:
				pass
		i=i+1
		setViewFilmes() 
	
def listar_episodios_animes(name,url,iconimage):	
	print url
	codigo = name.replace(' temporada','')
	html = gethtml(url)
	soup = html.find("li",{"class":"serie"+codigo+"-code"})
	episodios = soup("a")
	
	print episodios[0]
	
	a = []
	
	for episodio in episodios:
		try:
			xml = BeautifulSoup(abrir_url(episodio["href"]))
			title = xml.title.string.encode('utf-8').replace('Assistir ','')
			try:
				if "html" in os.path.basename(episodio["href"]):
					temp = [episodio["href"],title]
					a.append(temp)
			except:
				pass
		except:
			pass

	total = len(a)
	for url2, titulo, in a:
		titulo = titulo.replace('Assistir ','')
		addDir(titulo,url2,16,iconimage,False,total)
        setViewFilmes() 

def resolve_animes(name,url,iconimage):
	print url
	playlist = xbmc.PlayList(1)
	playlist.clear()	
	try:
		html = abrir_url(url)
		link = re.compile(r'<video src="(.+?)" width=".+?" height=".+?" controls autobuffer">').findall(html)[0]
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name.replace('Assistir o Filme: ','')})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
	    pass
		
def adicionar_favoritos_filmes(name,url,iconimage):
	arquivo = open(fav, 'r')
	texto = arquivo.readlines()
	texto.append(name+','+url+','+iconimage+','+'\n') 
	arquivo = open(fav, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line2, time, icon))	

def favoritos_filmes():
	arquivo = open(fav, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			rtmp = params[1]
			img = params[2]			
			addDirfvfilmes(nome,rtmp,4,img,False)
		except:
			pass
			setViewFilmes()

def limpar_lista_favoritos_filmes():
	arquivo = open(fav, 'r')
	ref = url
	linhas = arquivo.readlines()
	arquivo.close()
	arquivo = open(fav, 'w')
	for linha in linhas:
		if ref in linha:
			linhas.remove(linha)
			arquivo.writelines(linhas)
			arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line3, time, icon))			
	xbmc.executebuiltin("Container.Refresh")
	sys.exit(0)
	
def adicionar_favoritos_series(url):
	arquivo = open(favseries, 'r')
	texto = arquivo.readlines()
	texto.append(name+','+url+','+iconimage+','+'\n') 
	arquivo = open(favseries, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line2, time, icon))	

def favoritos_series():
	arquivo = open(favseries, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			rtmp = params[1]
			img = params[2]			
			addDirfvseries(nome,rtmp,8,img)
		except:
			pass	
	setViewFilmes()

def limpar_lista_favoritos_series():
	arquivo = open(favseries, 'r')
	ref = url
	linhas = arquivo.readlines()
	arquivo.close()
	arquivo = open(favseries, 'w')
	for linha in linhas:
		if ref in linha:
			linhas.remove(linha)
			arquivo.writelines(linhas)
			arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line3, time, icon))
	xbmc.executebuiltin("Container.Refresh")	
	sys.exit(0)

def adicionar_favoritos_animes(url):
	arquivo = open(favanimes, 'r')
	texto = arquivo.readlines()
	texto.append(name+','+url+','+iconimage+','+'\n') 
	arquivo = open(favanimes, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line2, time, icon))	

def favoritos_animes():
	arquivo = open(favanimes, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			rtmp = params[1]
			img = params[2]			
			addDirfvanimes(nome,rtmp,13,img)
		except:
			pass	
	setViewFilmes()

def limpar_lista_favoritos_animes():
	arquivo = open(favanimes, 'r')
	ref = url
	linhas = arquivo.readlines()
	arquivo.close()
	arquivo = open(favanimes, 'w')
	for linha in linhas:
		if ref in linha:
			linhas.remove(linha)
			arquivo.writelines(linhas)
			arquivo.close()
	xbmc.executebuiltin('Notification(%s, %s, %i, %s)'%(addonname,line3, time, icon))	
	xbmc.executebuiltin("Container.Refresh")
	sys.exit(0)	
	
def categoria_favorito():
    addDir("[B]Filmes Favoritos[/B]",'-',18,url_base2+'pn3igy0yr/Filmes_Favoritos.png')
    addDir("[B]Séries Favoritas[/B]",'-',24,url_base2+'edaslzvxf/S_ries_Favoritas.png')
    addDir("[B]Animes Favoritos[/B]",'-',27,url_base2+'jd88ty1k3/Animes_Favoritos.png')
    setViewMenu()
	
def trailer(name,url,iconimage):  
	    html = abrir_url(url)
	    link = re.compile(r'<iframe width=".+?" height=".+?" data-src=".+?://www.youtube.com/embed/(.+?)" frameborder=".+?" allowfullscreen>').findall(html)[0]
	    print link
	    xbmcPlayer = xbmc.Player()
	    xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id='+link)
		
def trailer2(name,url,iconimage):
	yt = "https://www.youtube.com/results?search_query="
	codigo_fonte = abrir_url(yt+'traileroficial'+name.replace(' ','%20'))
	print codigo_fonte
	a=[]
	idd = re.compile('" data-context-item-id="(.+?)"').findall(codigo_fonte)[0]
	print idd	
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id='+idd)	

def obtem_videobis(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'file: "(.*?)"',codigo_fonte)[1]
		return [url_video,"-"]
	except:
		return ["-","-"]
		
def obtem_neodrive(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_cloudzilla(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_openload(url):
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]

def obtem_videomega(url):
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]

def obtem_videott(url):
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]
		
def obtem_videobis(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'file: "(.*?)"',codigo_fonte)[1]
		return [url_video,"-"]
	except:
		return ["-","-"]
		
def obtem_videopw(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_vidto(url):
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]

def obtem_videowood(url):
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]		
	
def obtem_flashx(url):
    print url
    url = url.replace("embed-","").replace("-780x450.html","")
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]

def obtem_youwatch(url):
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]		

def player(name,url,iconimage):
	
	try:
		neodrive = r'src="(.*?neodrive.*?/embed.*?)"'
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		videobis = r'SRC="(.*?videobis.*?/embed.*?)"'
		videopw = r'src=".*?videopw.*?id=(.*?)"'
		cloudzilla = r'cloudzilla.php.id=(.*?)"'
		cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
		flashx = r'src="(.*?flashx.tv/.*?)"'
		openload = r'src="(.*?openload.co/embed/.*?)"'
		videomega = r'src=".*?videomega.tv/view.*?ref=(.*?)"'
		videott = r'src=".*?videott.*?id=(.*?)"'
		vidto = r'src=".*?vidto.me/embed-(.*?)"'
		videowood = r'src=".*?videowood.tv/embed/(.*?)"'
		youwatch = r'src=".*?youwatch.org/embed-(.*?)"'		
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Armagedon Pirata', 'Procurando fontes ativas para '+name,'Por favor aguarde...')
		mensagemprogresso.update(33)
		links = []
		hosts = []
		matriz = []
		codigo_fonte = abrir_url(url)
		
		try:
			links.append('http://videopw.com/e/'+re.findall(videopw, codigo_fonte)[0])
			hosts.append('Videopw')
		except:
			pass
			
		try:
			links.append(re.findall(videobis, codigo_fonte)[0])
			hosts.append('Videobis')
		except:
			pass
		
		try:
			links.append(re.findall(neodrive, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass
		
		try:
			links.append('http://neodrive.co/embed/'+re.findall(neomega, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass	
			
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla,codigo_fonte)[0])
			hosts.append('CloudZilla')
		except:
			pass
		
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla_t,codigo_fonte)[0])
			hosts.append('CloudZilla(Legendado)')
		except:
			pass
			
		try:
			links.append(re.findall(flashx, codigo_fonte)[0])
			hosts.append('Flashx')
		except:
			pass			
			
		try:
			links.append('http://videomega.tv/view.php?ref='+re.findall(videomega, codigo_fonte)[0])
			hosts.append('Videomega')
		except:
			pass			
			
		try:
			links.append(re.findall(openload, codigo_fonte)[0])
			hosts.append('Openload')
		except:
			pass
			
		try:
			links.append('http://youwatch.org/embed-'+re.findall(youwatch, codigo_fonte)[0])
			hosts.append('Youwatch')
		except:
			pass			

		try:
			links.append('http://www.video.tt/watch_video.php?v='+re.findall(videott, codigo_fonte)[0])
			hosts.append('Videott')
		except:
			pass

		try:
			links.append('http://vidto.me/embed-'+re.findall(vidto, codigo_fonte)[0])
			hosts.append('Vidto')
		except:
			pass

		try:
			links.append('http://videowood.tv/embed/'+re.findall(videowood, codigo_fonte)[0])
			hosts.append('Videowood')
		except:
			pass			
			
		if not hosts:
			return
		
		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
		
		if index == -1:
			return
		
		url_video = links[index]
		mensagemprogresso.update(66,'Resolvendo fonte para ' + name,'Por favor aguarde...')
		
		print 'Player url: %s' % url_video  
		if 'cloudzilla' in url_video:
			matriz = obtem_cloudzilla(url_video)
		elif 'videobis' in url_video:
			matriz = obtem_videobis(url_video)
		elif 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'videopw' in url_video:
			matriz = obtem_videopw(url_video)
		elif 'flashx.tv' in url_video:
			matriz = obtem_flashx(url_video)		
		elif 'openload.co/embed' in url_video:
			matriz = obtem_openload(url_video)	
		elif 'videomega' in url_video:
			matriz = obtem_videomega(url_video)
		elif 'video.tt' in url_video:
			matriz = obtem_videott(url_video)
		elif 'vidto' in url_video:
			matriz = obtem_vidto(url_video)
		elif 'videowood' in url_video:
			matriz = obtem_videowood(url_video)
		elif 'youwatch' in url_video:
			matriz = obtem_youwatch(url_video)			
		else:
			print "Falha: " + str(url_video)
		print matriz
		url = matriz[0]
		print url
		if url=='-': return
		legendas = matriz[1]
		print "Url do gdrive: " + str(url_video)
		print "Legendas: " + str(legendas)
		
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage) # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(url,listitem)
		#try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		if legendas != '-':
			if 'timedtext' in legendas:
				#legenda = xmltosrt.convert(legendas)
				#try:
					import os.path
					sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
					sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
					sub_file_xml = open(sfile_xml,'w')
					sub_file_xml.write(urllib2.urlopen(legendas).read())
					sub_file_xml.close()
					print "Sfile.srt : " + sfile_xml
					xmltosrt.main(sfile_xml)
					xbmcPlayer.setSubtitles(sfile)
				#except:
				#	pass
			else:
				xbmcPlayer.setSubtitles(legendas)
		#except:
		#	dialog = xbmcgui.Dialog()
		#	dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		#	pass
	except:
		print "erro ao abrir o video"
		print url_video
		pass

def pesquisar_series():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_series(url)
		
def pesquisar_filmes():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_filmes(url)

def pesquisar_animes():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_animes(url)

def config():
		selfAddon.openSettings()
		setViewMenu()
		sys.exit(0)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setViewMenu():
		xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
		opcao = selfAddon.getSetting('menuVisu')
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

def setViewFilmes():
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		opcao = selfAddon.getSetting('filmesVisu')
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")		

############################################################################################################
#                                                  FUNCÕES                                                 #
############################################################################################################
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup

def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	

def addDirf(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?url=%s&mode=21)'%(sys.argv[0], urllib.quote_plus(url))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addDirfb(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def addDircf(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def addDirfvfilmes(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR orange]Remover um Favorito do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=19&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	
	
def addDirfvseries(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR orange]Remover um Favorito do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=25&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def addDirfvanimes(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR orange]Remover um Favorito do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=28&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDirts(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=23&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def addDirta(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Adicionar a Favoritos do addon[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=26&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	contextMenuItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=31&iconimage=%s)'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	

############################################################################################################
#                                             MAIS PARÂMETROS                                              #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None


try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

try:        
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass


print "Mode: "+ str(mode)
print "URL: "+ str(url)
print "Name: "+ str(name)
print "Iconimage: "+ str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1:
    print ""
    menu()
elif mode==2:
	print ""
	todas_categorias(url)
elif mode==3:
    print  ""
    listar_filmes(url)
elif mode==4:
    print ""
    player(name,url,iconimage)
elif mode==5:
    print ""
    listar_filmes_colecoes(url)	
elif mode==6:
    print ""
    listar_filmes_colecoes2(url)
elif mode==7:
    print ""
    listar_series(url)
elif mode==8:
    print "Mode 8"
    listar_temporadas_series(url)
elif mode==9:
    print ""
    listar_episodios_series(name,url,iconimage)
elif mode==10:
    print ""
    pesquisar_series()
elif mode==11:
    print ""
    pesquisar_filmes()
elif mode==12:
    print ""
    listar_animes(url)
elif mode==13:
    print ""
    listar_temporadas_animes(name,url,iconimage)
elif mode==14:
    print ""
    listar_episodios_animes(name,url,iconimage)
elif mode==15:
    print ""
    pesquisar_animes()
elif mode==16:
    print ""
    resolve_animes(name,url,iconimage)
elif mode==17:
    print ""
    adicionar_favoritos_filmes(name,url,iconimage)
elif mode==18:
    print ""
    favoritos_filmes()	
elif mode==19:
    print ""
    limpar_lista_favoritos_filmes()
elif mode==21:
    print ""
    trailer(name,url,iconimage)
elif mode==22:
    print ""
    categoria_favorito()
elif mode==23:
    print ""
    adicionar_favoritos_series(url)
elif mode==24:
    print ""
    favoritos_series()	
elif mode==25:
    print ""
    limpar_lista_favoritos_series()
elif mode==26:
    print ""
    adicionar_favoritos_animes(url)
elif mode==27:
    print ""
    favoritos_animes()	
elif mode==28:
    print ""
    limpar_lista_favoritos_animes()
elif mode==31:
    print ""
    trailer2(name,url,iconimage)
elif mode==32:
    print  ""
    listar_filmes_bluray(url)
elif mode ==33:
    print"" 
    config()	
	
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))	