console.clear();

const loginBtn = document.getElementById('login');
const signupBtn = document.getElementById('signup');

loginBtn.addEventListener('click', (e) => {
    let parent = e.target.parentNode.parentNode;
    Array.from(e.target.parentNode.parentNode.classList).find((element) => {
        if(element !== "slide-up") {
            parent.classList.add('slide-up')
        }else{
            signupBtn.parentNode.classList.add('slide-up')
            parent.classList.remove('slide-up')
        }
    });
});

signupBtn.addEventListener('click', (e) => {
    let parent = e.target.parentNode;
    Array.from(e.target.parentNode.classList).find((element) => {
        if(element !== "slide-up") {
            parent.classList.add('slide-up')
        }else{
            loginBtn.parentNode.parentNode.classList.add('slide-up')
            parent.classList.remove('slide-up')
        }
    });
});
//****REGISTER TO API** */
$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission
  
      const name = $('#nameInput').val();
      const email = $('#emailInput').val();
      const password = $('#passwordInput').val();
  
      const data = {
        name: name,
        email: email,
        password: password
      };
      $.ajax({
        url: 'https://d492-105-41-171-186.ngrok-free.app/monkey%20pox%20detection/backEnd/public/api/auth/register',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
          console.log('Registration successful');
          // Add your desired behavior here, such as showing a success message or redirecting to another page
        },
        error: function(error) {
          console.error('Registration failed');
          // Add your desired behavior here, such as showing an error message
        }
      });
    });
  });
//ALERT//
var passPattern=/^(.{8,})$/
function validatePassword(pass)
{
    if(passPattern.test(pass)==true)
    {
        console.log("Valid")
        document.getElementById("wrong-pass").style.display="none"
        document.getElementById("correct-pass").style.display="block"
        document.getElementById("message").style.display="none"
        valid=true
        console.log(valid)
    }
    else{
        console.log("invalid")
        document.getElementById("correct-pass").style.display="none"
        document.getElementById("message").style.display="block"
        document.getElementById("wrong-pass").style.display="block"
        valid=false
        console.log(valid)
    }
    if(pass=="")
    {
        document.getElementById("correct-pass").style.display="none"
        document.getElementById("wrong-price").style.display="none"
        document.getElementById("message").style.display="none"
        valid=false
        console.log(valid)
    }
}
