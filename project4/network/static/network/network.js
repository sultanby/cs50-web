document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.alert').style.display = 'none';

    if (document.querySelector('#new_post'))
    {
      document.querySelector('#new_post').addEventListener('click', () => new_post());
    }
    //calls function edit() for clicked edit post button
    document.querySelectorAll('.edit-post-btn')
        .forEach(item => {
            item.addEventListener('click',() => edit(item));
        });

    document.querySelectorAll('.like-btn')
        .forEach(item => {
            item.addEventListener('click',() => like(item));
        });
});

function new_post(){
    let postText = document.querySelector('#post-text').value;
    let body = new FormData()
    body.append('new_post_text', postText)
    fetch('/post', {
      method: 'POST',
      body: body,
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]) {
          console.log(result);
          document.querySelector('#message').innerHTML = result["error"];
          document.querySelector('.alert').style.display = 'block';
          document.body.scrollTop = document.documentElement.scrollTop = 0;
        }
        else {
          console.log(result);
          document.querySelector('.alert').style.display = 'none';
        }
    });

    document.querySelector('#post-text').value = '';
}

function edit(item) {
    let id = item.getAttribute("id");
    console.log(id);
    document.querySelector(`#post-text-for-${id}`).style.display = "none";
    document.querySelector(`.edit-btn-${id}`).style.display = "none";
    document.querySelector(`#textarea-edit-for-${id}`).style.display = "block";
    document.querySelector(`#save-edit-for-${id}`).style.display = "inline-block";
    document.querySelector(`#cancel-edit-for-${id}`).style.display = "inline-block";
    document.querySelector(`#cancel-edit-for-${id}`).addEventListener('click', function(){
        document.querySelector(`#post-text-for-${id}`).style.display = "block";
        document.querySelector(`.edit-btn-${id}`).style.display = "inline";
        document.querySelector(`#textarea-edit-for-${id}`).style.display = "none";
        document.querySelector(`#save-edit-for-${id}`).style.display = "none";
        document.querySelector(`#cancel-edit-for-${id}`).style.display = "none";
    });
    document.querySelector(`#save-edit-for-${id}`).addEventListener('click', () => saveEdit(id));
}

function saveEdit(id){
    let editedPostText = document.querySelector(`#textarea-edit-for-${id}`).value;
    console.log(id, editedPostText);

    let formData = new FormData();
    formData.append("id", id);
    formData.append("editedPostText", editedPostText);
    //console.log(formData);
    /*for (var key of formData.entries()) {
			console.log(key[0] + ', ' + key[1])
		}
	*/

    fetch("/edit", {
        body: formData,
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]){
            console.log(result);
            document.querySelector('#message').innerHTML = result["error"];
            document.querySelector('.alert').style.display = 'block';
        }
        else {
            console.log(result);
            document.querySelector('.alert').style.display = 'none';
            document.querySelector(`#post-text-for-${id}`).innerHTML = editedPostText;
            document.querySelector(`#post-text-for-${id}`).style.display = "block";
            document.querySelector(`.edit-btn-${id}`).style.display = "inline";
            document.querySelector(`#textarea-edit-for-${id}`).style.display = "none";
            document.querySelector(`#save-edit-for-${id}`).style.display = "none";
            document.querySelector(`#cancel-edit-for-${id}`).style.display = "none";
            document.querySelector(`#textarea-edit-for-${id}`).value = editedPostText;
        }

    });

}
function renderLike(id){
    document.querySelector(`#like-icon-${id}`).src = "/static/network/media/unlike.png";
    document.querySelector(`#like-text-${id}`).innerHTML = "Like";
}

function renderUnlike(id){
    document.querySelector(`#like-icon-${id}`).src = "/static/network/media/like.png";
    document.querySelector(`#like-text-${id}`).innerHTML = "Unlike";
}
function like(item){
    let pre_id = item.getAttribute("id");
    let id = pre_id.slice(11);
    console.log(id);

    let formData = new FormData();
    formData.append("id", id);

    fetch("/like", {
        body: formData,
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        result["remove"] ? renderLike(id) : renderUnlike(id);
        document.querySelector(`.like-count-${id}`).innerHTML = result["like_count"];
    });

}