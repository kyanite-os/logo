# Les outils qui écrivent le dossier `logo/`

Le dessin est **asymétrique et irrégulier par construction** : grain de
granite, plans de clivage brisés, lamelles, fractures, fente qui
divague. Tout cela est tiré d'un générateur à graine fixe — donc
parfaitement reproductible — mais serait intenable à tenir à la main.

Les SVG produits restent commentés, en polygones seulement, et se
modifient à la main sans problème.

```sh
sh construire.sh        # reconstruit les trois SVG et les neuf PNG
```

| fichier | rôle |
|---|---|
| `bloc.py` | La géométrie : contour, coupes d'angle, biseau, lames de kyanite, grain, fractures, fente. Vérifie numériquement qu'aucun pan de biseau ne se retourne. |
| `dessine.py` | Le logo complet : plans translucides, paillettes, double biseau, écriture du SVG. |
| `icone.py` | La version simplifiée pour petites tailles. |
| `logotype.py` | Le symbole suivi du mot, Inter SemiBold vectorisé (fontTools). |
| `exporte.py` | Les PNG, via Chromium sans interface. |
| `svgo.config.mjs` | Réglages d'optimisation. Garde les identifiants, dont dépendent les masques de découpe. |

## Les deux molettes

En bas de `dessine.py` : l'opacité des plans traversants et la taille
des paillettes. Le réglage livré est `1.55` / `1.30`.

## Dépendances

`python3`, `fonttools` (pour le logotype), `svgo`, et un Chromium sans
interface (pour les PNG). Le chemin de Chromium est en haut de
`exporte.py`.
