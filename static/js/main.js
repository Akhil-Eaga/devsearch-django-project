// GET THE SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// CHECKING IF SEARCHFORM EXISTS
if (searchForm) {
    for (let i = 0; i < pageLinks.length; i++) {
        pageLinks[i].addEventListener('click', function (event) {
            // PREVENTING THE DEFAULT BEHAVIOUR ON CLICK EVENT
            // THE PAGE-LINKS DEFAULT BEHAVIOUR IS TO ADD A QUERY PARAM OF "PAGE"
            event.preventDefault();

            // GETTING THE DATA ATTRIBUTE OF THE PAGE-LINKS
            let page = this.dataset.page;

            // THE REASON WHY THE ABOVE LINE OF CODE WORKS AND FETCHES THE DATA-PAGE CUSTOM ATTRIBUTE FROM THE PROFILES.HTML AND PROJECTS.HTML PAGES IS GIVEN IN THE LINK BELOW
            // https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset

            // ADDING A HIDDEN INPUT FIELD WITH THE NAME AS PAGE AND VALUE AS THE PAGE NUMBER THAT IS CLICKED ON
            searchForm.innerHTML = searchForm.innerHTML + `<input value=${page} name="page" hidden />`

            // SUBMIT THE FORM (THIS HAS TO BE DONE MANUALLY BECAUSE WE PREVENTED THE DEFAULT BEHAVIOUR)
            searchForm.submit();
        })
    }
}