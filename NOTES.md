# Journal de conception du logo

Ce fichier garde les raisons derrière le dessin. Pour s'en servir, voir
[`logo/README.md`](logo/README.md) ; pour le reconstruire, voir
[`outils/README.md`](outils/README.md).

Fond sombre dans tous les cas.

## Le dessin

Un K **taillé dans un bloc**, pas dessiné au trait. Contour unique,
angles coupés au ciseau, biseau d'épaisseur constante tout autour.
Chaque pan du biseau prend sa valeur de l'orientation de son arête sous
**une seule lumière venant du haut-gauche**. Aucune perspective.

### Dissymétrie

- Les deux obliques n'ont ni la même pente (4/7 et 5/8), ni la même
  longueur, ni la même épaisseur, ni le tranchant à la même abscisse.
- **Les attaches sont courtes.** La fourche est descendue à mi-hauteur
  moins deux, et la branche basse rejoint le jambage sur 23 unités
  seulement : le contre-poinçon du bas fait 19 unités de haut contre 11
  auparavant. Sans ça la branche basse et le jambage se lisaient comme
  une seule masse.
- Épaisseurs : jambage 30, branche haute 22,6, branche basse 21,2.
  Le biseau est à 3, pour laisser respirer les encoches.
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

**La fente est comblée.** C'est le dernier changement de fond, et le
plus important.

Une fente ouverte dans le logo d'un système qui se vend comme immuable
et durci dit le contraire de ce qu'on veut : on lit de la casse. Une
fente **remplie** dit l'inverse — scellée, consolidée. En minéralogie
c'est un filon secondaire qui colmate une fracture ; ailleurs c'est le
kintsugi. Même langage minéral, message retourné.

Ce qui fait lire « rempli » plutôt que « cassé » n'est pas la couleur,
c'est **la continuité** :

- un **ménisque** — la remontée de la résine contre la paroi — qui
  court sans interruption le long de la lèvre amont. Une arête de
  cassure, elle, donne un reflet haché. Il doit rester un filet :
  large, il bave dès les petites tailles ;
- des bords nets, et **aucun éclat manquant** : les écaillures de la
  version ouverte sont supprimées ;
- un liseré de pierre sombre dessous, qui pose le filon *dans* la
  pierre au lieu de le faire flotter dessus ;
- la matière est translucide, donc le grain transparaît au travers —
  `fill-opacity`, pas un aplat ;
- les fissures secondaires sont comblées elles aussi : c'est tout le
  réseau qui est scellé.

Le tracé garde ses irrégularités — il divague, il pince et gonfle, les
deux lèvres dérivent indépendamment — mais moins que la cassure
ouverte : la résine épouse la fracture, sa surface est lisse.

Le bruit qui pilote tout cela est **lissé**. Un bruit décorrélé d'un
point au suivant donnerait des dents de scie ; une fracture, elle,
dérive lentement.

Deux dosages existent dans `outils/bloc.py` — `RESINE_CLAIRE`, retenue,
et `RESINE_SOMBRE`, plus discrète et plus minérale.

**Paillettes.** Elles deviennent des **bulles prises dans la résine** :
petits éclats anguleux et losanges, clairs et sombres. Aucune forme en
étoile.

**Plans translucides.** La kyanite est transparente. Quinze larges plans
à faible opacité se croisent suivant trois directions de clivage qui ne
sont celles d'aucune face visible ; là où ils se superposent, la valeur
s'accumule. Deux plans passent par-dessus tout, comme la lumière qui
traverse la masse.

L'opacité est l'attribut SVG `fill-opacity`, **pas un filtre** : le rendu
reste identique partout, y compris en icône système.

## Finesse : quatre échelles qui se recouvrent

Pour qu'on ne lise plus les formes de base, aucune des quatre n'a de
contour rectiligne :

1. **Les lames** de kyanite, brisées en six segments avec une dérive
   perpendiculaire à chaque nœud. Deux lames voisines partagent
   exactement la même brisure : elles pavent la bande sans jour.
2. **Les lamelles**, courtes et fines, prises entre les grandes. Ce sont
   des éclats, pas des traits qui traversent.
3. **Le grain** granitique, à trois tailles, densité inégale.
4. **Les fractures** sèches, en travers du clivage, toutes de
   longueur, largeur et contraste différents. Une sur trois ne prend
   pas la lumière. Elles restent ouvertes, elles : ce sont des micro-
   fêlures de surface, pas la fracture traversante.

Le biseau est double : une arête vive étroite (0,8) qui s'écarte de son
pan — plus sombre à l'ombre, plus vive au jour — puis le pan principal.

Dosage retenu : `K3 — fond de mine`, plans translucides à 1,55 et
paillettes à 1,30. Les deux molettes sont en bas de
`outils/dessine.py`.

## Palette (fond `#0F1522`)

| rôle | hex |
|---|---|
| roche, 9 valeurs | `#15306A` `#1B3B7C` `#21468E` `#2851A0` `#2E5CB1` `#3668C1` `#3F75CE` `#4A83DA` `#5793E4` |
| biseau, 5 valeurs | `#112A58` `#1C4184` `#3A74C8` `#86B7F2` `#DBEBFF` |
| mica | `#1C3C76` `#22477F` |
| quartz | `#86B6EE` `#A8CCF4` |
| fente | creux `#15376E`, fond `#0E2650`, paroi aval `#3570C4`, lèvre `#8FBDF4` |
| paillettes | `#C6DEFA` `#A8CCF4` `#88B8F0` `#6AA0E8` `#4D86DA` |
| plans | clair `#BBD8F8`, sombre `#0C2149` |

## Contraintes tenues

Polygones uniquement. Aucun filtre, aucun bitmap, aucun dégradé.
Les masques de découpe sont des polygones.

Le générateur vérifie numériquement qu'aucun pan de biseau ne se
retourne : sur une arête plus courte que le biseau, les deux pans
voisins se refermeraient l'un sur l'autre et fabriqueraient une dent.
Ils sont repliés en pointe.

## La version icône

Sous 128 px, le grain, les paillettes et les plans ne font plus que du
bruit. `kyanite-icon.svg` les retire, allège le contour de ses
décrochements, et porte le biseau de 3 à 5.

**Ce qui survit, mesuré et non supposé :**

| | 16 px | 22–32 px | 48–128 px |
|---|---|---|---|
| silhouette | oui | oui | oui |
| contraste entre les trois traits | oui | oui | oui |
| arête éclairée en haut-gauche | oui, dominante | oui | oui |
| fente | **non** | ligne sourde | oui |

À 16 px la fente a disparu : il ne reste que la silhouette, le
contraste des traits, et une arête claire qui tire l'œil vers le coin
haut-gauche. C'est l'ordre dans lequel il faut penser l'icône.
