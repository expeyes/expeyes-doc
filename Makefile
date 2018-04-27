DESTDIR =
LANG = en es fr de nl

all:
	for l in $(LANG); do \
	  [ ! -d "$$l/Docs" ] || make -C $$l/Docs all; \
	  [ ! -d "$$l/Docs-jr" ] || make -C $$l/Docs-jr all; \
	  [ ! -d "$$l/Progman-jr" ] || make -C $$l/Progman-jr all; \
	  [ ! -d "$$l/Brochure-eyes17" ] || make -C $$l/Brochure-eyes17 all; \
	done

clean:
	for l in $(LANG); do \
	  [ ! -d "$$l/Docs" ] || make -C $$l/Docs clean; \
	  [ ! -d "$$l/Docs-jr" ] || make -C $$l/Docs-jr clean; \
	  [ ! -d "$$l/Progman-jr" ] || make -C $$l/Progman-jr clean; \
	  [ ! -d "$$l/Brochure-eyes17" ] || make -C $$l/Brochure-eyes17 clean; \
	done
	# remove generated eps files
	find . -name "*.eps" -exec rm {} \;
	rm -f *~

install:
	install -d $(DESTDIR)/usr/share/expeyes/doc
	for l in $(LANG); do \
	  for p in $$l/Docs/*.pdf $$l/Docs-jr/*.pdf $$l/Progman-jr/*.pdf $$l/Brochure-eyes17/*.svg; do \
	    install -m 644 $$p $(DESTDIR)/usr/share/expeyes/doc/$$l-$$(basename $$p); \
	  done; \
	done

.PHONY: all clean install
