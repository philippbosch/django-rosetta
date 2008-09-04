var rosetta = {};
rosetta.toggle_ref = function(o){
     var doShow = o.className == 'showall show';
     o.className= doShow? 'showall hide':'showall show';
     var codes = o.parentNode.getElementsByTagName('code');
     for (var i=0;i<codes.length;i++) {
         var code=codes[i];
         if (code.className == 'hide' && doShow) {
             code.style.display = 'block';
         } else if (code.className == 'hide') {
             code.style.display = 'none';
         }
     }
     return false;
}
