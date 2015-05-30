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
from BeautifulSoup import BeautifulSoup
h = HTMLParser.HTMLParser()


versao = '1.0.0'
addon_id = 'plugin.video.iptvbrondemand'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
 

###################################################MENUS############################################

	
def  menus():        		
	dialog = xbmcgui.Dialog()
	dialog.ok("SEJAM BEM VINDOS", "PRONTOS PARA CURTIREM OS MELHORES CANAIS DE TV,FILMES,SÉRIES,DESENHOS,FUTEBOL E LUTAS DO UFC EM CASA ?                                                                                               ENTÃO PREPAREM A PIPOCA QUE É HORA DO SHOW !!!")
	addDir('FILMES HD','-',3,artfolder + 'Movies-icon.png')
	addDir('SÉRIES HD/SD','-',4,artfolder + 'Icon_series.png')
	addDir('FILMES SD','-',9,artfolder + 'Movies-icon.png')	
	addDir('EVENTOS AO VIVO','-',7,artfolder + 'live-events.png')
	addDir('DESENHOS 24hrs','-',11,artfolder + 'Desenhos.png')	
	
	

def  temporarios():
	dialog = xbmcgui.Dialog()
	dialog.ok("FILMES VARIADOS", "OS FILMES A SEGUIR SÃO DE BAIXA QUALIDADE,SE DESEJAR ASSISTIR EM QUALIDADE FULL HD VÁ PARA A OPÇÃO FILMES HD,OU SE DESEJAR CONTINUAR CLICK EM OK!!!")
	addDir('FILMES VARIADOS','https://copy.com/hmyyzK71z8yMvo8S?download=1',2,artfolder + 'Movies-icon.png')
	addDir('FILMES 2k','http://www.filmes2k.info/01/',2,artfolder + '2k.png')	

	
def  series():
	dialog = xbmcgui.Dialog()
	dialog.ok("SÉRIES ON DEMAND", "                   SUAS SÉRIES FAVORITAS A UM CLICK!!!")
	addDir('SÉRIES SD','http://www.armagedomfilmes.biz/?cat=21|1',6,artfolder + 'Icon_series.png')
	addDir('PESQUISAR SÉRIES','-',8,artfolder + 'lupa.png')	
	

def  categorias():
	dialog = xbmcgui.Dialog()
	dialog.ok("FILMES SOB DEMANDA", "SELECIONE A SEGUIR A CATEGORIA DO FILME DESEJADO !!!")
	addDir('AÇÃO','https://copy.com/Iyt3UBHMKPehfPPs?download=1',2,artfolder + 'acao.jpg')
	addDir('ANIMAÇÃO','https://copy.com/rdkdvoVAFOoD6FVu?download=1',2,artfolder + 'animacao.jpg')
	addDir('AVENTURA','https://copy.com/RK9DFiXkF6BRenUv?download=1',2,artfolder + 'AVENTURA.jpg')
	addDir('COMÉDIA','https://copy.com/PMDC1RJbl06erivh?download=1',2,artfolder + 'comedia.jpg')
	addDir('DRAMA','https://copy.com/VQzV2J4YDwigMRor?download=1',2,artfolder + 'DRAMA.jpg')
	addDir('GUERRA','https://copy.com/e4gfUvkzwIVKDvCH?download=1',2,artfolder + 'GUERRA.jpg')
	addDir('NACIONAL','https://copy.com/vgLne99gBhJlkQyE?download=1',2,artfolder + 'NACIONAL.jpg')
	addDir('RELIGIOSO','https://copy.com/eolYU1Zfh6sSOT3L?download=1',2,artfolder + 'RELIGIOSO.jpg')
	addDir('ROMANCE','https://copy.com/KgOtLnPaaKPqFUp4?download=1',2,artfolder + 'ROMANCE.jpg')
	addDir('SUSPENSE','https://copy.com/NaVFwAKelkVEmC4O?download=1',2,artfolder + 'SUSPENSE.jpg')
	addDir('TERROR','https://copy.com/HgCH4omqtdRAr76O?download=1',2,artfolder + 'TERROR.jpg')
	
	
def  eventos_ao_vivo():	
	dialog = xbmcgui.Dialog()
	dialog.ok("EVENTOS ESPORTIVOS","                                                                      ASSISTA Á JOGOS E LUTAS AO VIVO")
	addDir('FUTEBOL','https://copy.com/TOyFN7PDhGvb9nVf?download=1',2,artfolder + 'futebol.png')
	addDir('LUTAS','https://copy.com/dvX6pkFBatyi2Q6T?download=1',2,artfolder + 'lutas.png')
	

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
	  
	  
def Desenhos():	
	dialog = xbmcgui.Dialog()
	dialog.ok("DESENHOS 24hrs", "                    ASSISTA AOS MELHORES DESENHOS 24 HORAS!!!")
	addDir('DESENHOS 24hrs','?download=1',2,artfolder + 'Desenhos.png')	  
	  
	  
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

	addDir('Página Seguinte >>','http://www.armagedomfilmes.biz/?cat=21&paged='+pagina+'|'+pagina,6,artfolder + 'next.png')


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
				addDir(titulo,url,10,img,True,total)
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
	
def obtem_cloudzilla(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def player(name,url,iconimage):
	
	try:
		dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
		dropmega = r'src=".*?drop.*?id=(.*?)"'
		neodrive = r'src="(.*?neodrive.*?/embed.*?)"'
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		videobis = r'SRC="(.*?videobis.*?/embed.*?)"'
		videopw = r'src=".*?videopw.*?id=(.*?)"'
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


def pesquisa_serie():
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
	  
	  
		###################################################################################	  
	  
	  
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

def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
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

elif mode==3:
	print ""
	categorias()	
	
elif mode==2: 
	print ""
	listar_canais(url)
	
elif mode==9: 
	print ""
        temporarios()
	
elif mode==4:
	print ""
	series()
	
elif mode==7:
	print ""
	eventos_ao_vivo()

elif mode==5:
	print ""
	listar_categorias()
	
elif mode==6:
	listar_series(url)
	
elif mode==10:
	print ""
	listar_series_f2(name,url)

elif mode==12:
	print "Mode 12"
	listar_temporadas(url)

elif mode==13:
	print ""
	player(name,url,iconimage)

elif mode==8:
	print ""
	pesquisa_serie()

elif mode==11:
	print ""
	Desenhos()	

	


	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
