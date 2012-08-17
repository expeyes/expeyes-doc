DESTDIR =
LANG    = fr
SOURCES = eyes.tex
PDFS    = $(patsubst %.tex, %.pdf, $(SOURCES))
WARNING = LaTeX Warning: Label(s) may have changed. Rerun

all: $(PDFS)

install: all
	install -m 644 $(PDFS) $(DESTDIR)

%.pdf: %.tex
	@echo -n "Language=$(LANG), shell=$$(echo $$SHELL), Running PDFLaTeX "
	@ok=0; texfile=$<; logfile=$$(echo $$texfile| sed s/tex/log/); \
	while [ $$ok = 0 ]; do \
	  echo -n "on $${texfile} ... "; \
	  pdflatex -interaction=nonstopmode $${texfile} >/dev/null 2>&1 || true; \
	  if ! grep -q "$(WARNING)" $${logfile}; then \
	    ok=1; \
	  fi; \
	done; \
	echo Done.

clean:
	rm -f *~ *.aux *.log *.toc *.lof
	[ -f /tmp/keep-expeyes-docs ] || rm -f $(PDFS)
