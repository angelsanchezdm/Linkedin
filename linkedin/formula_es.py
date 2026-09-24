#!/usr/bin/env python3
"""Detecta tics de "post LinkedIn escrito por IA" en español.

El detector de li-human está pensado para inglés. Este mira la estructura:
párrafos de una frase, listas de fragmentos, contrastes "No X. Y.",
frases-bisagra con dos puntos, cierres en paralelo, intensificadores.

    python3 formula_es.py post.txt [otro.txt ...]
"""
import re
import sys

INTENSIFICADORES = [
    "absolutamente", "completamente", "totalmente", "muchísimo", "realmente",
    "de forma sistemática", "enorme", "bastante más", "exactamente",
    "simplemente", "precisamente", "radicalmente", "clave",
]
BISAGRAS = [
    r"el problema es que", r"pero hay una pregunta", r"parece una diferencia",
    r"no lo es\.", r"y eso (cambia|modifica)", r"y ahí (creo que )?(está|hay)",
    r"la pregunta (real|de verdad|incómoda)", r"no es que .{0,40}\. es que",
    r"no (por|se trata de) .{0,40}\.\s*(sino|por|se trata)",
]


def parrafos(texto):
    return [p.strip() for p in re.split(r"\n\s*\n", texto) if p.strip()]


def frases(p):
    return [f for f in re.split(r"(?<=[.!?])\s+|\n", p) if f.strip()]


def analizar(texto):
    ps = parrafos(texto)
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    low = texto.lower()
    una_frase = sum(1 for p in ps if len(frases(p)) == 1)

    # listas de fragmentos: 3+ líneas seguidas de <7 palabras
    rachas, racha = 0, 0
    for l in lineas:
        if len(l.split()) < 7:
            racha += 1
        else:
            rachas += racha >= 3
            racha = 0
    rachas += racha >= 3

    # anáfora: 3+ líneas seguidas que empiezan con la misma palabra
    anaforas, prev, n = 0, None, 0
    for l in lineas:
        w = l.split()[0].lower()
        n = n + 1 if w == prev else 1
        anaforas += n == 3
        prev = w

    contraste = len(re.findall(r"(^|\n)\s*no [^.\n]{0,60}\.\s*\n+\s*(sino|es|por|se)\b", low))
    contraste += len(re.findall(r"no [^.\n]{0,50}, sino ", low))
    dos_puntos = sum(1 for l in lineas if l.endswith(":"))
    y_inicial = sum(1 for l in lineas if re.match(r"^(y|pero) ", l.lower()))
    intens = sum(low.count(w) for w in INTENSIFICADORES)
    bisagras = sum(len(re.findall(b, low)) for b in BISAGRAS)
    flechas = texto.count("→")

    cierre_paralelo = 0
    if len(ps) >= 2:
        a, b = ps[-2].split(), ps[-1].split()
        if a and b and len(ps[-1]) < 90 and len(ps[-2]) < 90 and (a[0] == b[0] or a[:2] == b[:2]):
            cierre_paralelo = 1

    m = {
        "párrafos de 1 frase (%)": round(100 * una_frase / max(len(ps), 1)),
        "listas de fragmentos": rachas,
        "anáforas (3+ líneas)": anaforas,
        "contrastes No X / Y": contraste,
        "líneas-bisagra con ':'": dos_puntos,
        "frases-bisagra típicas": bisagras,
        "líneas que empiezan por Y/Pero": y_inicial,
        "intensificadores": intens,
        "flechas": flechas,
        "cierre en paralelo": cierre_paralelo,
    }
    # puntuación de fórmula 0-100 (más alto = más plantilla)
    s = 0
    s += max(0, m["párrafos de 1 frase (%)"] - 60) * 0.5
    s += 6 * m["listas de fragmentos"] + 5 * m["anáforas (3+ líneas)"]
    s += 5 * m["contrastes No X / Y"] + 3 * m["líneas-bisagra con ':'"]
    s += 5 * m["frases-bisagra típicas"] + 1.5 * m["líneas que empiezan por Y/Pero"]
    s += 2 * m["intensificadores"] + 2 * m["flechas"] + 8 * m["cierre en paralelo"]
    return m, min(100, round(s))


def main():
    for path in sys.argv[1:]:
        m, s = analizar(open(path, encoding="utf-8").read())
        veredicto = "FÓRMULA" if s >= 50 else "REVISAR" if s >= 25 else "OK"
        print(f"\n{path}\n" + "-" * 50)
        for k, v in m.items():
            print(f"  {k:<34}{v}")
        print(f"  {'PUNTUACIÓN DE FÓRMULA':<34}{s}  {veredicto}")


if __name__ == "__main__":
    main()
