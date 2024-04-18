#!/usr/bin/env bash

# Create missing source files
for filename in vis/*.py; do
  if [[ "$filename" != *"__init__"* ]]; then
    file_no_py="${filename%.*}"
    md_filename="$file_no_py.md"
    content="::: $(echo "$file_no_py" | tr / .)"

    if ! test -f docs_source/"$md_filename"; then
      mkdir -p "docs_source/$(dirname "$md_filename")"
      touch docs_source/"$md_filename"
      echo "$content" > docs_source/"$md_filename"
    fi
  fi
done

cp README.md docs_source/index.md
cp -r readme_imgs docs_source
mkdocs build --clean

