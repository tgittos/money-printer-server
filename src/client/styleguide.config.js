const path = require("path");

module.exports = {
  sections: [
    {
      name: 'Introduction',
      content: 'styleguide/Introduction.md'
    },
    {
      name: 'Branding',
      content: 'styleguide/Branding.md'
    },
    {
      name: 'Structure',
      content: 'styleguide/Structure.md'
    },
    {
      name: 'Atoms',
      content: 'styleguide/Atoms.md'
    },
    {
      name: 'Component Reference',
      // content: 'docs/ui.md',
      components: 'src/components/**/*.{ts,tsx}',
      exampleMode: 'expand', // 'hide' | 'collapse' | 'expand'
      usageMode: 'expand' // 'hide' | 'collapse' | 'expand'
    }
  ],
  theme: 'styleguide/Styleguide.scss',
}