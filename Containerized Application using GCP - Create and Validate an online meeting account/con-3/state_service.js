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
  app.get('/online-users', async (req, res) => {
    try {
      // Get online users from Firestore
      const stateCollection = firestore.collection('state');
      const getStatus = await stateCollection.where('status', '==', 'online').get();
      const onlineUsers = getStatus.docs.map((doc) => doc.data());

      res.status(200).json({ onlineUsers });
    } catch (error) {
      console.error('Error extracting online users:', error);
      res.status(500).json({ error: 'Failed to extract online users' });
    }
  });

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
  app.post('/logout', async (req, res) => {
    try {
      const { name } = req.body;

      // Update user status to "offline" in Firestore based on the username
      const stateCollection = firestore.collection('state').where('name', '==', name);
      const getStatus = await stateCollection.get();
      
      if (getStatus.empty) {
        res.status(404).json({ error: 'User not found' });
        return;
      }
      const doc = getStatus.docs[0];
      await doc.ref.update({ status: 'offline' });
      res.status(200).json({ message: 'Logout successful' });
    } catch (error) {
      console.error('Error logging out user:', error);
      res.status(500).json({ error: 'Failed to log out user' });
    }
  });


  app.listen(3002, () => {
    console.log('State service running on port 3002');
  });
