#!/usr/bin/env python3
"""Essai : trois traitements de la fente, pour comparaison."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloc as G, dessine as D
# Sort les trois traitements cote a cote, pour juger. Rien n'est ecrit
# dans logo/ : cette branche ne sert qu'a comparer.
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "essais")
os.makedirs(OUT, exist_ok=True)
for slug, titre, res in (("a-creux", "fente ouverte (actuel)", None),
                         ("b-resine-claire", "résine laiteuse", G.RESINE_CLAIRE),
                         ("c-resine-sombre", "résine transparente", G.RESINE_SOMBRE)):
    open(os.path.join(OUT, slug + ".svg"), "w").write(D.build(titre, 1.55, 1.30, resine=res))
    print("ecrit", slug)
