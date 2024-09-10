const express = require('express');
const paypal = require('paypal-rest-sdk');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const app = express();

// PayPal configuration
paypal.configure({
    mode: 'sandbox', // or 'live' for production
    client_id: 'AVEZ72PV_k55rxd4irSKlOiMggCXQhUzZkKJUPUzWYjVUVzVfV-vPu-3HUKcrEnBZetD0OO0kdMLdH_T',
    client_secret: 'EEF54hMbeHLPG_NyLenr1h1liuETI3vNYMJeDc7lpgYxSa0XWmGoVPweWLoMoR4y696arVzG70C7lYjX'
});

// PostgreSQL configuration
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
        rejectUnauthorized: false
    }
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files (your HTML files)
app.use(express.static('public'));

// Route to create PayPal order
app.post('/create-paypal-transaction', (req, res) => {
    const { amount } = req.body;

    const create_payment_json = {
        intent: "sale",
        payer: {
            payment_method: "paypal"
        },
        transactions: [{
            amount: {
                currency: "USD",
                total: amount
            },
            description: "Nova PC purchase"
        }],
        redirect_urls: {
            return_url: "http://localhost:3000/success",
            cancel_url: "http://localhost:3000/cancel"
        }
    };

    paypal.payment.create(create_payment_json, function (error, payment) {
        if (error) {
            console.error(error);
            res.status(500).send(error);
        } else {
            for (let i = 0; i < payment.links.length; i++) {
                if (payment.links[i].rel === 'approval_url') {
                    res.json({ forwardLink: payment.links[i].href });
                    return;
                }
            }
        }
    });
});

// Route to handle success
app.get('/success', (req, res) => {
    const payerId = req.query.PayerID;
    const paymentId = req.query.paymentId;

    const execute_payment_json = {
        payer_id: payerId,
        transactions: [{
            amount: {
                currency: "USD",
                total: req.query.amount // Use the amount from the payment
            }
        }]
    };

    paypal.payment.execute(paymentId, execute_payment_json, function (error, payment) {
        if (error) {
            console.error(error.response);
            res.send('Payment Failed');
        } else {
            res.send('Payment Successful');
        }
    });
});

// Route to handle cancel
app.get('/cancel', (req, res) => res.send('Payment Cancelled'));

// New route to handle signup form submission
app.post('/signup', async (req, res) => {
    try {
        const { first_name, middle_initial, last_name, email, area_code, phone_number, street_address, city, state, zip_code, country } = req.body;
        
        const query = `
            INSERT INTO users (first_name, middle_initial, last_name, email, phone, street_address, city, state, zip_code, country)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id
        `;
        
        const values = [first_name, middle_initial, last_name, email, `(${area_code}) ${phone_number}`, street_address, city, state, zip_code, country];
        
        const result = await pool.query(query, values);
        
        res.status(201).json({ message: 'User registered successfully', userId: result.rows[0].id });
    } catch (error) {
        console.error('Error registering user:', error);
        res.status(500).json({ message: 'Error registering user' });
    }
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
