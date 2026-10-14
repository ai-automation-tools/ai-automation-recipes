# Security Toolkit

Goal: research and write a toolkit of **at least 24 security tools** — identity and access, offensive
and recon, detection and response, OSINT, privacy and encryption, AppSec and supply chain, cloud and
infrastructure, security AI, and the labs people learn on — sorted into buckets, plus a cover
description.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## WHAT THIS DIGEST IS — AND IS NOT

The **security corner of a working stack**: the scanner you run in CI, the directory you federate
against, the detection rules you import, the recon tool you point at your own estate, the encrypted
store you keep secrets in, the range you practise on.

The test for every candidate: **would a security engineer, an IAM engineer, or a blue/red teamer
install, deploy or subscribe to this?** A SAST scanner passes. An identity provider's open-source SDK
passes. A detection-rule repo passes. A CTF platform passes. A vendor's "AI-powered next-generation
platform" page with no product detail does not; neither does a news site or a conference.

**Lean practitioner.** About seven entries in ten should be something you install, deploy, self-host
or call. Hosted products are welcome where they're what people actually use.

### ⚠️ Tools, not targets — the content rule with consequences off the page

This digest is a **catalogue of published, publicly available security tooling**, in the spirit of
`awesome-pentest` or the ATT&CK tool index. It is **not** an attack guide:

- **Link the tool, never a weaponized proof-of-concept.** A scanner's repo is an entry; a working
  exploit for an unpatched CVE is not, even when it is public.
- **No live third-party targets.** Never name an organization, product instance or person as
  something to point a tool at. Describe offensive tools by *what they do*, on infrastructure the
  reader owns or is authorized to test.
- **No step-by-step intrusion instructions.** "Subdomain enumeration and takeover detection across a
  domain you own" is a description; a chained how-to against someone else's estate is not.

Overlap with `cool-websites` (its security categories), `ai-stack-radar`, `agent-toolkit` and the
repo digests is expected — this recipe is scoped by subject, and it does **not** skip a well-known
tool just because it is well known. `github.com/...` links are normal here.

--------------------------------------------------
## ALREADY FEATURED — DO NOT REPEAT

Everything earlier runs of this recipe listed (date · name — URL). Match on name and URL:

{{FEATURED}}

One carve-out: an entry may return **at least 6 months** after it was last covered if it has shipped
something that changes what it is for — a rewrite, a new detection surface, a licence change, a major
version. Say so in the entry ("last covered YYYY-MM-DD; returns because …").

--------------------------------------------------
## RESEARCH

Security tooling decays in a specific way: **projects are abandoned quietly**, **licences change**
(several notable tools went source-available or commercial), and **free tiers get cut**. A tool you
remember as the open-source default may not be one any more.

Places to mine for candidates, then go beyond them:

- **Identity:** IdP and directory projects, SSO/OIDC/SAML libraries, PAM and secrets managers,
  IGA/SCIM provisioning, passkey/WebAuthn implementations, Keycloak and Okta/Entra community tooling.
- **Offensive:** recon and pentest repos, `awesome-pentest`-style indexes, adversary-emulation
  frameworks, purple-team tooling, Kali/Parrot package changes, BloodHound-family tooling.
- **Defensive:** SIEM and log pipelines, EDR projects, Sigma / YARA / Suricata rule sets,
  threat-hunting notebooks, DFIR and forensics, honeypots and deception.
- **OSINT:** recon frameworks, asset and domain lookup, metadata and image analysis, geolocation,
  transport and infrastructure tracking.
- **Privacy and crypto:** E2EE messaging and storage, anonymity networks, secrets scanning,
  data-minimization tooling, modern crypto libraries.
- **AppSec and supply chain:** SAST/DAST/SCA, SBOM generation, artifact signing (Sigstore family),
  dependency-confusion and typosquat detection, CI security.
- **Cloud and infra:** CSPM and permission analysis, Kubernetes and container security, IaC scanning
  and policy-as-code, eBPF runtime security.
- **Security AI:** LLM guardrails, prompt-injection detection and red-teaming, AI-assisted triage,
  security MCP servers.
- **Practitioners:** Show HN, r/netsec, r/blueteamsec, tl;dr sec, SANS and DFIR communities,
  Black Hat Arsenal and DEF CON demo labs, GitHub Trending filtered to security topics.

**What earns a slot:**

- **Usable, with an obvious entry point** — install instructions, a container image, a package, or a
  real signup.
- **Alive** — activity in the last ~6 months. A dead security tool is worse than none: it produces
  confident output against threats it no longer recognises.
- **Licence stated where it matters** — source-available, BSL or a commercial-use restriction must be
  said; a reader deploying it at work needs to know first.
- **Specific** — name what it detects, scans, federates or enumerates.
- **Not a vendor front door** — link the repo, docs or rule set, not a "request a demo" page.

**Proven AND new, in every bucket:** at least one **established** entry (say what makes it the
default) and at least one **fresh** entry (shipped, rewritten or relicensed in roughly the last
6 months — say what and when).

--------------------------------------------------
## BUCKETS

**7–9 buckets, 2–4 entries each, at least 24 in total** (aim for 24–30). Use these names exactly.

- **Identity & Access** — IdPs, directories, SSO, MFA and passkeys, PAM, secrets, IGA/SCIM, authz engines
- **Offensive & Recon** — pentest and red-team frameworks, recon, adversary emulation. **Open this
  bucket with one italic line directly under its heading:** `*Every tool below is for systems you own
  or are contracted to test.*`
- **Defensive & Detection** — SIEM, EDR, detection rule sets, threat hunting, DFIR, deception
- **OSINT & Investigation** — recon frameworks, asset and domain lookup, metadata, geolocation
- **Privacy & Encryption** — E2EE, anonymity networks, secrets scanning, redaction, crypto libraries
- **AppSec & Supply Chain** — SAST/DAST/SCA, SBOM, signing and attestation, CI/CD security
- **Cloud & Infra Security** — CSPM, Kubernetes and containers, IaC and policy-as-code, eBPF
- **Security AI & Agents** — guardrails, prompt-injection detection, AI triage, security MCP servers
- **Labs & Learning** — CTF platforms, cyber ranges, vulnerable-by-design targets, training

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `digest.md`

```markdown
---
title: "Security Toolkit — <Month D, YYYY>"
date: {{DATE}}
type: security-toolkit
site_count: <number of tools listed>
categories: [<the bucket names you used, spelled exactly as above>]
tags: [security-toolkit, security, identity, iam, osint, appsec, detection, open-source]
---

# Security Toolkit — <Month D, YYYY>

> <One sentence: N security tools — identity, detection, recon, AppSec and the labs to practise on.>

## 🔑 Identity & Access

### [<Tool Name>](<https URL>)
<2–3 sentences: what it does, how a reader deploys or calls it, and why this one over its neighbours. Say whether it is the established pick or a recent arrival, with a date if new. Name the licence if it is anything other than plainly open source.> **Pricing:** <free / open source (licence) / source-available / freemium with the cap named / paid from $X — one clause>.

<...every bucket, every tool in the same shape...>

---

*<total> tools this run. Offensive tooling is listed for systems you own or are authorized to test.*
```

Rules for the body:

- Every tool is a `### [Name](URL)` link, the description, then **Pricing:** as the **last** thing in
  the paragraph. **Put the licence in it** when it isn't plainly permissive ("open source (AGPL)",
  "source-available, no commercial use", "BSL").
- No `**Replaces:**` clause. Put the entry point in the sentence (`docker run`, "a Helm chart", "one
  Sigma rule pack", `pip install`).
- Link the thing itself, never a blog post. Leading emoji on each `##`, bucket text exactly as above.
- **Tools, not targets** — see the scope rule above.

{{DIGEST_RULES}}

Skills installed for this run:

{{SKILLS}}

This digest's trap: the security industry's house voice — "enterprise-grade", "battle-tested",
"next-generation", "zero-trust", every README opening on a threat landscape. It hides what the tools
actually do.

--------------------------------------------------
## COVER IMAGE

Motif: abstract **"layered perimeter"** — nested boundaries, keyed interlocking forms, offset lattices
and gated apertures. Fixed palette: **graphite, signal red, steel blue, bone white**.

Dangerous nouns for this digest — its clichés are the strongest of any digest: "padlock", "shield",
"hacker", "hoodie", "binary code", "matrix rain", "fingerprint", "keyhole", "firewall", "skull",
"logo". **No glyphs that read as code** — a cover full of pseudo-hex is the exact failure this
digest attracts.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "Security Toolkit — <Month D, YYYY>",
  "slug": "security-toolkit",
  "summary": "<the intro sentence>",
  "site_count": 0,
  "cover_prompt": "<the full cover description>",
  "error": null
}
```
