DESTDIR =
LANG = en fr

all:
	for l in $(LANG); do \
	  make -C $$l/Docs all; \
	  make -C $$l/Docs-jr all; \
	done

clean:
	for l in $(LANG); do \
	  make -C $$l/Docs clean; \
	  make -C $$l/Docs-jr clean; \
	done

install:
	for l in $(LANG); do \
	  install -d $(DESTDIR)/../expeyes-doc-$$l/usr/share/expeyes/doc; \
	  for p in $$l/Docs/*.pdf $$l/Docs-jr/*.pdf; do \
	    install -m 644 $$p $(DESTDIR)/../expeyes-doc-$$l/usr/share/expeyes/doc/$$l-$$(basename $$p); \
	  done; \
	done

.PHONY: all clean install
