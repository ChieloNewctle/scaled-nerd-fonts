version := "v" + `date +%Y.%m.%d`

clean:
    rm SymbolsNerdFontScaled-{Bold,Italic,BoldItalic,Regular}.ttf

publish:
    zip -r "SymbolsNerdFontScaled-{{version}}.zip" \
        SymbolsNerdFontScaled-{Bold,Italic,BoldItalic,Regular}.ttf
    gh release create "{{version}}" --latest \
        -t "{{version}}" \
        "SymbolsNerdFontScaled-{{version}}.zip"
    rm "SymbolsNerdFontScaled-{{version}}.zip"
