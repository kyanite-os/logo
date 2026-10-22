# Esquisses — tour 3 (direction « bloc taillé »)

Fond sombre dans tous les cas. La palette est réglée pour ça.

## Le dessin

Un K **taillé dans un bloc**, pas dessiné au trait.

- **Rien de symétrique.** La branche haute monte à 4/7, la basse descend
  à 5/8 ; elles n'ont ni la même longueur ni la même épaisseur ; les
  tranchants ne sont pas à la même abscisse.
- **Les angles sont coupés inégalement** : chaque sommet reçoit deux
  coupes de longueurs différentes. Les arêtes longues portent de légers
  décrochements, comme une arête reprise au ciseau.
- **Un biseau d'épaisseur constante** fait le tour. Chaque pan prend sa
  valeur de l'orientation de son arête sous **une seule lumière venant du
  haut-gauche**. Aucune perspective : c'est une plaque chanfreinée vue de
  face, pas un volume en 3D.

## La matière

Lue comme du granite, à trois échelles :

1. **Les lames de kyanite** donnent la structure large et la lumière.
   Plans de clivage jamais tout à fait parallèles.
2. **Les plages**, de la taille d'un cristal de feldspath.
3. **Le grain fin** : éclats clairs (quartz) et points sombres (mica).

La densité du grain n'est pas uniforme : six foyers la font varier,
pour que la roche ne soit pas un quadrillage.

Par-dessus, des **fractures** brisées en travers du clivage : une lèvre
à l'ombre, une au jour.

## Les trois variantes

- **I — granite** : la pierre seule.
- **J — granite + filon** : un filon de cristal clair remonte le jambage
  et fourche dans la branche haute.
- **K — fond de mine** : pierre plus sombre, biseau plus contrasté,
  filon plus vif.

## Palette (fond sombre `#0F1522`)

| rôle | hex |
|---|---|
| roche, 9 valeurs | `#1B3C78` `#22488B` `#28539D` `#2F5FAF` `#366BC0` `#3F78CE` `#4A86DA` `#5795E4` `#67A4EC` |
| biseau, 5 valeurs | `#17376F` `#21488F` `#3A74C8` `#72ACEE` `#BEDCFA` |
| mica (points sombres) | `#1C3C76` `#22477F` |
| quartz (éclats clairs) | `#86B6EE` `#A8CCF4` |
| filon | cœur `#DCEBFE`, halo `#9DC4F3`, paroi `#122C5E` |

## Contraintes tenues

Polygones uniquement. Aucun filtre, aucun bitmap, aucun dégradé.
Les masques de découpe (`clipPath`) sont des polygones, supportés
partout, contrairement à `feTurbulence`.

## Reste à faire

Une **version icône simplifiée** : à 32 et 16 px le grain et le filon
deviennent du bruit. Elle ne sera dessinée qu'une fois la variante
choisie.
