---
title: Research & Projects
permalink: /research/
nav: research
description: Undergraduate research in thin films, two-dimensional materials, and biomedical photonics, with academic projects in vacuum technology, superconductivity, biophysics, and cosmology.
---
My current research focuses on thin films and two-dimensional materials, with hands-on experience in fabrication and characterization. My research background also includes biomedical photonics, alongside academic projects in vacuum technology, superconductivity, biophysics, and cosmology.

## Research experience

{% assign research = site.projects | where: 'category', 'Undergraduate research' | sort: 'order' %}
{% for project in research %}{% include project-entry.html project=project %}{% endfor %}

## Academic projects

{% assign projects = site.projects | where: 'category', 'Academic project' | sort: 'order' %}
<div class="project-list">{% for project in projects %}{% include project-entry.html project=project %}{% endfor %}</div>
