const express = require('express');
const Firestore = require('@google-cloud/firestore');

const app = express();
const firestore = new Firestore();

app.use(express.json());

/*
***************************************************************************************
*    Title: Firestore CRUD with NODE.JS
*    Author: Code with Kavit 
*    Date: 2022
*    Code version: 1.0
*    Availability: https://www.youtube.com/watch?v=8Se_F7c03UM
*
***************************************************************************************
*/
/*
***************************************************************************************
*    Title: Google Cloud Firestore in 10 mins (Node.js)
*    Author: Ambient Coder
*    Date: 2020
*    Code version: 1.0
*    Availability: https://www.youtube.com/watch?v=eT3WHdr8aCw
*
***************************************************************************************
*/
app.post('/register', async (req, res) => {
  try {
    const { name, email, password, location } = req.body;
    // Create Reg collection if not present
    // Save registration data to Firestore
    const regRef = firestore.collection('Reg');
    const docRef = await regRef.add({ name, email, password, location });

    res.status(200).json({ message: 'Registration successful'});
  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).json({ error: 'Failed to register user' });
  }
});

app.listen(3000, () => {
  console.log('Registration service running on port 3000');
});
