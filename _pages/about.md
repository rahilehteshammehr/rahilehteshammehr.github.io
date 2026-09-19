---
title: About me
permalink: /
nav: about
show_news: true
---
{% for paragraph in site.data.profile.bio %}
<p>{{ paragraph }}</p>
{% endfor %}

{% assign highlight = site.data.profile.highlight | default: '' | strip %}
{% if highlight != '' %}
<p class="profile-highlight"><strong>{{ highlight | escape }}</strong></p>
{% endif %}

<p class="intro-contacts"><a href="mailto:{{ site.data.profile.email }}">{% include icon.html name='mail' %}Email me</a><a href="{{ site.data.cv_pdf.published_file | relative_url }}">{% include icon.html name='download' %}Download CV (PDF)</a></p>

## Research interests

<ul class="interest-list">{% for interest in site.data.profile.interests %}<li>{{ interest }}</li>{% endfor %}</ul>

<div class="section-heading">
  <h2 id="research-experience">Research experience</h2>
  <a class="section-heading__link" href="{{ '/research/' | relative_url }}">All research &amp; projects <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
</div>

{% assign research = site.projects | where: 'category', 'Undergraduate research' | sort: 'order' %}
{% for project in research %}{% include project-entry.html project=project %}{% endfor %}

<div class="section-heading">
  <h2 id="beyond-physics">Beyond physics</h2>
  <a class="section-heading__link" href="{{ '/beyond-physics/' | relative_url }}">Read stories <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
</div>

{{ site.data.profile.personal }}

[fide-profile]: {{ site.data.profile.fide }}

## Get in touch

I'm exploring graduate study in experimental condensed matter physics and nanoscale materials. You can reach me at [{{ site.data.profile.email }}](mailto:{{ site.data.profile.email }}).
