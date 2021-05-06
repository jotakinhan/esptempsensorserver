const express = require('express')
const path = require('path')

//Let port be defined by Heroku
const port = process.env.PORT || 3000
const app = express()

app.set('view engine', 'hbs')
app.use(express.json())
app.use(express.static(path.join(__dirname + '/public')))

//Collect measured temps to this
let sensorData = []

//Show average of sensorData values
app.get('/', (req, res) => {

    let total = 0;
    for(let i = 0; i < sensorData.length; i++) {
    total += sensorData[i];
    }
    let avg = total / sensorData.length;
    let avground = Math.round(avg);

    res.render('webpage.hbs', {
        value: avground.toString()
    })
})

//Show all values of sensorData
app.get('/data', (req, res) => {
    res.send(sensorData)
})

//Receive a new temp value from ESP (max 60, 1 hour)
app.post('/postdata', (req, res) => {
    let value = req.body.value
    if (sensorData.length < 60) {
        sensorData.unshift(value)
    } else {
        sensorData.pop()
        sensorData.unshift(value)
    }
    console.log(sensorData)

    res.send(sensorData)
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Example app listening on port ${port}`)
})
