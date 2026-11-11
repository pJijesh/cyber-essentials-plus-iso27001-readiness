# Contributing

Thanks for taking an interest. This is a small, deliberately plain tool: standard library only, deterministic output, and careful claims. Changes should keep it that way.

## Ground rules

1. **No real data.** Examples use an invented group and invented sites. Do not add real organisation names, real assessment results, scan output or screenshots from a real environment.
2. **Standard library only** for the `readiness` package. `pytest` is the only test dependency.
3. **Deterministic output.** The same inputs and options must give identical files. Sort anything whose order matters and never write timestamps or absolute paths into outputs. Use `--as-of` in examples.
4. **No copied text.** Describe requirements and controls in your own words. Do not paste text from the NCSC or IASME documents or from ISO standards. Annex A titles are short paraphrases.
5. **Verify facts and say how.** When you change a statement about a scheme or standard, check it against the NCSC, IASME or ISO public pages, update [docs/sources.md](docs/sources.md) with the source type and date, and say so in the pull request. Do not add prices unless you can cite the current published source.
6. **Not legal advice.** Do not add claims about what any country's law requires.
7. **British English, plain tone.** No marketing language. Do not use the em dash or en dash characters. A test checks this.

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest
python -m pytest -q
```

## Changing behaviour

Files under `examples/` are checked by a test against a fresh run. If you change scoring, the reference data, the config or the reports, regenerate them in the same change:

```bash
python scripts/build_examples.py
python -m pytest -q
```

If figures quoted in the README or docs change, update them from the regenerated output. Every figure in the documentation should come from an actual run.

If you change a diagram, edit the `.mmd` file in `docs/images/` and render it again:

```bash
cd docs/images
mmdc -i certification-roadmap.mmd -o certification-roadmap.svg -c mmdc-config.json -b white
```

## Pull request checklist

- [ ] Tests added or updated and passing
- [ ] Examples regenerated if output changed
- [ ] Sources page updated if a fact about a scheme or standard changed
- [ ] No real data, and no text copied from standards or scheme documents
- [ ] Limitations in the README still accurate
