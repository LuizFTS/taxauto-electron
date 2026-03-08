# AppDesktop

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.3.9.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

```
app-desktop
├─ .agents
│  └─ skills
│     └─ interface-design
│        ├─ references
│        │  ├─ critique.md
│        │  ├─ example.md
│        │  ├─ principles.md
│        │  └─ validation.md
│        └─ SKILL.md
├─ .angular
│  └─ cache
│     └─ 20.3.18
│        └─ app-desktop
│           ├─ .tsbuildinfo
│           └─ vite
│              ├─ deps
│              │  ├─ @angular_cdk_bidi.js
│              │  ├─ @angular_cdk_bidi.js.map
│              │  ├─ @angular_common.js
│              │  ├─ @angular_common.js.map
│              │  ├─ @angular_common_http.js
│              │  ├─ @angular_common_http.js.map
│              │  ├─ @angular_core.js
│              │  ├─ @angular_core.js.map
│              │  ├─ @angular_forms.js
│              │  ├─ @angular_forms.js.map
│              │  ├─ @angular_material_icon.js
│              │  ├─ @angular_material_icon.js.map
│              │  ├─ @angular_platform-browser.js
│              │  ├─ @angular_platform-browser.js.map
│              │  ├─ @angular_router.js
│              │  ├─ @angular_router.js.map
│              │  ├─ chunk-2ZFTCAES.js
│              │  ├─ chunk-2ZFTCAES.js.map
│              │  ├─ chunk-55Z5APZ6.js
│              │  ├─ chunk-55Z5APZ6.js.map
│              │  ├─ chunk-ANR5MMQ4.js
│              │  ├─ chunk-ANR5MMQ4.js.map
│              │  ├─ chunk-RSS3ODKE.js
│              │  ├─ chunk-RSS3ODKE.js.map
│              │  ├─ chunk-RWYQOGLY.js
│              │  ├─ chunk-RWYQOGLY.js.map
│              │  ├─ chunk-WDMUDEB6.js
│              │  ├─ chunk-WDMUDEB6.js.map
│              │  ├─ chunk-XH3PQN2P.js
│              │  ├─ chunk-XH3PQN2P.js.map
│              │  ├─ chunk-ZVKCKDV4.js
│              │  ├─ chunk-ZVKCKDV4.js.map
│              │  ├─ package.json
│              │  ├─ rxjs.js
│              │  ├─ rxjs.js.map
│              │  ├─ zone__js.js
│              │  ├─ zone__js.js.map
│              │  └─ _metadata.json
│              └─ deps_ssr
│                 ├─ package.json
│                 └─ _metadata.json
├─ .editorconfig
├─ angular.json
├─ package-lock.json
├─ package.json
├─ public
│  └─ favicon.ico
├─ README.md
├─ src
│  ├─ app
│  │  ├─ app.config.ts
│  │  ├─ app.html
│  │  ├─ app.routes.ts
│  │  ├─ app.scss
│  │  ├─ app.spec.ts
│  │  ├─ app.ts
│  │  ├─ layouts
│  │  │  └─ window-layout
│  │  │     ├─ window-layout.html
│  │  │     ├─ window-layout.scss
│  │  │     ├─ window-layout.spec.ts
│  │  │     └─ window-layout.ts
│  │  ├─ models
│  │  │  ├─ apuracao-resultado.model.ts
│  │  │  ├─ arquivo-fiscal.model.ts
│  │  │  └─ periodo.model.ts
│  │  ├─ pages
│  │  │  ├─ apuracao
│  │  │  │  ├─ apuracao.html
│  │  │  │  ├─ apuracao.scss
│  │  │  │  ├─ apuracao.ts
│  │  │  │  └─ components
│  │  │  │     ├─ periodo-criar-modal-component
│  │  │  │     │  ├─ periodo-criar-modal-component.html
│  │  │  │     │  ├─ periodo-criar-modal-component.scss
│  │  │  │     │  └─ periodo-criar-modal-component.ts
│  │  │  │     ├─ processamento
│  │  │  │     │  ├─ processamento.html
│  │  │  │     │  ├─ processamento.scss
│  │  │  │     │  └─ processamento.ts
│  │  │  │     └─ resultado
│  │  │  │        ├─ resultado.html
│  │  │  │        ├─ resultado.scss
│  │  │  │        └─ resultado.ts
│  │  │  ├─ difal
│  │  │  │  ├─ difal.html
│  │  │  │  ├─ difal.scss
│  │  │  │  ├─ difal.spec.ts
│  │  │  │  └─ difal.ts
│  │  │  ├─ filiais
│  │  │  │  ├─ filiais.html
│  │  │  │  ├─ filiais.scss
│  │  │  │  └─ filiais.ts
│  │  │  ├─ home
│  │  │  │  ├─ home.html
│  │  │  │  ├─ home.scss
│  │  │  │  └─ home.ts
│  │  │  └─ livros-fiscais
│  │  │     ├─ components
│  │  │     │  └─ filiais-modal
│  │  │     │     ├─ filiais-modal.html
│  │  │     │     ├─ filiais-modal.scss
│  │  │     │     ├─ filiais-modal.spec.ts
│  │  │     │     └─ filiais-modal.ts
│  │  │     ├─ livros-fiscais.html
│  │  │     ├─ livros-fiscais.scss
│  │  │     └─ livros-fiscais.ts
│  │  ├─ services
│  │  │  ├─ api.service.ts
│  │  │  ├─ electron.service.ts
│  │  │  └─ modal.service.ts
│  │  ├─ shared
│  │  │  └─ components
│  │  │     ├─ button
│  │  │     │  ├─ button.html
│  │  │     │  ├─ button.scss
│  │  │     │  ├─ button.spec.ts
│  │  │     │  └─ button.ts
│  │  │     ├─ modal
│  │  │     │  ├─ modal.html
│  │  │     │  ├─ modal.scss
│  │  │     │  ├─ modal.spec.ts
│  │  │     │  └─ modal.ts
│  │  │     ├─ select
│  │  │     │  ├─ select.html
│  │  │     │  ├─ select.scss
│  │  │     │  ├─ select.spec.ts
│  │  │     │  └─ select.ts
│  │  │     ├─ sidemenu
│  │  │     │  ├─ sidemenu.html
│  │  │     │  ├─ sidemenu.scss
│  │  │     │  ├─ sidemenu.spec.ts
│  │  │     │  └─ sidemenu.ts
│  │  │     └─ topbar
│  │  │        ├─ topbar.html
│  │  │        ├─ topbar.scss
│  │  │        ├─ topbar.spec.ts
│  │  │        └─ topbar.ts
│  │  └─ types
│  │     └─ modal.types.ts
│  ├─ index.html
│  ├─ main.ts
│  └─ styles.scss
├─ tsconfig.app.json
├─ tsconfig.json
└─ tsconfig.spec.json

```