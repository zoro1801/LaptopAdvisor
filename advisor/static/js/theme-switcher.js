// Theme switcher functionality
class ThemeSwitcher {
    constructor() {
        this.darkMode = false;
        this.init();
    }

    init() {
        // Check for saved user preference, first in localStorage, then in system preferences
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            this.darkMode = savedTheme === 'dark';
        } else {
            this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
        }

        // Initial setup
        this.updateTheme();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Listen for theme toggle button clicks
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem('theme')) {
                this.darkMode = e.matches;
                this.updateTheme();
            }
        });
    }

    toggleTheme() {
        this.darkMode = !this.darkMode;
        this.updateTheme();
        this.savePreference();
    }

    updateTheme() {
        document.body.classList.toggle('dark-mode', this.darkMode);
        this.updateThemeIcon();
        this.updateCharts();
    }

    updateThemeIcon() {
        const icon = document.querySelector('#theme-toggle i');
        if (icon) {
            icon.className = this.darkMode ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    updateCharts() {
        // Update Chart.js charts if they exist
        if (window.Chart) {
            Chart.helpers.each(Chart.instances, (chart) => {
                const options = chart.config.options;
                
                options.plugins.legend.labels.color = this.darkMode ? '#fff' : '#666';
                options.scales.x.grid.color = this.darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
                options.scales.y.grid.color = this.darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
                options.scales.x.ticks.color = this.darkMode ? '#fff' : '#666';
                options.scales.y.ticks.color = this.darkMode ? '#fff' : '#666';
                
                chart.update();
            });
        }
    }

    savePreference() {
        localStorage.setItem('theme', this.darkMode ? 'dark' : 'light');
    }
}

// Initialize theme switcher when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeSwitcher = new ThemeSwitcher();
});