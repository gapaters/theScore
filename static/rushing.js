document.querySelector("#table-filter").addEventListener("submit", (event) => {
    event.preventDefault();

    const XHR = new XMLHttpRequest();
    const FD = new FormData(event.target);
    const paramString = new URLSearchParams(FD).toString();
    const action = event.submitter.value
    const uri = `${action}_data?${paramString}`
    const url = `${window.origin}/${uri}`

    XHR.onreadystatechange = request => {
        const response = request.target;

        if (response.readyState === 4 && response.status === 200) {
            if (action === 'filter') {
                document.querySelector('#table-data').innerHTML = response.responseText
            } else if (action === 'download') {
                let link = document.querySelector('#download_link')
                link.href = url
                link.click()
            }
        }
    };

    XHR.open("GET", url);
    XHR.send(FD)
});