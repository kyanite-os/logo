# Esquisses — tour 4. Variante K retenue, enrichie.

Fond sombre dans tous les cas.

## Le dessin

Un K **taillé dans un bloc**, pas dessiné au trait. Contour unique,
angles coupés au ciseau, biseau d'épaisseur constante tout autour.
Chaque pan du biseau prend sa valeur de l'orientation de son arête sous
**une seule lumière venant du haut-gauche**. Aucune perspective.

### Dissymétrie

- Les deux obliques n'ont ni la même pente (4/7 et 5/8), ni la même
  longueur, ni la même épaisseur, ni le tranchant à la même abscisse.
- **Le sommet et le pied du jambage ne sont pas de même nature** :
  en haut une seule coupe oblique franche, d'un seul geste ; en bas un
  angle droit franc à gauche — sans aucune coupe, le flanc reste
  d'aplomb jusqu'au sol — et à droite un gradin, le coin resté en l'air
  comme un bloc détaché.
- Les angles reçoivent deux coupes de longueurs différentes.
- Les arêtes longues portent des décrochements.

## La matière

Lue comme du granite, à trois échelles : les lames de kyanite (structure
large et lumière), des plages de la taille d'un cristal, puis le grain
fin — éclats clairs de quartz, points sombres de mica. La densité du
grain n'est pas uniforme : six foyers la font varier.

Par-dessus, des **fractures** brisées en travers du clivage.

## Les deux ajouts de ce tour

**Paillettes.** De petits éclats anguleux et des losanges semés le long
de la crevasse, serrés vers la lèvre éclairée. Aucune forme en étoile.

**Plans translucides.** La kyanite est transparente. Quinze larges plans
à faible opacité se croisent suivant trois directions de clivage qui ne
sont celles d'aucune face visible ; là où ils se superposent, la valeur
s'accumule. Deux plans passent par-dessus tout, comme la lumière qui
traverse la masse.

L'opacité est l'attribut SVG `fill-opacity`, **pas un filtre** : le rendu
reste identique partout, y compris en icône système.

## Dosage

Trois réglages du même dessin : `K1` discret, `K2` moyen, `K3` marqué.
Seules changent l'opacité des plans et la taille des paillettes.

## Palette (fond `#0F1522`)

| rôle | hex |
|---|---|
| roche, 9 valeurs | `#15306A` `#1B3B7C` `#21468E` `#2851A0` `#2E5CB1` `#3668C1` `#3F75CE` `#4A83DA` `#5793E4` |
| biseau, 5 valeurs | `#112A58` `#1C4184` `#3A74C8` `#86B7F2` `#DBEBFF` |
| mica | `#1C3C76` `#22477F` |
| quartz | `#86B6EE` `#A8CCF4` |
| filon | cœur `#DCEBFE`, halo `#9DC4F3`, paroi `#122C5E` |
| paillettes | `#FFFFFF` `#F2F8FF` `#D8E9FD` `#A9CCF4` |
| plans | clair `#BBD8F8`, sombre `#0C2149` |

## Contraintes tenues

Polygones uniquement. Aucun filtre, aucun bitmap, aucun dégradé.
Les masques de découpe sont des polygones.

Le générateur vérifie numériquement qu'aucun pan de biseau ne se
retourne : sur une arête plus courte que le biseau, les deux pans
voisins se refermeraient l'un sur l'autre et fabriqueraient une dent.
Ils sont repliés en pointe.

## Reste à faire

Une **version icône simplifiée** : sous 64 px le grain, les paillettes
et les plans deviennent du bruit. Contour, biseau, filon, rien d'autre.
