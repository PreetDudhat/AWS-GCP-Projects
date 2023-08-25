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

app.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Check if the provided email and password match the registered user in Firestore
    const regRef = firestore.collection('Reg');
    const getUserData = await regRef.where('email', '==', email).where('password', '==', password).get();

    if (getUserData.empty) {
      // User not found or credentials are incorrect
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    // Login successful
    const user = getUserData.docs[0].data();
    const userId = getUserData.docs[0].id;
    // Create state collection automatically if not present
    // Update user status to "online" in Firestore
    const stateRef = firestore.collection('state').doc(userId);
    await stateRef.set({ status: 'online', name: user.name });

    res.status(200).json({name: user.name, message: 'Login successful' });
  } catch (error) {
    console.error('Error logging in user:', error);
    res.status(500).json({ error: 'Failed to log in user' });
  }
});

app.listen(3001, () => {
  console.log('Login service running on port 3001');
});
