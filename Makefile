TITLEFILE=titleidx.sbx
AUTHORFILE=authidx.sbx

all: zpevnik.pdf

zpevnik.pdf: zpevnik.tex $(TITLEFILE) $(AUTHORFILE)
	latex $<
	latex $<
	pdflatex $<

$(TITLEFILE) $(AUTHORFILE)&: nowtex
	python3 ./akordy/maketoc.py nowtex $(TITLEFILE) $(AUTHORFILE)

zpevnik.tex: nowtex
	python3 ./akordy/merge.py nowtex $@
