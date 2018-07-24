---
layout: page
title: Albums
permalink: /albums/
---

<div markdown="0">	
	<ul class="this">	
	{% for post in site.posts %}
		{% if post.tags contains "album" %}		   			
			<li class="arch-list"><a href="{{site.baseurl}}{{ post.url }}">{{ post.title }}</a>&nbsp;<time>{{ post.date | date:"%d %b" }}</time></li>	
		{% endif %}				
	{% endfor %}
	</ul>
</div>