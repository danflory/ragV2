# Nexus Dashboard Version Policy

## Semantic Versioning (MAJOR.MINOR.PATCH)

The Nexus Dashboard uses semantic versioning following the pattern: `vMAJOR.MINOR.PATCH`

### Version Location
- **File:** `dashboard/index.html`
- **Line:** Header `<h1>` tag (currently line 34-36)

### Increment Rules

#### PATCH (v4.2.X)
Increment for:
- UI bug fixes
- Minor styling tweaks
- Performance optimizations
- Non-breaking improvements

#### MINOR (v4.X.0)
Increment for:
- New dashboard features
- New widgets or panels
- New API integrations
- Backward-compatible functionality

#### MAJOR (vX.0.0)
Increment for:
- Complete UI redesign
- Breaking changes to dashboard API
- Fundamental architecture changes

### Automatic Increment Policy

**RULE:** Every edit to the Nexus Dashboard (`dashboard/index.html`, `dashboard/app.js`, `dashboard/style.css`) must increment the **PATCH** version.

**Example:**
- Current: v4.2.1
- After next edit: v4.2.2
- After feature addition: v4.3.0

### Version Change Log

| Version | Date | Changes |
|---------|------|---------|
| v4.2.1 | 2026-01-05 | Added VRAM monitoring, mode restrictions UI, increased timeouts |
| v4.2.0 | 2026-01-XX | Initial Nexus Dashboard with SSE health streaming |
