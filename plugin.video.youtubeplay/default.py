#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############BIBLIOTECAS A IMPORTAR####################

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,urllib,urllib2,re
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

#######################SETTINGS#########################
versao = '1.0'
addon_id = 'plugin.video.youtubeplay'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'


###################################################MENUS############################################
	

def menus():
	addDir('[B]MENU YOUTUBE[/B]','-',6,'http://orig12.deviantart.net/617e/f/2011/224/4/6/android_glass_folder_youtube_by_fandvd-d46ai44.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(51)')

#############youtube globo reporter###################
def menu_youtube():
	addDir('[B]YOUTUBE STREAMS[/B]','https://copy.com/snmrGYAkwcVRh7C6?download=1',8,'http://bisakomputer.com/wp-content/uploads/2014/08/youtube.png')
	addDir('[B]PESQUISAR STREAMS[/B]','-',2, 'http://www.shoppingportaldaserra.com.br/2013/img/lupa.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(51)')

def youtube(url):
	html = gethtml(url)
	soup = html.find("ol", {"class" : "section-list"})
	videos = soup.findAll("h3", {"class" : "yt-lockup-title "})
	for video in videos:
		url = video.a["href"].replace('/watch?v=','')
		titulo = video.a.text
		addDir(titulo.encode('utf-8'),url,41,'https://i.ytimg.com/vi/' + url + '/mqdefault.jpg',False)
	pagnavi = html.find("div", {"class" : "yt-uix-pager search-pager branded-page-box spf-link "})
	navi = pagnavi.find("a", {"data-link-type" : "next"})	
	addDir('Próxima Página','https://www.youtube.com' + navi["href"],40,'https://cdn3.iconfinder.com/data/icons/stroke/53/Fast-Forward-512.png')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(51)')
		
def player_youtube(url):
	xbmcPlayer = xbmc.Player()
        xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +url)
		
def pesquisar_youtube(url):
	keyb = xbmc.Keyboard('', 'O que está procurando?...')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		parametro_pesquisa=urllib.quote(search)
		url = 'https://www.youtube.com/results?search_query=' + str(parametro_pesquisa)
		youtube(url)
		

##############################################################################################################
##											FUNÇÕES															##
##############################################################################################################
def listar_videostxt(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1]
                  print 'Link: ' + rtmp
                  addDirPlayer(nome,rtmp,41,'https://i.ytimg.com/vi/' + rtmp + '/mqdefault.jpg',False)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(51)")
	
def listar_categorias(url):
 print url
 html = abrir_url(url)
 soup = BeautifulSoup(html)
 a = []
 menu = soup("div", { "class" : "Box" })[0]
 links = menu("li")
 for link in links:
   titulo = link.a["title"]
   url = link.a['href']
   img = link.a['img']
   addDir(titulo.encode('utf-8'),url,5,img,len(links))
 xbmcplugin.setContent(int(sys.argv[1]), 'movies')
 xbmc.executebuiltin('Container.SetViewMode(51)')	

	
#################################################################################################################

def getSoup(url):
    links = abrir_url(url).decode('utf8')
    return BeautifulSOAP(links,convertEntities=BeautifulStoneSoup.XML_ENTITIES)	  

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
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def addDirPlayer(name,url,mode,iconimage,pasta=False,total=1):
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
elif mode==1: 
	menus()
elif mode==2: 
	pesquisar_youtube(url)
elif mode==5: 
	listar_videostxt(url)
elif mode==6: 
	menu_youtube()
elif mode==7: 
	listar_videos_xml(url)
elif mode==8: 
	listar_categorias(url)	
elif mode==40:
	youtube(url)
elif mode==41:
	player_youtube(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
