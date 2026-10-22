# Le logo de Kyanite

Un K taillé dans un bloc de kyanite, traversé d'un filon de résine
qui en scelle la fracture. Pour fond sombre.

![Le logotype Kyanite](png/banniere.png)

## Les fichiers

| fichier | pour quoi |
|---|---|
| `kyanite-logo.svg` | Le dessin complet. Site, bandeau de l'installeur, tout ce qui s'affiche **à 64 px ou plus**. |
| `kyanite-icon.svg` | La version simplifiée, pour **moins de 64 px** : icône système, favicon, barre des tâches. |
| `kyanite-logotype.svg` | Le symbole suivi du mot « Kyanite ». |
| `png/kyanite-<taille>.png` | 16, 22, 24, 32, 48, 64, 128, 256, 512 px, fond transparent. |
| `png/banniere.png` | Le logotype **avec son fond sombre**, pour un README ou une page dont on ne maîtrise pas le thème. |

Les PNG de moins de 128 px sont rendus depuis l'icône, les autres
depuis le logo complet. La bascule est à 128 et pas plus bas : à 64 et
96 px, le grain et les paillettes du dessin complet ne font plus que du
bruit et la fente bave — le rendu y serait moins lisible qu'à 48 px.

Pour tout reconstruire : `sh ../outils/construire.sh`.

**Les fichiers livrés sont déjà optimisés** — inutile de les repasser
dans un compresseur. Les SVG sont passés par svgo, les PNG par
pngquant puis oxipng : 226 Ko → 79 Ko pour le jeu complet, sans
différence visible.

## Palette

Le logo est **réglé pour fond sombre**. Fond de référence : `#0F1522`.

L'essentiel, si vous n'avez besoin que de quelques valeurs :

| rôle | hex |
|---|---|
| fond de référence | `#0F1522` |
| bleu kyanite, cœur | `#3668C1` |
| bleu kyanite, clair | `#5793E4` |
| arête éclairée | `#DBEBFF` |
| creux, ombre | `#112A58` |
| le mot, dans le logotype | `#DCE6F2` |

La palette complète :

| série | valeurs |
|---|---|
| la roche, 9 valeurs | `#15306A` `#1B3B7C` `#21468E` `#2851A0` `#2E5CB1` `#3668C1` `#3F75CE` `#4A83DA` `#5793E4` |
| le biseau, 5 valeurs | `#112A58` `#1C4184` `#3A74C8` `#86B7F2` `#DBEBFF` |
| la fente comblée | lèvre de pierre `#12305F` · résine `#9CC6F4` · cœur `#7FB3EE` · ménisque `#F2F8FF` · reflet `#C6DFFA` |
| bulles dans la résine | `#F7FBFF` `#285AA6` |
| paillettes | `#C6DEFA` `#A8CCF4` `#88B8F0` `#6AA0E8` `#4D86DA` |
| quartz, mica | `#86B6EE` `#A8CCF4` · `#1C3C76` `#22477F` |
| fractures | `#1E4588` `#6CA2E8` |
| plans traversants | clair `#BBD8F8` · sombre `#0C2149` |

## Comment l'employer

**Marge.** Laissez autour du symbole un vide d'au moins **un quart de sa
hauteur**, libre de tout texte, trait ou bord. Les SVG portent déjà une
marge interne d'environ 10 % : elle ne compte pas dans ce quart.

**Fond.** Un fond sombre et uni, entre `#0A0E18` et `#1E2534` environ.
Au-delà, le contraste s'effondre : la moitié droite du jambage se
confond avec le fond.

**Attention au fond clair.** Les PNG ont un fond transparent : posés
sur du blanc, l'arête éclairée du haut-gauche (`#DBEBFF`) disparaît et
le contour s'ouvre. C'est le cas d'un README GitHub lu en thème clair.
Dans ce cas, servez `png/banniere.png`, qui porte son fond, ou posez le
logo sur un aplat sombre vous-même.

**Tailles minimales.** 16 px pour l'icône. 120 px de large pour le
logotype — en dessous, le mot devient illisible bien avant le symbole.

**Bascule.** Sous 64 px, servez `kyanite-icon.svg`. Au-dessus,
`kyanite-logo.svg`.

## Ce qu'il ne faut pas faire

- **Ne pas le poser sur fond clair.** Il n'a pas été dessiné pour ça et
  il n'existe pas de variante claire. Si vous en avez besoin, demandez
  plutôt qu'improviser.
- **Ne pas le recolorer.** La lumière vient du haut-gauche et les
  valeurs sont calculées à partir de l'orientation de chaque pan.
  Changer la teinte casse cette cohérence.
- **Ne pas le faire tourner ni le refléter.** Même raison : la lumière
  viendrait d'ailleurs.
- **Ne pas l'étirer.** Les proportions sont réglées pour le carré.
- **Ne pas y ajouter d'ombre portée, de lueur, de contour ni de relief.**
  Le relief est déjà dans le dessin.
- **Ne pas le rogner** dans un cercle ou un carré arrondi : le pied et
  les tranchants seraient coupés. Posez-le dans la forme, avec sa marge.
- **Ne pas se servir du symbole comme d'une lettre** dans un mot ou un
  titre.
- **Ne pas redessiner le mot** dans une autre police : utilisez
  `kyanite-logotype.svg`.

## Nom et logo

Le code de Kyanite est sous licence libre. **Le nom « Kyanite » et ce
logo ne le sont pas** : ils désignent le projet et restent réservés à
son usage.

Vous pouvez les reproduire pour parler de Kyanite — un article, une
présentation, une page de liens, un dépôt de paquets. Vous ne pouvez
pas vous en servir pour nommer ou signer une image dérivée, un produit
ou un service, ni laisser entendre que le projet vous soutient.
Reconstruisez une image à partir du code autant que vous voulez, mais
donnez-lui son propre nom et sa propre marque.

Pour un usage qui sort de ce cadre, demandez.

## Deux points techniques

Le mot du logotype est composé en **Inter SemiBold puis vectorisé** :
aucune police n'est requise à l'affichage. Inter est sous licence SIL
Open Font License, qui autorise explicitement les travaux dérivés.

Les trois SVG n'emploient que des **polygones** : aucun filtre, aucune
image bitmap, aucun dégradé. Les seules fonctions SVG employées au-delà
des formes sont `clipPath` et `fill-opacity`, toutes deux universelles.
C'est délibéré : un `feTurbulence` ou un dégradé rend mal, voire pas du
tout, dans les thèmes d'icônes et les conversions automatiques.

Le logo ne ressemble volontairement ni au « f » de Fedora ni à
l'engrenage de KDE, qui sont des marques déposées.
