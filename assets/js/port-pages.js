/**
 * Port Pages JavaScript
 * Handles navigation, mega menu, and interactive features for all port pages
 */

// Port List Data for Dropdown (All 49 ports from Excel)
const ports = [
  "Bissau Ship Chandler - Guinea",
  "Conakry Ship Chandler",
  "Dakar Ship Chandler",
  "Douala Ship Chandler",
  "Ivory Coast Ship Chandler",
  "Liberia Ship Chandler",
  "Monrovia Ship Chandler",
  "Namibia Ship Chandler",
  "Nouadhibou Ship Chandler",
  "San Pedro Ship Supply Chandler",
  "Ship Chandler Abidjan",
  "Ship Chandler Angola",
  "Ship Chandler Apapa",
  "Ship Chandler Beira",
  "Ship Chandler Cabinda",
  "Ship Chandler Cape Verde",
  "Ship Chandler Casablanca",
  "Ship Chandler Congo",
  "Ship Chandler Cotonou",
  "Ship Chandler Dakar",
  "Ship Chandler Dar Es Salaam",
  "Ship Chandler Djibouti",
  "Ship Chandler Freetown",
  "Ship Chandler Gabon",
  "Ship Chandler Gentil Port - Gabon",
  "Ship Chandler Kamsar",
  "Ship Chandler Lobito",
  "Ship Chandler Luanda",
  "Ship Chandler Maputo",
  "Ship Chandler Matadi",
  "Ship Chandler Mindelo",
  "Ship Chandler Mombasa",
  "Ship Chandler Namibia",
  "Ship Chandler Onne Port Nigeria",
  "Ship Chandler Owendo",
  "Ship Chandler Port Ambon",
  "Ship Chandler Safi Port Morocco",
  "Ship Chandler Senegal",
  "Ship Chandler Soyo",
  "Ship Chandler Takoradi",
  "Ship Chandler Tema",
  "Ship Chandlers Richards Bay",
  "Ship Chandlers Saldanha Bay",
  "ShipChandler Lome",
  "Shipchandler Lagos",
  "Shipchandler Pointe Noire",
  "Walvis Bay Ship Chandler"
];

/**
 * Convert text to URL-friendly slug
 */
function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[-\s]+/g, '-')
    .trim();
}

/**
 * Populate Mega Menu with port links
 */
function populateMegaMenu() {
  const megaList = document.getElementById('mega-port-list');
  if (!megaList) return;

  // Sort ports alphabetically
  const sortedPorts = [...ports].sort();
  
  // Split into three columns
  const third = Math.ceil(sortedPorts.length / 3);
  const col1 = sortedPorts.slice(0, third);
  const col2 = sortedPorts.slice(third, third * 2);
  const col3 = sortedPorts.slice(third * 2);

  function createPortGroup(title, items) {
    const group = document.createElement('div');
    group.className = 'mega-group';
    group.innerHTML = `<h4>${title}</h4>`;
    
    items.forEach(port => {
      const a = document.createElement('a');
      const slug = slugify(port);
      a.href = `${slug}.html`;
      a.textContent = port;
      group.appendChild(a);
    });
    
    return group;
  }

  megaList.appendChild(createPortGroup('Ports (A-G)', col1));
  megaList.appendChild(createPortGroup('Ports (H-N)', col2));
  megaList.appendChild(createPortGroup('Ports (O-Z)', col3));
}

/**
 * Setup Mega Menu Search functionality
 */
function setupMegaMenuSearch() {
  const searchInput = document.getElementById('mega-port-search');
  if (!searchInput) return;

  const megaList = document.getElementById('mega-port-list');
  
  searchInput.addEventListener('input', function (e) {
    const query = e.target.value.toLowerCase();
    const allLinks = megaList.querySelectorAll('a');
    const groups = megaList.querySelectorAll('.mega-group');

    allLinks.forEach(link => {
      const text = link.textContent.toLowerCase();
      link.style.display = text.includes(query) ? 'block' : 'none';
    });

    groups.forEach(group => {
      const hasVisible = Array.from(group.querySelectorAll('a')).some(
        a => a.style.display !== 'none'
      );
      group.style.display = hasVisible ? 'block' : 'none';
    });
  });
}

/**
 * Setup sticky header effect
 */
function setupStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/**
 * Setup mobile navigation toggle
 */
function setupMobileNav() {
  const navToggle = document.querySelector('.nav-toggle');
  const primaryNav = document.querySelector('.primary-nav');
  
  if (!navToggle || !primaryNav) return;

  navToggle.addEventListener('click', function () {
    primaryNav.classList.toggle('open');
    
    const spans = this.querySelectorAll('span');
    if (primaryNav.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  });
}

/**
 * Setup mobile dropdown toggles
 */
function setupMobileDropdowns() {
  const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
  
  dropdownItems.forEach(item => {
    const link = item.querySelector('.nav-link');
    
    link.addEventListener('click', function (e) {
      if (window.innerWidth <= 1024) {
        e.preventDefault();
        item.classList.toggle('open');
      }
    });
  });
}

/**
 * Setup scroll reveal animation
 */
function setupScrollReveal() {
  const revealElements = document.querySelectorAll('.reveal');
  
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));
}

/**
 * Initialize all functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function () {
  populateMegaMenu();
  setupMegaMenuSearch();
  setupStickyHeader();
  setupMobileNav();
  setupMobileDropdowns();
  setupScrollReveal();
  
  console.log('✓ Port page initialized successfully');
});
