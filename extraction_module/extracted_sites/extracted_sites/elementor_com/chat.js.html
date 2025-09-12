// Version 1.0.8 - 2025-06-24

(() => {

    if ( !isChatAllowed() ) {
        return;
    };

    let isChatLoaded = false;
    let isClickToLoadAndOpen = false;
    let workflowTag = "Presale";
    let isCare = window.location.href.includes('/care/') || window.location.href.includes('/service/');

    if ( isCare ) {
        workflowTag = "Presale - Care";
    }


    if( ifLoadChatOnLoad() ){
        loadChat();

    }else{
        const style = document.createElement('style');
        style.innerHTML = `.chat-button{position:fixed;bottom:20px;right:27px;z-index:9999;width:60px;cursor:pointer;}.chat-button:hover{transform:scale(1.1)}.blink{animation:1s infinite blink}@keyframes blink{0%,100%{opacity:1}50%{opacity:.5}}`;
        document.head.appendChild( style );
        
        const img = document.createElement('img');
        img.src = 'data:image/png;base64,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';
        img.classList.add( 'chat-button' );
        img.setAttribute('alt', 'Start a chat with an Elemebtor agent');
        img.addEventListener('click', clickToLoadAndOpen );
        document.body.appendChild( img );
    }


    window.addEventListener('message', (event) => {
        if ( event.data.event === 'forethoughtWidgetLoaded' ) {
            if ( isClickToLoadAndOpen ){
                window.Forethought("widget", "open");
                isClickToLoadAndOpen = false;
            }
            document.querySelector('.chat-button')?.remove();
            loadkustomer();
        }
    });


    function clickToLoadAndOpen(){
        document.querySelector('.chat-button')?.classList.add('blink');
        isClickToLoadAndOpen = true;
        loadChat();
    }


    function loadChat(){
        if ( isChatLoaded ){
            return;
        }

        const script = document.createElement("script");
        script.setAttribute("src", "https://solve-widget.forethought.ai/embed.js");
        script.setAttribute("id", "forethought-widget-embed-script");
        script.setAttribute("data-api-key", "0fffb09d-5131-42e2-aedd-33e3740d7924");
        script.setAttribute("data-ft-Chat-Source", location.href);
        script.setAttribute("data-ft-Description", "");
        script.setAttribute("data-ft-Email", "");
        script.setAttribute("data-ft-Embed-Script-Language", "javascript");
        script.setAttribute("data-ft-First-User-Intent", "");
        script.setAttribute("data-ft-Subject", "");
        script.setAttribute("data-ft-Support-Level", "");
        script.setAttribute("data-ft-User", "unauthenticated");
        script.setAttribute("data-ft-workflow-tag", workflowTag );
        script.setAttribute("config-ft-ignore-persistence-parameters", "data-ft-chat-source");
        script.setAttribute("config-ft-disable-proactive-prompt", "true");

        if ( isCare ) {
            script.removeAttribute("config-ft-disable-proactive-prompt");
        }

        document.head.append( script );
        sessionStorage.setItem('chatSession', 'true');
        isChatLoaded = true;
    }

    function loadkustomer(){
        const kustomerScript = document.createElement("script");
        kustomerScript.setAttribute("src", "https://cdn.kustomerapp.com/chat-web/widget.js");
        kustomerScript.setAttribute("data-kustomer-api-key", "eyJhbGciOiJub25lIn0.eyJvcmciOiI1ZjdlMzJlNjI2MTVmYWZlODE0YWE1ZGEiLCJvcmdOYW1lIjoiZWxlbWVudG9yIiwicG9kIjoicHJvZDIiLCJyb2xlcyI6WyJvcmcudHJhY2tpbmciXX0.");
        document.body.append( kustomerScript );
    }

    window.addEventListener('kustomerLoaded', function() {
        Kustomer.start({
            brandId: '65cb3dad67603d6fedf87546'
        });
    });



    function isChatAllowed() {
        const cookie = document.cookie.split(';').find( cookie => cookie.includes('OptanonConsent=') );
        if ( cookie?.includes('C0003%3A0') ) {
            return false;
        }
        return true;
    }


    window.addEventListener('loadChat', () => {
        if ( isChatLoaded ) {
            window.Forethought("widget", "open");
            return;
        }
        clickToLoadAndOpen();
    });

    function ifLoadChatOnLoad(){
        if ( isCare ) {
            return true;
        }
        if ( sessionStorage.getItem('chatSession') === 'true' ) {        
            return true;
        }
    }

})();
