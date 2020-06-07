TITLEFILE=titleidx.sbx
AUTHORFILE=authidx.sbx

all: zpevnik.pdf

zpevnik.pdf: zpevnik.tex $(TITLEFILE) $(AUTHORFILE)
	latex $<
	latex $<
	pdflatex $<

$(TITLEFILE) $(AUTHORFILE)&: pisnicky
	python3 ./akordy/maketoc.py pisnicky $(TITLEFILE) $(AUTHORFILE)

zpevnik.tex: pisnicky
	python3 ./akordy/merge.py pisnicky $@
