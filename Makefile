DESTDIR =
LANG = en fr

all:
	for l in $(LANG); do \
	  make -C $$l/Docs all; \
	  make -C $$l/Docs-jr all; \
	  make -C $$l/Progman-jr all; \
	  make -C $$l/Brochure-eyes17 all; \
	done

clean:
	for l in $(LANG); do \
	  make -C $$l/Docs clean; \
	  make -C $$l/Docs-jr clean; \
	  make -C $$l/Progman-jr clean; \
	  make -C $$l/Brochure-eyes17 clean; \
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
