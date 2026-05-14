---
tags:
  - projekt/packcheck
---

> 🤖 Auto-generiert – manuelle Edits werden überschrieben

# PackCheck — Frontend

Next.js 14 mit App-Router, TypeScript strict, Tailwind CSS, Three.js für
3D-Hero-Elemente. Build-Output ist `standalone` — das Docker-Image kommt
ohne volle `node_modules` aus, dadurch ~10× kleiner.

## App-Router-Struktur

```
app/
├── layout.tsx               Root-Layout (Header, Providers, CookieBanner)
├── page.tsx                 Landing
├── about/                   Static
├── contact/                 Form
├── legal/                   Impressum / DSGVO / AGB
├── login/                   Public, redirect to /dashboard|/admin if logged in
├── register/                Public, registriert via /auth/register
├── forgot-password/         Frontend existiert, Backend-Flow fehlt (siehe [[offene_fragen]])
├── process/                 Erklärt den Verpackungs-Workflow
├── dashboard/               Customer-Bereich (auth required)
└── admin/                   Admin-Bereich (auth + is_admin required)
```

## Auth-Guard via `middleware.ts`

Cookie-basiert, läuft auf jeder Page-Request (außer `_next/static`,
`_next/image`, `favicon.ico`, `api`).

| Route-Pattern | Bedingung | Aktion |
|---|---|---|
| `/dashboard/**`, `/admin/**` | kein `token`-Cookie | Redirect → `/login?redirect=<path>` |
| `/admin/**` | `token` da, aber `isAdmin != 'true'` | Redirect → `/dashboard` |
| `/login`, `/register` | `token` da | Redirect → `/admin` oder `/dashboard` je nach Rolle |

> **Sicherheits-Hinweis:** Der `isAdmin`-Cookie wird im Browser gelesen
> und ist **nicht httpOnly** — die Middleware vertraut ihm nur für
> Routing-Hinweise. Die *autoritative* Admin-Prüfung passiert serverseitig
> per `req.user.isAdmin` aus dem JWT (siehe [[security_auth]]).

## API-Client (`lib/api.ts`)

Single axios-Instance mit zwei Interceptors:

- **Request-Interceptor:** Liest `localStorage.getItem('token')` (im
  Browser) und setzt `Authorization: Bearer <token>`. Cookie ist nur
  Backup für SSR/Middleware.
- **Response-Interceptor:** Bei `401` → `localStorage.removeItem('token')`
  + `window.location.href = '/login'` (Schutz gegen Endlos-Redirect-Loop:
  nur falls `pathname !== '/login'`).

Module-Exports: `authAPI`, `customerAPI`, `adminAPI` mappen 1:1 auf das
Backend-Routing aus [[api_contract]].

`API_URL` kommt aus `process.env.NEXT_PUBLIC_API_URL` (Build-time) mit
Fallback `https://api.lucidexpress.de`.

## State-Storage

| Was | Wo | Warum |
|---|---|---|
| JWT-Token | `localStorage` + Cookie `token` (Domain `.lucidexpress.de`) | localStorage für `Authorization`-Header, Cookie für Server-Middleware |
| `isAdmin`-Flag | Cookie `isAdmin=true|false` | Middleware liest es ohne Token zu parsen |
| User-Objekt | nichts persistent — `GET /auth/me` on demand | Vermeidet Stale-Daten |

## Three.js / 3D-Komponenten

`@react-three/fiber` + `@react-three/drei`, DRACO-Decoder unter
`public/draco/` (756 KB, Mesh-Kompression).

| Komponente | Zweck |
|---|---|
| `RealisticGlobe.tsx` | Hero-Globe auf Landing, nutzt `public/earth.jpg` als Texture |
| `DynamicGlobe.tsx` | Lighter-Variant, lazy-loaded |
| `PackagingViewer.tsx` | 3D-Vorschau der Verpackungstypen im Dashboard |
| `Success3DAnimation.tsx` | Erfolgs-Animation nach Form-Submit |
| `ParticlesBackground.tsx`, `FloatingElements.tsx` | dekorative Backgrounds |

## UI-Layer

Tailwind-only, kein Component-Framework. Eigene Primitives:
`Modal.tsx`, `Toast.tsx`, `LoadingSpinner.tsx`, `Header.tsx`,
`Footer.tsx`, `Logo.tsx`, `Icons.tsx`. Domain-spezifische:
`ExportModal.tsx`, `QuarterlyConfirmModal.tsx`, `UrgencyBanner.tsx`,
`CookieBanner.tsx`.

`Providers.tsx` umschließt App in `app/layout.tsx` (Toast-Context,
ggf. Theme).

## Internationalisierung

Locales unter `public/locales/` — siehe Email-Templates in `lib/`,
die DE/EN/ZH Versionen enthalten. UI-Sprachschalter ist im
Aktuell-Stand noch nicht in der Middleware verdrahtet.

## Public Assets

```
public/
├── draco/        DRACO-Decoder (von Three.js zur Mesh-Decompression geladen)
├── earth.jpg     Hero-Globe-Texture
├── images/       Marketing-Bilder
├── locales/      i18n-Strings
└── favicon.ico
```
