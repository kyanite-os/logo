# Esquisses — tour 1

Quatre pistes à juger. Même squelette géométrique pour les quatre :
seules la découpe et la matière changent.

## Géométrie commune (viewBox 0 0 100 100)

- Jambage : x 12 → 34, y 14 → 86 (épaisseur 22).
- Point de jonction des deux branches : (34, 50).
- Branches à pente 3:2, emprise 26 sur l'arête du jambage
  (haute : y 24 → 50 ; basse : y 50 → 76).
- Empreinte : x 12 → 88, y 14 → 86. Centrée.
- Aucune perspective. Une seule direction de lumière : haut-gauche.
  La face tournée vers le haut-gauche est claire, l'autre est dans l'ombre.
- Le jambage est la masse la plus épaisse du cristal : il reste la zone
  la plus dense. La branche haute est la lame la plus fine : la plus claire.

## Palette

| rôle | hex |
|---|---|
| v1 — jambage, face d'ombre | `#27559F` |
| v2 — veines sombres | `#3267B8` |
| v3 — branches, faces d'ombre | `#3F7AD0` |
| v4 — jambage, face éclairée | `#4F8EE0` |
| v5 — branche basse, face éclairée | `#68A4EB` |
| v6 — branche haute, face éclairée | `#8CBDF3` |
| fond de fente | `#1A3A72` |
| retombée de l'éclat | `#C3DDFA` |
| accent — éclat du cœur | `#EAF4FF` |

Plancher volontairement relevé : la valeur la plus sombre reste lisible
sur fond `#11182A`.

## Variantes

- **A** — facettes nettes. 6 polygones.
- **B** — A + veines : lames parallèles, vraies formes géométriques
  (pas de `feTurbulence`, donc rendu identique partout).
- **C** — A + branche haute fendue, cœur brillant.
- **D** — B + fente.

## Contraintes tenues

Polygones uniquement, arêtes partagées exactement, aucun filtre,
aucun bitmap, aucun dégradé. Une silhouette posée dessous évite
tout liseré d'anticrénelage entre facettes adjacentes.
