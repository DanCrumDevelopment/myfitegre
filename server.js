const express = require('express');
const paypal = require('paypal-rest-sdk');
const bodyParser = require('body-parser');
const app = express();

// PayPal configuration
paypal.configure({
    mode: 'sandbox', // or 'live' for production
    client_id: 'AVEZ72PV_k55rxd4irSKlOiMggCXQhUzZkKJUPUzWYjVUVzVfV-vPu-3HUKcrEnBZetD0OO0kdMLdH_T',
    client_secret: 'EEF54hMbeHLPG_NyLenr1h1liuETI3vNYMJeDc7lpgYxSa0XWmGoVPweWLoMoR4y696arVzG70C7lYjX'
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

// Start the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
