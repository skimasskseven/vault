#!/usr/bin/env python3
"""build_knowledge_graph.py

Synchronisiert Projekte aus einem Dev-Verzeichnis in einen Obsidian-Vault
und verknüpft sie inhaltlich, so dass Muster über Projekte hinweg sichtbar
werden.

USAGE
    python build_knowledge_graph.py [--dev-dir PATH] [--vault-dir PATH]
                                    [--projects p1,p2,...] [--force]
                                    [--no-git-pull]

Standard-Pfade werden plattformabhängig erraten:
    Windows:  C:\\Users\\Max\\Desktop\\vault            (Vault)
              C:\\Users\\Max\\dev oder %USERPROFILE%\\dev (Dev)
    WSL:      /mnt/c/Users/Max/Desktop/vault            (Vault)
              ~/dev                                       (Dev)
    Linux:    ~/dev/vault                                 (Vault)
              ~/dev                                       (Dev)

Auto-generierte Dateien (werden bei jedem Lauf überschrieben):
    20_projekte/<projekt>/_MOC.md
    20_projekte/<projekt>/übersicht.md
    10_infrastruktur/*.md
    00_meta/Pattern-Dashboard.md

Manuell editierbare Dateien (nur beim ersten Lauf kopiert, danach nie
überschrieben):
    20_projekte/<projekt>/<kopierte-doc>.md  (aus <repo>/docs/)
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# =============================================================================
# Konfiguration
# =============================================================================

AUTO_BANNER = "> 🤖 Auto-generiert – manuelle Edits werden überschrieben"

COMPONENTS = {
    # ---------- Languages / Frameworks / Frontend ----------
    "Next.js": {
        "package_deps": ["next"],
        "category": "frontend",
        "desc": "React-basiertes Full-Stack-Framework (SSR/SSG, App Router).",
    },
    "React": {
        "package_deps": ["react"],
        "category": "frontend",
        "desc": "UI-Library für komponentenbasierte Frontends.",
    },
    "Tailwind CSS": {
        "package_deps": ["tailwindcss"],
        "category": "frontend",
        "desc": "Utility-First CSS-Framework.",
    },
    "Three.js": {
        "package_deps": ["three", "@react-three/fiber", "@react-three/drei"],
        "category": "frontend",
        "desc": "WebGL-basiertes 3D-Rendering (oft mit react-three-fiber).",
    },
    "GSAP": {
        "package_deps": ["gsap"],
        "category": "frontend",
        "desc": "Animations-Library für High-End-Web-Animationen.",
    },
    "Flutter": {
        "keywords": ["flutter", "dart", "riverpod"],
        "category": "frontend",
        "desc": "Cross-Platform Mobile-Framework von Google (Dart).",
    },
    "Mapbox": {
        "keywords": ["mapbox"],
        "category": "frontend",
        "desc": "Vector-Maps + Geocoding (Mobile/Web).",
    },
    "TypeScript": {
        "package_deps": ["typescript"],
        "category": "frontend",
        "desc": "Typisiertes JavaScript.",
    },

    # ---------- Backend / Runtime ----------
    "FastAPI": {
        "py_deps": ["fastapi"],
        "category": "backend",
        "desc": "Async Python-Web-Framework auf Starlette + Pydantic.",
    },
    "SQLAlchemy": {
        "py_deps": ["sqlalchemy"],
        "category": "backend",
        "desc": "Python ORM/Query-Builder (async via asyncpg).",
    },
    "Alembic": {
        "py_deps": ["alembic"],
        "category": "backend",
        "desc": "SQLAlchemy-Migrations-Tool.",
    },
    "Archon": {
        "keywords": ["archon", "openclaw"],
        "category": "ai",
        "desc": "Multi-Agent-Workflow-Engine (vendored als Submodul, "
                "treibt Conformis' Lead-Pipeline).",
    },

    # ---------- Datenbanken ----------
    "PostgreSQL": {
        "compose_image": [r"postgres(:|\b)", r"postgis/postgis"],
        "env_vars": [r"^POSTGRES_", r"DATABASE_URL.*postgres"],
        "py_deps": ["asyncpg", "psycopg"],
        "package_deps": ["postgres"],
        "category": "db",
        "desc": "Open-Source-RDBMS. Default-DB für State + Audit-Logs.",
    },
    "PostGIS": {
        "compose_image": [r"postgis/postgis"],
        "py_deps": ["geoalchemy2"],
        "category": "db",
        "desc": "PostgreSQL-Extension für Geodaten (Spatial Queries, "
                "Indexe). Pflicht für Map/GPS-Features.",
    },

    # ---------- External Services ----------
    "Telegram Bot": {
        "env_vars": [r"^TELEGRAM_"],
        "category": "comms",
        "desc": "Bot-API für Notifications, Approval-Flows, Alerts.",
    },
    "Stripe": {
        "package_deps": ["stripe"],
        "env_vars": [r"^STRIPE_"],
        "category": "payment",
        "desc": "Payment-Provider (Checkout, Subscriptions, Webhooks).",
    },
    "Brevo": {
        "env_vars": [r"^BREVO_"],
        "category": "email",
        "desc": "Transactional + Marketing-Email-Provider (ex-Sendinblue).",
    },
    "OpenRouter": {
        "env_vars": [r"^OPENROUTER_"],
        "category": "ai",
        "desc": "LLM-Gateway, vereinheitlicht Claude/GPT/Mistral/… hinter "
                "OpenAI-kompatibler API.",
    },
    "Claude API": {
        "env_vars": [r"^CLAUDE_API_KEY", r"^CLAUDE_CODE_OAUTH_TOKEN",
                     r"^ANTHROPIC_API_KEY"],
        "keywords": ["claude haiku", "claude sonnet", "claude opus",
                     "@anthropic-ai/sdk",
                     "@anthropic-ai/claude-agent-sdk"],
        "category": "ai",
        "desc": "Anthropic Claude LLM (Haiku/Sonnet/Opus).",
    },
    "Strava API": {
        "keywords": ["strava"],
        "category": "external",
        "desc": "OAuth2-API für Fitness-Aktivitäten, Segments, Athleten.",
    },
    "Apple Health": {
        "keywords": ["apple health", "healthkit"],
        "category": "external",
        "desc": "On-Device Health-Data (iOS) — kein Server-Token.",
    },
    "Garmin": {
        "keywords": ["garmin"],
        "category": "external",
        "desc": "OAuth-API für Garmin-Connect Fitness-Daten.",
    },
    "Google Fit": {
        "keywords": ["google fit"],
        "category": "external",
        "desc": "OAuth-API für Android Fitness-Daten.",
    },
    "Firebase Cloud Messaging": {
        "keywords": ["fcm push", "firebase cloud messaging"],
        "category": "comms",
        "desc": "Push-Notifications (iOS + Android).",
    },
    "Instagram (Native Share)": {
        "keywords": ["instagram stories", "instagram share"],
        "category": "external",
        "desc": "Social-Sharing via Native-Share-Sheet (kein Server-Token).",
    },

    # ---------- Lead-Gen / Compliance APIs (Conformis) ----------
    "OSM Overpass": {
        "env_vars": [r"^OVERPASS_", r"^OSM_"],
        "keywords": ["overpass-api"],
        "category": "external",
        "desc": "OpenStreetMap-Query-API. Lead-Source für DE-KMUs ohne "
                "Handelsregister-Key.",
    },
    "Companies House": {
        "env_vars": [r"^COMPANIES_HOUSE_"],
        "category": "external",
        "desc": "UK-Register-API (Firmenstammdaten).",
    },
    "DIP (Bundestag)": {
        "env_vars": [r"^DIP_API_"],
        "category": "external",
        "desc": "Deutscher Bundestag — parlamentarische Vorgänge "
                "(Gesetzgebungsmonitoring).",
    },
    "Tranco": {
        "env_vars": [r"^TRANCO_"],
        "keywords": ["tranco"],
        "category": "external",
        "desc": "Domain-Popularitäts-Ranking (Top-1M-Liste).",
    },

    # ---------- Infra ----------
    "Docker": {
        "files": ["docker-compose.yml", "Dockerfile"],
        "category": "infra",
        "desc": "Containerisierung (lokale Dev + Prod-Deployment).",
    },
    "Caddy / Let's Encrypt": {
        "env_vars": [r"^LE_EMAIL"],
        "keywords": ["caddy"],
        "category": "infra",
        "desc": "Reverse-Proxy mit automatischem ACME/TLS.",
    },
    "DuckDNS": {
        "env_vars": [r"^DUCKDNS_"],
        "category": "infra",
        "desc": "Dynamisches DNS (Hobby/Bootstrap-Hostnames).",
    },
    "Hostinger VPS": {
        "keywords": ["hostinger", "vps"],
        "category": "infra",
        "desc": "Self-hosted Linux-VPS (Hostinger). Trägt sowohl Conformis "
                "als auch tutgut-Backend.",
    },
    "Playwright": {
        "package_deps": ["playwright", "@playwright/test"],
        "keywords": ["playwright"],
        "category": "external",
        "desc": "Browser-Automation (Click-Guides, E2E-Tests, Screenshots).",
    },
    "bcrypt": {
        "py_deps": ["bcrypt"],
        "package_deps": ["bcrypt"],
        "category": "backend",
        "desc": "Password/Session-Token-Hashing.",
    },
    "pgcrypto": {
        "keywords": ["pgcrypto"],
        "category": "db",
        "desc": "PostgreSQL-Extension für symmetrische Verschlüsselung "
                "(Integration-Tokens at rest).",
    },
}


DOMAIN_HEURISTICS = {
    "compliance": ["compliance", "dsgvo", "gdpr", "rechteradar", "law-monitor"],
    "b2b-saas": ["b2b", "saas", "cold-outreach", "lead-finder", "outreach"],
    "consumer-mobile": ["flutter", "mobile", "social", "fitness"],
    "geo-spatial": ["postgis", "mapbox", "gps", "geo"],
    "ai-agents": ["archon", "openclaw", "agent", "orchestrator"],
}


# =============================================================================
# Pfad-Auto-Detection
# =============================================================================

def detect_default_paths() -> tuple[Path, Path]:
    home = Path.home()
    system = platform.system()
    is_wsl = "microsoft" in platform.release().lower()

    if system == "Windows":
        dev = Path(r"C:\Users\Max\dev")
        if not dev.exists():
            dev = home / "dev"
        vault = Path(r"C:\Users\Max\Desktop\vault")
    elif is_wsl:
        dev = home / "dev"
        vault = Path("/mnt/c/Users/Max/Desktop/vault")
        if not vault.exists():
            vault = home / "dev" / "vault"
    else:
        dev = home / "dev"
        vault = home / "dev" / "vault"

    return dev, vault


# =============================================================================
# Git
# =============================================================================

def git_pull_if_repo(repo_path: Path) -> str:
    if not (repo_path / ".git").exists():
        return "kein git-repo"
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "pull", "--ff-only"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return f"pull ok: {result.stdout.strip().splitlines()[-1] if result.stdout.strip() else 'up-to-date'}"
        return f"pull fehlgeschlagen: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'unknown error'}"
    except Exception as exc:
        return f"pull-error: {exc}"


def last_commit_info(repo_path: Path) -> dict | None:
    candidates = [repo_path, repo_path / "code", repo_path / "docs"]
    for cand in candidates:
        if not (cand / ".git").exists():
            continue
        try:
            result = subprocess.run(
                ["git", "-C", str(cand), "log", "-1",
                 "--format=%h|%cI|%s"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                h, date, subject = result.stdout.strip().split("|", 2)
                return {"hash": h, "date": date, "subject": subject,
                        "subdir": cand.name if cand != repo_path else "."}
        except Exception:
            pass
    return None


# =============================================================================
# Repo-Scan
# =============================================================================

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def extract_package_deps(pkg_json_path: Path) -> set[str]:
    try:
        data = json.loads(pkg_json_path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    deps: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        if isinstance(data.get(key), dict):
            deps.update(data[key].keys())
    return deps


def extract_py_deps(path: Path) -> set[str]:
    content = read_text(path)
    if not content:
        return set()
    deps: set[str] = set()
    if path.name == "pyproject.toml":
        m = re.search(r"dependencies\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if m:
            for entry in re.findall(r'["\']([^"\']+)["\']', m.group(1)):
                pkg = re.split(r"[<>=!~\[]", entry)[0].strip().lower()
                if pkg:
                    deps.add(pkg)
        for m2 in re.finditer(
            r"\[project\.optional-dependencies\][^\[]*", content
        ):
            for entry in re.findall(r'["\']([^"\']+)["\']', m2.group(0)):
                pkg = re.split(r"[<>=!~\[]", entry)[0].strip().lower()
                if pkg:
                    deps.add(pkg)
    else:
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            pkg = re.split(r"[<>=!~\[;]", line)[0].strip().lower()
            if pkg:
                deps.add(pkg)
    return deps


def extract_compose_images_and_services(path: Path) -> tuple[set[str], set[str]]:
    content = read_text(path)
    images: set[str] = set()
    services: set[str] = set()
    if not content:
        return images, services
    for m in re.finditer(r"^\s*image:\s*(\S+)", content, re.MULTILINE):
        images.add(m.group(1).strip('"\''))
    in_services = False
    base_indent = None
    for line in content.splitlines():
        stripped = line.lstrip()
        if not in_services:
            if stripped.startswith("services:"):
                in_services = True
            continue
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(stripped)
        if base_indent is None:
            base_indent = indent
        if indent == base_indent and stripped.endswith(":"):
            services.add(stripped[:-1].strip())
        elif indent < (base_indent or 0):
            in_services = False
    return images, services


def extract_env_vars(path: Path) -> set[str]:
    content = read_text(path)
    vars_: set[str] = set()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=", line)
        if m:
            vars_.add(m.group(1))
    return vars_


def collect_indicators(repo_path: Path) -> dict:
    indicators: dict = {
        "package_deps": set(),
        "py_deps": set(),
        "compose_images": set(),
        "compose_services": set(),
        "env_vars": set(),
        "files_found": set(),
        "keywords_text": "",
    }

    skip_dirs = {"node_modules", ".git", ".venv", "venv", "__pycache__",
                 "dist", "build", ".next", "vendor"}

    code_dir = repo_path / "code"
    scan_roots = [code_dir if code_dir.exists() else repo_path]

    for root in scan_roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            rel = Path(dirpath).relative_to(root)
            depth = len(rel.parts)
            if depth > 3:
                dirnames[:] = []
                continue
            for fname in filenames:
                fp = Path(dirpath) / fname
                if fname == "package.json":
                    indicators["package_deps"] |= extract_package_deps(fp)
                    indicators["files_found"].add("package.json")
                elif fname == "pyproject.toml":
                    indicators["py_deps"] |= extract_py_deps(fp)
                    indicators["files_found"].add("pyproject.toml")
                elif fname == "requirements.txt":
                    indicators["py_deps"] |= extract_py_deps(fp)
                    indicators["files_found"].add("requirements.txt")
                elif re.match(r"docker-compose.*\.ya?ml$", fname):
                    imgs, svcs = extract_compose_images_and_services(fp)
                    indicators["compose_images"] |= imgs
                    indicators["compose_services"] |= svcs
                    indicators["files_found"].add("docker-compose.yml")
                elif fname == ".env.example":
                    indicators["env_vars"] |= extract_env_vars(fp)
                    indicators["files_found"].add(".env.example")
                elif fname == "Dockerfile":
                    indicators["files_found"].add("Dockerfile")

    keyword_files: list[Path] = []
    for cand in [repo_path / "CLAUDE.md", repo_path / "README.md",
                 (repo_path / "code" / "CLAUDE.md"),
                 (repo_path / "code" / "README.md")]:
        if cand.exists():
            keyword_files.append(cand)
    docs_dir = repo_path / "docs"
    if docs_dir.exists():
        for md in docs_dir.rglob("*.md"):
            try:
                if md.is_file() and md.stat().st_size <= 200_000:
                    keyword_files.append(md)
            except Exception:
                pass
    for env_ex in (repo_path / "code").rglob(".env.example") if (
            (repo_path / "code").exists()) else repo_path.rglob(".env.example"):
        if any(part in {"node_modules", "vendor", ".git"}
               for part in env_ex.parts):
            continue
        keyword_files.append(env_ex)

    raw_text = "\n".join(read_text(p) for p in keyword_files)
    indicators["keywords_text_raw"] = raw_text
    indicators["keywords_text"] = raw_text.lower()
    indicators["root_readmes"] = [
        p for p in [repo_path / "code" / "README.md",
                    repo_path / "README.md"]
        if p.exists()
    ]
    high_signal_files: list[Path] = []
    for cand in [repo_path / "CLAUDE.md", repo_path / "README.md",
                 repo_path / "code" / "CLAUDE.md",
                 repo_path / "code" / "README.md"]:
        if cand.exists():
            high_signal_files.append(cand)
    indicators["high_signal_text"] = "\n".join(
        read_text(p) for p in high_signal_files
    ).lower()

    return indicators


def detect_components(indicators: dict) -> list[str]:
    found: list[str] = []
    for name, spec in COMPONENTS.items():
        match = False

        for dep in spec.get("package_deps", []):
            if any(dep == pd or pd.startswith(dep + "/") or pd == dep
                   for pd in indicators["package_deps"]):
                match = True
                break

        if not match:
            for dep in spec.get("py_deps", []):
                if any(pd == dep or pd.startswith(dep + "-")
                       for pd in indicators["py_deps"]):
                    match = True
                    break

        if not match:
            for pat in spec.get("compose_image", []):
                if any(re.search(pat, img, re.IGNORECASE)
                       for img in indicators["compose_images"]):
                    match = True
                    break

        if not match:
            for svc in spec.get("compose_service", []):
                if svc in indicators["compose_services"]:
                    match = True
                    break

        if not match:
            for pat in spec.get("env_vars", []):
                if any(re.search(pat, v) for v in indicators["env_vars"]):
                    match = True
                    break

        if not match:
            for kw in spec.get("keywords", []):
                if kw.lower() in indicators["keywords_text"]:
                    match = True
                    break

        if not match:
            for fname in spec.get("files", []):
                if fname in indicators["files_found"]:
                    match = True
                    break

        if match:
            found.append(name)

    return found


def detect_domains(indicators: dict, project_name: str) -> list[str]:
    text = indicators.get("high_signal_text",
                          indicators["keywords_text"]) + " " + project_name.lower()
    return sorted([d for d, kws in DOMAIN_HEURISTICS.items()
                   if any(kw in text for kw in kws)])


# =============================================================================
# Vault-IO
# =============================================================================

def is_auto_generated(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:2048]
    except Exception:
        return False
    return AUTO_BANNER in head


def write_auto(path: Path, content: str, force: bool = False) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force and not is_auto_generated(path):
        return f"SKIP (manuell editiert): {path}"
    path.write_text(content, encoding="utf-8")
    return f"WROTE: {path}"


def copy_doc(src: Path, dst: Path, project: str) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not is_auto_generated(dst):
        return f"SKIP (manuell editiert): {dst}"
    raw = read_text(src)
    project_tag = f"projekt/{project}"

    if raw.startswith("---\n"):
        end = raw.find("\n---", 4)
        if end > 0:
            frontmatter = raw[4:end]
            rest = raw[end + 4:].lstrip("\n")
            frontmatter = ensure_project_tag(frontmatter, project_tag)
            content = (f"---\n{frontmatter}\n---\n\n"
                       f"{AUTO_BANNER}\n\n{rest}")
        else:
            content = (build_frontmatter([project_tag]) +
                       AUTO_BANNER + "\n\n" + raw)
    else:
        content = (build_frontmatter([project_tag]) +
                   AUTO_BANNER + "\n\n" + raw)

    dst.write_text(content, encoding="utf-8")
    return f"COPIED: {dst}"


def ensure_project_tag(frontmatter: str, project_tag: str) -> str:
    if project_tag in frontmatter:
        return frontmatter
    m = re.search(r"^tags\s*:\s*\[([^\]]*)\]\s*$",
                  frontmatter, re.MULTILINE)
    if m:
        existing = m.group(1).strip()
        new_list = f"[{existing}, {project_tag}]" if existing else f"[{project_tag}]"
        return frontmatter[:m.start()] + f"tags: {new_list}" + frontmatter[m.end():]
    m = re.search(r"^tags\s*:\s*\n((?:\s+-\s+\S+\s*\n)+)",
                  frontmatter, re.MULTILINE)
    if m:
        block = m.group(1)
        indent_match = re.match(r"^(\s+)-", block)
        indent = indent_match.group(1) if indent_match else "  "
        new_block = block + f"{indent}- {project_tag}\n"
        return frontmatter[:m.start()] + f"tags:\n{new_block}" + frontmatter[m.end():]
    sep = "" if frontmatter.endswith("\n") else "\n"
    return f"{frontmatter}{sep}tags:\n  - {project_tag}"


def build_frontmatter(tags: list[str], **extra: str) -> str:
    lines = ["---"]
    for k, v in extra.items():
        lines.append(f"{k}: {v}")
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + "\n"


def safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "-", name).strip()


# =============================================================================
# Generatoren
# =============================================================================

def gen_infra_file(component: str, spec: dict, used_by: list[str]) -> str:
    slug = safe_filename(component)
    tags = [f"infra/{slug.lower().replace(' ', '-')}"]
    category = spec.get("category", "infra")
    tags.append(f"stack-category/{category}")
    for proj in used_by:
        tags.append(f"used-in/{proj}")

    used_by_lines = "\n".join(f"- [[20_projekte/{p}/übersicht|{p}]]"
                              for p in sorted(used_by)) or "_(noch nicht verwendet)_"

    return f"""{build_frontmatter(tags, type='infrastruktur-komponente')}{AUTO_BANNER}

# {component}

{spec.get("desc", "_(keine Beschreibung hinterlegt)_")}

## Verwendet in

{used_by_lines}

## Kategorie

`{category}`

## Konfigurationsnotizen

_(automatisch aus Specs extrahiert — bei Bedarf hier manuell ergänzen, aber dann den AUTO_BANNER oben entfernen, sonst wird die Datei beim nächsten Lauf überschrieben.)_
"""


def gen_mermaid_for_project(components: list[str], project: str) -> str:
    cats: dict[str, list[str]] = defaultdict(list)
    for c in components:
        cat = COMPONENTS[c].get("category", "external")
        cats[cat].append(c)

    lines = ["```mermaid", "flowchart LR"]
    lines.append('  user(["👤 User"])')

    if cats.get("frontend"):
        fe = " / ".join(cats["frontend"][:2])
        lines.append(f'  fe["🖥️  Frontend<br/>{fe}"]')
        lines.append("  user --> fe")

    if cats.get("backend") or cats.get("ai"):
        backend_label_parts = cats.get("backend", []) + cats.get("ai", [])
        be = " / ".join(backend_label_parts[:3])
        lines.append(f'  be["⚙️  Backend<br/>{be}"]')
        if cats.get("frontend"):
            lines.append("  fe --> be")
        else:
            lines.append("  user --> be")

    if cats.get("db"):
        db = " + ".join(cats["db"])
        lines.append(f'  db[("💾 {db}")]')
        if cats.get("backend") or cats.get("ai"):
            lines.append("  be --> db")

    side_buckets = {
        "payment":   ("💳 Payments",        ""),
        "email":     ("📧 Email",            ""),
        "comms":     ("📣 Notifications",    ""),
        "external":  ("🌐 External APIs",    ""),
    }
    for cat, (label, _) in side_buckets.items():
        items = cats.get(cat)
        if not items:
            continue
        node_id = f"{cat}_node"
        items_str = "<br/>".join(items)
        lines.append(f'  {node_id}["{label}<br/>{items_str}"]')
        if cats.get("backend") or cats.get("ai"):
            lines.append(f"  be --> {node_id}")
        elif cats.get("frontend"):
            lines.append(f"  fe --> {node_id}")
        else:
            lines.append(f"  user --> {node_id}")

    lines.append("```")
    return "\n".join(lines)


def gen_uebersicht(project: str, components: list[str],
                   indicators: dict, domains: list[str],
                   purpose_paragraph: str) -> str:
    tags = [f"projekt/{project}", "type/overview"]
    for d in domains:
        tags.append(f"domain/{d}")

    mermaid = gen_mermaid_for_project(components, project)

    stack_lines = []
    for c in sorted(components):
        slug = safe_filename(c)
        stack_lines.append(f"- [[10_infrastruktur/{slug}|{c}]]"
                           f" — *{COMPONENTS[c].get('category', 'misc')}*")
    stack_md = "\n".join(stack_lines) or "_(keine Komponenten erkannt)_"

    return f"""{build_frontmatter(tags, type='overview')}{AUTO_BANNER}

# {project} — Übersicht

## Zweck / Geschäftsmodell

{purpose_paragraph}

## Tech-Stack

{stack_md}

## Architektur

{mermaid}

## Status & nächste Schritte

_(Status manuell pflegen — siehe `_MOC.md` für Einstiegslinks. Wenn du diese
Datei manuell editieren willst, entferne den AUTO_BANNER oben, sonst wird
sie beim nächsten Lauf überschrieben.)_

## Erkannte Indikatoren (Roh-Daten)

<details>
<summary>Tech-Stack-Files</summary>

```
{sorted(indicators["files_found"])}
```

</details>

<details>
<summary>Compose Services / Images</summary>

```
services: {sorted(indicators["compose_services"])}
images:   {sorted(indicators["compose_images"])}
```

</details>

<details>
<summary>Erkannte ENV-Variablen (Auszug)</summary>

```
{sorted(indicators["env_vars"])[:40]}
```

</details>
"""


def gen_moc(project: str, doc_files: list[Path], components: list[str]) -> str:
    tags = [f"projekt/{project}", "type/moc"]
    doc_links = "\n".join(
        f"- [[20_projekte/{project}/{p.stem}|{p.stem}]]"
        for p in sorted(doc_files)
    ) or "_(keine Specs gefunden)_"
    stack_links = "\n".join(
        f"- [[10_infrastruktur/{safe_filename(c)}|{c}]]"
        for c in sorted(components)
    ) or "_(keine Komponenten erkannt)_"

    return f"""{build_frontmatter(tags)}{AUTO_BANNER}

# {project} — Map of Content

Einstiegspunkt für alle Inhalte zu **{project}**.

## ➡ Start hier

- [[20_projekte/{project}/übersicht|Übersicht]]

## 📄 Specs

{doc_links}

## 🧩 Tech-Stack

{stack_links}

## 🔗 Cross-Project

- [[00_meta/Pattern-Dashboard|Pattern-Dashboard]]
"""


def gen_pattern_dashboard(per_project: dict[str, dict],
                          all_components: list[str]) -> str:
    projects = sorted(per_project.keys())

    header = "| Komponente | " + " | ".join(projects) + " | Σ |"
    sep = "|---|" + "---|" * (len(projects) + 1)
    rows = []
    component_usage: dict[str, list[str]] = defaultdict(list)
    for c in all_components:
        marks = []
        count = 0
        for p in projects:
            if c in per_project[p]["components"]:
                marks.append("✅")
                count += 1
                component_usage[c].append(p)
            else:
                marks.append(" ")
        cat = COMPONENTS[c].get("category", "misc")
        rows.append(f"| [[10_infrastruktur/{safe_filename(c)}|{c}]] "
                    f"`{cat}` | " + " | ".join(marks) + f" | {count} |")

    rows.sort(key=lambda r: (-int(re.search(r"\|\s*(\d+)\s*\|\s*$", r).group(1)),
                              r.lower()))

    matrix = "\n".join([header, sep, *rows])

    shared = sorted(
        [c for c, ps in component_usage.items() if len(ps) >= 2],
        key=lambda c: (-len(component_usage[c]), c.lower())
    )
    shared_md = "\n".join(
        f"- **{c}** ({COMPONENTS[c].get('category')}) — "
        f"genutzt in: {', '.join(f'[[20_projekte/{p}/übersicht|{p}]]' for p in component_usage[c])}"
        for c in shared
    ) or "_(keine geteilten Komponenten)_"

    unique_md_parts = []
    for p in projects:
        unique = sorted(set(per_project[p]["components"]) - set(shared))
        items = "\n".join(f"  - {c}" for c in unique) or "  - _(keine)_"
        unique_md_parts.append(f"**{p}:**\n{items}")
    unique_md = "\n\n".join(unique_md_parts)

    git_lines = []
    for p in projects:
        commit = per_project[p].get("commit")
        if commit:
            git_lines.append(
                f"- **{p}** ({commit['subdir']}/): `{commit['hash']}` — "
                f"{commit['date'][:10]} — _{commit['subject']}_"
            )
        else:
            git_lines.append(f"- **{p}**: _(kein git-repo)_")
    git_md = "\n".join(git_lines)

    domain_usage: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for d in per_project[p].get("domains", []):
            domain_usage[d].append(p)
    domain_md = "\n".join(
        f"- `#domain/{d}` → {', '.join(domain_usage[d])}"
        for d in sorted(domain_usage)
    ) or "_(keine Domain-Tags)_"

    tags = ["type/dashboard", "meta/pattern-analyse"]
    return f"""{build_frontmatter(tags)}{AUTO_BANNER}

# Pattern-Dashboard

Cross-Projekt-Analyse: welche Tech-Bausteine wiederholen sich, welche sind
unique. Wird bei jedem Lauf von `build_knowledge_graph.py` neu generiert.

Stand: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**

## 🧮 Matrix: Komponente × Projekt

{matrix}

## 🔁 Gemeinsame Muster (in ≥ 2 Projekten)

{shared_md}

## ✨ Unique pro Projekt

{unique_md}

## 🌐 Domain-Cluster

{domain_md}

## 📜 Letzter Commit pro Projekt

{git_md}
"""


def gen_purpose_paragraph(project: str, indicators: dict) -> str:
    SKIP_PATTERNS = [
        "claude code", "this file provides guidance",
        "source-of-truth", "edit here when designing",
    ]
    for readme in indicators.get("root_readmes", []):
        text = read_text(readme)
        if not text:
            continue
        in_code = False
        paragraph_lines: list[str] = []
        header_seen = False
        for line in text.split("\n"):
            s = line.strip()
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if s.startswith("#"):
                if header_seen and paragraph_lines:
                    break
                header_seen = True
                continue
            if not s:
                if paragraph_lines:
                    break
                continue
            if s.startswith(">") or s.startswith("|") or s.startswith("-"):
                if paragraph_lines:
                    break
                continue
            low = s.lower()
            if any(pat in low for pat in SKIP_PATTERNS):
                continue
            paragraph_lines.append(s)
        if paragraph_lines:
            para = " ".join(paragraph_lines)
            if len(para) > 600:
                para = para[:600].rsplit(". ", 1)[0] + "."
            return para
    return (f"_(Zweck/Geschäftsmodell für **{project}** konnte nicht "
            f"automatisch extrahiert werden — bitte manuell ergänzen.)_")


# =============================================================================
# Pipeline
# =============================================================================

def process_project(project: str, repo_path: Path, vault_dir: Path,
                    do_pull: bool, force: bool, log: list[str]) -> dict:
    log.append(f"\n### {project}")

    if do_pull:
        pull_status = git_pull_if_repo(repo_path)
        log.append(f"  git: {pull_status}")
        for sub in ("code", "docs"):
            sp = repo_path / sub
            if sp.exists():
                s = git_pull_if_repo(sp)
                log.append(f"  git {sub}/: {s}")

    indicators = collect_indicators(repo_path)
    components = detect_components(indicators)
    domains = detect_domains(indicators, project)
    commit = last_commit_info(repo_path)
    purpose = gen_purpose_paragraph(project, indicators)

    log.append(f"  Komponenten erkannt ({len(components)}): "
               f"{', '.join(components)}")
    log.append(f"  Domains: {', '.join(domains) or '-'}")

    docs_src = repo_path / "docs"
    project_vault = vault_dir / "20_projekte" / project
    project_vault.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    if docs_src.exists():
        for src in docs_src.rglob("*.md"):
            if not src.is_file():
                continue
            rel = src.relative_to(docs_src)
            dst_name = " — ".join(part for part in rel.parts)
            dst = project_vault / safe_filename(dst_name)
            result = copy_doc(src, dst, project)
            log.append(f"  {result}")
            copied.append(dst)
    else:
        log.append("  (kein docs/-Ordner)")

    moc_path = project_vault / "_MOC.md"
    log.append("  " + write_auto(moc_path, gen_moc(project, copied, components),
                                  force=True))

    ueb_path = project_vault / "übersicht.md"
    log.append("  " + write_auto(ueb_path,
                                  gen_uebersicht(project, components,
                                                 indicators, domains, purpose),
                                  force=True))

    return {
        "components": components,
        "domains": domains,
        "commit": commit,
        "indicators": indicators,
    }


def main() -> int:
    default_dev, default_vault = detect_default_paths()

    parser = argparse.ArgumentParser(
        description="Synchronisiert Dev-Repos in einen Obsidian-Vault "
                    "und visualisiert geteilte Muster.")
    parser.add_argument("--dev-dir", type=Path, default=default_dev)
    parser.add_argument("--vault-dir", type=Path, default=default_vault)
    parser.add_argument("--projects", type=str,
                        default="conformis,running_app")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-git-pull", action="store_true")
    args = parser.parse_args()

    dev_dir: Path = args.dev_dir.expanduser().resolve()
    vault_dir: Path = args.vault_dir.expanduser().resolve()
    projects = [p.strip() for p in args.projects.split(",") if p.strip()]

    log: list[str] = []
    log.append(f"## build_knowledge_graph @ "
               f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append(f"  dev-dir:   {dev_dir}")
    log.append(f"  vault-dir: {vault_dir}")
    log.append(f"  projects:  {projects}")
    log.append(f"  git-pull:  {not args.no_git_pull}")

    if not dev_dir.exists():
        print(f"FEHLER: dev-dir existiert nicht: {dev_dir}", file=sys.stderr)
        return 2
    if not vault_dir.exists():
        print(f"FEHLER: vault-dir existiert nicht: {vault_dir}",
              file=sys.stderr)
        return 2

    for d in ("00_meta", "10_infrastruktur", "20_projekte", "30_ressourcen"):
        (vault_dir / d).mkdir(parents=True, exist_ok=True)

    per_project: dict[str, dict] = {}
    for project in projects:
        repo = dev_dir / project
        if not repo.exists():
            log.append(f"\n### {project}\n  SKIP: {repo} existiert nicht")
            continue
        per_project[project] = process_project(
            project, repo, vault_dir, not args.no_git_pull, args.force, log)

    log.append("\n### Infrastruktur-Dateien")
    used_by_component: dict[str, list[str]] = defaultdict(list)
    for proj, data in per_project.items():
        for c in data["components"]:
            used_by_component[c].append(proj)

    for component, spec in COMPONENTS.items():
        if component not in used_by_component and not spec.get("write_always"):
            continue
        slug = safe_filename(component)
        path = vault_dir / "10_infrastruktur" / f"{slug}.md"
        body = gen_infra_file(component, spec, used_by_component[component])
        log.append("  " + write_auto(path, body, force=True))

    log.append("\n### Pattern-Dashboard")
    dash_path = vault_dir / "00_meta" / "Pattern-Dashboard.md"
    all_used_components = sorted(used_by_component.keys())
    log.append("  " + write_auto(dash_path,
                                  gen_pattern_dashboard(per_project,
                                                        all_used_components),
                                  force=True))

    konv_path = vault_dir / "00_meta" / "konventionen.md"
    if not konv_path.exists():
        konv_path.write_text(
            build_frontmatter(["type/meta"]) +
            f"# Konventionen\n\n"
            f"Auto-generierte Dateien tragen oben den Banner:\n\n"
            f"`{AUTO_BANNER}`\n\n"
            f"Diese Dateien werden bei jedem `build_knowledge_graph.py`-Lauf "
            f"überschrieben. Wenn du eine kopierte Spec manuell weiter "
            f"pflegen willst, entferne den Banner — dann respektiert das "
            f"Script die Datei.\n\n"
            f"## Tag-Schema\n\n"
            f"- `projekt/<name>` — Projekt-Zugehörigkeit\n"
            f"- `infra/<slug>` — Infra-Komponente\n"
            f"- `stack-category/<cat>` — frontend/backend/db/ai/...\n"
            f"- `used-in/<projekt>` — Backlink-Tag auf Komponenten\n"
            f"- `domain/<bereich>` — Geschäftsdomäne\n"
            f"- `type/<typ>` — overview/moc/dashboard/meta\n",
            encoding="utf-8")
        log.append(f"  WROTE: {konv_path}")

    print("\n".join(log))

    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    print(f"  Projekte verarbeitet: {len(per_project)}")
    print(f"  Komponenten erkannt:  {len(all_used_components)}")
    print(f"  Vault-Wurzel:         {vault_dir}")
    print(f"  Pattern-Dashboard:    {dash_path}")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
