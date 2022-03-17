// Invoke Functions Call on Document Loaded
let alertWrapper = document.querySelector(".alert")
let alertClose = document.querySelector(".alert__close")

if (alertWrapper) {
  alertClose.addEventListener('click', () => {
    alertWrapper.style.display = 'none';
  })
}

document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});
