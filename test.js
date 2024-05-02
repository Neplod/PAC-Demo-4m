async function foo() {

    let url = 'https://timeapi.io/api/Time/current/zone?timeZone=Europe/Madrid';
    let obj = "";
    let momentoActual = "";
    try
    {
        obj = await( await fetch(url) ).json();
        momentoActual = new Date( Date.parse(obj["dateTime"]) );
    } catch(e) {
        momentoActual = new Date();
    }
    console.log(momentoActual);
    let nHoras = momentoActual.getHours().toString();
    let nMinutos = momentoActual.getMinutes().toString();
    let nSegundos = momentoActual.getSeconds().toString();

    console.log(nHoras);
    console.log(nMinutos);
    console.log(nSegundos);
}

foo()