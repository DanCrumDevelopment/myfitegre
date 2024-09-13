<?php
// Start the session
session_start();

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Here you would typically validate the login credentials
    // For now, we'll just set a session variable
    $_SESSION['user'] = $_POST['email'];
    header("Location: index.php"); // Redirect to home page after login
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Myfitegre Technologies LLC - Login</title>
    <link rel="icon" href="docs/assets/images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="styles.css">
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .login-title {
            margin-bottom: 20px;
            color: #333;
        }
        .login-form input {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .login-button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .login-button:hover {
            background-color: #0056b3;
        }
        .signup-link {
            margin-top: 20px;
            display: block;
            color: #007bff;
            text-decoration: none;
        }
        .signup-link:hover {
            text-decoration: underline;
        }

        .popup {
            display: none;
            position: fixed;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: #f8d7da;
            color: #721c24;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            text-align: center;
            z-index: 1000;
        }

        .popup-content {
            margin-bottom: 15px;
        }

        .popup-button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        .popup-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-wrapper">
            <div class="main-nav">
                <a href="index.php">Home</a>
                <a href="buynow.php">Buy Now</a>
                <a href="about.php">About</a>
                <a href="contact.php">Contact</a>
                <a href="warranty.php">Warranty</a>
            </div>
            <div class="user-section">
                <div class="profile-circle"></div>
                <a href="login.php" class="active">Login</a>
            </div>
        </div>
    </nav>

    <div class="login-container">
        <h2 class="login-title">Login</h2>
        <form class="login-form" action="login.php" method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="login-button">Login</button>
        </form>
        <a href="signup.php" class="signup-link">Don't have an account? Sign up</a>
    </div>

    <?php
    // Display error message if login failed
    if (isset($_GET['error'])) {
        echo '<div id="loginPopup" class="popup" style="display:block;">
                <div class="popup-content">Login Failed!</div>
                <button class="popup-button" onclick="closePopup()">OK</button>
              </div>';
    }
    ?>

    <script>
        function closePopup() {
            document.getElementById('loginPopup').style.display = 'none';
        }
    </script>
</body>
</html>
