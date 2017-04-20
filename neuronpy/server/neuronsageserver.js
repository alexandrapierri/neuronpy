var axajObject = createRequestObject();

function createRequestObject() {  
    var xmlhttp;
    try { xmlhttp=new ActiveXObject("Msxml2.XMLHTTP"); }
    catch(e) {
        try {
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch(e) {
            xmlhttp=null;
        }
    }
    if(!xmlhttp&&typeof XMLHttpRequest!="undefined") {
        xmlhttp=new XMLHttpRequest();
    }
    return  xmlhttp;
}

function sendRequest(event) {
    var code = document.getElementById("code").value;
    if (code.length > 0 && event.keyCode == 13) {
        var ecode = encodeURIComponent(code);
        var req = "/eval?code=" + ecode;
        try{
            axajObject.open("POST", req, true);
            axajObject.setRequestHeader('Content-Type',  "text/html");
            axajObject.onreadystatechange = handleResponse;
            axajObject.send("");
        }
        catch(e){
            // caught an error
            alert('Request send failed.');
        }
        finally{}
    }
}

function handleResponse() {
    if(axajObject.readyState == 4){
        var response = axajObject.responseText;
        var code = document.getElementById("code").value;
        var res = "<p>Result of " + code + ":&nbsp;&nbsp;" + response + "</p>";
        document.getElementById("output").innerHTML = res; 
    }
}
