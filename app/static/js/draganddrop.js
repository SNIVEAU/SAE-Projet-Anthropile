document.addEventListener("DOMContentLoaded", () => {
    const dropContainer = document.getElementById("dropcontainer");
    const fileInput = document.getElementById("images");


    dropContainer.addEventListener("dragover", (e) => {
        // prevent default to allow drop
        e.preventDefault();
        dropContainer.classList.add("drop-active");
    });


    dropContainer.addEventListener("dragenter", () => {
        dropContainer.classList.add("drop-active");
    });


    dropContainer.addEventListener("dragleave", () => {
        dropContainer.classList.remove("drop-active");
    });


    dropContainer.addEventListener("drop", (e) => {
        e.preventDefault();
        dropContainer.classList.remove("drop-active");
        fileInput.files = e.dataTransfer.files;
    });
    });

