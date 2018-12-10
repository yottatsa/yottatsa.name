#!/usr/bin/make -f

.PHONY: sitemap.txt

sitemap.txt: index.html render/render.py Papers Papers/* cv/index.txt robots.txt Makefile
	. .python/bin/activate; python -m render index.html cv/index.txt $$(ls -t Papers/*.md Papers/*.rst)

render/render.py: render/requirements.txt .python
	. .python/bin/activate; pip install -r $<
	touch $@

.python:
	virtualenv --system-site-packages .python
