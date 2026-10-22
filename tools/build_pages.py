"""Builds the game pages, the old-Wix redirect pages and 404.html from the data below.

Run from the repo root:  python tools/build_pages.py
The header and footer are copied from index.html, so edit them there and re-run.
Re-run after editing css/site.css or js/site.js too: every page links them with a
content hash (?v=...) so visitors' browsers fetch the new version instead of a cached one.
Everything this script writes is plain HTML and can also be edited by hand,
but a re-run overwrites those files.
"""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.dbkgames.com"

GAMES = [
    {
        "slug": "spacebourne-2",
        "name": "SpaceBourne 2",
        "title_lines": ["SpaceBourne 2"],
        "appid": 1646850,
        "tagline": "Embark on a journey to greatness.",
        "lede": "A single-player, open-universe RPG and third-person shooter. Fly, fight, trade and explore "
                "tens of thousands of solar systems, then build an empire of your own.",
        "release": "Nov 18, 2025",
        "release_iso": "2025-11-18",
        "genre": "Space RPG · Shooter",
        "genres": ["Space simulation", "RPG", "Third-person shooter", "Open world"],
        "languages": ["English", "Turkish", "Portuguese (Brazil)", "French", "Italian", "German", "Spanish",
                      "Simplified Chinese", "Traditional Chinese", "Japanese", "Korean", "Polish", "Russian",
                      "Ukrainian"],
        "audio": "Full English voice-over",
        "about": [
            "SpaceBourne 2 is a single-player, open-universe RPG and third-person shooter with role-playing, "
            "mining, trading, piracy, crafting and deep exploration. The story picks up where SpaceBourne left off. "
            "This time your goal is to build a new empire in the galaxy, and how you do it is up to you.",
            "Every scenario needs a hero, and here you have two: your pilot and your ship. Create a lifelike "
            "character, modify your ships the way you like and take them into a galaxy where factions, Starlords "
            "and noble houses all have their own plans.",
            "Any galaxy is too big for one person to rule. Companions fight beside you, lead your squads and "
            "take on roles in the faction you build.",
        ],
        "features": [
            ("Tens of thousands of systems", "Procedurally generated solar systems, each with its own planets, stations and secrets to find."),
            ("Planets you can walk", "Massive surfaces with their own climate and gravity, plus cities, villages, caves and outposts."),
            ("Your own faction", "Set its policies and structure, grow its military, capture stations or build new ones."),
            ("Starlords and houses", "Diplomacy reaches past factions to the Starlords and houses who change the balance of power."),
            ("Pilot and ship", "Character creation on Unreal Engine and deep ship customization. Fly it, then fight on foot."),
            ("Companions", "Recruit a team, assign them roles and let them lead in combat."),
        ],
        "reqs": [
            ("OS", "Windows 7 / 8 / 10, 64-bit"),
            ("Processor", "Intel Core i5-2500K @ 2.9 GHz or AMD FX 6300 @ 2.9 GHz"),
            ("Memory", "8 GB RAM"),
            ("Graphics", "NVIDIA GeForce GTX 780 (3 GB) or AMD Radeon R9 290 (4 GB)"),
            ("DirectX", "Version 11"),
            ("Storage", "22 GB available space"),
        ],
    },
    {
        "slug": "spacebourne",
        "name": "SpaceBourne",
        "title_lines": ["SpaceBourne"],
        "appid": 732240,
        "tagline": "Load up your weapons, ready your ship and warp to adventure.",
        "lede": "An open space exploration game with RPG elements. The galaxy's factions are at war. "
                "Choose a side, stay on no one's side, or build a force of your own.",
        "release": "Jul 18, 2020",
        "release_iso": "2020-07-18",
        "genre": "Space sim · RPG",
        "genres": ["Space simulation", "RPG", "Open world"],
        "languages": ["English", "Turkish"],
        "audio": "Full English voice-over",
        "about": [
            "SpaceBourne is a space simulation, arcade and open-world RPG built around player freedom. Mine "
            "asteroids, salvage derelict ships, hunt bounties, turn pirate or chart unknown systems and anomalies "
            "like black holes.",
            "It began on a regular day in July 2029, when an unidentified alien craft appeared in our skies and "
            "simply hovered there. The nations of the world formed the World Air Defense Platform to prepare for "
            "the worst. What follows is yours to play, between the main story, side missions and the wars of "
            "four alien races.",
            "Apart from the main storyline, the universe is generated when you start a new game, so every "
            "playthrough brings new events and locations.",
        ],
        "features": [
            ("100+ solar systems", "Over 400 planets and 37 space stations you can land on."),
            ("Hundreds of weapons", "More than 300 weapons with their own characteristics, plus ships to buy and modify."),
            ("Four races", "Distinct ships and specialties, and more than 3,000 entities to deal with."),
            ("Play your way", "Trader, miner, salvager, bounty hunter or pirate. Help or hinder the warring sides."),
            ("Character growth", "Passive traits improve with your playstyle; active traits are yours to pick as you level."),
            ("A new galaxy each time", "Content outside the main story is randomly generated for every new game."),
        ],
        "reqs": [
            ("OS", "Windows 7 / 8 / 10, 64-bit"),
            ("Processor", "Quad-core CPU (4 × 2 GHz)"),
            ("Memory", "6 GB RAM"),
            ("Graphics", "NVIDIA GTX 470 or equivalent"),
            ("DirectX", "Version 11"),
            ("Storage", "14 GB available space"),
        ],
    },
    {
        "slug": "mesel",
        "name": "Mesel",
        "title_lines": ["Mesel"],
        "appid": 440690,
        "tagline": "Create your own novel with your own decisions.",
        "lede": "Become the protagonist and the writer of a novel at the same time. Explore an abandoned "
                "children's hospital and write the story with every choice you make.",
        "release": "Feb 23, 2016",
        "release_iso": "2016-02-23",
        "genre": "Narrative · Adventure",
        "genres": ["Adventure", "Narrative", "Puzzle"],
        "languages": ["English", "Turkish"],
        "audio": "Full English voice-over",
        "about": [
            "Mesel takes place in the abandoned Gölcük Children's Hospital. All it wants from you is to be "
            "discovered.",
            "Every choice you make and every mystery you uncover is added to your novel, so how it reads depends "
            "on how you play. Depending on your style, the novel can run up to 100 pages.",
            "There is no fighting or shooting. Intelligence, curiosity and a sharp eye are all you need.",
        ],
        "features": [
            ("Visions from the past", "Use flashbacks to reveal hidden memories and add them to your novel."),
            ("Your novel", "Choices and discoveries become pages. A full playthrough can write up to 100 of them."),
            ("Puzzles", "Solve the puzzles waiting in the hospital to reveal more of its mysteries."),
            ("Real documents", "Notes, records and letters left behind, most of them taken from real hospital records."),
            ("No combat", "No bots to kill. You get through it by observing and thinking."),
            ("One haunting place", "A single, detailed setting: an abandoned children's hospital in Gölcük."),
        ],
        "reqs": [
            ("OS", "Windows 7"),
            ("Processor", "Intel Core i3 2.0 GHz"),
            ("Memory", "4 GB RAM"),
            ("Graphics", "NVIDIA GeForce GTS 250"),
            ("Storage", "4 GB available space"),
        ],
    },
]

# Old Wix addresses that do not have a page of their own any more.
REDIRECTS = {"about": "/#studio", "contact": "/#contact"}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Michroma&family=Hanken+Grotesk:'
         'wght@300;400;500;600&family=IBM+Plex+Mono:wght@300;400;500&display=swap">')
ICONS = ('<link rel="icon" type="image/svg+xml" href="/img/logo.svg">\n'
         '<link rel="icon" type="image/png" href="/img/favicon.png">\n'
         '<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">')
VER = hashlib.md5((ROOT / "css/site.css").read_bytes() + (ROOT / "js/site.js").read_bytes()).hexdigest()[:8]
SCRIPTS = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
           '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
           f'<script src="/js/site.js?v={VER}"></script>')

e = html.escape


def chrome_from_index():
    """Header and footer from index.html, with in-page anchors turned into links back to the home page."""
    src = (ROOT / "index.html").read_text(encoding="utf8")
    header = re.search(r'<header class="nav".*?</header>', src, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
    fix = lambda s: re.sub(r'href="#top"', 'href="/"', re.sub(r'href="#(?!top")([\w-]+)"', r'href="/#\1"', s))
    return fix(header), fix(footer).replace('src="img/', 'src="/img/')


def head(title, desc, url, image, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{ICONS}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#06070a">
{FONTS}
<link rel="stylesheet" href="/css/site.css?v={VER}">
{extra}</head>
<body>
"""


def game_page(g, header, footer):
    url = f"{SITE}/{g['slug']}/"
    steam = f"https://store.steampowered.com/app/{g['appid']}/"
    img = f"/img/{g['slug']}"
    others = [o for o in GAMES if o is not g]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "VideoGame", "name": g["name"], "url": url, "description": g["lede"],
             "image": f"{SITE}{img}/hero.jpg", "datePublished": g["release_iso"], "genre": g["genres"],
             "gamePlatform": "PC", "operatingSystem": "Windows", "inLanguage": g["languages"],
             "author": {"@type": "Person", "name": "Burak Dabak"},
             "publisher": {"@type": "Organization", "name": "DBK Games", "url": f"{SITE}/"},
             "offers": {"@type": "Offer", "url": steam}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "DBK Games", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Games", "item": f"{SITE}/#games"},
                {"@type": "ListItem", "position": 3, "name": g["name"], "item": url}]},
        ],
    }
    ld_tag = f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=1)}\n</script>\n'
    title_lines = "".join(f'<span class="ln"><span class="chrome">{e(t)}</span></span>' for t in g["title_lines"])
    about = "\n".join(f"        <p>{e(p)}</p>" for p in g["about"])
    feats = "\n".join(
        f'      <div><span class="k">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(g["features"]))
    shots = sorted((ROOT / "img" / g["slug"]).glob("shot-*.jpg"))
    gallery = "\n".join(
        f'      <a href="{img}/{s.name}"><img src="{img}/{s.name}" alt="{e(g["name"])} screenshot {i + 1}" '
        f'loading="lazy" width="1280" height="720"></a>' for i, s in enumerate(shots))
    reqs = "\n".join(f"          <tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in g["reqs"])
    more = "\n".join(f"""        <article class="game small-row">
          <div class="media"><img src="/img/{o['slug']}/hero.jpg" alt="" loading="lazy"></div>
          <div class="body">
            <h3 class="chrome">{e(o['name'])}</h3>
            <p>{e(o['tagline'])}</p>
            <div class="links"><a class="btn" href="/{o['slug']}/">Explore <span class="arr">→</span></a></div>
          </div>
        </article>""" for o in others)
    desc = f"{g['name']} by DBK Games. {g['lede']}"

    return head(f"{g['name']} | DBK Games", desc, url, f"{SITE}{img}/hero.jpg", ld_tag) + f"""{header}

<main id="top">
  <section class="ghero">
    <div class="art"><img src="{img}/hero.jpg" alt="" fetchpriority="high"></div>
    <div class="wrap">
      <nav class="crumbs g-in" aria-label="Breadcrumb"><a href="/">DBK Games</a><span>/</span><a href="/#games">Games</a><span>/</span><span aria-current="page">{e(g['name'])}</span></nav>
      <h1 aria-label="{e(g['name'])}">{title_lines}</h1>
      <p class="lede g-in">{e(g['lede'])}</p>
      <div class="ctas g-in">
        <a class="btn primary" href="{steam}" target="_blank" rel="noopener">Get it on Steam <span class="arr">↗</span></a>
        <a class="btn" href="https://www.youtube.com/@DBK_Games" target="_blank" rel="noopener">Watch trailers <span class="arr">↗</span></a>
      </div>
      <dl class="gmeta g-in">
        <div><dt>Release</dt><dd>{e(g['release'])}</dd></div>
        <div><dt>Genre</dt><dd>{e(g['genre'])}</dd></div>
        <div><dt>Platform</dt><dd>PC · Windows</dd></div>
        <div><dt>Languages</dt><dd>{len(g['languages'])}</dd></div>
      </dl>
    </div>
  </section>

  <section class="gsec">
    <div class="wrap about">
      <div class="copy">
        <p class="eyebrow">About the game</p>
        <h2 class="rv">{e(g['tagline'])}</h2>
{about}
      </div>
      <aside class="steam-card" aria-label="Steam store">
        <p class="mono">Available on Steam</p>
        <iframe src="https://store.steampowered.com/widget/{g['appid']}/" title="{e(g['name'])} on Steam" loading="lazy"></iframe>
        <p class="langs"><strong>Languages:</strong> {e(', '.join(g['languages']))}. {e(g['audio'])}.</p>
      </aside>
    </div>
  </section>

  <section class="gsec" aria-labelledby="feat-h">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Features</p><h2 class="rv" id="feat-h">What you'll do</h2></div></div>
      <div class="features">
{feats}
      </div>
    </div>
  </section>

  <section class="gsec" aria-labelledby="gal-h">
    <div class="wrap">
      <div class="strip-head"><h2 class="eyebrow" id="gal-h">Screenshots</h2><p class="mono">Select to enlarge</p></div>
      <div class="gallery" data-lightbox>
{gallery}
      </div>
    </div>
  </section>

  <section class="gsec" aria-labelledby="req-h">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">System requirements</p><h2 class="rv" id="req-h">Minimum specs</h2></div>
        <p class="lede">Taken from the Steam store page. Check Steam for recommended specs and the latest changes.</p></div>
      <div class="reqs-wrap"><table class="reqs"><tbody>
{reqs}
      </tbody></table></div>
    </div>
  </section>

  <section class="gsec" aria-labelledby="more-h">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">More from DBK Games</p><h2 class="rv" id="more-h">Other games</h2></div></div>
      <div class="pair">
{more}
      </div>
    </div>
  </section>
</main>

{footer}

{SCRIPTS}
</body>
</html>
"""


def redirect_page(target):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DBK Games</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}")</script>
</head>
<body style="background:#06070a;color:#e8ebf0;font-family:system-ui,sans-serif">
<p>This page has moved. <a href="{target}" style="color:#8fb8ff">Continue to DBK Games</a>.</p>
</body>
</html>
"""


def not_found(header, footer):
    links = "\n".join(f'          <a class="btn" href="/{g["slug"]}/">{e(g["name"])} <span class="arr">→</span></a>' for g in GAMES)
    return head("Page not found | DBK Games", "This page does not exist on dbkgames.com.", f"{SITE}/404.html",
                f"{SITE}/img/sb2-portal.jpg", '<meta name="robots" content="noindex">\n') + f"""{header}

<main id="top">
  <section class="lost">
    <canvas id="stars" data-warp="off" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;z-index:-2"></canvas>
    <div class="wrap">
      <p class="eyebrow">Error 404 · Signal lost</p>
      <h1 class="chrome">404</h1>
      <p class="lede">This page drifted out of range. It may have moved when we rebuilt the site.</p>
      <div class="ctas">
        <a class="btn primary" href="/">Back to home <span class="arr">→</span></a>
{links}
      </div>
    </div>
  </section>
</main>

{footer}

{SCRIPTS}
</body>
</html>
"""


def stamp_index():
    """Point index.html at the current css/js versions."""
    p = ROOT / "index.html"
    src = p.read_text(encoding="utf8")
    src = re.sub(r'/css/site\.css(\?v=\w+)?"', f'/css/site.css?v={VER}"', src)
    src = re.sub(r'/js/site\.js(\?v=\w+)?"', f'/js/site.js?v={VER}"', src)
    p.write_text(src, encoding="utf8")


def main():
    stamp_index()
    header, footer = chrome_from_index()
    for g in GAMES:
        out = ROOT / g["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(game_page(g, header, footer), encoding="utf8")
        print("wrote", out.relative_to(ROOT))
    for slug, target in REDIRECTS.items():
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(redirect_page(target), encoding="utf8")
        print("wrote", out.relative_to(ROOT))
    (ROOT / "404.html").write_text(not_found(header, footer), encoding="utf8")
    print("wrote 404.html")


if __name__ == "__main__":
    main()
