#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############BIBLIOTECAS A IMPORTAR####################

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,urllib,urllib2,re
from BeautifulSoup import BeautifulSoup

#######################SETTINGS#########################
versao = '1.0'
addon_id = 'plugin.video.ouvirmusica'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
icon = fanart = addonfolder + '/icon.png'
url_base = 'https://ouvirmusica.com.br'

###################################################MENUS############################################

def Menu_inicial():
	addDir('[B]Generos Musicais[/B]',url_base,2,icon)
	addDir('[B]Buscar Artista[/B]','-',8,artfolder+'lupa.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(51)')

def Listar_generos(url):
 html = gethtml(url_base)
 menu = html.find("div", { "class" : "genre g-1055" })
 links = menu.findAll("li")
 for link in links:
		url = link.a['href']
		titulo = link.a.text
		addDir(titulo.encode('utf-8'),url_base+url,3,icon)
		xbmc.executebuiltin('Container.SetViewMode(51)')

def sub_menu(url):
	addDir('Tops',url,4,icon)
	addDir('Todos os artistas',url,5,icon)
	xbmc.executebuiltin('Container.SetViewMode(51)')
	
def tops(url):
	html = gethtml(url)
	soup = html.find("ul", { "class" : "list list--color list--num" })
	tops = soup.findAll("li")
	for top in tops:
		titulo = top.a.text
		url = top.a["href"]
		addDir(titulo.encode('utf-8'),url_base+url,6,icon)
		xbmc.executebuiltin('Container.SetViewMode(51)')
		
def artistas(url):
	html = gethtml(url)
	soup = html.find("ul", { "class" : "list--letter" })
	artistas = soup.findAll("a")
	for artista in artistas:
		titulo = artista.text
		url = artista["href"]
		addDir(titulo.encode('utf-8'),url_base+url,6,icon) 
		xbmc.executebuiltin('Container.SetViewMode(51)')

def listar_musicas(url):
	html = gethtml(url)
	soup = html.find("div", { "class" : "widget-playlist" })
	tops = soup.findAll("li", { "itemprop" : "track" })
	for top in tops:
		titulo = top.a.span.text
		url = top.a["href"]
		artist = top.b.text
		addDir(titulo.encode('utf-8'),titulo.encode('utf-8')+" "+artist.encode('utf-8'),7,icon,False)
		xbmc.executebuiltin('Container.SetViewMode(51)')	
		
def resolver(url):
	yt = "https://www.youtube.com/results?search_query="
	html = abrir_url(yt+url.replace(' ','%20'))
	idd = re.compile('" data-context-item-id="(.+?)"').findall(html)[0]	
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +idd)
	
def Pesquisar_playlist(url):
	keyb = xbmc.Keyboard('', 'Digite o nome do artista corretamente...')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'https://ouvirmusica.com.br/' + str(parametro_pesquisa)
		listar_musicas(url)	
		
 #####################################################FUNÇÕES############################################################

def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link	

def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

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
    Menu_inicial()
elif mode==2:
    Listar_generos(url)
elif mode==3: 
	sub_menu(url)
elif mode==4: 
	tops(url)
elif mode==5: 
	artistas(url)	
elif mode==6: 
	listar_musicas(url)	
elif mode==7: 
	resolver(url)
elif mode==8: 
	Pesquisar_playlist(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))