.PHONY: all quick clean view count

MAIN = thesis

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex chapters/*.tex bibliography/references.bib
	xelatex $(MAIN)
	biber $(MAIN)
	xelatex $(MAIN)
	xelatex $(MAIN)

quick:
	xelatex $(MAIN)

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
	rm -f *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml
	rm -f chapters/*.aux appendices/*.aux

view: $(MAIN).pdf
	evince $(MAIN).pdf &

count:
	@echo "Word count (approximate):"
	@texcount -inc -incbib -sum $(MAIN).tex 2>/dev/null || echo "Install texcount for accurate word count"
