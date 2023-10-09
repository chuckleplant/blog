function enable()  {
    DarkReader.setFetchMethod(window.fetch)
    DarkReader.enable();
    localStorage.setItem('dark-mode', 'true');
  }
  
  function disable() {
    DarkReader.disable();
    localStorage.setItem('dark-mode', 'false');
  }

function darkmode() {
    let enabled = localStorage.getItem('dark-mode')    
    
    if (enabled === null) {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          enable();
      }
    } else if (enabled === 'true') {
      enable()
    }
  
    if (localStorage.getItem('dark-mode') === 'false') {
        enable();
    } else {
        disable();
    }
  }

document.addEventListener('DOMContentLoaded', function() {
    var darkModeButton = document.getElementsByClassName('dark-mode-button')[0];
    if(darkModeButton) { // Check if the element exists
        darkModeButton.onclick = function() {
            darkmode();
        };
    } else {
        console.error("Couldn't find the .dark-mode-button element.");
    }
});