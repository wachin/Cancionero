/* generated javascript */
var skin = 'monobook';
var stylepath = '/skins-1.5';

/* MediaWiki:Common.js */
/** Execute function on page load *********************************************
  *
  *  Description: Wrapper around addOnloadHook() for backwards compatibility.
  *               Will be removed in the near future.
  *  Maintainers: [[User:R. Koot]]
  */
 
 function addLoadEvent( f ) { addOnloadHook( f ); }


 /* Test if an element has a certain class **************************************
  *
  * Description: Uses regular expressions and caching for better performance.
  * Maintainers: [[User:Mike Dillon]], [[User:R. Koot]], [[User:SG]]
  */
 
 var hasClass = (function () {
     var reCache = {};
     return function (element, className) {
         return (reCache[className] ? reCache[className] : (reCache[className] = new RegExp("(?:\\s|^)" + className + "(?:\\s|$)"))).test(element.className);
     };
 })();

 /** Internet Explorer bug fix **************************************************
  *
  *  Description: UNDOCUMENTED
  *  Maintainers: [[User:Tom-]]?
  */
 
 if (window.showModalDialog && document.compatMode)
 {
   var oldWidth;
   var docEl = document.documentElement;
 
   function fixIEScroll()
   {
     if (!oldWidth || docEl.clientWidth > oldWidth)
       doFixIEScroll();
     else
       setTimeout(doFixIEScroll, 1);
   
     oldWidth = docEl.clientWidth;
   }
 
   function doFixIEScroll() {
     docEl.style.overflowX = (docEl.scrollWidth - docEl.clientWidth < 4) ? "hidden" : "";
   }
   try {
     document.attachEvent("onreadystatechange", fixIEScroll);
     attachEvent("onresize", fixIEScroll);
   }
   catch(e) { }
 }

 /** Collapsible tables *********************************************************
 *
 *  Description: Allows tables to be collapsed, showing only the header. See
 *               [[Wikipedia:NavFrame]].
 *  Maintainers: [[User:R. Koot]]
 */

var autoCollapse = 2;
var collapseCaption = "ocultar";
var expandCaption = "mostrar";

function collapseTable( tableIndex )
{
    var Button = document.getElementById( "collapseButton" + tableIndex );
    var Table = document.getElementById( "collapsibleTable" + tableIndex );

    if ( !Table || !Button ) {
        return false;
    }

    var Rows = Table.rows;

    if ( Button.firstChild.data == collapseCaption ) {
        for ( var i = 1; i < Rows.length; i++ ) {
            Rows[i].style.display = "none";
        }
        Button.firstChild.data = expandCaption;
    } else {
        for ( var i = 1; i < Rows.length; i++ ) {
            Rows[i].style.display = Rows[0].style.display;
        }
        Button.firstChild.data = collapseCaption;
    }
}

function createCollapseButtons()
{
    var tableIndex = 0;
    var NavigationBoxes = new Object();
    var Tables = document.getElementsByTagName( "table" );

    for ( var i = 0; i < Tables.length; i++ ) {
        if ( hasClass( Tables[i], "collapsible" ) ) {

            /* only add button and increment count if there is a header row to work with */
            var HeaderRow = Tables[i].getElementsByTagName( "tr" )[0];
            if (!HeaderRow) continue;
            var Header = HeaderRow.getElementsByTagName( "th" )[0];
            if (!Header) continue;

            NavigationBoxes[ tableIndex ] = Tables[i];
            Tables[i].setAttribute( "id", "collapsibleTable" + tableIndex );

            var Button     = document.createElement( "span" );
            var ButtonLink = document.createElement( "a" );
            var ButtonText = document.createTextNode( collapseCaption );

            Button.style.styleFloat = "right";
            Button.style.cssFloat = "right";
            Button.style.fontWeight = "normal";
            Button.style.textAlign = "right";
            Button.style.width = "6em";

            ButtonLink.style.color = Header.style.color;
            ButtonLink.setAttribute( "id", "collapseButton" + tableIndex );
            ButtonLink.setAttribute( "href", "javascript:collapseTable(" + tableIndex + ");" );
            ButtonLink.appendChild( ButtonText );

            Button.appendChild( document.createTextNode( "[" ) );
            Button.appendChild( ButtonLink );
            Button.appendChild( document.createTextNode( "]" ) );

            Header.insertBefore( Button, Header.childNodes[0] );
            tableIndex++;
        }
    }

    for ( var i = 0;  i < tableIndex; i++ ) {
        if ( hasClass( NavigationBoxes[i], "collapsed" ) || ( tableIndex >= autoCollapse && hasClass( NavigationBoxes[i], "autocollapse" ) ) ) {
            collapseTable( i );
        }
    }
}

addOnloadHook( createCollapseButtons );

 //fix edit summary prompt for undo
 //this code fixes the fact that the undo function combined with the "no edit summary prompter" causes problems if leaving the
 //edit summary unchanged
 //this was added by [[User:Deskana]], code by [[User:Tra]]
 addOnloadHook(function () {
   if (document.location.search.indexOf("undo=") != -1
   && document.getElementsByName('wpAutoSummary')[0]) {
     document.getElementsByName('wpAutoSummary')[0].value='';
   }
 })

/*</pre>
== Búsqueda especial extendida (specialsearch) ==
Añade a la página [[Special:Search]] enlaces a buscadores externos como Yahoo, Google, MSN Live y Exalead.

Trabaja en conjunto con el módulo [[MediaWiki:SpecialSearch.js]] y está basado en [[w:fr:MediaWiki:Monobook.js]].
<pre><nowiki> */

document.write('<script type="text/javascript" src="' 
+ '/w/index.php?title=MediaWiki:SpecialSearch.js'
+ '&action=raw&ctype=text/javascript&dontcountme=s&smaxage=3600"></script>');

/*</nowiki></pre>
== Cerrar mensajes ==
Ver ejemplo en [[Usuario:Chabacano/Fírmalo]], por [[Usuario:Platonides]].
<pre><nowiki> */

 addOnloadHook( function() {

 if (document.getElementById("cierraPadre")) {
      document.getElementById("cierraPadre").childNodes[0].onclick= function () { 
      document.getElementById("cierraPadre").style.cursor = 'pointer';
      document.getElementById("cierraPadre").parentNode.style.display = 'none';
      return false; /*no seguir el href*/} 
   }
 });


/*</nowiki></pre>
== Scripts sólo para biblios ==
<pre><nowiki> */

function userInGroup(group) {
  return (wgUserGroups && (('|' + wgUserGroups.join('|') + '|').indexOf('|' + group + '|') != -1));
}

if ( userInGroup('sysop') ) 
    importScript( "MediaWiki:Sysop.js" );

/*</pre>
== Wikimedia Player ==
Añade reproductor en la misma página.
<pre><nowiki> */

document.write('<script type="text/javascript" src="' 
+ '/w/index.php?title=MediaWiki:Wikimediaplayer.js'
+ '&action=raw&ctype=text/javascript&dontcountme=s&smaxage=3600"></script>');


/** WikiMiniAtlas *******************************************************
  *
  *  Description: WikiMiniAtlas is a popup click and drag world map.
  *               This script causes all of our coordinate links to display the WikiMiniAtlas popup button.
  *               The script itself is located on meta because it is used by many projects.
  *               See [[Meta:WikiMiniAtlas]] for more information. 
  *  Created by: [[User:Dschwen]]
  */
 
document.write('<script type="text/javascript" src="' 
+ 'http://meta.wikimedia.org/w/index.php?title=MediaWiki:Wikiminiatlas.js' 
+ '&action=raw&ctype=text/javascript&smaxage=21600&maxage=86400"></script>');

/*</pre>
== Mejoras de diseño de la Portada ==
<pre><nowiki> */

/** Mejoras de diseño de la Portada *********************************************************
  *
  *  Descripción:        Varias mejoras de diseño para la portada, incluyendo un
  *                      enlace adicional a la lista completa de idiomas disponibles.
  *  Adaptado de [[en:MediaWiki:Common.js]]
  */
 
 function mainPageAppendCompleteListLink() {
     try {
         var node = document.getElementById( "p-lang" )
                            .getElementsByTagName('div')[0]
                            .getElementsByTagName('ul')[0];
 
         var aNode = document.createElement( 'a' );
         var liNode = document.createElement( 'li' );
 
         aNode.appendChild( document.createTextNode( 'Lista completa' ) );
         aNode.setAttribute( 'href' , 'http://meta.wikimedia.org/wiki/Lista_de_Wikipedias' );
         liNode.appendChild( aNode );
         liNode.style.fontWeight = 'bold';
         node.appendChild( liNode );
      } catch(e) {
        // lets just ignore what's happened
        return;
     }
 }

 if ( wgPageName == "Wikipedia:Portada" ) {
        addOnloadHook( mainPageAppendCompleteListLink );
 }
/*</nowiki></pre>

== Redefinición de ordenación de tablas "sortable" ==

Traido de la Inclopedia. Ordena nombres de meses en español y cambia puntos por comas.

<pre><nowiki>*/

function ts_dateToSortKey(date) {	
	// y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
	if (date.length == 11) {
		switch (date.substr(3,3).toLowerCase()) {
			case "ene": var month = "01"; break;
			case "feb": var month = "02"; break;
			case "mar": var month = "03"; break;
			case "abr": var month = "04"; break;
			case "may": var month = "05"; break;
			case "jun": var month = "06"; break;
			case "jul": var month = "07"; break;
			case "ago": var month = "08"; break;
			case "sep": var month = "09"; break;
			case "oct": var month = "10"; break;
			case "nov": var month = "11"; break;
			case "dic": var month = "12"; break;
			// default: var month = "00";
		}
		return date.substr(7,4)+month+date.substr(0,2);
	} else if (date.length == 10) {
		if (ts_europeandate == false) {
			return date.substr(6,4)+date.substr(0,2)+date.substr(3,2);
		} else {
			return date.substr(6,4)+date.substr(3,2)+date.substr(0,2);
		}
	} else if (date.length == 8) {
		yr = date.substr(6,2);
		if (parseInt(yr) < 50) { 
			yr = '20'+yr; 
		} else { 
			yr = '19'+yr; 
		}
		if (ts_europeandate == true) {
			return yr+date.substr(3,2)+date.substr(0,2);
		} else {
			return yr+date.substr(0,2)+date.substr(3,2);
		}
	}
	return "00000000";
}

function ts_parseFloat(num) {
        if (!num) return 0;
        num = num.replace(/\./g, "");
        num = num.replace(/,/, ".");
        num = parseFloat(num);
        return (isNaN(num) ? 0 : num);
}

function ts_sort_caseinsensitive(a,b) {
var aa = a[1].toLowerCase();
var bb = b[1].toLowerCase();
return(aa.localeCompare(bb));
}


addOnloadHook ( function() {
     var n = Math.round(Math.random() * 9); //10 opciones

       for (i=0; i < document.styleSheets.length; i++) {
         if (document.styleSheets[0].href.substring(0, wgServer.length) == wgServer) { //NS_ERROR_DOM_SECURITY_ERR: http://permalink.gmane.org/gmane.science.linguistics.wikipedia.technical/40588

             if (document.styleSheets[0].cssRules) {
                for (i=document.styleSheets.length-1; i >= 0; i--) {
                    try {
                         //Añadir al final (Gecko)
                         document.styleSheets[i].insertRule('.rotate_0 { display: none }', document.styleSheets[i].cssRules.length);
                         document.styleSheets[i].insertRule('.rotate_' + n + ' { display: block; }', document.styleSheets[i].cssRules.length);
                         break;
                     } catch(e) {
                         //Ignorar el error y probar con la hoja de estilos anterior.
                         //Así, por ejemplo [[Usuario:Axxgreazz/Monobook-Suite/popups.js]] carga una hoja de estilos desde en.wikipedia.org, lo que provoca un error 'Access to URI denied' (NS_ERROR_DOM_BAD_URI).
                     }
                 }
             } else if (document.styleSheets[0].rules) { //IE
                document.styleSheets[document.styleSheets.length-1].addRule('.rotate_0', 'display: none');
                document.styleSheets[document.styleSheets.length-1].addRule('.rotate_' + n, 'display: block');
             }
             break;
        }
  }
 } );

var wma_settings =
{
buttonImage: "http://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Erioll_world.svg/15px-Erioll_world.svg.png"
}

/* MediaWiki:Monobook.js */
//Tooltips and access keys

ta = new Object();
ta['pt-userpage'] = new Array('.','Mi página de usuario'); 
ta['pt-anonuserpage'] = new Array('.','La página de usuario de la IP desde la que editas'); 
ta['pt-mytalk'] = new Array('n','Mi página de discusión'); 
ta['pt-anontalk'] = new Array('n','Discusión sobre ediciones hechas desde esta dirección IP'); 
ta['pt-preferences'] = new Array('','Mis preferencias'); 
ta['pt-watchlist'] = new Array('l','La lista de páginas para las que estás vigilando los cambios'); 
ta['pt-mycontris'] = new Array('y','Lista de mis contribuciones'); 
ta['pt-login'] = new Array('o','Te animamos a registrarte antes de editar, aunque no es obligatorio'); 
ta['pt-anonlogin'] = new Array('o','Te animamos a registrarte antes de editar, aunque no es obligatorio'); 
ta['pt-logout'] = new Array('o','Salir de la sesión'); 
ta['ca-talk'] = new Array('t','Discusión acerca del artículo'); 
ta['ca-edit'] = new Array('e','Puedes editar esta página. Por favor, usa el botón de previsualización antes de grabar.'); 
ta['ca-addsection'] = new Array('+','Añadir un comentario a esta discusión'); 
ta['ca-viewsource'] = new Array('e','Esta página está protegida, sólo puedes ver su código fuente'); 
ta['ca-history'] = new Array('h','Versiones anteriores de esta página y sus autores'); 
ta['ca-protect'] = new Array('=','Proteger esta página'); 
ta['ca-delete'] = new Array('d','Borrar esta página'); 
ta['ca-undelete'] = new Array('d','Restaurar las ediciones hechas a esta página antes de que fuese borrada'); 
ta['ca-move'] = new Array('m','Trasladar (renombrar) esta página'); 
ta['ca-nomove'] = new Array('','No tienes los permisos necesarios para trasladar esta página'); 
ta['ca-watch'] = new Array('w','Añadir esta página a tu lista de seguimiento'); 
ta['ca-unwatch'] = new Array('w','Borrar esta página de tu lista de seguimiento'); 
ta['search'] = new Array('f','Buscar en este wiki'); 
ta['p-logo'] = new Array('','Portada'); 
ta['n-mainpage'] = new Array('z','Visitar la Portada'); 
ta['n-portal'] = new Array('','Acerca del proyecto, qué puedes hacer, dónde encontrar información'); 
ta['n-currentevents'] = new Array('','Información de contexto sobre acontecimientos actuales'); 
ta['n-recentchanges'] = new Array('r','La lista de cambios recientes en el wiki'); 
ta['n-randompage'] = new Array('x','Cargar una página aleatoriamente'); 
ta['n-help'] = new Array('','El lugar para aprender'); 
ta['n-sitesupport'] = new Array('','Respáldanos'); 
ta['t-whatlinkshere'] = new Array('j','Lista de todas las páginas del wiki que enlazan con ésta'); 
ta['t-recentchangeslinked'] = new Array('k','Cambios recientes en las páginas que enlazan con esta otra'); 
ta['feed-rss'] = new Array('','Suscripción RSS de esta página'); 
ta['feed-atom'] = new Array('','Suscripción Atom de esta página'); 
ta['t-contributions'] = new Array('','Ver la lista de contribuciones de este usuario'); 
ta['t-emailuser'] = new Array('','Enviar un mensaje de correo a este usuario'); 
ta['t-upload'] = new Array('u','Subir imágenes o archivos multimedia'); 
ta['t-specialpages'] = new Array('q','Lista de todas las páginas especiales'); 
ta['ca-nstab-main'] = new Array('c','Ver el artículo'); 
ta['ca-nstab-user'] = new Array('c','Ver la página de usuario'); 
ta['ca-nstab-media'] = new Array('c','Ver la página de multimedia'); 
ta['ca-nstab-special'] = new Array('','Esta es una página especial, no se puede editar la página en sí'); 
ta['ca-nstab-wp'] = new Array('a','Ver la página de proyecto'); 
ta['ca-nstab-image'] = new Array('c','Ver la página de la imagen'); 
ta['ca-nstab-mediawiki'] = new Array('c','Ver el mensaje de sistema'); 
ta['ca-nstab-template'] = new Array('c','Ver la plantilla'); 
ta['ca-nstab-help'] = new Array('c','Ver la página de ayuda'); 
ta['ca-nstab-category'] = new Array('c','Ver la página de categoría');
ta['wpConfirmB'] = new Array('s','Borrar realmente la página');


// == Código del plegado/desplegado de plantillas ==

var NavigationBarHide = 'Plegar';
var NavigationBarShow = 'Desplegar';

var NavigationBarShowDefault = 0;

document.write('<script type="text/javascript" ' +
  'src="/w/index.php?title=MediaWiki:NavigationBar.js' +
  '&amp;action=raw&amp;smaxage=3600&amp;ctype=text/javascript&amp;dontcountme=s"></scr' +
  'ipt>');


// == Código para artículos destacados ==
		
function LinkFA() 
{
   // iterate over all <span>-elements
   for (var i=0; a = document.getElementsByTagName("span")[i]; i++) {
      // if found a FA span
      if(a.className == "destacado") {
         // iterate over all <li>-elements
         for(var j=0; b = document.getElementsByTagName("li")[j]; j++) {
            // if found a FA link
            if (b.className == "interwiki-" + a.id) {
               b.className += " destacado";
               b.title = "Este es un artículo destacado en esta Wikipedia.";
            }
         }
      }
   }
}

if (window.addEventListener) window.addEventListener("load",LinkFA,false);
else if (window.attachEvent) window.attachEvent("onload",LinkFA);


function LinkAB() 
{
   // iterate over all <span>-elements
   for (var i=0; a = document.getElementsByTagName("span")[i]; i++) {
      if(a.className == "bueno") {
         // iterate over all <li>-elements
         for(var j=0; b = document.getElementsByTagName("li")[j]; j++) {
            // if found a AB link
            if (b.className == "interwiki-" + a.id) {
               b.className += " bueno";
               b.title = "Este es un artículo bueno en esta Wikipedia.";
            }
         }
      }
   }
}

if (window.addEventListener) window.addEventListener("load",LinkAB,false);
else if (window.attachEvent) window.attachEvent("onload",LinkAB);

function addLoadEvent(func) {
   if (window.addEventListener) {
       window.addEventListener("load", func, false);
   } else if (window.attachEvent) {
       window.attachEvent("onload", func);
   }
}


/*
// == Interproyectos en un recuadro a la izquierda ==
 Modificado a partir de de:wikt:Mediawiki:monobook.js
 Funcionan con la plantilla <nowiki>{{</nowiki>[[Plantilla:interproyecto|interproyecto]]<nowiki>}}</nowiki> y en breve con otras
 [[:Categoría:Wikipedia:Plantillas_de_enlace_entre_proyectos|plantillas de enlace entre proyectos]]
*/

 document.write('<style type="text/css">#interProject {display: none; speak: none;} #p-tb .pBody {padding-right: 0;}<\/style>');
 function iProject() {
  var elementos = new Array();
  var els = document.getElementsByTagName("span");
  var elsLen = els.length;
  for (i = 0, j = 0; i < elsLen; i++) {
    if ( "interProject" == els[i].className) {
      elementos[j] = els[i];
      j++;
    }
  }
  if (j) {
     var IPY='<h5>otros proyectos<\/h5><div class="pBody"><ul>';
     for (i = 0; i< elementos.length; i++) {
         IPY += '<li>'+elementos[i].innerHTML+'</li>';
     }
     var interProject = document.createElement("div");
     interProject.style.marginTop = "0.7em";
     interProject.innerHTML = IPY+'</ul><\/div>';
     document.getElementById("p-tb").appendChild(interProject);
   }
 }
 addLoadEvent(iProject);


/*
// == Caracteres especiales (edittools) ==
Crea (y coloca) el ''combobox'' que permite seleccionar un conjunto determinado de
caracteres especiales bajo la caja de edición.
Funciona en conjunto con [[MediaWiki:Edittools]] y [[MediaWiki:Edittools.js]].

Basado en [[commons:MediaWiki:Edittools.js]].
*/

document.write('<script type="text/javascript" ' +
               'src="/w/index.php?title=MediaWiki:Edittools.js' +
               '&action=raw&smaxage=3600' +
               '&ctype=text/javascript' +
               '&dontcountme=s"></scr' +
               'ipt>');

function MenuDeCaracteresEspecialesWrp()
{
  if (typeof(quieroEditToolsSimple) != "undefined" && !quieroEditToolsSimple)
      MenuDeCaracteresEspeciales();
}

addLoadEvent(MenuDeCaracteresEspecialesWrp);

/*
// == Título incorrecto ==
Desde en: (Maintainers: User:Interiot, User:Mets501). Incorporado por [[Usuario:Platonides]] 
*/

// For pages that have something like Template:Lowercase, replace the title, but only if it is cut-and-pasteable as a valid wikilink.
//      (for instance iPod's title is updated.  But [[C#]] is not an equivalent wikilink, so [[C Sharp]] doesn't have its main title changed)
//
// The function looks for a banner like this: 
 // <div id="RealTitleBanner">    
 //   <span id="RealTitle">title</span>
 // </div>
 // An element with id=DisableRealTitle disables the function.
var disableRealTitle = 0;               // users can disable this by making this true from their monobook.js
if (wgIsArticle) {                      // don't display the RealTitle when editing, since it is apparently inconsistent (doesn't show when editing sections, doesn't show when not previewing)
    addOnloadHook(function() {
        try {
                var realTitleBanner = document.getElementById("RealTitleBanner");
                if (realTitleBanner && !document.getElementById("DisableRealTitle") && !disableRealTitle) {
                        var realTitle = document.getElementById("RealTitle");
                        if (realTitle) {
                                var realTitleHTML = realTitle.innerHTML.replace(/<\/?(sub|sup|small|big)>/gi, function(match) { return match.toLowerCase(); });
                                realTitleText = pickUpText(realTitle);

                                var isPasteable = 0;
                                //var containsHTML = /</.test(realTitleHTML);        // contains ANY HTML
                                var containsTooMuchHTML = /</.test( realTitleHTML.replace(/<\/?(sub|sup|small|big)>/gi, "") ); // contains HTML that will be ignored when cut-n-pasted as a wikilink
                                // calculate whether the title is pasteable
                                var verifyTitle = realTitleText.replace(/^ +/, "");             // trim left spaces
                                verifyTitle = verifyTitle.charAt(0).toUpperCase() + verifyTitle.substring(1, verifyTitle.length);       // uppercase first character

                                // if the namespace prefix is there, remove it on our verification copy.  If it isn't there, add it to the original realValue copy.
                                if (wgNamespaceNumber != 0) {
                                        if (wgCanonicalNamespace == verifyTitle.substr(0, wgCanonicalNamespace.length).replace(/ /g, "_") && verifyTitle.charAt(wgCanonicalNamespace.length) == ":") {
                                                verifyTitle = verifyTitle.substr(wgCanonicalNamespace.length + 1);
                                        } else {
                                                realTitleText = wgCanonicalNamespace.replace(/_/g, " ") + ":" + realTitleText;
                                                realTitleHTML = wgCanonicalNamespace.replace(/_/g, " ") + ":" + realTitleHTML;
                                        }
                                }

                                // verify whether wgTitle matches
                                verifyTitle = verifyTitle.replace(/^ +/, "").replace(/ +$/, "");                // trim left and right spaces
                                verifyTitle = verifyTitle.replace(/_/g, " ");           // underscores to spaces
                                verifyTitle = verifyTitle.charAt(0).toUpperCase() + verifyTitle.substring(1, verifyTitle.length);       // uppercase first character
                                isPasteable = (verifyTitle == wgTitle);

                                var h1 = document.getElementsByTagName("h1")[0];
                                if (h1 && isPasteable) {
                                        h1.innerHTML = containsTooMuchHTML ? realTitleText : realTitleHTML;
                                        if (!containsTooMuchHTML)
                                                realTitleBanner.style.display = "none";
                                }
                                document.title = realTitleText + " - Wikipedia, la enciclopedia libre";
                        }
                }
        } catch (e) {
                /* Something went wrong. */
        }
    });
}

// similar to innerHTML, but only returns the text portions of the insides, excludes HTML
function pickUpText(aParentElement) {
  var str = "";

  function pickUpTextInternal(aElement) {
    var child = aElement.firstChild;
    while (child) {
      if (child.nodeType == 1)          // ELEMENT_NODE 
        pickUpTextInternal(child);
      else if (child.nodeType == 3)     // TEXT_NODE
        str += child.nodeValue;

      child = child.nextSibling;
    }
  }

  pickUpTextInternal(aParentElement);

  return str;
}

/*
// == Botones [editar] justo a la derecha de los títulos ==
Traído por [[Usuario:Chlewey|Carlos Th]] desde [[:de:MediaWiki:Monobook.js]].
* moveEditsection
* Este script mueve los botones [editar] del borde derecho de la ventana
* justo a la derecha del título correspondiente.
* Dieses Script verschiebt die [Bearbeiten]-Buttons vom rechten Fensterrand
* direkt rechts neben die jeweiligen Überschriften.
* This script moves the [edit]-buttons from the right border of the window
* directly right next to the corresponding headings.
*
* Si alguien desea conservar el comportamiento original de los botones,
* puede copiar en su propia botonera (Usuario:Nombre/nomobook.js):
* var oldEditsectionLinks = true;
*
* dbenzhuser (de:Benutzer:Dbenzhuser)
*/
function moveEditsection() {
    if (typeof oldEditsectionLinks == 'undefined' || oldEditsectionLinks == false) {
        var spans = document.getElementsByTagName("span");
        for(var i = 0; i < spans.length; i++) {
            if(spans[i].className == "editsection") {
                spans[i].style.fontSize = "small";
                spans[i].style.fontWeight = "normal";
                spans[i].style.cssFloat = "none";
                spans[i].style.marginLeft = "0px";
                spans[i].parentNode.appendChild(document.createTextNode(" "));
                spans[i].parentNode.appendChild(spans[i]);
            }
        }
    }
}
// onload
addOnloadHook(moveEditsection);