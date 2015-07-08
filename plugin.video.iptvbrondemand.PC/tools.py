# -*- coding: UTF-8 -*-
import urllib2, re
import requestsX
import mechanize
import cookielib


def abrir_url2(url):
	# Browser
	br = mechanize.Browser()
	
	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	
	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	
	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	
	# Want debugging messages?
	#br.set_debug_http(True)
	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)
	
	# User-Agent (this is cheating, ok?)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	r = br.open(url)
	return r.read()

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def exists(path):
    r = requestsX.head(path)
    return r.status_code == requestsX.codes.ok

def teste_url(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read(20)
		response.close()
		return True
	except:
		return False


spc = (('&#192;','A'),	('&#193;','A'),	('&#194;','A'),	('&#195;','A'),	('&#196;','A'),	('&#199;','C'),	('&#200;','E'),	('&#201;','E'), ('&#198;','AE'),
	('&#202;','E'),	('&#203;','E'),	('&#204;','I'),	('&#205;','I'),	('&#207;','I'),	('&#217;','U'),	('&#218;','U'),	('&#220;','U'),
	('&#219;','U'),	('&#224;','a'),	('&#225;','a'),	('&#226;','a'),	('&#227;','a'),	('&#228;','a'),	('&#231;','ç'),	('&#232;','e'),
	('&#233;','e'),	('&#234;','e'),	('&#235;','e'),	('&#236;','i'),	('&#237;','i'),	('&#238;','i'),	('&#239;','i'),	('&#242;','o'),
	('&#243;','o'),	('&#244;','o'),	('&#245;','o'),	('&#249;','u'),	('&#250;','u'),	('&#251;','u'),	('&#252;','u'),	('&#221;','Y'),	('&#253;','y'), ('A&#161;','a'),('A&#173;','i'),('A&#169;','e'))

def html_replace_clean(s):
	s = cleanHtml(s)
	for code,caracter in spc:
		s = s.replace(code,caracter)
	return s

def cleanHtml(dirty):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean