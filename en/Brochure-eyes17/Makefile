SOURCES = $(shell ls *.svg)
TARGETS = $(patsubst %.svg, %_en.ts, $(SOURCES))
EXTRACT_STRING = ../../svg2ts.py

all: $(TARGETS)

%_en.ts : %.svg $(EXTRACT_STRING)
	$(EXTRACT_STRING) $< $@

clean:
	rm -f *~ *bak
