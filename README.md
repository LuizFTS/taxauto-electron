
```
taxauto-electron
├─ app-desktop
│  ├─ .agents
│  │  └─ skills
│  │     └─ interface-design
│  │        ├─ references
│  │        │  ├─ critique.md
│  │        │  ├─ example.md
│  │        │  ├─ principles.md
│  │        │  └─ validation.md
│  │        └─ SKILL.md
│  ├─ .editorconfig
│  ├─ .prettierrc.json
│  ├─ angular.json
│  ├─ eslint.config.js
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  └─ favicon.ico
│  ├─ README.md
│  ├─ src
│  │  ├─ app
│  │  │  ├─ app.config.ts
│  │  │  ├─ app.html
│  │  │  ├─ app.routes.ts
│  │  │  ├─ app.scss
│  │  │  ├─ app.spec.ts
│  │  │  ├─ app.ts
│  │  │  ├─ core
│  │  │  │  ├─ config
│  │  │  │  │  └─ tipos-arquivo.config.ts
│  │  │  │  ├─ index.ts
│  │  │  │  ├─ models
│  │  │  │  │  ├─ apuracao-detalhe.model.ts
│  │  │  │  │  ├─ apuracao-filial.model.ts
│  │  │  │  │  ├─ arquivo-fiscal.model.ts
│  │  │  │  │  ├─ criar-periodo-response.model.ts
│  │  │  │  │  ├─ empresa.model.ts
│  │  │  │  │  ├─ filial.model.ts
│  │  │  │  │  ├─ grupo-empresas.model.ts
│  │  │  │  │  ├─ periodo.model.ts
│  │  │  │  │  └─ processamento-status.model.ts
│  │  │  │  ├─ services
│  │  │  │  │  ├─ api
│  │  │  │  │  │  └─ apuração-api.service.ts
│  │  │  │  │  ├─ electron.service.ts
│  │  │  │  │  └─ modal.service.ts
│  │  │  │  └─ types
│  │  │  │     ├─ electron.d.ts
│  │  │  │     ├─ modal.d.ts
│  │  │  │     ├─ status-arquivo.d.ts
│  │  │  │     ├─ status-periodo.d.ts
│  │  │  │     └─ tipo-arquivo.d.ts
│  │  │  ├─ features
│  │  │  │  ├─ apuracao
│  │  │  │  │  ├─ apuracao.html
│  │  │  │  │  ├─ apuracao.scss
│  │  │  │  │  ├─ apuracao.ts
│  │  │  │  │  └─ components
│  │  │  │  │     ├─ periodo-criar-modal-component
│  │  │  │  │     │  ├─ periodo-criar-modal-component.html
│  │  │  │  │     │  ├─ periodo-criar-modal-component.scss
│  │  │  │  │     │  └─ periodo-criar-modal-component.ts
│  │  │  │  │     ├─ processamento
│  │  │  │  │     │  ├─ processamento.html
│  │  │  │  │     │  ├─ processamento.scss
│  │  │  │  │     │  └─ processamento.ts
│  │  │  │  │     └─ resultado
│  │  │  │  │        ├─ resultado.html
│  │  │  │  │        ├─ resultado.scss
│  │  │  │  │        └─ resultado.ts
│  │  │  │  ├─ difal
│  │  │  │  │  ├─ difal.html
│  │  │  │  │  ├─ difal.scss
│  │  │  │  │  └─ difal.ts
│  │  │  │  ├─ filiais
│  │  │  │  │  ├─ filiais.html
│  │  │  │  │  ├─ filiais.scss
│  │  │  │  │  └─ filiais.ts
│  │  │  │  └─ livros-fiscais
│  │  │  │     ├─ components
│  │  │  │     │  └─ filiais-modal
│  │  │  │     │     ├─ filiais-modal.html
│  │  │  │     │     ├─ filiais-modal.scss
│  │  │  │     │     ├─ filiais-modal.spec.ts
│  │  │  │     │     └─ filiais-modal.ts
│  │  │  │     ├─ livros-fiscais.html
│  │  │  │     ├─ livros-fiscais.scss
│  │  │  │     └─ livros-fiscais.ts
│  │  │  └─ shared
│  │  │     ├─ components
│  │  │     │  ├─ button
│  │  │     │  │  ├─ button.html
│  │  │     │  │  ├─ button.scss
│  │  │     │  │  ├─ button.spec.ts
│  │  │     │  │  └─ button.ts
│  │  │     │  ├─ modal
│  │  │     │  │  ├─ modal.html
│  │  │     │  │  ├─ modal.scss
│  │  │     │  │  ├─ modal.spec.ts
│  │  │     │  │  └─ modal.ts
│  │  │     │  ├─ select
│  │  │     │  │  ├─ select.html
│  │  │     │  │  ├─ select.scss
│  │  │     │  │  ├─ select.spec.ts
│  │  │     │  │  └─ select.ts
│  │  │     │  ├─ sidemenu
│  │  │     │  │  ├─ sidemenu.html
│  │  │     │  │  ├─ sidemenu.scss
│  │  │     │  │  ├─ sidemenu.spec.ts
│  │  │     │  │  └─ sidemenu.ts
│  │  │     │  └─ topbar
│  │  │     │     ├─ topbar.html
│  │  │     │     ├─ topbar.scss
│  │  │     │     ├─ topbar.spec.ts
│  │  │     │     └─ topbar.ts
│  │  │     ├─ index.ts
│  │  │     └─ layouts
│  │  ├─ index.html
│  │  ├─ main.ts
│  │  └─ styles.scss
│  ├─ tsconfig.json
│  └─ tsconfig.spec.json
├─ backend
│  ├─ core
│  │  ├─ config
│  │  │  └─ settings.py
│  │  └─ database
│  │     └─ connection.py
│  ├─ main.py
│  ├─ main.spec
│  ├─ modules
│  │  ├─ automation
│  │  │  ├─ application
│  │  │  │  ├─ dto
│  │  │  │  │  └─ livros_fiscais_dto.py
│  │  │  │  └─ usecases
│  │  │  │     └─ run_livros_fiscais.py
│  │  │  ├─ automations
│  │  │  │  └─ livros_fiscais
│  │  │  │     ├─ navigation
│  │  │  │     │  ├─ erp_session.py
│  │  │  │     │  └─ navigate_to_livros_fiscais.py
│  │  │  │     ├─ orchestrator
│  │  │  │     │  └─ livros_fiscais_orchestrator.py
│  │  │  │     ├─ services
│  │  │  │     │  ├─ close_book_service.py
│  │  │  │     │  ├─ open_book_service.py
│  │  │  │     │  ├─ refresh_book_service.py
│  │  │  │     │  ├─ save_pdf_service.py
│  │  │  │     │  └─ save_spreadsheet_service.py
│  │  │  │     └─ state
│  │  │  │        └─ book_state_service.py
│  │  │  ├─ domain
│  │  │  │  ├─ entities
│  │  │  │  │  └─ tasks.py
│  │  │  │  └─ repositories
│  │  │  ├─ infrastructure
│  │  │  └─ presentation
│  │  │     └─ routes
│  │  │        └─ livros_fiscais_routes.py
│  │  └─ data_process
│  │     ├─ application
│  │     │  └─ usecases
│  │     │     └─ create_period.py
│  │     ├─ domain
│  │     │  └─ entities
│  │     │     └─ periodo.py
│  │     ├─ infrastructure
│  │     │  └─ repositories
│  │     │     └─ sqlite_period_repository.py
│  │     └─ presentation
│  │        └─ routes
│  │           └─ periodo_routes.py
│  ├─ pyproject.toml
│  ├─ requirements.txt
│  ├─ scripts
│  │  ├─ run-api.ps1
│  │  └─ setup.ps1
│  └─ shared
│     ├─ application
│     ├─ domain
│     │  └─ errors.py
│     ├─ infrastructure
│     │  └─ filesystem
│     │     └─ workspace_manager.py
│     └─ presentation
├─ electron
│  ├─ main.js
│  └─ preload.js
├─ package-lock.json
├─ package.json
└─ resources
   └─ scripts
      └─ bot_automacao.py

```