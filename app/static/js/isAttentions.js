/**
 * Created by q on 2018/3/9.
 */
function toAttention(user_id) {
   $.post("/to_attention/",
   {
        be_user_id:user_id,
   },
   function(data){
        alert(data);
        location.href="/1";
   });
}
function unAttention(user_id,url) {
   full_url = url+window.location.search;
   $.post("/un_attention/",
   {
        be_user_id:user_id,
   },
   function(data){
        alert(data);
        location.href=full_url;
   });
}
function postError(rs_id) {
   url = $("li.active").children().attr('href')+window.location.search;
   $.post("/post_error/",
   {
        url_info:$("input[name='url-info']:checked").val(),
        rs_id:rs_id,
   },
   function(data){
        alert(data);
        location.href = url;
   });
}
