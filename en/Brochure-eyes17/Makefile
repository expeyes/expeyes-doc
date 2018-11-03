SOURCES = $(shell ls *.svg)
TARGETS = $(patsubst %.svg, %_en.ts, $(SOURCES))
EXTRACT_STRING = ../../svg2ts.py

all: $(TARGETS)

%_en.ts : %.svg $(EXTRACT_STRING)
	$(EXTRACT_STRING) $< $@

brochure-en.pdf: $(SOURCES)
	convert Front.svg Front.pdf
	convert Back.svg Back.pdf
	pdftk Front.pdf Back.pdf cat output $@
	rm Front.pdf Back.pdf

clean:
	rm -f *~ *bak *pdf
