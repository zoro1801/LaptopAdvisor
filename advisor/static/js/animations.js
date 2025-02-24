// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form submission animation
function showLoadingSpinner() {
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm ms-2';
    spinner.setAttribute('role', 'status');
    submitBtn.appendChild(spinner);
    submitBtn.disabled = true;
}

function hideLoadingSpinner() {
    const submitBtn = document.querySelector('form button[type="submit"]');
    const spinner = submitBtn.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }
    submitBtn.disabled = false;
}

// Card hover effects
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
    });
});

// Progress bar animation
function animateProgressBar() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
}

// Chart animations
function animateCharts() {
    const charts = document.querySelectorAll('canvas');
    charts.forEach(chart => {
        if (chart.chart) {
            chart.chart.data.datasets.forEach(dataset => {
                const originalData = [...dataset.data];
                dataset.data = new Array(originalData.length).fill(0);
                chart.chart.update('none');

                // Animate to actual values
                const steps = 30;
                for (let i = 0; i <= steps; i++) {
                    setTimeout(() => {
                        dataset.data = originalData.map(value => (value * i) / steps);
                        chart.chart.update('none');
                    }, (1000 * i) / steps);
                }
            });
        }
    });
}

// Form validation animations
document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('invalid', function(e) {
        e.preventDefault();
        this.classList.add('shake');
        setTimeout(() => this.classList.remove('shake'), 500);
    });
});

// Add custom animations class
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('animate-ready');
    animateProgressBar();
    setTimeout(animateCharts, 500);
});