TITLE = 'DanceTrippin TV'
ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################
def Start():

	ObjectContainer.title1 = TITLE
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

####################################################################################################
@handler('/video/dancetrippin', TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()

	for genre in HTML.ElementFromURL('http://www.dancetrippin.tv/videos/dj-sets').xpath('//div[@id="genrelist"]/div[@class="genre"]/a/text()'):

		oc.add(DirectoryObject(
			key = Callback(Videos, genre=genre),
			title = genre
		))

	return oc

####################################################################################################
@route('/video/dancetrippin/videos')
def Videos(genre):

	oc = ObjectContainer(title2=genre)

	for video in HTML.ElementFromURL('http://www.dancetrippin.tv/videos/dj-sets').xpath('//div[@id="grid-content"]//a[@class="filter" and contains(., "%s")]/parent::div/parent::div/div[@class="image"]' % (genre)):

		title = video.xpath('./a/@title')[0]
		url = 'http://www.dancetrippin.tv%s' % (video.get('href'))
		thumb = video.get('style').split('background-image: url(')[-1].split(')')[0].replace('-thumb', '')

		if not thumb.startswith('http://'):
			thumb = 'http://www.dancetrippin.tv%s' % thumb

		oc.add(VideoClipObject(
			url = url,
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)
		))

	if len(oc) < 1:
		return ObjectContainer('Empty', 'This directory is empty')
	else:
		return oc
