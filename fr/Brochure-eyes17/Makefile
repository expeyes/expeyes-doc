LANG = fr
SOURCE_TS = $(shell ls ../../en/Brochure-eyes17/*_en.ts)
SOURCE_SVG = $(shell ls ../../en/Brochure-eyes17/*.svg)

TARGET_TS = $(patsubst ../../en/Brochure-eyes17/%_en.ts, %_$(LANG).ts, $(SOURCE_TS))
TARGET_SVG = $(patsubst ../../en/Brochure-eyes17/%.svg, %.svg, $(SOURCE_SVG))
TRANSLATE_SVG = ../../translateSvg.py

test:
	@echo $(SOURCE_SVG)

all: $(TARGET_TS) $(TARGET_SVG)

%_$(LANG).ts: ../../en/Brochure-eyes17/%_en.ts
	if [ -e $@ ]; then \
	  lconvert $< $@ -o $@; \
	else \
	  cp $< $@; \
	fi

Back.svg: Back_$(LANG).ts
	$(TRANSLATE_SVG) ../../en/Brochure-eyes17/Back.svg Back_$(LANG).ts $@

Front.svg: Front_$(LANG).ts
	$(TRANSLATE_SVG) ../../en/Brochure-eyes17/Front.svg Front_$(LANG).ts $@

clean:
	rm -f *~ *bak
