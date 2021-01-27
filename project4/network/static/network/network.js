document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.alert').style.display = 'none';

    if (document.querySelector('#new_post'))
    {
      document.querySelector('#new_post').addEventListener('click', () => new_post());
    }
    //calls function edit() for clicked edit post button
    document.querySelectorAll('.edit-post')
        .forEach(item => {
            item.addEventListener('click',() => edit(item));
        });

    document.querySelectorAll('.like-btn')
        .forEach(item => {
            item.addEventListener('click',() => like(item));
        });
});

function new_post(){
    fetch('/post', {
      method: 'POST',
      body: JSON.stringify({
          newPostText: document.querySelector('#post-text').value,
      })

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
    document.querySelector(`#save-edit-for-${id}`).style.display = "block";
    document.querySelector(`#cancel-edit-for-${id}`).style.display = "block";
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

function like(item){
    let id = item.getAttribute("id");
    console.log(id);
}