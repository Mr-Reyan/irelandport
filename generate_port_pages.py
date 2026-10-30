import os
import re
import openpyxl
import json

# Configuration Paths
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PORTS_DIR = os.path.join(REPO_ROOT, "ports")
CSS_FILE = os.path.join(REPO_ROOT, "assets", "css", "port-pages.css")
EXCEL_PATH = r"D:\FalconXoft Ship Chandler\Website Data\Ship_Chandler_SEO_49_Pages_FULL.xlsx"

def build_ports_js_array(ports_list):
    """
    Builds the JavaScript array of real ports for the mega menu dropdown
    """
    sorted_ports = sorted(ports_list, key=lambda x: x['name'])
    lines = []
    lines.append("    const ports = [")
    for p in sorted_ports:
        lines.append(f'      {{ name: "{p["name"]}", slug: "{p["slug"]}" }},')
    lines.append("    ];")
    return "\n".join(lines)


def render_article_html(desc_text, page_name):
    """
    Parses Markdown description into semantic HTML
    matching the exact structure and styling of the modern port theme
    """
    blocks = [b.strip() for b in desc_text.split('\n\n') if b.strip()]
    lines = []
    
    for b in blocks:
        if b.startswith('# '):
            # Top-level H1 is rendered in Hero section
            continue
        elif b.startswith('## '):
            heading_text = b[3:].strip()
            heading_text = heading_text.replace(' – ', ' &ndash; ').replace(' - ', ' &ndash; ')
            lines.append(f'            <h2>{heading_text}</h2>')
        elif b.startswith('- '):
            lines.append('            <ul>')
            for item in b.split('\n'):
                item = item.strip()
                if not item:
                    continue
                val = re.sub(r'^\s*-\s*', '', item)
                lines.append(f'              <li>{val}</li>')
            lines.append('            </ul>')
        else:
            if b.startswith('**') and b.endswith('**'):
                bold_content = b[2:-2].strip().replace(' – ', ' &ndash; ').replace(' - ', ' &ndash; ')
                lines.append(f'            <p><strong>{bold_content}</strong></p>')
            else:
                p_text = b.replace('\n', ' ')
                lines.append(f'            <p>{p_text}</p>')

    # Bottom Article CTA
    lines.append('')
    lines.append('            <!-- Article CTA -->')
    lines.append('            <div class="article-cta">')
    lines.append(f'              <h3>Need Supply at {page_name}?</h3>')
    lines.append('              <p>Send us your complete vessel requisition and our team will respond with a competitive quotation.</p>')
    lines.append('              <a href="../request-quote.html" class="btn btn-primary">Request a Quote <i class="fas fa-arrow-right"></i></a>')
    lines.append('            </div>')
    
    return '\n'.join(lines)


def format_hero_title(h1):
    """
    Formats the hero title with an italicized accent if hyphen/dash is present
    """
    if ' - ' in h1:
        parts = h1.split(' - ', 1)
        return f'{parts[0]} - <em>{parts[1]}</em>'
    elif ' – ' in h1:
        parts = h1.split(' – ', 1)
        return f'{parts[0]} &ndash; <em>{parts[1]}</em>'
    return h1


def generate_page_html(page_name, h1, meta_title, meta_desc, full_desc, slug, ports_js_array):
    """
    Generates complete HTML for a port page using centralized CSS and exact Ireland theme
    """
    article_html = render_article_html(full_desc, page_name)
    hero_title = format_hero_title(h1)
    
    # Extract port location name for hero bottomline
    location_name = page_name.replace('Ship Chandler', '').replace('Shipchandler', '').replace('Ship Supply Chandler', '').strip(' -–')
    location_name = re.sub(r'\s+', ' ', location_name).strip(' -–')
    if not location_name:
        location_name = page_name

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="ship chandler, ship supply, provisions, marine stores, bonded stores, deck stores, engine stores, vessel supply, marine procurement">
  <meta name="author" content="SHIP CHANDLER IRELAND">
  <link rel="canonical" href="https://shipchandlerireland.com/ports/{slug}">

  <!-- Open Graph Meta Tags -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://shipchandlerireland.com/ports/{slug}">
  <meta property="og:site_name" content="Ship Chandler Ireland">
  <meta name="theme-color" content="#14583f">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../assets/imgs/favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">

  <!-- Google Fonts: Inter + Plus Jakarta Sans + Playfair Display -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap"
    rel="stylesheet">

  <!-- Font Awesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Centralized Port Pages CSS -->
  <link rel="stylesheet" href="../assets/css/port-pages.css">
</head>

<body>
  <!-- =========================================
       SITE HEADER (Exact Ireland Match)
  ========================================= -->
  <header class="site-header" id="site-header">
    <div class="container header-inner">
      <a class="logo" href="../index.html" aria-label="Ship Chandler Ireland home">
        <img src="../assets/imgs/logo.png" alt="Ship Chandler Ireland Logo" class="site-logo-img" width="44" height="44">
        <span class="logo-text">
          <strong>Ship Chandler</strong>
          <span>Ireland</span>
        </span>
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Open navigation">
        <i class="fa-solid fa-bars"></i>
      </button>

      <nav class="primary-nav" id="primary-nav" aria-label="Main navigation">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>

          <!-- Services Dropdown (Direct under button, reduced width) -->
          <li class="nav-item has-dropdown">
            <a class="nav-link dropdown-trigger" href="../services.html" aria-haspopup="true" aria-expanded="false">
              Services <span class="nav-arrow"><i class="fa-solid fa-chevron-down"></i></span>
            </a>
            <div class="dropdown-menu">
              <a href="../services.html#provisions"><i class="fa-solid fa-carrot"></i>Provisions Supply</a>
              <a href="../services.html#bonded"><i class="fa-solid fa-boxes-stacked"></i>Bonded Stores</a>
              <a href="../services.html#deck"><i class="fa-solid fa-anchor"></i>Deck Stores</a>
              <a href="../services.html#engine"><i class="fa-solid fa-gears"></i>Engine Stores</a>
              <a href="../services.html#cabin"><i class="fa-solid fa-bed"></i>Cabin &amp; Galley</a>
              <a href="../services.html#safety"><i class="fa-solid fa-helmet-safety"></i>Safety &amp; PPE</a>
              <a href="../services.html#electrical"><i class="fa-solid fa-bolt"></i>Electrical Stores</a>
              <a href="../services.html#chemicals"><i class="fa-solid fa-flask"></i>Marine Chemicals</a>
              <a href="../services.html#welding"><i class="fa-solid fa-fire-burner"></i>Welding Equipment</a>
              <a href="../services.html#spare-parts"><i class="fa-solid fa-screwdriver-wrench"></i>Spare Parts</a>
              <a href="../services.html#publications"><i class="fa-solid fa-compass"></i>Nautical Charts</a>
              <a href="../services.html#tools"><i class="fa-solid fa-toolbox"></i>Tools &amp; Hardware</a>
              <a href="../services.html#urgent"><i class="fa-solid fa-truck-fast"></i>Urgent Supply</a>
            </div>
          </li>

          <!-- Ports Dropdown (Center aligned, anti-flicker bridge, reduced height) -->
          <li class="nav-item has-dropdown active">
            <a class="nav-link dropdown-trigger" href="javascript:void(0)" aria-haspopup="true" aria-expanded="false">
              Ports <span class="nav-arrow"><i class="fa-solid fa-chevron-down"></i></span>
            </a>
            <div class="mega-menu">
              <div class="mega-header">
                <div class="mega-header-title">
                  Port Network &amp; Anchorages
                  <small>Comprehensive port supply &amp; anchorage coverage</small>
                </div>
                <div class="mega-search">
                  <i class="fa-solid fa-magnifying-glass"></i>
                  <input type="search" id="mega-port-search" placeholder="Search ports..." aria-label="Search ports">
                </div>
              </div>
              <div class="mega-grid" id="mega-port-list">
                <!-- Populated via JavaScript dynamically -->
              </div>
            </div>
          </li>

          <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
        </ul>

        <a class="btn btn-primary" href="../request-quote.html">
          Request a Quote <i class="fa-solid fa-arrow-right"></i>
        </a>
      </nav>
    </div>
    <div class="nav-scrim" aria-hidden="true"></div>
  </header>

  <main>
    <!-- =========================================
         PORT HERO (No button in hero as requested)
    ========================================= -->
    <section class="hero">
      <div class="container">
        <div class="hero-copy">
          <ul class="breadcrumb">
            <li><a href="../index.html">Home</a></li>
            <li><span>/</span></li>
            <li><a href="../services.html">Ports</a></li>
            <li><span>/</span></li>
            <li style="color: rgba(255,255,255,0.7);">{page_name}</li>
          </ul>
          <span class="hero-eyebrow">Professional Marine Supply</span>
          <h1 class="hero-title">{hero_title}</h1>
          <p class="hero-desc">
            {meta_desc}
          </p>
        </div>
      </div>
      <div class="hero-bottomline">
        <div class="container hero-bottom-inner">
          <span><i class="fa-solid fa-location-dot"></i> Port of {location_name}, Terminals &amp; Offshore Anchorages</span>
          <span><i class="fa-solid fa-clock"></i> Rapid RFQ &amp; Berth Turnaround Dispatch</span>
          <span><i class="fa-solid fa-anchor"></i> IMPA &amp; ISSA Compliant Maritime Procurement</span>
        </div>
      </div>
    </section>

    <!-- =========================================
         ARTICLE CONTENT SECTION (Preserving 100% Client Content)
    ========================================= -->
    <section class="article-section">
      <div class="container article-layout">

        <!-- Main Complete Content Column -->
        <div class="article-main-card">
          <article class="article-content">
{article_html}
          </article>
        </div>

        <!-- Sticky Sidebar: Quick Actions & Support (No WhatsApp button in aside as requested) -->
        <aside class="article-sidebar reveal">
          <div class="sidebar-widget">
            <span class="sidebar-widget-badge">Direct Port Support</span>
            <h3>Requisition Assistance</h3>
            <p>Our marine operations desk coordinates supplies directly with incoming vessel ETAs and dock berthing permits.</p>

            <div class="sidebar-fast-links">
              <a href="../services.html#provisions" class="sidebar-fast-link">
                <i class="fa-solid fa-carrot"></i> Fresh Food Provisions
              </a>
              <a href="../services.html#bonded" class="sidebar-fast-link">
                <i class="fa-solid fa-boxes-stacked"></i> Bonded &amp; Duty-Free
              </a>
              <a href="../services.html#deck" class="sidebar-fast-link">
                <i class="fa-solid fa-anchor"></i> Deck Equipment &amp; Ropes
              </a>
              <a href="../services.html#engine" class="sidebar-fast-link">
                <i class="fa-solid fa-gears"></i> Engine Stores &amp; Filters
              </a>
              <a href="../services.html#safety" class="sidebar-fast-link">
                <i class="fa-solid fa-shield-halved"></i> SOLAS Safety Equipment
              </a>
            </div>

            <a class="btn btn-primary" style="width: 100%; margin-bottom: 14px;" href="../request-quote.html">
              Submit Requisition <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </aside>

      </div>
    </section>
  </main>

  <!-- =========================================
       SITE FOOTER (Exact 3-Column Ireland Match)
  ========================================= -->
  <footer class="site-footer" id="contact">
    <div class="container">
      <div class="footer-top">
        <!-- Col 1: Brand Info with logo.png -->
        <div class="footer-brand">
          <a class="logo" href="../index.html" aria-label="Ship Chandler Ireland home">
            <img src="../assets/imgs/logo.png" alt="Ship Chandler Ireland Logo" class="site-logo-img" width="44" height="44">
            <span class="logo-text">
              <strong>Ship Chandler</strong>
              <span>Ireland</span>
            </span>
          </a>
          <p>
            SHIP CHANDLER IRELAND is a licensed marine supplier providing provisions, technical stores, bonded goods,
            and emergency vessel supply across commercial ports and anchorages.
          </p>
        </div>

        <!-- Col 2: Quick Links -->
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul class="footer-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../about.html">About Us</a></li>
            <li><a href="../services.html">Services Catalogue</a></li>
            <li><a href="../contact.html">Contact Us</a></li>
            <li><a href="../request-quote.html">Request a Quote</a></li>
          </ul>
        </div>

        <!-- Col 3: Direct Contact with Non-Wrapping WhatsApp Button -->
        <div class="footer-col footer-contact">
          <h4>Contact Marine Operations</h4>
          <ul class="footer-contact-list">
            <li>
              <i class="fa-solid fa-location-dot"></i>
              <span>Port of Dublin, Port Centre, Alexandra Road, Dublin 1, D01 H4C6, Ireland</span>
            </li>
            <li>
              <i class="fa-solid fa-envelope"></i>
              <a href="mailto:sales@shipchandlerireland.com">sales@shipchandlerireland.com</a>
            </li>
            <li>
              <i class="fa-solid fa-user-tie"></i>
              <span class="contact-person-badge">Patrick Murphy</span>
            </li>
            <li>
              <!-- WhatsApp Bar with Strict Non-Wrapping Properties -->
              <a class="hero-whatsapp-bar" href="https://wa.me/6590190005" target="_blank" rel="noopener noreferrer"
                aria-label="Direct WhatsApp contact (+65-9019-0005)">
                <span class="hero-whatsapp-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                    <path
                      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                  </svg>
                </span>
                <span class="hero-whatsapp-tag">WHATSAPP:</span>
                <span class="hero-whatsapp-num">(+65-9019-0005)</span>
                <span class="hero-whatsapp-arrow" aria-hidden="true">&rarr;</span>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 SHIP CHANDLER IRELAND. All rights reserved.</p>
        <p>Licensed Port Chandler &amp; Offshore Supply Network</p>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Button -->
  <a class="whatsapp-float" href="https://wa.me/6590190005" target="_blank" rel="noopener noreferrer"
    aria-label="Chat on WhatsApp">
    <i class="fa-brands fa-whatsapp"></i>
  </a>

  <!-- =========================================
       PAGE JAVASCRIPT & INTERACTIONS
  ========================================= -->
  <script>
{ports_js_array}

    function getPortUrl(portSlug) {{
      return portSlug;
    }}

    // Populate Mega Menu in 3 Groups from Excel Data
    const megaList = document.getElementById('mega-port-list');
    if (megaList) {{
      const third = Math.ceil(ports.length / 3);
      const col1 = ports.slice(0, third);
      const col2 = ports.slice(third, third * 2);
      const col3 = ports.slice(third * 2);

      function createPortGroup(title, items) {{
        const group = document.createElement('div');
        group.className = 'mega-group';
        group.innerHTML = '<h4>' + title + '</h4>';
        items.forEach(port => {{
          const a = document.createElement('a');
          a.href = getPortUrl(port.slug);
          a.textContent = port.name;
          a.dataset.port = port.name.toLowerCase();
          group.appendChild(a);
        }});
        return group;
      }}

      megaList.appendChild(createPortGroup('Ports & Terminals (A–G)', col1));
      megaList.appendChild(createPortGroup('Commercial Hubs (L–S)', col2));
      megaList.appendChild(createPortGroup('Regional Ports (S–W)', col3));

      const searchInput = document.getElementById('mega-port-search');
      if (searchInput) {{
        searchInput.addEventListener('input', function (e) {{
          const query = e.target.value.trim().toLowerCase();
          const groups = megaList.querySelectorAll('.mega-group');

          groups.forEach(group => {{
            let hasVisible = false;
            const links = group.querySelectorAll('a');
            links.forEach(link => {{
              const matches = link.dataset.port.includes(query);
              link.style.display = matches ? 'flex' : 'none';
              if (matches) hasVisible = true;
            }});
            group.style.display = hasVisible ? 'block' : 'none';
          }});
        }});
      }}
    }}

    // --- Interactive Navigation, Anti-Flicker Dropdowns & Reveal Observers ---
    document.addEventListener('DOMContentLoaded', () => {{
      const header = document.getElementById('site-header');
      const nav = document.getElementById('primary-nav');
      const toggle = document.querySelector('.nav-toggle');
      const scrim = document.querySelector('.nav-scrim');
      const dropdownItems = Array.from(document.querySelectorAll('.nav-item.has-dropdown'));

      const closeDropdowns = (except) => {{
        dropdownItems.forEach(item => {{
          if (item !== except) {{
            item.classList.remove('is-open');
            const trigger = item.querySelector('.dropdown-trigger');
            if (trigger) trigger.setAttribute('aria-expanded', 'false');
          }}
        }});
      }};

      const closeMobileNav = () => {{
        nav.classList.remove('open');
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open navigation');
        toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
        scrim.classList.remove('visible');
        closeDropdowns();
      }};

      toggle.addEventListener('click', () => {{
        const opening = !nav.classList.contains('open');
        nav.classList.toggle('open', opening);
        document.body.classList.toggle('menu-open', opening);
        toggle.setAttribute('aria-expanded', String(opening));
        toggle.setAttribute('aria-label', opening ? 'Close navigation' : 'Open navigation');
        toggle.innerHTML = opening ? '<i class="fa-solid fa-xmark"></i>' : '<i class="fa-solid fa-bars"></i>';
        scrim.classList.toggle('visible', opening);
        if (!opening) closeDropdowns();
      }});

      scrim.addEventListener('click', closeMobileNav);

      // Desktop Hover + Mobile Click with Anti-Flicker Debounce
      dropdownItems.forEach(item => {{
        const trigger = item.querySelector('.dropdown-trigger');
        if (!trigger) return;
        let closeTimer = null;

        trigger.addEventListener('click', (event) => {{
          if (window.innerWidth <= 900 || trigger.getAttribute('href') === 'javascript:void(0)' || trigger.getAttribute('href') === '#') {{
            event.preventDefault();
            const opening = !item.classList.contains('is-open');
            closeDropdowns(item);
            item.classList.toggle('is-open', opening);
            trigger.setAttribute('aria-expanded', String(opening));
          }}
        }});

        item.addEventListener('mouseenter', () => {{
          if (window.innerWidth > 900) {{
            if (closeTimer) {{
              clearTimeout(closeTimer);
              closeTimer = null;
            }}
            closeDropdowns(item);
            item.classList.add('is-open');
            trigger.setAttribute('aria-expanded', 'true');
          }}
        }});

        item.addEventListener('mouseleave', () => {{
          if (window.innerWidth > 900) {{
            closeTimer = setTimeout(() => {{
              item.classList.remove('is-open');
              trigger.setAttribute('aria-expanded', 'false');
            }}, 180);
          }}
        }});
      }});

      document.addEventListener('click', (event) => {{
        if (window.innerWidth > 900 && !event.target.closest('.nav-item.has-dropdown')) {{
          closeDropdowns();
        }}
      }});

      document.addEventListener('keydown', (event) => {{
        if (event.key === 'Escape') {{
          closeDropdowns();
          if (window.innerWidth <= 900) closeMobileNav();
        }}
      }});

      window.addEventListener('resize', () => {{
        if (window.innerWidth > 900) closeMobileNav();
      }});

      const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 20);
      onScroll();
      window.addEventListener('scroll', onScroll, {{ passive: true }});

      // Scroll Reveal Animations
      const revealElements = document.querySelectorAll('.reveal');
      if ('IntersectionObserver' in window) {{
        const observer = new IntersectionObserver((entries) => {{
          entries.forEach(entry => {{
            if (entry.isIntersecting) {{
              entry.target.classList.add('active');
              observer.unobserve(entry.target);
            }}
          }});
        }}, {{
          threshold: 0.08,
          rootMargin: '0px 0px -30px 0px'
        }});

        revealElements.forEach(el => observer.observe(el));
      }} else {{
        revealElements.forEach(el => el.classList.add('active'));
      }}

      document.querySelectorAll('.nav-list a:not(.dropdown-trigger), .primary-nav > .btn').forEach(link => {{
        link.addEventListener('click', () => {{
          if (window.innerWidth <= 900) closeMobileNav();
        }});
      }});
    }});
  </script>
</body>

</html>"""
    return html


def main():
    print(f"Reading Excel workbook from: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    sheet = wb['SEO Pages']
    rows = list(sheet.iter_rows(values_only=True))[1:]
    
    print(f"Loaded {len(rows)} rows from Excel.")
    
    # 1. Collect unique ports list
    ports_dict = {}
    for r in rows:
        page_name = r[1]
        slug = re.sub(r'[^a-z0-9]+', '-', str(page_name).lower()).strip('-') + '.html'
        if slug not in ports_dict:
            ports_dict[slug] = page_name

    ports_list = [{'name': name, 'slug': slug} for slug, name in ports_dict.items()]
    ports_js = build_ports_js_array(ports_list)
    
    # 2. Generate each port page
    generated = 0
    generated_slugs = set()
    
    for r in rows:
        num, page_name, h1, meta_title, meta_desc, full_desc = r[:6]
        if not page_name:
            continue
            
        slug = re.sub(r'[^a-z0-9]+', '-', str(page_name).lower()).strip('-') + '.html'
        
        # Avoid duplicate writes for the exact same file
        if slug in generated_slugs:
            print(f"[{num:02d}/49] Skipping duplicate slug: {slug}")
            continue
            
        out_path = os.path.join(PORTS_DIR, slug)
        page_html = generate_page_html(
            page_name=str(page_name).strip(),
            h1=str(h1).strip(),
            meta_title=str(meta_title).strip(),
            meta_desc=str(meta_desc).strip(),
            full_desc=str(full_desc).strip(),
            slug=slug,
            ports_js_array=ports_js
        )
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
        generated += 1
        generated_slugs.add(slug)
        print(f"[{num:02d}/49] Generated: {slug} ({page_name})")

    print("\n" + "="*60)
    print(f"SUCCESS: Successfully generated {generated} port pages in '{PORTS_DIR}'")
    print(f"Centralized CSS link: '../assets/css/port-pages.css'")
    print(f"Default port hero image: '../assets/imgs/port-hero.jpg'")
    print("="*60)


if __name__ == "__main__":
    main()
