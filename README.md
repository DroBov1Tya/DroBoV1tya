### Neil Ermak · Application Security Engineer and Rust developer

I test web applications, APIs and infrastructure for security flaws, and I build backend services
and security tools, mostly in Rust. Most of my recent work is on AI agents: a coding agent, and MCP
servers that give agents memory and a contained Kali box.

[Site](https://drobov1tya.github.io/persona/) · [LinkedIn](https://www.linkedin.com/in/neil-ermak/) · [Telegram](https://t.me/Ufb3heud)

## Dusk Code

<a href="https://drobov1tya.github.io/dusk_code/"><img align="right" width="96" src="https://raw.githubusercontent.com/DroBov1Tya/dusk_code/main/projects/clients/desktop/assets/icon.png" alt="Dusk Code"></a>

An open-source coding agent in Rust. One core with three clients (desktop app, terminal, browser)
over one protocol. Chats are stored locally in SQLite, and you pick the model provider. Subagents,
skills and MCP servers are built in; plugins run in a sandbox, never see your keys and install
from a signed store. MIT.

| Repository | What it is |
|---|---|
| **[dusk_code](https://github.com/DroBov1Tya/dusk_code)** | The core and its clients · [site](https://drobov1tya.github.io/dusk_code/) · [releases](https://github.com/DroBov1Tya/dusk_code/releases) |
| **[duskcode-plugins](https://github.com/DroBov1Tya/duskcode-plugins)** | The plugin store: signed packages and the [Workshop](https://drobov1tya.github.io/duskcode-plugins/) |

![Stars](https://img.shields.io/github/stars/DroBov1Tya/dusk_code?style=flat-square&label=stars) ![Release](https://img.shields.io/github/v/release/DroBov1Tya/dusk_code?style=flat-square&label=release)

<img src="https://raw.githubusercontent.com/DroBov1Tya/dusk_code/main/docs/screenshots/desktop.png" alt="The Dusk Code desktop app: a project chat and its task list" width="820">

## Projects

| Project | What it does | Stack |
|---|---|---|
| **[Aether](https://github.com/DroBov1Tya/Aether)** | Self-hosted internet reconnaissance. Distributed agents run masscan, nmap, httpx, nuclei, tlsx and dnsx over IPs, domains or CIDRs; results get a Shodan-style search with scan history. | Rust · Docker |
| **[kali-mcp](https://github.com/DroBov1Tya/kali-mcp)** | A Kali Linux container exposed to AI agents over MCP. A gateway owns the network: Kali runs without `NET_ADMIN` and `NET_RAW`, and traffic leaves only through the configured SOCKS5 proxy, with no direct fallback. | Python · Docker |
| **[PentaCore](https://github.com/DroBov1Tya/PentaCore)** | Working memory for AI agents over MCP: goals, steps, attempts, findings and entities that the next session picks up. One local binary, one SQLCipher file. | Rust · SQLite |
| **[Rusty-Hook](https://github.com/DroBov1Tya/Rusty-Hook)** | Self-hosted webhook inspector, an alternative to webhook.site. Requests show up live over SSE; sign-in by admin key or OIDC. | Rust · Leptos · PostgreSQL · Docker |
| **[xbot](https://github.com/DroBov1Tya/xbot)** | Telegram bot that sells VPN subscriptions on top of a Remnawave panel. Telegram Stars and CryptoBot payments; one process serves many bots. | Rust · PostgreSQL · Docker |
| **[DBMorph](https://github.com/DroBov1Tya/DBMorph)** | Streaming converter for large, messy CSV, JSON, XLSX, SQL dumps, SQLite and Parquet. Detects encodings, repairs what it can, keeps memory flat for files larger than RAM. | Rust |
| **[hermes_auto](https://github.com/DroBov1Tya/hermes_auto)** | Interactive installer for a Hermes Agent security-assessment profile: pick MCP servers (PentaCore, kali-mcp, Playwright) and skill groups from a terminal menu. | Bash |
| **[Wifi-Scanner](https://github.com/DroBov1Tya/Wifi-Scanner)** | Wi-Fi scanner for single-board computers. Records BSSID, SSID, signal, security and first and last seen time in SQLite, via `nmcli`. | Rust · SQLite |

## Stack

| Area | Tools |
|---|---|
| Languages | Rust, Python, Bash |
| Security | Burp Suite, Metasploit, Wireshark, Kali Linux |
| Data | PostgreSQL, MongoDB, ClickHouse, SQLite, Redis |
| Backend and infrastructure | FastAPI, Docker, Proxmox, Nginx, Linux, GitHub Actions |

## Contact

- **Bug in one of my tools:** open an issue in the repository.
- **Security issue:** report it privately via *Security → Report a vulnerability* in the affected repository, not in a public issue.
- **Collaboration:** reach me through [the site](https://drobov1tya.github.io/persona/), start a discussion, or mention me in an issue.
