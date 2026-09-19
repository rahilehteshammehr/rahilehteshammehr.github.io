---
title: Curriculum vitae
permalink: /cv/
nav: cv
description: Education, research, academic projects, awards, skills, teaching, and service of Rahil Ehtesham Mehr.
---
<div class="cv-print-identity"><p><strong>{{ site.data.profile.name }}</strong><br><a href="mailto:{{ site.data.profile.email }}">{{ site.data.profile.email }}</a></p></div>
<div class="cv-actions"><a class="button" href="{{ site.data.cv_pdf.published_file | relative_url }}" download>{% include icon.html name='download' %}Download CV (PDF)</a><button class="print-button" type="button" hidden>Print this page</button></div>
<p class="content-meta">Updated {{ site.data.cv.updated }}</p>
<nav class="cv-contents" aria-label="CV sections"><a href="#education">Education</a><a href="#research-experience">Research</a><a href="#academic-projects">Projects</a><a href="#honors--awards">Awards</a><a href="#teaching">Teaching</a><a href="#skills--languages">Skills</a><a href="#selected-coursework">Coursework</a><a href="#service">Service</a></nav>

## Education

<div class="cv-entry"><h3>{{ site.data.cv.education.degree }}</h3><p>{{ site.data.cv.education.institution }}, {{ site.data.cv.education.location }}</p><p class="content-meta">{{ site.data.cv.education.period }}</p><p>GPA: {{ site.data.cv.education.gpa }} ({{ site.data.cv.education.standing | downcase }})</p></div>

## Research interests

<ul class="interest-list">{% for interest in site.data.profile.interests %}<li>{{ interest }}</li>{% endfor %}</ul>

## Research experience

{% assign research = site.projects | where: 'category', 'Undergraduate research' | sort: 'order' %}
{% for project in research %}{% include project-entry.html project=project %}{% endfor %}

## Academic projects

{% assign projects = site.projects | where: 'category', 'Academic project' | sort: 'order' %}
{% for project in projects %}{% include project-entry.html project=project %}{% endfor %}

## Honors & Awards

{% for item in site.data.cv.honors %}<div class="cv-entry"><h3>{{ item.title }}</h3><p class="content-meta">{{ item.period }}</p><p>{{ item.detail }}</p></div>{% endfor %}

## Teaching

{% for item in site.data.cv.teaching %}<div class="cv-entry"><h3>{{ item.title }}</h3><p class="content-meta">{{ item.organization }}{% if item.period %} · {{ item.period }}{% endif %}</p><p>{{ item.detail }}</p></div>{% endfor %}

## Skills & Languages

<dl class="skills-list">{% for item in site.data.cv.skills %}<div><dt>{{ item.label }}</dt><dd>{{ item.value }}</dd></div>{% endfor %}{% for item in site.data.cv.languages %}<div><dt>{{ item.label }}</dt><dd>{{ item.value }}</dd></div>{% endfor %}</dl>

## Selected coursework

<table class="course-table"><caption>Selected undergraduate courses; grades out of 20.</caption><thead><tr><th scope="col">Course</th><th scope="col">Grade</th></tr></thead><tbody>{% for course in site.data.cv.courses %}<tr><td>{{ course.name }}</td><td>{{ course.grade }}</td></tr>{% endfor %}</tbody></table>

## Service

{% for item in site.data.cv.service %}<div class="cv-entry"><h3>{{ item.title }}</h3><p>{{ item.organization }}</p><p class="content-meta">{{ item.period }}</p><p>{{ item.detail }}</p></div>{% endfor %}
