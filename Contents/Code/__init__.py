TITLE = 'Dance Trippin'
ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################
def Start():

	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'

####################################################################################################
@handler('/video/dancetrippin', TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer(view_group='List')

	for category in HTML.ElementFromURL('http://player.dancetrippin.tv/').xpath('//ul[@class="video-categories-list"]//a'):
		title = category.xpath('./text()')[0]
		category_id = category.xpath('./@href')[0].strip('#')

		if category_id in ('other'):
			continue

		oc.add(DirectoryObject(
			key = Callback(Videos, title=title, category_id=category_id),
			title = title
		))

	return oc

####################################################################################################
@route('/video/dancetrippin/{category_id}')
def Videos(title, category_id):

	oc = ObjectContainer(title2=title, view_group='InfoList')

	for video in JSON.ObjectFromURL('http://player.dancetrippin.tv/video/list/%s/' % category_id):

		if not video['title']:
			continue

		title = video['title']
		url = 'http://player.dancetrippin.tv/video/%s/#%s' % (video['slug'], category_id)
		summary = String.DecodeHTMLEntities(String.StripTags(video['description'])).strip()

		if video['image']:
			thumb = 'http://player.dancetrippin.tv/media/%s' % video['image']

		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)
		))

	if len(oc) < 1:
		return ObjectContainer('Empty', 'This directory is empty')
	else:
		return oc
