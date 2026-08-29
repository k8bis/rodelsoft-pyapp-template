document.addEventListener("DOMContentLoaded", () => {

    const openBtn = document.getElementById("menuOpenTestModal");
    const closeBtn = document.getElementById("closeTestModal");
    const modal = document.getElementById("testModal");

    if (openBtn && modal) {

        openBtn.addEventListener("click", (event) => {

            event.preventDefault();

            modal.classList.add("show");

        });

    }

    if (closeBtn && modal) {

        closeBtn.addEventListener("click", () => {

            modal.classList.remove("show");

        });

    }

});