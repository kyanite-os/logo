// Reglages d'optimisation des SVG livres.
//
// Deux precautions :
//  - on garde les identifiants, parce que les masques de decoupe
//    (clipPath) y font reference ;
//  - on garde desc, qui sert a l'accessibilite (title est conserve
//    par defaut).
export default {
  multipass: true,
  floatPrecision: 2,
  plugins: [
    { name: "preset-default",
      params: { overrides: {
        cleanupIds: false,
        removeDesc: false,
      } } },
    "convertStyleToAttrs",
    "sortAttrs",
  ],
};
