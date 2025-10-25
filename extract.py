#!/usr/bin/env python3
"""
Génère un fichier Sublime Text .sublime-completions à partir des fichiers CATKnowledge sources.
Ajuste SOURCE_DIR et OUTPUT_FILE selon ton environnement.
"""

import re
import json
from pathlib import Path

# ----- CONFIG -----
SOURCE_DIR = Path(__file__).parent  # dossier de ce script
OUTPUT_FILE = Path("EKL.CATKnowledge.sublime-completions")
FILE_GLOB = ["*.CATKweIdx"]  # extensions à scanner

# regex heuristiques (ajuste si nécessaire)
IDX_LINE = re.compile(r'^Idx:([^;]+);Type:(\d+);')  # capture signature and type

# patterns à ignorer (mots communs)
SKIP_PREFIXES = tuple("+-/*=<>")  # opérateurs

def parse_idx_signature(sig: str):
    """Retourne (name, params:list[str], ret:str|None) à partir de 'Access@Feature@String@@UndefinedType'."""
    # Ex: 'Access@Feature@String@@UndefinedType'
    if not sig or sig.startswith(SKIP_PREFIXES):
        return None
    # sometimes sig can be a type like '2DArc' with no @
    if '@' not in sig:
        return (sig, [], None)
    # split head and tail
    head, _, tail = sig.partition('@@')
    parts = head.split('@')
    if not parts:
        return None
    name = parts[0]
    params = parts[1:] if len(parts) > 1 else []
    ret = tail if tail else None
    # filter weird empty tokens
    params = [p for p in params if p]
    return (name, params, ret)

def extract_entries_from_text(text):
    functions = []
    types = set()
    for line in text.splitlines():
        m = IDX_LINE.match(line.strip())
        if not m:
            continue
        sig, ttype = m.group(1), m.group(2)
        parsed = parse_idx_signature(sig)
        if not parsed:
            continue
        name, params, ret = parsed
        if not name:
            continue
        # Type 1 appears to be type entries; include for type completions
        if ttype == '1' and name[0].isalpha():
            types.add(name)
            continue
        # Type 2 are callable/operator signatures; include only if starting with a letter
        if ttype == '2' and name[0].isalpha():
            functions.append((name, params, ret))
    return functions, sorted(types)

def scan_sources(source_dir: Path):
    funcs = []
    types = set()
    for g in FILE_GLOB:
        for p in source_dir.glob(g):
            try:
                print(f"Reading {p}")
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"Warning reading {p}: {e}")
                continue
            f, t = extract_entries_from_text(txt)
            funcs.extend(f)
            types.update(t)
    # deduplicate functions by name+arity, keep first
    seen = set()
    uniq_funcs = []
    for name, params, ret in funcs:
        key = (name, len(params))
        if key in seen:
            continue
        seen.add(key)
        uniq_funcs.append((name, params, ret))
    return uniq_funcs, sorted(types)

def build_param_placeholder(param_type: str, idx: int) -> str:
    # Nom lisible pour placeholder
    aliases = {
        'String': 'name', 'Real': 'real', 'Integer': 'int', 'Boolean': 'bool',
        'Feature': 'feat', 'List': 'list', 'Angle': 'angle', 'LENGTH': 'len', 'TIME': 'time',
        'Magnitude': 'mag'
    }
    key = param_type.strip()
    base = aliases.get(key, key.lower() if key else f'arg{idx}')
    return f'${{{idx}:{base}}}'

def build_completions(functions, types):
    completions = []
    # functions with parameterized snippets
    for name, params, ret in functions:
        placeholders = ", ".join(build_param_placeholder(p, i+1) for i, p in enumerate(params))
        snippet = f"{name}({placeholders})" if params else f"{name}()"
        hint = f"\t{','.join(params)}" if params else "\t()"
        completions.append({
            "trigger": f"{name}{hint}",
            "contents": snippet
        })
    # also add type names as bare completions
    for t in types:
        completions.append({
            "trigger": f"{t}\tType",
            "contents": t
        })
    return {
        "scope": "source.ekl",
        "completions": completions
    }

def main():
    if not SOURCE_DIR.exists():
        print("SOURCE_DIR n'existe pas:", SOURCE_DIR)
        return
    funcs, types = scan_sources(SOURCE_DIR)
    print(f"Functions: {len(funcs)} | Types: {len(types)}")
    comp = build_completions(funcs, types)
    OUTPUT_FILE.write_text(json.dumps(comp, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Wrote completions to", OUTPUT_FILE)

if __name__ == "__main__":
    main()
