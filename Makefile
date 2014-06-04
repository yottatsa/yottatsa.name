#!/usr/bin/make -f

.PHONY: sitemap.txt

sitemap.txt: index.html render/render.py Papers Papers/* cv/index.txt robots.txt Makefile
	python -m render index.html cv/index.txt $$(ls -t Papers/*.md Papers/*.rst)

render/render.py: render/requirements.txt
	pip install -r $^
	touch $@
