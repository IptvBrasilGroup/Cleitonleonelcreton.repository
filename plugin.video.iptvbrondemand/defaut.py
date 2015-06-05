#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,base64,xmltosrt,os
from BeautifulSoup import BeautifulStoneSoup,BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from xbmcgui import ListItem
from tools import *
import mechanize, cookielib, base64

import re, htmlentitydefs
h = HTMLParser.HTMLParser()


versao = '1.1'
addon_id = 'plugin.video.iptvbrondemand'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
filmes_base = 'http://www.filmesonline2.com/category/acao/'
series_base = 'http://assistirserieshd.com/'
 

###################################################MENUS############################################

	
def  menus():        		
	dialog = xbmcgui.Dialog()
	dialog.ok("SEJAM BEM VINDOS", "PRONTOS PARA CURTIREM OS MELHORES CANAIS DE TV,FILMES,SÉRIES,DESENHOS,ANIMES,FUTEBOL E LUTAS DO UFC EM CASA ?                                                                                               ENTÃO PREPAREM A PIPOCA QUE É HORA DO SHOW !!!")
	addDir('FILMES HD/SD','-',24,artfolder + 'Movies-icon.png')	
	addDirM('SÉRIES HD/SD','-',5,artfolder + 'Icon_series.png')	
	addDir('EVENTOS AO VIVO','-',6,artfolder + 'live-events.png')
	addDir('ANIMAÇÃO','-',15,artfolder + 'animacao.png')	
	
	
def  filmes_hd_sd():
	addDir('FILMES HD','-',2,artfolder + 'Movies-icon.png')
	addDir('FILMES SD','-',4,artfolder + 'Movies-icon.png')	
	

def  temporarios():
	dialog = xbmcgui.Dialog()
	dialog.ok("FILMES VARIADOS", "OS FILMES A SEGUIR SÃO DE BAIXA QUALIDADE,SE DESEJAR ASSISTIR EM QUALIDADE FULL HD VÁ PARA A OPÇÃO FILMES HD,OU SE DESEJAR CONTINUAR CLICK EM OK!!!")
	addDir('FILMES VARIADOS','https://copy.com/hmyyzK71z8yMvo8S?download=1',3,artfolder + 'Movies-icon.png')
	addDir('FILMES SD','-',8,artfolder + '2k.png')	

	
def  series():
	dialog = xbmcgui.Dialog()
	dialog.ok("SÉRIES ON DEMAND", "                   SUAS SÉRIES FAVORITAS A UM CLICK!!!")
	addDirM('SÉRIES HD','-',16,artfolder + 'Icon_series.png')
	addDirM('SÉRIES HD POR LETRA','-',23,artfolder + 'Icon_series.png')	
	addDir('SÉRIES SD','http://www.armagedomfilmes.biz/?cat=21|1',10,artfolder + 'Icon_series.png')	
	addDirM('PESQUISAR SÉRIES HD','-',30,artfolder + 'lupa.png')
	addDir('PESQUISAR SÉRIES SD','-',14,artfolder + 'lupa.png')	
	

def  categorias():
	dialog = xbmcgui.Dialog()
	dialog.ok("FILMES SOB DEMANDA", "SELECIONE A SEGUIR A CATEGORIA DO FILME DESEJADO !!!")
	addDir('AÇÃO','https://copy.com/Iyt3UBHMKPehfPPs?download=1',3,artfolder + 'acao.jpg')
	addDir('ANIMAÇÃO','https://copy.com/rdkdvoVAFOoD6FVu?download=1',3,artfolder + 'animacao.jpg')
	addDir('AVENTURA','https://copy.com/RK9DFiXkF6BRenUv?download=1',3,artfolder + 'AVENTURA.jpg')
	addDir('COMÉDIA','https://copy.com/PMDC1RJbl06erivh?download=1',3,artfolder + 'comedia.jpg')
	addDir('DRAMA','https://copy.com/VQzV2J4YDwigMRor?download=1',3,artfolder + 'DRAMA.jpg')
	addDir('GUERRA','https://copy.com/e4gfUvkzwIVKDvCH?download=1',3,artfolder + 'GUERRA.jpg')
	addDir('NACIONAL','https://copy.com/vgLne99gBhJlkQyE?download=1',3,artfolder + 'NACIONAL.jpg')
	addDir('RELIGIOSO','https://copy.com/eolYU1Zfh6sSOT3L?download=1',3,artfolder + 'RELIGIOSO.jpg')
	addDir('ROMANCE','https://copy.com/KgOtLnPaaKPqFUp4?download=1',3,artfolder + 'ROMANCE.jpg')
	addDir('SUSPENSE','https://copy.com/NaVFwAKelkVEmC4O?download=1',3,artfolder + 'SUSPENSE.jpg')
	addDir('TERROR','https://copy.com/HgCH4omqtdRAr76O?download=1',3,artfolder + 'TERROR.jpg')
	
	
def  eventos_ao_vivo():	
	dialog = xbmcgui.Dialog()
	dialog.ok("EVENTOS ESPORTIVOS","                     ASSISTA Á JOGOS E LUTAS AO VIVO !!!")
	addDir('FUTEBOL','https://copy.com/TOyFN7PDhGvb9nVf?download=1',3,artfolder + 'futebol.png')
	addDir('LUTAS','https://copy.com/dvX6pkFBatyi2Q6T?download=1',3,artfolder + 'lutas.png')
	
	
def Animacao():	
	dialog = xbmcgui.Dialog()
	dialog.ok("ASSISTA AQUI:", "          OS MELHORES ANIMES E DESENHOS 24 HORAS!!!")
	addDir('ANIMES','-',25,artfolder + 'anime.png')	
	addDir('DESENHOS 24hrs','https://copy.com/0ZeS9pyD92GXM9rM?download=1',3,artfolder + 'Desenhos.png')


def Animes():
	addDir('CATEGORIAS','http://anitube.xpg.uol.com.br/categories',26,artfolder + 'categorias5.png')
	addDir('RECENTES','http://anitube.xpg.uol.com.br/videos/basic/mr',27,artfolder + 'recentes.png')
	addDir('BUSCAR ANIME','http://anitube.xpg.uol.com.br/',29,artfolder + 'pesquisa.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')


def Listar_categorias2(url):
	print url
	html = abrir_url(url)
	html = unicode(html, 'ascii', errors='ignore')
	soup = BeautifulSoup(html)

	a = []
	categorias = soup.findAll("li", { "class" : "mainList" })
	#resultados = content.findAll("td",  { "width" : "1%" })
	for categoria in categorias:
		temp = [categoria.a["href"],"%s" % (categoria.a.img["alt"].encode('ascii', 'ignore')),categoria.a.img["src"],categoria.a["title"]] 
		a.append(temp)
	total = len(a)
	
	for url2, titulo, img, plot in a:
		titulo = cleanHtml(titulo)
		addDir(titulo,url2,27,img,True,total,plot)
	pages = soup.find('ul',{ "id" : "pagination-flickr" }).findAll('a')
	print pages
	for prox_pagina in pages:
		if prox_pagina.text == 'Next':
			addDir('Página Seguinte >>',prox_pagina['href'],26,artfolder + 'next.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	

def Listar_episodios2(url):
	print url
	html = abrir_url(url)
	html = unicode(html, 'ascii', errors='ignore')
	soup = BeautifulSoup(html)

	a = []
	categorias = soup.findAll("li", { "class" : "mainList" })
	#resultados = content.findAll("td",  { "width" : "1%" })
	for categoria in categorias:
		try:
			temp = [categoria.a["href"],"%s" % (categoria.a.img["alt"].encode('ascii', 'ignore')),categoria.a.img['src'],''] 
			a.append(temp)
		except:
			pass
	a.sort()
	total = len(a)
	
	for url2, titulo, img, plot in a:
		titulo = cleanHtml(titulo)
		addDir(titulo,url2,28,img,True,total,plot)
	try:
		pages = soup.find('ul',{ "id" : "pagination-flickr" }).findAll('a')
		for prox_pagina in pages:
			if prox_pagina.text == 'Next':
				addDir('Página Seguinte >>',prox_pagina['href'],27,artfolder + 'next.png')
	except:
		pass
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	

def Resolve_episodio(url):
	print url
	html = abrir_url(url)
	xml_url = "http://anitube.xpg.uol.com.br/nuevo/econfig.php?key=" + re.findall(r'src="http://anitube.xpg.uol.com.br/embed/(.+?)"',html)[0]
	xml = abrir_url(xml_url)
	soup = BeautifulSoup(xml)
	file_url = ''
	filehd_url = ''
	image = ''
	try:
		file_url = soup.config.file.text
	except:
		pass
	try:
		filehd_url = soup.config.filehd.text
	except:
		pass
	try:
		image = soup.config.image.text
	except:
		pass
	if filehd_url:
		addLink('HD', filehd_url, image)
	if file_url:
		addLink('SD', file_url, image)
		

def Pesquisa():
	keyb = xbmc.Keyboard('', 'Pesquisar...')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://anitube.xpg.uol.com.br/search/?search_id=' + str(parametro_pesquisa)
		Listar_episodios(url)	
	
	
def Listar_categorias_series(url=series_base):
 print url
 html = abrir_url2(url)
 #html = html.encode('ascii','xmlcharrefreplace')
 soup = BeautifulSoup(html,convertEntities=BeautifulStoneSoup.XML_ENTITIES)

 a = []
 menu = soup("ul", { "class" : "SubMenu" })[0]
 #print menu
 links = menu("a")
 #resultados = content.findAll("td",  { "width" : "1%" })
 for link in links:
  if not link['href'] == '#' and not html_replace_clean(link.text.encode('ascii','xmlcharrefreplace')) == 'Pagina Inicial':
   #print link['href']
   addDirM(html_replace_clean(link.text.encode('ascii','xmlcharrefreplace')),link['href'],17,'https://copy.com/AalWGHh9t4MPy9Nr?download=1',len(links),True)
 xbmcplugin.setContent(int(sys.argv[1]), 'movies')
 xbmc.executebuiltin('Container.SetViewMode(51)')
 
 
def Listar_categorias_series_letra(url=series_base):
 print url
 html = abrir_url(url)
 #html = html.encode('ascii','xmlcharrefreplace')

 soup = BeautifulSoup(html,convertEntities=BeautifulStoneSoup.XML_ENTITIES)

 a = []
 links = soup("a", { "rel" : "nofollow" })
 #ow = open('G:\html_list\series.html', 'w')
 #ow.write(str(links))
 #ow.close()
 #print links
 #print menu
 #resultados = content.findAll("td",  { "width" : "1%" })
 for link in links:
  if len(link.text) == 1:
   #print link['href']
   addDirM('Séries com a letra: '+ html_replace_clean(link.text.encode('ascii','xmlcharrefreplace')).upper(),series_base+link['href'],17,'https://copy.com/AalWGHh9t4MPy9Nr?download=1',len(links),True)
 xbmcplugin.setContent(int(sys.argv[1]), 'movies')
 xbmc.executebuiltin('Container.SetViewMode(51)') 
 
 
def listar_series2(url):
 print url
 html = abrir_url(url)
 #html = unicode(html, 'ascii', errors='ignore')
 soup = BeautifulSoup(html)

 a = []
 categorias = soup("div", { "id" : "Conteudo" })[0]
 #print str(categorias)

 series = categorias("div", { "class" : "amazingcarousel-image" })
 for serie in series:
  #print serie
  img = serie.img['src']
  titulo = html_replace_clean(serie.img['alt'].encode('ascii','xmlcharrefreplace'))#episodio.img['alt']
  url = serie.a['href']
  #addDirM(name,url,mode,iconimage,total=0,pasta=True)
  addDir(titulo,url,18,img,len(series),True)
  #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
  #xbmc.executebuiltin('Container.SetViewMode(500)')


def listar_episodios_series(url):
 #print url
 html = abrir_url(url)
 #html = unicode(html, 'ascii', errors='ignore')
 soup = BeautifulSoup(html)

 a = []
 categorias = soup("div", { "id" : "Conteudo" })[0]
 #print str(categorias)

 episodios = categorias("div", { "class" : "Episodio" })
 
 for episodio in episodios:
  img = episodio.img['src']
  titulo = html_replace_clean(episodio.img['alt'].encode('ascii','xmlcharrefreplace'))#episodio.img['alt']
  url = episodio.a['href']
  #addDir(name,url,mode,iconimage,total=0,pasta=True)
  addDirM(titulo,url,19,img,len(episodios),False)
 if len(episodios) == 0:
  addDirM('Esta temporada não tem episodios ainda...aguarde.','',0,'',0,False)
 links = soup("div", { "class" : "Temporadas" })[0]('a')
 if len(links) > 1:
    addDirM('---------------------------','',0,'',0,False)
 for link in links:
	if not link['href'] == '#':
	    addDirM("Temporada: " + link.string,link['href'],18,'',len(episodios)+1)

 xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
 xbmc.executebuiltin('Container.SetViewMode(503)')
 
 
def listar_series3(url):
 print url
 html = abrir_url(url)
 #html = unicode(html, 'ascii', errors='ignore')
 soup = BeautifulSoup(html)

 a = []
 categorias = soup("div", { "id" : "Conteudo" })[0]
 #print str(categorias)

 series = categorias("div", { "class" : "amazingcarousel-image" })
 for serie in series:
  #print serie
  img = serie.img['src']
  titulo = html_replace_clean(serie.img['alt'].encode('ascii','xmlcharrefreplace'))#episodio.img['alt']
  url = serie.a['href']
  #addDir(name,url,mode,iconimage,total=0,pasta=True)
  addDir(titulo,url,18,img,len(series),True)
  #xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
  #xbmc.executebuiltin('Container.SetViewMode(503)') 


def Resolve_episodio_serie(url):
	#print url
	pg = 0
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Trabalhando', 'Gerando playlist','Por favor aguarde...')
	pg += 10
	mensagemprogresso.update(pg)
	html = abrir_url(url)
	soup = BeautifulSoup(html)
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	pg += 10
	mensagemprogresso.update(pg)
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	pg += 10
	mensagemprogresso.update(pg)
	br.open(series_base)
	br.select_form(nr=0)
	br.form['senha']=base64.b64decode('MTIzNDU2')
	br.form['email']=base64.b64decode('YXJsZWlyYS5jYXN0cm9AZ21haWwuY29t')
	br.submit()
	pg += 10
	mensagemprogresso.update(pg)
	page = br.open(url).read()

	links = re.findall('src: "(.*?)"',page)
	pg += 10
	mensagemprogresso.update(pg)
	if links:
		for link in links:
		    listitem = xbmcgui.ListItem('Episodio', thumbnailImage='src')
		    listitem.setInfo('video', {'Title': 'Episodio'})
		    playlist.add(url=link, listitem=listitem, index=7)
		mensagemprogresso.update(100)
		xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
	else:
		mensagemprogresso.update(100)
		dialog = xbmcgui.Dialog()
		dialog.ok("Indisponivel", "Este ainda não esta disponivel, tente novamente em breve.") 
 

def Listar_programacao(url=filmes_base):
 print url
 html = abrir_url2(url)
 #html = html.encode('ascii','xmlcharrefreplace')
 soup = BeautifulSoup(html,convertEntities=BeautifulStoneSoup.XML_ENTITIES)

 a = []
 menu = soup("div", { "class" : "agrupador" })[0]
 #print menu
 links = menu("a")
 #resultados = content.findAll("td",  { "width" : "1%" })
 for link in links:
  if not link['href'] == '#' and not html_replace_clean(link.text.encode('ascii','xmlcharrefreplace')) == 'Pagina Inicial':
   #print link['href']
   addDir(html_replace_clean(link.text.encode('ascii','xmlcharrefreplace')),link['href'],9,'https://copy.com/9aPDiAF23J6XKems?download=1',len(links),True)
 xbmcplugin.setContent(int(sys.argv[1]), 'movies')
 xbmc.executebuiltin('Container.SetViewMode(51)')

 
def Listar_episodios(url):
 print url
 html = abrir_url2(url)
 #html = unicode(html, 'ascii', errors='ignore')
 soup = BeautifulSoup(html)

 a = []
 categorias = soup("div", { "class" : "box_item" })[0]
 #print categorias
 episodios = categorias("div", { "class" : "peli" })
 for episodio in episodios:
  img = episodio.img['src']
  titulo = html_replace_clean(episodio.img['alt'].encode('ascii','xmlcharrefreplace'))#episodio.img['alt']
  url = episodio.a['href']
  #addDir(name,url,mode,iconimage,total=0,pasta=True)
  addDir(titulo,url,13,img,False)
 pages = soup("a",{ "class" : "nextpostslink" })
 for prox_pagina in pages:
  addDir('Próxima Página >>',prox_pagina["href"],9,artfolder + 'next.png')
  
 xbmcplugin.setContent(int(sys.argv[1]), 'movies')
 xbmc.executebuiltin('Container.SetViewMode(500)')	
	

def listar_canais(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  img = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
                  print 'Img: ' + img
                  rtmp = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
                  print 'Link: ' + rtmp
                  addLink(nome,rtmp,img)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(500)")	
	  
	  
def listar_series(url):
	pagina = str(int(url.split('|')[1])+1)
	url = url.split('|')[0]

	soup = BeautifulSoup(abrir_url(url))
	content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
	series = content("div", { "class" : "bic-miniatura" })
	codigo_fonte = abrir_url(url)
	
	total = len(series)
	for serie in series:
		titulo = serie.a['title']
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
		try:
			addDir(titulo.encode('utf-8'),serie.a['href'],12,serie.img['src'],True,total)
		except:
			pass

	addDir('Página Seguinte >>','http://www.armagedomfilmes.biz/?cat=21&paged='+pagina+'|'+pagina,10,artfolder + 'next.png') 


def listar_temporadas(url):

	codigo_fonte = abrir_url(url)
	soup = BeautifulSoup(abrir_url(url))
	conteudo = BeautifulSoup(soup.find("ul", { "class" : "bp-series" }).prettify())
	temporadas = conteudo("li")
	
	total = len(temporadas)
	i=1
	print total
	
	while i <= total:
		temporada = conteudo("li", { "class" : "serie"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,11,img,True,total)
			except:
				pass
		i=i+1
		
		

def listar_series_f2(name,url):

	n = name.replace(' temporada','')
	
	soup = BeautifulSoup(abrir_url(url))
	content = BeautifulSoup(soup.find("li", { "class" : "serie"+n+"-code" }).prettify())
	episodios = content.findAll("a")
	print episodios[0]
	
	a = [] # url titulo img
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
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
		addDir(titulo,url2,13,'',False,total)
		
		
def listar_videos_series(url):
	codigo_fonte = abrir_url(url)

	soup = BeautifulSoup(abrir_url(url))
	lista_filmes = BeautifulSoup(soup.find("div", { "class" : "repeat" }).prettify())
	print lista_filmes
	series = lista_filmes.findAll("div", {"class":"miniatura"})
	print series
	#resultados = series.findAll("div",{ "id" : "quadrado" })
	a=[]
	for resultado in series:
		print 'href'
		print resultado
		try:
		    temp = ['http://www.cinefilmeshd.com/seriados/' + resultado.a["href"],"%s (%s)" % (resultado.h2.text.encode('ascii', 'ignore').capitalize(),resultado.span.text),resultado.text.encode('ascii', 'ignore'),resultado.img["src"]] 
		    a.append(temp)
		except:
		    temp = ['http://www.cinefilmeshd.com/seriados/' + resultado.a["href"],"%s" % (resultado["search"].encode('ascii', 'ignore').capitalize()),resultado.text.encode('ascii', 'ignore'),resultado.img["src"]] 
		    a.append(temp)
		
	total = len(a)
	for url2, titulo, plot, img in a:
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'")	
		addDir(titulo,url2,12,img,True,total,plot)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(500)')
		
		
def listar_videos_series_f2(url):

	codigo_fonte = abrir_url(url)
	soup = BeautifulSoup(abrir_url(url))
	conteudo = BeautifulSoup(soup.find("ul", { "id" : "filmes" }).prettify())
	temporadas = conteudo("li")
	
	total = len(temporadas)
	i=1
	print total
	
	while i <= total:
		temporada = conteudo("ul", { "class" : "series"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,11,img,True,total)
			except:
				pass
		i=i+1


def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url)
	try:
		if not 'dropvideo.com/embed/' in url:
			id_video = re.findall(r'<iframe src="http://www.dropvideo.com/embed/(.*?)/"',codigo_fonte)[0]
			codigo_fonte = abrir_url('http://www.dropvideo.com/embed/%s/' % id_video)
			url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
			url_legendas =	re.compile('var vsubtitle = "(.*?)";').findall(codigo_fonte)[0]
			print url_video
			print url_legendas
		else:
			codigo_fonte = abrir_url(url)
			url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
			url_legendas =	re.compile('var vsubtitle = "(.*?)";').findall(codigo_fonte)[0]
			print url_video
			print url_legendas			
	except:
		url_video = '-'
		url_legendas = '-'
	return [url_video,url_legendas]
	
def obtem_videobis(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'file: "(.*?)"',codigo_fonte)[1]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url)
	
	try:
		video = re.findall(r'|post|(.*?)',codigo_fonte)[0]
		print video
		url_video = "http://fs013.dropvideo.com/v/"+video+".mp4"
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_url_Dropvideo(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
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

def obtem_videopw(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_shared2(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'src:"(.*?)"',codigo_fonte)[0]
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

def player(name,url):
	
	try:
		dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
		Dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
		dropmega = r'src=".*?drop.*?id=(.*?)"'
		neodrive = r'src="(.*?neodrive.*?/embed.*?)"'
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		videobis = r'SRC="(.*?videobis.*?/embed.*?)"'
		videopw = r'src=".*?videopw.*?id=(.*?)"'
		shared2 = r'src=".*?shared2.*?/embed/(.*?)"'
		cloudzilla = r'cloudzilla.php.id=(.*?)"'
		cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('TRABALHANDO', 'Abrindo stream','Por favor aguarde...')
		mensagemprogresso.update(33)
		links = []
		hosts = []
		matriz = []
		codigo_fonte = abrir_url(url)
		
		try:
			links.append(re.findall(dropvideo, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://www.dropvideo.com/embed/'+re.findall(dropmega, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://videopw.com/e/'+re.findall(videopw, codigo_fonte)[0])
			hosts.append('Videopw')
		except:
			pass
			
		try:
			links.append('http://www.shared2.net/embed/'+re.findall(shared2, codigo_fonte)[0])
			hosts.append('shared2')
		except:
			pass			
			
		try:
			links.append('http://www.dropvideo.com/embed/'+re.findall(Dropvideo, codigo_fonte)[0])
			hosts.append('Dropvideo')
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
			
		if not hosts:
			return
		
		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
		
		if index == -1:
			return
		
		url_video = links[index]
		mensagemprogresso.update(66)
		
		print 'Player url: %s' % url_video
		if 'dropvideo.com/embed' in url_video:
			matriz = obtem_url_dropvideo(url_video)   # esta linha está a mais
		elif 'cloudzilla' in url_video:
			matriz = obtem_cloudzilla(url_video)
		elif 'videobis' in url_video:
			matriz = obtem_videobis(url_video)
		elif 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'videopw' in url_video:
			matriz = obtem_videopw(url_video)
		elif 'shared2' in url_video:
			matriz = obtem_shared2(url_video)			
		elif 'Dropvideo' in url_video:
			matriz = obtem_url_vidzi(url_video)			
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
		
		listitem = xbmcgui.ListItem() # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		#try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
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
		listar_series_f2(url)


def pesquisa_serie_sd():
	keyb = xbmc.Keyboard('', 'faca a procura') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto Ã©, escapa os parametros necessarios para ser incorporado num endereÃ§o url
		url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa) #nova definicao de url. str forÃ§a o parametro de pesquisa a ser uma string
		print url
		soup = BeautifulSoup(abrir_url(url))
		content = BeautifulSoup(soup.find("div", { "class" : "bic-miniaturas" }).prettify())
		series = content("div", { "class" : "bic-miniatura" })
		codigo_fonte = abrir_url(url)

		total = len(series)
		for serie in series:
			titulo = serie.a['title']
			titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
			try:
				addDir(titulo.encode('utf-8'),serie.a['href'],12,serie.img['src'],True,total)
			except:
				pass


def pesquisa_serie_hd():
	keyb = xbmc.Keyboard('', 'O que está procurando?...')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'http://assistirserieshd.com/busca.php?busca=' + str(parametro_pesquisa)
		listar_series2(url)
	  
	  
		###################################################################################	  
	  
	  
def addDirM(name,url,mode,iconimage,total=0,pasta=True):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)	  
	  
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link	

def real_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.geturl()
	response.close()
	return link
	
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	
	
	
############################################################################################################
#                                               GET PARAMS                                                 #
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


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)


###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode==None or url==None or len(url)<1:
    print ""
    menus()

elif mode==2:
	print ""
	categorias()	
	
elif mode==3: 
	print ""
	listar_canais(url)
	
elif mode==4: 
	print ""
        temporarios()
	
elif mode==5:
	print ""
	series()
	
elif mode==6:
	print ""
	eventos_ao_vivo()

elif mode==7:
	print ""
	listar_categorias()
	
elif mode==8:
	print ""
	Listar_programacao()

elif mode==9:
	print ""
	Listar_episodios(url)	
	
elif mode==10:
	listar_series(url)
	
elif mode==11:
	print ""
	listar_series_f2(name,url)

elif mode==12:
	print "Mode 12"
	listar_temporadas(url)

elif mode==13:
	print ""
	player(name,url)

elif mode==14:
	print ""
	pesquisa_serie_sd()

elif mode==15:
	print ""
	Animacao()

elif mode==16:
    Listar_categorias_series()

elif mode==17:
    print ""
    listar_series2(url)

elif mode==18:
    print ""
    listar_episodios_series(url)

elif mode==19:
    Resolve_episodio_serie(url)

elif mode==20:   
        print ""
	listar_videos_series(url)
	
elif mode==21:
    listar_videos_series_f2(url)

elif mode==22:
    print ""
    listar_series3(url)

elif mode==23:
    Listar_categorias_series_letra()

elif mode==24:
    filmes_hd_sd()

elif mode==25:
    Animes()

elif mode==26:
	print "Mode: 26 - Listar categorias2"
	Listar_categorias2(url)
	
elif mode==27:
	print "Mode: 27 - Listar episodios2 "
	Listar_episodios2(url)

elif mode==28:
	print "Mode: 28 - Resolve episodio"
	Resolve_episodio(url)

elif mode==29:
	print 'Mode: 29 - Pesquisa'
	Pesquisa()

elif mode==30:
	print ""
	pesquisa_serie_hd()	
	

	


	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
