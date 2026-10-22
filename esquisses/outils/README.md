# Les deux scripts qui écrivent le SVG

Le dessin est **asymétrique et irrégulier par construction** : grain de
granite, plans de clivage brisés, lamelles, fractures. Tout cela est
tiré d'un générateur à graine fixe, donc parfaitement reproductible,
mais ce serait intenable à maintenir à la main.

- `bloc.py` — la géométrie : le contour, les coupes d'angle, le biseau,
  les lames de kyanite, le grain, les fractures, le filon.
  Il vérifie numériquement qu'aucun pan de biseau ne se retourne.
- `dessine.py` — l'assemblage : plans translucides, paillettes, double
  biseau, et l'écriture du SVG.

```
python3 dessine.py      # réécrit ../kyanite-k.svg
```

Deux molettes en bas de `dessine.py` : l'opacité des plans traversants
et la taille des paillettes.

Le SVG produit se lit et se modifie à la main sans problème — il est
commenté et n'emploie que des polygones. Le générateur n'est là que
pour poser les milliers de coordonnées du grain.
