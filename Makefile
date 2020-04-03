#!/usr/bin/make -f

PYTHON=python3.7
.PHONY: sitemap.txt

sitemap.txt: index.html render/render.py Activism Activism/* Papers Papers/* cv/index.txt robots.txt Makefile
	. .$(PYTHON)/bin/activate; python -m render index.html cv/index.txt $$(ls -t Papers/*.md Papers/*.rst Activism/*.md)

render/render.py: render/requirements.txt .$(PYTHON)
	. .$(PYTHON)/bin/activate; pip install -r $<
	touch $@

.$(PYTHON):
	$(PYTHON) -m venv --system-site-packages .$(PYTHON)
