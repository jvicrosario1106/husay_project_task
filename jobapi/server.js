const express = require("express");
const axios = require("axios");
const cors = require("cors");
const app = express();

app.use(cors({ origin: true }));

const API_KEY =
  "c06cc87167ff82c14347678ee97e37dcadfbcef75692e41e8cc1c71f29d62a01";

app.get("/job-api", (req, res) => {
  const listOfJobs = [
    "graphic+designer",
    "illustrator",
    "motion+graphic+artist",
    "producer",
    "artist",
    "creative+director",
    "game+designer",
    "multimedia+artist",
    "musician",
    "singer",
    "sound+engineer",
  ];

  listOfJobs.forEach((job) => {
    try {
      axios
        .get(
          `https://serpapi.com/search.json?engine=google_jobs&q=${job}+philippines&hl=en&api_key=${API_KEY}`
        )
        .then((data) => {
          data.data.jobs_results.map((results) => {
            console.log(results.title);
            console.log(results.company_name);
            console.log(results.location);
            console.log(results.via);
            console.log(results.description);
            console.log(results.extensions[1]);
            console.log(
              results.detected_extensions.schedule_type &&
                results.detected_extensions.schedule_type
            );
          });

          data.data.chips.map((results) => {});
        })
        .catch((err) => console.log(err.data));
    } catch (err) {
      console.error("Error: ", err);
    }
  });
});

app.listen(3000, () => {
  console.log("Listing to port 3000");
});
