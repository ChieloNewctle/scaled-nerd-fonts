version := `date +%Y.%m.%d`

clean:
    rm SymbolsNerdFontScaled-{Bold,Italic,BoldItalic,Regular}.ttf

publish:
    gh release create "v{{ version }}" --latest \
        -t "v{{ version }}" \
        SymbolsNerdFontScaled-{Bold,Italic,BoldItalic,Regular}.ttf
