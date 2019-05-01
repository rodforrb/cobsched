# Makefile
# 
# Converts Markdown to other formats (HTML, PDF, DOCX, RTF, ODT, EPUB) using Pandoc
# <http://johnmacfarlane.net/pandoc/>
#
# Run "make" (or "make all") to convert to all other formats
#
# Run "make clean" to delete converted files

# Convert all files in this directory that have a .rmd suffix
SOURCE_DOCS := slides.rmd

EXPORTED_DOCS= index.html

RM=/bin/rm

PANDOC=/bin/pandoc

PANDOC_OPTIONS=--standalone

PANDOC_HTML_OPTIONS=-t slidy --slide-level=1 --mathml

# Pattern-matching Rules

index.html : slides.rmd
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_HTML_OPTIONS) -o $@ $<

# Targets and dependencies

.PHONY: all clean

all : $(EXPORTED_DOCS)

clean:
	- $(RM) $(EXPORTED_DOCS)
