# Implementation Plan - Gravitas Grounded Research Station

The goal is to deploy a self-hosted "Research Station" for Gravitas members using `code-server` (VS Code in the browser), customized into three distinct modes:
1.  **Rich Editor** (WYSIWYG Markdown)
2.  **Research View** (Split Panes + PDF-to-Text)
3.  **Beach Mode** (E-Ink/Mobile optimized)

## User Review Required
> [!IMPORTANT]
> **Constraint Check:** This plan assumes we are using the existing 48GB/16-core server.
> **Security:** We will rely on Linux user isolation (OS-level security) for the MVP. Docker isolation is deferred to Phase 2.

## Proposed Changes

### Infrastructure Layer
#### [NEW] `scripts/deploy_research_station.sh`
- **Purpose:** Automates the installation of code-server and required dependencies.
- **Key Actions:**
    - Installs strictly defined version of `code-server`.
    - Creates the `gravitas-research` system service.
    - Configures the bind address (127.0.0.1:8080) for Nginx reverse proxying.

#### [NEW] `scripts/provision_user.sh`
- **Purpose:** Creates a new "Vault" for a user.
- **Key Actions:**
    - Creates Linux user (if not exists) or dedicated workspace folder.
    - Symlinks the shared "Library" folder.
    - **Crucial:** Pre-populates the `.vscode/settings.json` and `.vscode/extensions.json` to enforce our "Grounded" settings.

### Configuration & Customization
#### [NEW] `config/research-station/settings.json`
- **Purpose:** The "Master Settings" file that gets copied to every user.
- **Content:**
    - Disables telemetry.
    - Hides "Run/Debug" and "Source Control" sidebars by default.
    - Configures "Auto Save" to `afterDelay`.
    - **Beach Mode Key:** `cursorBlinking: "solid"`, `smoothScrolling: false`.

#### [NEW] `config/research-station/extensions_list.txt`
- **Purpose:** List of extensions to auto-install for every user.
- **Includes:**
    - `yzhang.markdown-all-in-one` (General helpers)
    - `mushan.vscode-paste-image` (Paste images -> auto-save to /assets)
    - `jebbs.markdown-extended` (Export to PDF/HTML)
    - `tomoki1207.pdf` (PDF Viewer in-editor)
    - **[TBD]** `Mark Sharp` or equivalent for WYSIWYG.

### Integration Layer
#### [MODIFY] `code-oss-browser-vault.md`
- **Status:** Already updated. Serves as the source of truth.

## Verification Plan

### Automated Tests
- **Script Validation:** Run `deploy_research_station.sh --dry-run` to verify dependency checks.
- **Port Check:** Verify `curl localhost:8080` returns the code-server login page (after deploy).

### Manual Verification (User-Driven)
This is a highly visual feature, so manual verification is key.
1.  **The "Writer" Test:**
    - Open a `.md` file.
    - Verify "Rich Mode" toolbar appears.
    - Paste an image from clipboard. Verify it saves to `./assets` and links correctly.
2.  **The "Researcher" Test:**
    - Open a PDF in the left pane.
    - Open a `.md` file in the right pane.
    - Verify scrolling is independent.
3.  **The "Beach" Test (Mobile):**
    - Connect via Phone.
    - Verify "High Contrast" theme is active (or selectable).
    - Verify no animations/smooth scrolling (crisp updates).
