#!/bin/bash
# cleanup.sh - Remove all LaTeX auxiliary files

echo "Cleaning up LaTeX auxiliary files..."

# Remove auxiliary files in root
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot
rm -f *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml
rm -f *.nav *.snm *.vrb

# Remove auxiliary files in subdirectories
find . -name "*.aux" -type f -delete
find . -name "*.log" -type f -delete
find . -name "*.out" -type f -delete

# Keep build directory but remove contents except PDF
if [ -d "build" ]; then
    find build -type f ! -name "thesis.pdf" -delete
fi

echo "✓ Cleanup complete!"
