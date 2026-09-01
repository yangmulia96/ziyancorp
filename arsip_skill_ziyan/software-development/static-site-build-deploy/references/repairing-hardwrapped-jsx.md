# Repairing hard-wrapped / truncated JSX from an LLM canvas

## Symptom

`npm run build` fails with esbuild errors like:

```
ERROR: Unterminated string literal
  insights: ["Realokasi 15% ...", "Lindung nilai
                                                ^
```

The paste inserted hard newlines mid-string. There can be dozens. Fixing them
one `patch` call at a time is slow and you will lose count.

## Procedure

1. **Back up first**: `cp src/App.jsx src/App.jsx.bak`.
2. Run `scripts/unwrap-jsx.mjs` (copy it into the project, run with node, then
   delete it before committing). It is a small tokenizer that walks the file
   tracking `code / 'sq' / "dq" / \`tpl\`` states plus `${...}` nesting, and
   collapses any newline+indent occurring *inside* a `'`/`"` literal into a
   single space. Template literals and comments are left untouched, so
   multi-line `className={\`...\`}` blocks survive.
3. Rebuild. Remaining errors are now real structural ones.

## The nastier failure: the paste is TRUNCATED

Check line counts before/after. In one case the original file simply ended
mid-attribute (`...drop-shadow-[0_0_15px_rgba(25`) — roughly the last third of
the component was never pasted. esbuild reports this as
`Unexpected end of file`.

Recovery:
1. `head -<lastGoodLine> src/App.jsx > src/App_new.jsx`, cutting at the last
   complete JSX element.
2. Write the missing tail yourself in a separate file, then
   `cat tail.jsx >> src/App_new.jsx && mv src/App_new.jsx src/App.jsx`.
3. Derive the missing markup from state already declared in the file
   (`tabData`, `activeTab`, `investment`, imported lucide icons) so the rewrite
   matches the original design intent and no imports go unused.
4. Expect JSX tag-balance errors on the seam
   (`Unexpected closing "section" tag does not match opening "div" tag`) — the
   error line numbers point straight at the missing/extra `</div>`.
5. **Tell the user which sections you rewrote.** They may have the complete
   original and can re-paste.

## Related JSX gotcha

Text followed by an expression on the next line loses its space:

```jsx
<span>Status: Aktif ·
{tabData[activeTab].title}</span>   // renders "Aktif ·OPTIMASI..."
```

Fix with an explicit `{' '}` at the end of the text line.
