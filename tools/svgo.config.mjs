// Optimisation settings for the delivered SVGs.
//
// Two precautions:
//  - we keep the identifiers, because the clipping masks (clipPath)
//    refer to them;
//  - we keep desc, which serves accessibility (title is kept by
//    default).
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
