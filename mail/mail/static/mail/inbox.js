document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('.alert').style.display = 'none';

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-open').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        if (result["error"]) {
          document.querySelector('#message').innerHTML = result["error"];
          document.querySelector('.alert').style.display = 'block';
          document.body.scrollTop = document.documentElement.scrollTop = 0;
        }
        else {
          document.querySelector('.alert').style.display = 'none';
          load_mailbox('sent')
        }
    });
    return false;

  };

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-open').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


    fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        for (let i = 0; i < emails.length; i++) {
            const index = 'email-box' + i.toString(10);
            const email = emails[i];

            document.querySelector('#emails-view').innerHTML += ` 
                <div class="read-${email["read"]}" id="${index}"><div class="p-2 email-inner">${email["sender"]}</div>
                <div class="p-2 email-inner ">${email["subject"]}</div>
                <div class="px-2 email-inner right">${email["timestamp"]}</div></div>`;
        }

        for (let i = 0; i < emails.length; i++) {
            const index = 'email-box' + i.toString(10);
            let el = document.getElementById(index);
            const email = emails[i];
            if (el) {
                el.addEventListener("click", () => {email_open(email); console.log(email);});
            }
        }
    });
}

function email_open(email) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-open').style.display = 'block';

  fetch('/emails/' + email.id, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
  })

  document.querySelector('#email-open').innerHTML = `
      <div>Sender: ${email["sender"]}</div>
      <div>Recipients: ${email["recipients"]}</div>
      <div>Subject: ${email["subject"]}</div>
      <div>Time: ${email["timestamp"]}</div>
      <div>Body: ${email["body"]}</div>`

  document.querySelector('#email-open').innerHTML += `
      <button class="btn btn-primary" id="archive">${email["archived"] ? "Unarchive" : "Archive"}</button>`


    document.querySelector('#archive').onclick = () => {
        fetch('/emails/' + email.id, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email["archived"]
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result["error"]) {
                document.querySelector('#message').innerHTML = result["error"];
                document.querySelector('.alert').style.display = 'block';
                document.body.scrollTop = document.documentElement.scrollTop = 0;
            } else {
                document.querySelector('.alert').style.display = 'none';
                load_mailbox('inbox')
            }
        });
        return false;
    }

}