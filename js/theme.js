document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('theme-toggle');

    // Set or get theme from localStorage
    const currentTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Initial icon setup based on theme
    const icon = document.querySelector('.toggle-button use');
    icon.setAttribute('xlink:href', `#icon-${currentTheme}`);

    toggleButton.addEventListener('click', function() {
        const current = document.documentElement.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        const svgIcon = current === 'dark' ? 'sun' : 'moon';

        // Swap themes
        if(newTheme === 'dark') {
            document.documentElement.style.setProperty('--palette-bg', '#011a20');
            document.documentElement.style.setProperty('--palette-bg-accent', 'rgba(1, 26, 32, 1.05)'); // Adjusted for 5% lighten
            document.documentElement.style.setProperty('--palette-dark', '#ffe3c4');
            document.documentElement.style.setProperty('--palette-contrast', '#af3b13');
            document.documentElement.style.setProperty('--palette-accent', '#d2b541');
            document.documentElement.style.setProperty('--palette-highlight', '#ffe3c4');
        } else {
            document.documentElement.style.setProperty('--palette-bg', '#e8e6ea');
            document.documentElement.style.setProperty('--palette-bg-accent', '#a6b6de');
            document.documentElement.style.setProperty('--palette-dark', '#2b3949');
            document.documentElement.style.setProperty('--palette-contrast', '#000100');
            document.documentElement.style.setProperty('--palette-accent', '#c76625');
            document.documentElement.style.setProperty('--palette-highlight', '#e9ab00');
        }

        // Update localStorage and data-theme attribute
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Swap the SVG icon
        icon.setAttribute('xlink:href', `#${svgIcon}`);
    });
});
