const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    // ensure Cypress looks in the repository's cypress/e2e folder for specs
    specPattern: 'cypress/e2e/**/*.cy.js',
    // path to the support file relative to the project root
    supportFile: 'cypress/support/e2e.js',
    setupNodeEvents(on, config) {
      // implement node event listeners here if needed
      return config
    },
  },
})
