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
$(document).ready(function() {
    // Track the form validity
    let validName = false;
    let validEmail = false;
    let validPassword = false;
  
    // Function to check form validity
    function checkFormValidity() {
      if (validName && validEmail && validPassword) {
        $('#signupButton').prop('disabled', false); // Enable signup button
      } else {
        $('#signupButton').prop('disabled', true); // Disable signup button
      }
    }
  
    // Event listener for name input
    $('#nameInput').on('input', function() {
      const name = $(this).val().trim();
      validName = name.length > 0;
      checkFormValidity();
    });
  
    // Event listener for email input
    $('#emailInput').on('input', function() {
      const email = $(this).val().trim();
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      validEmail = emailPattern.test(email);
      if (validEmail==true) {
        console.log("Valid");
        $("#wrong-email").hide();
        $("#correct-email").show();
        $("#emailMessage").hide();
    } else {
        console.log("Invalid");
        $("#correct-email").hide();
        $("#emailMessage").show();
        $("#wrong-email").show();
    }
    
    if (email === "") {
        $("#correct-email").hide();
        $("#wrong-email").hide();
        $("#emailMessage").hide();
    }
      checkFormValidity();
    });
  
    // Event listener for password input
    $('#passwordInput').on('input', function() {

      const password = $(this).val();
      const passPattern = /^(.{8,})$/;
      validPassword = passPattern.test(password);
      if (validPassword==true) {
        console.log("Valid");
        $("#wrong-pass").hide();
        $("#correct-pass").show();
        $("#passMessage").hide();
    } else {
        console.log("Invalid");
        $("#correct-pass").hide();
        $("#passMessage").show();
        $("#wrong-pass").show();
    }
    
    if (password === "") {
        $("#correct-pass").hide();
        $("#wrong-pass").hide();
        $("#passMessage").hide();
    }
    
      checkFormValidity();

    });
  
    // Submit form
    $('#registerForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission
  
      const name = $('#nameInput').val().trim();
      const email = $('#emailInput').val().trim();
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
          // Redirect to another page
          window.location.href = 'index.html';
        },
        error: function(error) {
          console.error('Registration failed');
          // Add your desired behavior here, such as showing an error message
        }
      });
    });
  });
  
