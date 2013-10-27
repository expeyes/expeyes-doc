DESTDIR =
PODIR   = ../../../po
LANG    = fr
SOURCES = $(shell ls *.lyx)
PDFS    = $(patsubst %.lyx, %.pdf, $(SOURCES))
TEXS    = $(patsubst %.lyx, %.tex, $(SOURCES))
WARNING=LaTeX Warning: Label(s) may have changed. Rerun

all: $(PDFS)

install: all
	install -m 644 $(PDFS) $(DESTDIR)

%.tex: %.lyx
	@echo -n "Language=$(LANG), exporting $< to a LaTeX file ... "
	@lyx -e latex $< >/dev/null 2>&1
	@echo Done.

%.pdf: %.tex
	@echo -n "Running PDFLaTeX"
	@ok=0; \
	logfile=$$(echo $< | sed 's/\.tex/.log/'); \
	while [ $$ok = 0 ]; do \
	  echo -n " ... "; \
	  pdflatex -interaction=nonstopmode $< >/dev/null 2>&1 || true; \
	  if ! grep -q "$(WARNING)" $${logfile}; then \
	    ok=1; \
	  fi; \
	done
	@echo Done.

clean:
	rm -f *~ *.aux *.log *.toc *.lof *.out $(TEXS)
	[ -f /tmp/keep-expeyes-docs ] || rm -f $(PDFS) $(TEXS)
