const express = require('express');
const axios = require('axios');
const app = express();
const cors = require("cors")
require("dotenv").config();

 
app.use(express.json());
app.use(cors())


app.post('/get-recipe', async (req, res) => {
  try {
    const { name, top_n } = req.body;

   
    const result = await axios.post(`http://localhost:8000/recommend_recipe`, {
      name,
      top_n
    });
    res.json(result.data);
  } catch (e) {
    res.status(500).json({ error: 'Python API error', details: e.message });
  }
});

app.post('/get-mood-food', async (req, res) => {
  try {
    const { mood,top_n } = req.body;
    const result = await axios.post(`http://localhost:8000/recommend_food`, {
      mood,
      top_n
    });
    res.json(result.data);
  } catch (e) {
    res.status(500).json({ error: 'Python API error', details: e.message });
  }
});


app.get("/healthcheck",(req,res)=>{
res.json({status:ok})
})
app.listen(5000, () => console.log('Express API running on port 5000'));
