<?php
// Start the session (if you're using sessions for login)
session_start();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Myfitegre Technologies LLC - Home</title>
    <link rel="icon" href="docs/assets/images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="styles.css">
    <style>
        /* Page-specific styles */
        .banner-container {
            width: 100%;
            overflow: hidden;
        }
        .banner {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        .offerings-image {
            max-width: 20%;
            height: auto;
            margin: 20px auto;
            padding: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            display: block;
        }
        .offerings {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .offering {
            text-align: center;
            margin: 10px;
        }
        .offering img {
            max-width: 200px;
            height: auto;
        }
        .highlight-text {
            background-color: black;
            color: white;
            padding: 10px;
            display: inline-block;
            margin: 20px 0;
        }
        .flashing-green {
            color: green;
            animation: flash 1s infinite;
        }
        .rainbow-text {
            background-image: linear-gradient(to left, violet, indigo, blue, green, yellow, orange, red);
            -webkit-background-clip: text;
            color: transparent;
        }
        .small-black-text {
            font-size: 0.8em;
            color: black;
        }
        @keyframes flash {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        .welcome-blurb {
            background-color: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 20px;
            margin: 20px auto;
            max-width: 80%;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            border: 3px solid white;
            font-size: 18px;
            line-height: 1.6;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .welcome-blurb:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-wrapper">
            <div class="main-nav">
                <a href="index.php" class="active">Home</a>
                <a href="buynow.php">Buy Now</a>
                <a href="about.php">About</a>
                <a href="contact.php">Contact</a>
                <a href="warranty.php">Warranty</a>
            </div>
            <div class="user-section">
                <div class="profile-circle"></div>
                <?php
                if (isset($_SESSION['user'])) {
                    echo '<a href="logout.php">Logout</a>';
                } else {
                    echo '<a href="login.php">Login</a>';
                }
                ?>
            </div>
        </div>
    </nav>
    <div class="banner-container">
        <img src="docs/assets/images/banner.jpeg" alt="Myfitegre Technologies LLC Banner" class="banner">
    </div>
    <div class="welcome-blurb">
        <p>Welcome. We have devised three builds. First is our budget build that packs a serious punch out the box on the AMD AM4 platform called the Nova. We are also introducing our Siren build and the Apocalypse (both on the AMD AM5 platform).</p>
    </div>
    <div style="text-align:center;">
        <img src="docs/assets/images/offerings.jpeg" alt="Our Offerings" style="max-width: 20%; height: auto; margin: 20px auto; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); border-radius: 8px;">
    </div>
    
    <div style="text-align:center;">
        <div class="highlight-text">Click Images Below!!!</div>
    </div>
    
    <section class="offerings">
        <div class="offering">
            <a href="novaclass.php">
                <img src="docs/assets/images/nova.jpeg" alt="Nova PC">
                <h3>Nova</h3>
            </a>
            <div style="text-align:center;">
                <div class="flashing-green">$1,011.40</div>
                <br>
                <div class="rainbow-text">Available Now!</div>
                <br>
                <div class="small-black-text">Final Price - includes delivery & tax</div>
            </div>
        </div>
        <div class="offering">
            <a href="sirenclass.php">
                <img src="docs/assets/images/siren.jpeg" alt="Siren PC">
                <h3>Siren</h3>
            </a>
        </div>
        <div class="offering">
            <a href="apocalypseclass.php">
                <img src="docs/assets/images/apocalypse.jpeg" alt="Apocalypse PC">
                <h3>Apocalypse</h3>
            </a>
        </div>
    </section>
</body>
</html>


