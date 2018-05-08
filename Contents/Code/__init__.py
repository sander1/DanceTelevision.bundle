TITLE = "DanceTelevision"
ART = "art-default.jpg"
ICON = "icon-default.jpg"

####################################################################################################
def Start():

	ObjectContainer.title1 = TITLE
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"

####################################################################################################
@handler('/video/dancetelevision', TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	html = HTML.ElementFromURL('http://www.dancetelevision.net/videos')

	for genre in html.xpath('//div[@id="genrelist"]/div[@class="genre"]/a/text()'):

		videos = html.xpath('//div[@id="grid-content"]//a[@class="filter" and contains(., "{}")]/parent::div/parent::div/div[@class="image"]'.format(genre))

		if len(videos) < 1:
			Log(" --> Genre '{}' does not contain videos, skipping.".format(genre))
			continue

		oc.add(DirectoryObject(
			key = Callback(Videos, genre=genre),
			title = genre
		))

	return oc

####################################################################################################
@route('/video/dancetelevision/videos')
def Videos(genre):

	oc = ObjectContainer(title2=genre)

	for video in HTML.ElementFromURL('http://www.dancetelevision.net/videos').xpath('//div[@id="grid-content"]//a[@class="filter" and contains(., "{}")]/parent::div/parent::div/div[@class="image"]'.format(genre)):

		title = video.xpath('./a/@title')[0]
		url = 'http://www.dancetelevision.net{}'.format(video.get('href'))
		thumb = video.get('style').split('background-image: url(')[-1].split(')')[0].replace('-thumb', '')

		if not thumb.startswith('http://'):
			thumb = 'http://www.dancetelevision.net{}'.format(thumb)

		oc.add(VideoClipObject(
			url = url,
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)
		))

	if len(oc) < 1:
		return ObjectContainer(header="Empty", message="This directory is empty")
	else:
		return oc
