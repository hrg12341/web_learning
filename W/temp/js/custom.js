var flag =0
var c=0
function handleFile(elem)
    {
        file_name = elem.files[0].name;
        //alert(file_name);
        file_name = file_name.substring(file_name.lastIndexOf(".") + 1);
        if(file_name != "txt" && file_name != "fasta" && file_name != undefined){
            flag = 1;
            alert("The upload file must be txt or fasta file.");
            return false;
        }
        flag = 0;

    }


function timedCount() {
if(flag == 0)
	{
            document.getElementById('time').value=c;
 	    c=c+1;
 	    t=setTimeout("timedCount()",1000);
 	    document.getElementById('txtt').style.visibility="visible";
 	    return true;
        }
        else if(flag == 1)
        {
            alert("Sorry, the upload file must be txt or fasta file.");
            return false;
        }
}


function delayURL(url) {
    var delay=30;
//var delay = document.getElementById("time").innerHTML;//取到id="time"的对象，.innerHTML取到对象的值
//alert(delay);
if(delay > 0) {
   delay--;
   document.getElementById("time").innerHTML = delay;
} else {
   window.top.location.href = url;//跳转到URL
    }
    setTimeout("delayURL('" + url + "')", 1000);    //delayURL() 就是每间隔1000毫秒 调用delayURL(url);
}