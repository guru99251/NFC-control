require('dotenv').config();
const express = require('express');
const app = express();
app.use(express.json());

// TODO: import routes...
app.listen(process.env.PORT || 3000, () => {
  console.log('API Server running');
});
