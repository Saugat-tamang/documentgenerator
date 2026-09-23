
/* ---------------- i18n: English + Romanized Nepali ---------------- */
const dict = {
  en: {
    brand:"Baato", nav_main:"Main", nav_overview:"Overview", nav_projects:"Projects",
    nav_team:"Team", nav_billing:"Billing", nav_manage:"Manage", nav_reports:"Reports",
    nav_settings:"Settings", role_admin:"Project Admin",
    page_title:"Overview", page_sub:"Wednesday, 23 September",
    search_ph:"Search projects, people...",
    stat_projects:"Active projects", stat_tasks:"Open tasks", stat_team:"Team members", stat_revenue:"Revenue",
    vs_last:"vs last month", new_this_month:"new this month",
    chart_title:"Weekly task completion", chart_note:"Tasks closed per day, this week",
    legend_completed:"Completed", legend_target:"Target",
    tasks_title:"Today's priorities",
    table_title:"Team activity", table_note:"Last updated 4 minutes ago",
    col_person:"Person", col_project:"Project", col_status:"Status", col_hours:"Hours logged", col_amount:"Amount",
    footer_text:"Sample data for demonstration — connect your own data source to replace it.",
    status_active:"Active", status_pending:"Pending", status_blocked:"Blocked",
    menu_profile:"Your profile", menu_settings:"Account settings", menu_logout:"Log out",
    toast_logout:"Logged out (demo only)",
    days:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    tasks:[
      {name:"Finalize client wireframes", meta:"Due today · Design", tag:"High", tagClass:"tag-high"},
      {name:"Review Q3 budget sheet", meta:"Due today · Finance", tag:"Med", tagClass:"tag-med"},
      {name:"Onboard new backend dev", meta:"Tomorrow · HR", tag:"Med", tagClass:"tag-med"},
      {name:"Update server certificates", meta:"Fri · DevOps", tag:"Low", tagClass:"tag-low"},
      {name:"Client call — Himal Traders", meta:"Today, 4pm · Sales", tag:"High", tagClass:"tag-high"},
    ],
    rows:[
      {name:"Anisha Rai", mail:"anisha@baato.io", project:"Marketplace App", status:"active", hours:"6.5h", amount:"Rs 12,400"},
      {name:"Bikash Thapa", mail:"bikash@baato.io", project:"Inventory Sync", status:"pending", hours:"3.0h", amount:"Rs 6,000"},
      {name:"Sarita Magar", mail:"sarita@baato.io", project:"Client Portal", status:"active", hours:"7.2h", amount:"Rs 14,900"},
      {name:"Prakash KC", mail:"prakash@baato.io", project:"Billing Revamp", status:"blocked", hours:"1.5h", amount:"Rs 2,800"},
      {name:"Nisha Shrestha", mail:"nisha@baato.io", project:"Marketplace App", status:"active", hours:"5.8h", amount:"Rs 11,100"},
    ]
  },
  ne: {
    brand:"Baato", nav_main:"Mukhya", nav_overview:"Overview", nav_projects:"Project haru",
    nav_team:"Team", nav_billing:"Billing", nav_manage:"Byabasthapan", nav_reports:"Report haru",
    nav_settings:"Setting", role_admin:"Project Admin",
    page_title:"Overview", page_sub:"Budhbar, 23 Asoj",
    search_ph:"Project, manche khojnus...",
    stat_projects:"Chalu project haru", stat_tasks:"Baki kaam haru", stat_team:"Team ka sadasya", stat_revenue:"Aamdani",
    vs_last:"agilo mahina bhanda", new_this_month:"yo mahina naya",
    chart_title:"Haptaiko kaam sakiyeko wiwaran", chart_note:"Din pratidin sakine kaam, yo hapta",
    legend_completed:"Sakiyo", legend_target:"Lakshya",
    tasks_title:"Ajako pahilo priority",
    table_title:"Team ko activity", table_note:"4 minute agadi update bhayo",
    col_person:"Manche", col_project:"Project", col_status:"Sthiti", col_hours:"Ghanta lagayeko", col_amount:"Rakam",
    footer_text:"Yo demo data ho — aafno data source jodera replace garnus.",
    status_active:"Chalu", status_pending:"Parkhirako", status_blocked:"Rokieko",
    menu_profile:"Tapaiko profile", menu_settings:"Account setting", menu_logout:"Log out garne",
    toast_logout:"Log out bhayo (demo matra)",
    days:["Som","Mangal","Budh","Bihi","Sukra","Sani","Aita"],
    tasks:[
      {name:"Client ko wireframe final garne", meta:"Aaja deadline · Design", tag:"High", tagClass:"tag-high"},
      {name:"Q3 budget sheet check garne", meta:"Aaja deadline · Finance", tag:"Med", tagClass:"tag-med"},
      {name:"Naya backend dev onboard garne", meta:"Bholi · HR", tag:"Med", tagClass:"tag-med"},
      {name:"Server certificate update garne", meta:"Sukrabar · DevOps", tag:"Low", tagClass:"tag-low"},
      {name:"Himal Traders sanga call", meta:"Aaja, 4 baje · Sales", tag:"High", tagClass:"tag-high"},
    ],
    rows:[
      {name:"Anisha Rai", mail:"anisha@baato.io", project:"Marketplace App", status:"active", hours:"6.5 ghanta", amount:"Rs 12,400"},
      {name:"Bikash Thapa", mail:"bikash@baato.io", project:"Inventory Sync", status:"pending", hours:"3.0 ghanta", amount:"Rs 6,000"},
      {name:"Sarita Magar", mail:"sarita@baato.io", project:"Client Portal", status:"active", hours:"7.2 ghanta", amount:"Rs 14,900"},
      {name:"Prakash KC", mail:"prakash@baato.io", project:"Billing Revamp", status:"blocked", hours:"1.5 ghanta", amount:"Rs 2,800"},
      {name:"Nisha Shrestha", mail:"nisha@baato.io", project:"Marketplace App", status:"active", hours:"5.8 ghanta", amount:"Rs 11,100"},
    ]
  }
};

let currentLang = 'en';
let currentTheme = 'light';

function applyI18n(lang){
    const t = dict[lang];
    document.querySelectorAll('[data-i18n]').forEach(el=>{
        const key = el.getAttribute('data-i18n');
        if(t[key] !== undefined) el.textContent = t[key];
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
        const key = el.getAttribute('data-i18n-ph');
        if(t[key] !== undefined) el.setAttribute('placeholder', t[key]);
    });
    document.documentElement.lang = lang === 'ne' ? 'ne-Latn' : 'en';
    document.querySelectorAll('.nav-item[data-page]').forEach(btn=>{
        const label = btn.querySelector('span')?.textContent || '';
        btn.title = label;
    });
    renderTasks(t);
    renderTable(t);
    renderChart(t);
}

function renderTasks(t){
    const list = document.getElementById('taskList');
    list.innerHTML = '';
    t.tasks.forEach((task, i)=>{
        const row = document.createElement('div');
        row.className = 'task-row';
        row.innerHTML = `
        <button class="task-check" data-idx="${i}" aria-label="toggle done">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
        </button>
        <div class="task-body">
            <div class="task-name">${task.name}</div>
            <div class="task-meta">${task.meta}</div>
        </div>
        <span class="task-tag ${task.tagClass}">${task.tag}</span>
        `;
        list.appendChild(row);
    });
    list.querySelectorAll('.task-check').forEach(btn=>{
        btn.addEventListener('click', ()=>{
        btn.classList.toggle('done');
        const nameEl = btn.parentElement.querySelector('.task-name');
        nameEl.classList.toggle('done');
        });
    });
}

const avatarColors = ['#C4791F','#2F7A72','#B5453B','#5B6EC7','#8E5FB8'];
function initials(name){
  return name.split(' ').map(p=>p[0]).slice(0,2).join('').toUpperCase();
}
function renderTable(t){
    const body = document.getElementById('tableBody');
    body.innerHTML = '';
    t.rows.forEach((r, i)=>{
        const tr = document.createElement('tr');
        const statusLabel = t['status_'+r.status];
        const statusClass = 'status-' + r.status;
        tr.innerHTML = `
        <td>
            <div class="person">
            <div class="avatar" style="background:${avatarColors[i % avatarColors.length]}">${initials(r.name)}</div>
            <div>
                <div class="pname">${r.name}</div>
                <div class="pmail">${r.mail}</div>
            </div>
            </div>
        </td>
        <td>${r.project}</td>
        <td><span class="status-pill ${statusClass}">${statusLabel}</span></td>
        <td>${r.hours}</td>
        <td class="amount">${r.amount}</td>
        `;
        body.appendChild(tr);
    });
}

const chartData = [6,9,7,10,8,4,3];
const targetLine = 8;
function renderChart(t){
    const svg = document.getElementById('barChart');
    const W = 560, H = 220, padL = 26, padB = 26, padT = 10, padR = 10;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;
    const maxVal = Math.max(...chartData, targetLine) + 2;
    const barW = chartW / chartData.length * 0.5;
    const gap = chartW / chartData.length;

    const cssAccent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
    const cssLine = getComputedStyle(document.documentElement).getPropertyValue('--line').trim();
    const cssInkSoft = getComputedStyle(document.documentElement).getPropertyValue('--ink-soft').trim();

    let bars = '';
    chartData.forEach((v, i)=>{
        const x = padL + i * gap + (gap - barW)/2;
        const h = (v / maxVal) * chartH;
        const y = padT + chartH - h;
        const trackH = chartH;
        bars += `<rect class="bar-track" x="${x}" y="${padT}" width="${barW}" height="${trackH}" rx="5"></rect>`;
        bars += `<rect class="bar-fill" x="${x}" y="${y}" width="${barW}" height="${h}" rx="5" fill="${cssAccent}"></rect>`;
        bars += `<text class="axis-label" x="${x + barW/2}" y="${H - 6}" text-anchor="middle" fill="${cssInkSoft}">${t.days[i]}</text>`;
    });

    const targetY = padT + chartH - (targetLine / maxVal) * chartH;
    const targetLineSvg = `<line x1="${padL}" y1="${targetY}" x2="${W - padR}" y2="${targetY}" stroke="${cssInkSoft}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"></line>`;

    svg.innerHTML = bars + targetLineSvg;
}

/* ---------------- Theme ---------------- */
function applyTheme(theme){
    if(theme === 'dark'){
        document.documentElement.setAttribute('data-theme','dark');
    } else {
        document.documentElement.setAttribute('data-theme','light');
    }
    try{ localStorage.setItem('baato-theme', theme); }catch(e){}
    renderChart(dict[currentLang]);
}

document.getElementById('themeToggle').addEventListener('click', ()=>{
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(currentTheme);
});

document.getElementById('langToggle').addEventListener('click', (e)=>{
    const btn = e.target.closest('button[data-lang]');
    if(!btn) return;
    currentLang = btn.getAttribute('data-lang');
    document.querySelectorAll('#langToggle button').forEach(b=>b.classList.toggle('on', b === btn));
    try{ localStorage.setItem('baato-lang', currentLang); }catch(e){}
    applyI18n(currentLang);
});

/* ---------------- Sidebar: desktop collapse + mobile drawer ---------------- */
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const isDesktop = () => window.innerWidth > 860;

document.getElementById('hamburger').addEventListener('click', ()=>{
    if(isDesktop()){
        sidebar.classList.toggle('collapsed');
        try{ localStorage.setItem('baato-sidebar', sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded'); }catch(e){}
        closeProfileMenu();
    } else {
        sidebar.classList.add('open');
        overlay.classList.add('show');
    }
});

overlay.addEventListener('click', ()=>{
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
});

window.addEventListener('resize', ()=>{
    if(isDesktop()){
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    }
});

/* ---------------- Profile popover (logout, settings) ---------------- */
const profileBtn = document.getElementById('profileBtn');
const profileMenu = document.getElementById('profileMenu');

function closeProfileMenu(){
    profileMenu.classList.remove('open');
    profileBtn.setAttribute('aria-expanded', 'false');
}

function toggleProfileMenu(){
    const open = profileMenu.classList.toggle('open');
    profileBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
}

profileBtn.addEventListener('click', (e)=>{
    e.stopPropagation();
    toggleProfileMenu();
});

document.addEventListener('click', (e)=>{
    if(!e.target.closest('#profileArea')){
        closeProfileMenu();
    }
});

document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape'){
        closeProfileMenu();
    }
});

/* ---------------- Toast ---------------- */
let toastTimer;

function showToast(msg){
    const toast = document.getElementById('toast');

    if(!toast){
        return;
    }

    toast.textContent = msg;
    toast.classList.add('show');

    clearTimeout(toastTimer);

    toastTimer = setTimeout(()=>{
        toast.classList.remove('show');
    }, 2400);
}


/* ---------------- Logout ---------------- */

const LOGOUT_URL = '/user/auth/logout/';
const LOGIN_URL = '/user/auth/login/';

async function handleLogout(){
    closeProfileMenu();

    try{

        const response = await fetch(LOGOUT_URL, {
        method: 'POST',

        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },

        credentials: 'same-origin'
        });

        if(response.ok){
        window.location.href = response.redirected ? response.url : LOGIN_URL;
        return;
        }

        showToast(dict[currentLang].toast_logout_failed || 'Logout failed. Please try again.');

    }catch(error){
        showToast(dict[currentLang].toast_logout_failed || 'Logout failed. Please try again.');
  }
}


/* ---------------- CSRF Cookie ---------------- */

function getCookie(name){
  let cookieValue = null;

  if(document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for(let cookie of cookies){
      cookie = cookie.trim();
      if(cookie.startsWith(name + '=')){
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}

/* ---------------- Profile menu actions ---------------- */

profileMenu.addEventListener('click', (e)=>{
    const item = e.target.closest('.profile-menu-item');
    if(!item){
        return;
    }
    const action = item.getAttribute('data-action');
    if(action === 'logout'){
        handleLogout();
        return;
    }

    if(action === 'profile'){
        closeProfileMenu();
        window.location.href = '/user/profile/';
        return;
    }

    if(action === 'settings'){
        closeProfileMenu();
        window.location.href = '/user/settings/';
        return;
    }
});

/* ---------------- Nav item active state ---------------- */
document.querySelectorAll('.nav-item').forEach(btn=>{
    btn.addEventListener('click', ()=>{
        document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    });
});

/* ---------------- Init ---------------- */
(function init(){
    let savedTheme = 'light';
    let savedLang = 'en';
    let savedSidebar = 'expanded';

    try{
        savedTheme = localStorage.getItem('baato-theme') || 'light';
        savedLang = localStorage.getItem('baato-lang') || 'en';
        savedSidebar = localStorage.getItem('baato-sidebar') || 'expanded';
    }catch(e){}

    currentTheme = savedTheme;
    currentLang = savedLang;
    if(savedSidebar === 'collapsed' && isDesktop()){
        document.getElementById('sidebar').classList.add('collapsed');
    }

    document.querySelectorAll('.nav-item[data-page]').forEach(btn=>{
        const label = btn.querySelector('span')?.textContent || '';
        btn.title = label;
    });
    applyTheme(currentTheme);
    document.querySelectorAll('#langToggle button').forEach(b=>{
        b.classList.toggle('on', b.getAttribute('data-lang') === currentLang);
    });
    applyI18n(currentLang);
})();