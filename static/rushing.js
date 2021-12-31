document.querySelector("#table-filter").addEventListener("submit", (event) => {
	event.preventDefault();

	const XHR = new XMLHttpRequest();
    const FD = new FormData(event.target);

    XHR.onreadystatechange = request => {
    	const response = request.target;
    	
    	if (response.readyState === 4 && response.status === 200) {
    		document.querySelector('#table-data').innerHTML = response.responseText
    	}
    };

    XHR.open( "POST", `${window.origin}/filter_data`);
    XHR.send(FD)

    console.log('meow');
});