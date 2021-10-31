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
      name: 'Chrome',
      content: 'src/components/chrome/Chrome.md'
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
      name: 'Charts',
      content: 'styleguide/Charts.md'
    },
    {
      name: 'Profile',
      content: 'src/apps/profile/Profile.md'
    },
    {
      name: 'Component Reference',
      components: 'src/components/shared/**/*.{ts,tsx}',
      exampleMode: 'expand', // 'hide' | 'collapse' | 'expand'
      usageMode: 'expand' // 'hide' | 'collapse' | 'expand'
    }
  ],
  // only include documented components
  skipComponentsWithoutExample: true,
  theme: 'styleguide/Styleguide.scss',
}