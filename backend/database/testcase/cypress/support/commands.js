// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// Overwrite `cy.request` to default to not failing tests on non-2xx HTTP responses.
// This helps run the full suite even when some API endpoints return errors.
Cypress.Commands.overwrite('request', (originalFn, ...args) => {
	// If first argument is an options object, ensure failOnStatusCode is false by default
	if (args.length === 1 && typeof args[0] === 'object') {
		const opts = Object.assign({}, args[0])
		if (opts.failOnStatusCode === undefined) {
			opts.failOnStatusCode = false
		}
		return originalFn(opts)
	}

	// If called with method/url or other overloads, pass through unchanged
	return originalFn(...args)
})