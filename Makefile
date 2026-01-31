# Makefile for thesis compilation
# Usage: make, make clean, make view

MAIN = thesis
BUILD_DIR = build
LATEX = pdflatex
BIBTEX = bibtex
LATEX_FLAGS = -output-directory=$(BUILD_DIR) -interaction=nonstopmode

.PHONY: all clean view quick help

all:
	@mkdir -p $(BUILD_DIR)
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(BIBTEX) $(BUILD_DIR)/$(MAIN)
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	@echo "✓ Compilation complete: $(BUILD_DIR)/$(MAIN).pdf"

quick:
	@mkdir -p $(BUILD_DIR)
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	@echo "✓ Quick compilation complete: $(BUILD_DIR)/$(MAIN).pdf"

clean:
	rm -rf $(BUILD_DIR)
	@echo "✓ Build directory cleaned"

view:
	@if [ -f "$(BUILD_DIR)/$(MAIN).pdf" ]; then \
		open $(BUILD_DIR)/$(MAIN).pdf || xdg-open $(BUILD_DIR)/$(MAIN).pdf; \
	else \
		echo "Error: PDF file does not exist. Run 'make' first."; \
	fi

help:
	@echo "Available targets:"
	@echo "  make          - Full compilation (3 passes + bibtex)"
	@echo "  make quick    - Quick compilation (1 pass, no bibtex)"
	@echo "  make clean    - Remove build directory"
	@echo "  make view     - Open PDF in viewer"
	@echo "  make help     - Show this help message"