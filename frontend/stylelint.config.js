export default {
  extends: ["stylelint-config-standard"],
  rules: {
    "selector-pseudo-element-no-unknown": [
      true,
      {
        ignorePseudoElements: ["v-deep"],
      },
    ],
    "media-query-no-invalid": null,
  },
};
