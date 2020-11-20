document.addEventListener('DOMContentLoaded', function() {


    if (document.querySelector('#new_post'))
    {
      document.querySelector('#new_post').addEventListener('click', () => new_post());
    }

    document.querySelector('.alert').style.display = 'none';

  });

function new_post(){
    fetch('/post', {
      method: 'POST',
      body: JSON.stringify({
          new_post_text: document.querySelector('#post-text').value,
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